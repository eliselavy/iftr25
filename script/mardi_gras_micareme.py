import pandas as pd
import holidays
from datetime import datetime, date, timedelta

def get_mardi_gras_micareme_dataframe(start_year=1880, end_year=1970, country='FR'):
    """
    Create a DataFrame with Mardi Gras and Mi-Carême dates for specified years.
    
    Args:
        start_year: Starting year (default 1880)
        end_year: Ending year (default 1970)
        country: Country code (default 'FR' for France)
    
    Returns:
        pandas.DataFrame: DataFrame with columns for year, mardi_gras, mi_careme
    """
    
    data = []
    
    for year in range(start_year, end_year + 1):
        # Get holidays for the year
        year_holidays = holidays.country_holidays(country, years=year)
        
        # Find Easter date first
        easter_date = None
        for holiday_date, holiday_name in year_holidays.items():
            if any(keyword in holiday_name.lower() for keyword in ['easter', 'pâques']):
                easter_date = holiday_date
                break
        
        # If no Easter found in holidays, calculate it manually
        if easter_date is None:
            easter_date = calculate_easter(year)
        
        # Calculate Mardi Gras (47 days before Easter)
        mardi_gras_date = easter_date - timedelta(days=47)
        
        # Calculate Mi-Carême (21 days before Easter, adjusted to Thursday)
        mi_careme_date = easter_date - timedelta(days=21)
        # Adjust to the nearest Thursday
        while mi_careme_date.weekday() != 3:  # 3 = Thursday
            mi_careme_date -= timedelta(days=1)
        
        data.append({
            'year': year,
            'mardi_gras': mardi_gras_date,
            'mi_careme': mi_careme_date,
            'easter': easter_date
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add additional useful columns
    df['mardi_gras'] = pd.to_datetime(df['mardi_gras'])
    df['mardi_gras_weekday'] = df['mardi_gras'].dt.day_name()
    df['mi_careme'] = pd.to_datetime(df['mi_careme'])
    df['mi_careme_weekday'] = df['mi_careme'].dt.day_name()
    df['days_between'] = (df['mi_careme'] - df['mardi_gras']).dt.days
    
    return df

def calculate_easter(year):
    """
    Calculate Easter date using the Gregorian calendar algorithm.
    Fallback method if holidays package doesn't have the date.
    """
    # Gregorian calendar Easter calculation
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    
    return date(year, month, day)

def check_date_in_dataframe(df, check_date):
    """
    Check if a given date is Mardi Gras or Mi-Carême in the DataFrame.
    
    Args:
        df: DataFrame created by get_mardi_gras_micareme_dataframe
        check_date: date object or string 'YYYY-MM-DD'
    
    Returns:
        dict: Information about the date
    """
    if isinstance(check_date, str):
        check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
    
    # Check Mardi Gras
    mardi_gras_match = df[df['mardi_gras'] == check_date]
    # Check Mi-Carême
    mi_careme_match = df[df['mi_careme'] == check_date]
    
    result = {
        'date': check_date,
        'is_mardi_gras': len(mardi_gras_match) > 0,
        'is_mi_careme': len(mi_careme_match) > 0,
        'year': None
    }
    
    if len(mardi_gras_match) > 0:
        result['year'] = mardi_gras_match.iloc[0]['year']
        result['type'] = 'Mardi Gras'
    elif len(mi_careme_match) > 0:
        result['year'] = mi_careme_match.iloc[0]['year']
        result['type'] = 'Mi-Carême'
    
    return result

# Example usage
if __name__ == "__main__":
    # You need to install required packages first:
    # pip install pandas holidays
    
    print("Creating Mardi Gras and Mi-Carême DataFrame (1880-1970)")
    print("=" * 55)
    
    # Create the DataFrame
    df = get_mardi_gras_micareme_dataframe(1880, 1970)
    
    # Display basic info
    print(f"DataFrame shape: {df.shape}")
    print(f"Years covered: {df['year'].min()} to {df['year'].max()}")
    print()
    
    # Display first few rows
    print("First 10 rows:")
    print(df.head(10).to_string(index=False))
    print()
    
    # Display last few rows
    print("Last 10 rows:")
    print(df.tail(10).to_string(index=False))
    print()
    
    # Some statistics
    print("Statistics:")
    print(f"- Total years: {len(df)}")
    print(f"- Mardi Gras always on: {df['mardi_gras_weekday'].unique()}")
    print(f"- Mi-Carême always on: {df['mi_careme_weekday'].unique()}")
    print(f"- Average days between Mardi Gras and Mi-Carême: {df['days_between'].mean():.1f}")
    print()
    
    # Test specific dates
    test_dates = ['1900-02-27', '1920-03-11', '1950-02-21']
    print("Testing specific dates:")
    for test_date in test_dates:
        result = check_date_in_dataframe(df, test_date)
        print(f"  {test_date}: {result}")
    print()
    
    # Export options
    print("To save to CSV:")
    print("df.to_csv('mardi_gras_micareme_1880_1970.csv', index=False)")
    print()
 

    # Optionally, save automatically
    df.to_csv('mardi_gras_micareme_1880_1970.csv', index=False)
    # df.to_excel('mardi_gras_micareme_1880_1970.xlsx', index=False)