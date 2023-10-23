import json
import csv
import re
from difflib import SequenceMatcher
import pycountry

def clean_country_name(name):
    """Nettoye le nom du pays."""
    name = name.replace('é', 'E')
    name = name.replace('è', 'E')
    return re.sub(r'[^A-Z\s]', '', name.upper())

def translate_country_name(name):
    """Traduit le nom du pays en français si possible."""
    try:
        country = pycountry.countries.get(name=name)
        if country and 'fr' in country.translations:
            return country.translations['fr']
        return name
    except AttributeError:
        return name

def is_similar(a, b):
    """Vérifie si deux chaînes sont similaires."""
    return SequenceMatcher(None, a, b).ratio() > 0.95

def load_data_files():
    """Charge les fichiers de données et renvoie les données consolidées."""
    with open(vie_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data_names = {clean_country_name(name): name for name in data.keys()}
    
    load_csv_data(pib_file, data, data_names, '\ufeff"Country Name"', 'Last PIB', years_range=range(1960, 2023))
    load_csv_data(criminality_file, data, data_names, 'Pays', ['Indice de Criminalité', 'Indice de Sécurité'], delimiter=';')
    load_csv_data(median_income_file, data, data_names, 'country', ['medianIncome','meanIncome','gdpPerCapitaPPP'], delimiter=',')
    
    return data

def load_csv_data(filename, data, data_names, name_field, target_fields, delimiter=',', years_range=None):
    """Charge les données CSV dans le dictionnaire de données."""
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in csvreader:
            # country_name = clean_country_name(row[name_field])
            country_name_original = row[name_field]
            country_name_translated = translate_country_name(country_name_original)
            country_name = clean_country_name(country_name_translated)
            matched = False
            for cleaned_name, original_name in data_names.items():
                if is_similar(country_name, cleaned_name):
                    if isinstance(target_fields, list):
                        for field in target_fields:
                            data[original_name][field] = row[field]
                    elif years_range:
                        for year in reversed(years_range):
                            if row[str(year)]:
                                data[original_name][target_fields] = row[str(year)]
                                break
                    matched = True
                    break
            if not matched:
                print(f"Le pays {country_name} n'est pas dans le fichier {filename}")

def calculate_ratios(data):
    """Calcule les ratios d'indemnité/criminalité*pib/habitant."""
    list_criminality_ratio = []
    alpha = 0.5
    
    for country, values in data.items():
        indemnity = clean_numeric_value(values.get("INDEMNITE TOTALE", "N/A"))
        pib = clean_numeric_value(values.get("Last PIB", "N/A"))
        criminality = clean_numeric_value(values.get("Indice de Criminalité", "N/A"))
        
        if pib != "N/A" and criminality != "N/A":
            ratio = indemnity / (pib * alpha + criminality * (1 - alpha))
            list_criminality_ratio.append((country, ratio))
            
    return sorted(list_criminality_ratio, key=lambda x: x[1], reverse=True)

def clean_numeric_value(value):
    """Nettoye et convertit la valeur numérique."""
    cleaned_value = value.replace('€', '').replace(',', '.').replace(' ', '').strip()
    return float(cleaned_value) if cleaned_value != "N/A" else "N/A"

def calculate_indemnity_by_pib(data):
    ratios = []
    for country, values in data.items():
        indemnity = clean_numeric_value(values.get("INDEMNITE TOTALE", "N/A"))
        pib = clean_numeric_value(values.get("Last PIB", "N/A"))
        
        if pib != "N/A":
            ratio = indemnity / (pib/12)
            ratios.append((country, ratio))
    return sorted(ratios, key=lambda x: x[1], reverse=True)

def calculate_indemnity_by_criminality(data):
    ratios = []
    for country, values in data.items():
        indemnity = clean_numeric_value(values.get("INDEMNITE TOTALE", "N/A"))
        criminality = clean_numeric_value(values.get("Indice de Criminalité", "N/A"))
        
        if criminality != "N/A":
            ratio = indemnity / (criminality * 100)
            ratios.append((country, ratio))
    return sorted(ratios, key=lambda x: x[1], reverse=True)

def calculate_indemnity_by_dangerosity_and_pib(data):
    ratios = []
    alpha = 1
    for country, values in data.items():
        indemnity = clean_numeric_value(values.get("INDEMNITE TOTALE", "N/A"))
        pib = clean_numeric_value(values.get("Last PIB", "N/A"))
        criminality = clean_numeric_value(values.get("Indice de Criminalité", "N/A"))
        
        if pib != "N/A" and criminality != "N/A":
            ratio = indemnity / (pib * alpha + criminality)
            ratios.append((country, ratio))
    return sorted(ratios, key=lambda x: x[1], reverse=True)

def calculate_indemnity_by_median_income(data):
    """Calcule le ratio entre l'indemnité totale et le revenu médian."""
    ratios = []
    for country, values in data.items():
        indemnity = clean_numeric_value(values.get("INDEMNITE TOTALE", "N/A"))
        median_income = clean_numeric_value(values.get("medianIncome", "N/A"))
        
        if median_income != "N/A":
            ratio = indemnity / median_income
            ratios.append((country, ratio))
    return sorted(ratios, key=lambda x: x[1], reverse=True)

def display_ratios(title, ratios, n):
    formatted_title = title.replace("...", str(n))
    print(formatted_title)
    print("-" * len(formatted_title))
    for country, ratio in ratios[:n]:
        print(f"{country} : {ratio:.2f}")
    print()

if __name__ == "__main__":
    n=10
    
    file_path = "data/"
    
    vie_file = file_path + "data_vie.json"
    pib_file = file_path + "data_pib.csv"
    criminality_file = file_path + "data_criminality.csv"
    median_income_file = file_path + "median-income_data.csv"
    
    data = load_data_files()
    sorted_criminality_ratio = calculate_ratios(data)
    
    pib_ratios = calculate_indemnity_by_pib(data)
    criminality_ratios = calculate_indemnity_by_criminality(data)
    combined_ratios = calculate_indemnity_by_dangerosity_and_pib(data)
    median_income_ratios = calculate_indemnity_by_median_income(data)
    
    display_ratios("Top ... des pays par indemnité/PIB par habitant:", pib_ratios, n)
    display_ratios("Top ... des pays par indemnité/Indice de Criminalité:", criminality_ratios, n)
    display_ratios("Top ... des pays par indemnités/dangerosité*PIB par habitant:", combined_ratios, n)
    display_ratios("Top ... des pays par indemnité/Revenu Médian:", median_income_ratios, n)