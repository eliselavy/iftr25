# Context newspapers

## Escher Tageblett ( 1913-1950)

Attention : Pendant l'occupation du Grand-Duché de Luxembourg par l'Allemagne nazie - du 10 mai 1940 au 10 septembre 1944 - la presse était d'abord censurée, puis, après confiscation des maisons d'édition et des imprimeries, éditée par l'occupant lui-même, tout en maintenant les entêtes d'avant-guerre. Les éditions du Tageblatt après 1950 sont consultables sur microfilm pour tout lecteur inscrit à la Bibliothèque nationale.

## L'indépendance luxembourgeoise (1871-1934)

A la suite de son journal « L’Avenir » (avril 1868 à septembre 1871) l’éditeur Jean Joris (1828-1893) publie le 1er octobre 1871 le premier numéro du quotidien « l’Indépendance luxembourgeoise ». Au-delà de la mort de son créateur en 1893, le journal en langue française continue à paraitre plus de 60 ans, jusqu’au 31 décembre 1934 sous la responsabilité de l'imprimeur-éditeur Joseph Beffort (1845-1923) et ses successeurs. Parmi les rédacteurs, collaborateurs et directeurs successifs, on peut noter Etienne Hamélius (1856-1929), Joseph Hansen (1874-1952), Charles Becker (1881-1952), Marcel Noppeney (1877-1966) et Paul Weber (1898-1976).


Documentation Tropy: https://www.bulac.fr/sites/default/files/medias/fichiers/2023/04/Guide_Tropy.pdf


Attention : du 10.5.1940 au 10.9.1944, la presse était sous contrôle de l'occupant nazi.



{
  "event": {
    "title": "La Redoute masquée \"Ailes Hannevir\"",
    "organiser": "Le Nouvel Automobile-Club du Grand-Duché de Luxembourg",
    "publication_date": null,
    "place": null,
    "event_date": "27 février 1937"
  },
  "source": {
    "newspaper": null,
    "page": null
  }
}

{
  "event": {
    "title": "Soirée Carnavalesque",
    "organiser": "Association des Commerçants Esch",
    "publication_date": "1936-02-22",
    "place": "Hôtel de la Poste",
    "event_date": "Lundi de carnaval, 1936"
  },
  "source": {
    "newspaper": "Escher Tageblatt",
    "page": 3
  }
}

To determine the specific date for "Lundi de carnaval" (Carnival Monday) in 1936, I need to calculate when Easter fell that year, since carnival dates are tied to the Easter calendar.
In the Western Christian tradition, Carnival Monday (also called Rose Monday in some regions) falls 48 days before Easter Sunday.
For 1936:

Easter Sunday was on April 12, 1936
Counting back 48 days from Easter Sunday places Carnival Monday on February 24, 1936

So "Lundi de carnaval, 1936" refers specifically to February 24, 1936.



import os
import json
import anthropic
from typing import Dict, Any, Optional

class EventExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the EventExtractor with an Anthropic API key."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def extract_event_json(self, text: str) -> Dict[str, Any]:
        """Extract event information from text and return as JSON."""
        prompt = f"""
        Please analyze the following event announcement and extract key details into a JSON structure.
        Include the following fields if available: event title, organizer, publication date, place, event date.
        Only extract information that is explicitly stated in the text.
        
        Event announcement:
        {text}
        
        Provide ONLY a valid JSON response with no additional text.
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

def main():
    # Example usage
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return
    
    extractor = EventExtractor(api_key)
    
    # Example text
    event_text = """
    ASSOCIATION DES COMMERQANTS ESCH. SOIREE
    Escher Tageblatt Newspaper
    Saturday, February 22, 1936 – p.3
    Personal use (no export) — provided by
    Luxembourg National Library
    * ASSOCIATION DES COMMERQANTS ESCH. SOIREE *CARNAVALESQUE* ä l'hötel de la Poste 1 u n d i de *carnaval*
    """
    
    result = extractor.extract_event_json(event_text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()