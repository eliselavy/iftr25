import os
import json
import csv
import anthropic
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from datetime import datetime

class EventExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the EventExtractor with an Anthropic API key."""
        self.api_key = api_key 
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def extract_event_json(self, text: str, publication_date: str) -> Dict[str, Any]:
        """Extract event information from text and return as JSON."""
        prompt = f"""
        Please analyze the following event announcement and extract key details into a JSON structure.
        Include the following fields : event title, organizer, publication date, place, event date,event_date_deducted 
        The publication date is provided as: {publication_date}.
        Only extract information that is explicitly stated in the text.
        Use the publication date and the event announcement to infer the event date if possible, it will be the date in the field event_date_deducted
        The 6 properties need to be filled if nothing is found: event_title, organizer, publication_date, place, event_date, event_date_deducted.
        Event announcement:
        {text}
        
        Provide ONLY a valid JSON response with no additional text. And if you see in the OCR some mistake, correct the answer.
        """
        
        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0,
            system="You extract event information from text and return it as valid JSON with no additional text.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract JSON from the response
        try:
            # The response content should be just JSON
            json_str = response.content[0].text
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            # If there's an issue parsing the JSON
            return {"error": f"Failed to parse JSON: {str(e)}", "raw_response": response.content[0].text}

    def extract_event_csv(self, key: str, text: str, publication_date: datetime, csv_file: str = "event_bal_masque_annonce.csv"):
        """Extract event information from text and append it to a CSV file."""
        # Format the publication date
        formatted_publication_date = publication_date.strftime('%Y-%m-%d-%H:%M:%S')

        # Extract event details as JSON
        event_data = self.extract_event_json(text, formatted_publication_date)

        # Ensure all required fields are present
        event_title = event_data.get("event_title", "")
        organizer = event_data.get("organizer", "")
        publication_date = event_data.get("publication_date", formatted_publication_date)
        place = event_data.get("place", "")
        event_date = event_data.get("event_date", "")
        event_date_deducted = event_data.get("event_date_deducted", "")

        # Write to CSV
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            # Write header if the file is new
            if not file_exists:
                writer.writerow(["key", "event_title", "organizer", "publication_date", "place", "event_date", "event_date_deducted"])
            # Write the event data
            writer.writerow([key, event_title, organizer, publication_date, place, event_date, event_date_deducted])

def main():
    # Take from .env
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve the API key from the environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
  
    
    if not api_key:
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return
    
    extractor = EventExtractor(api_key)
    
    # Example loop to process multiple events
    events = {
        "event_1": ("Hotel Metropole ♦ Bal Carnavalesque Lundi soil. - Entree libie.", datetime(2023, 2, 15, 10, 0, 0)),
        "event_2": ("ASSOCIATION DES COMMERÇANTS ESCH. SOIRÉE CARNAVALESQUE à l'hôtel de la Poste lundi de carnaval.", datetime(2023, 2, 16, 12, 0, 0))
    }

    # Process each event and write to CSV
    for key, (event_text, publication_date) in events.items():
        extractor.extract_event_csv(key, event_text, publication_date)

    print("Events have been written to event.csv")

if __name__ == "__main__":
    main()