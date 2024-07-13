# Importing the pandas library for data manipulation and analysis.
import pandas as pd

# Importing the re (regular expression) library for string matching.
import re

# Scraping the table with data from a Wikipedia page.
# URL of the page.
url = 'https://en.wikipedia.org/wiki/Animal_rights_by_country_or_territory'

# Using pandas to read the tables directly from the page.
tables = pd.read_html(url)

# The table of interest is the forty-first on the page.
df = tables[40]

# Cleaning values in the "Country" column.
# Function to clean the country names.
def clean_country_name(name):
    # Removing non-letter characters using regex.
    cleaned_name = re.sub(r'[^a-zA-Z\s]', '', name)
    return cleaned_name.strip()

# Applying the function to the "Country" column.
df['Country'] = df['Country'].apply(clean_country_name)

# Cleaning column names.
df.rename(columns={
    'Anti-cruelty laws meet OIE standards[10]': 'Anti-cruelty laws meet OIE standards',
    'Support at the United Nations [a]': 'Support at the United Nations'
}, inplace=True)

# Converting string values to numerical to be able to calculate an overall score. 
# Function to convert values to numerical scores.
def convert_to_score(value):
    if value == "No":
        return 0
    elif value == "Yes":
        return 1
    elif "Partial" in value:
        return 0.5
    elif "unenforced" in value:
        return 0.5
    elif value == "Unknown":
        return None
    return None

# Creating new columns for numerical scores by applying the conversion function.
for col in df.columns[1:]:
    df[col + ' (Score)'] = df[col].apply(convert_to_score)

# Defining weights for each column to use in the weighted average calculation.
weights = {
    'Recognition of animal sentience (Score)': 0.2,
    'Recognition of animal suffering (Score)': 0.2,
    'Anti-cruelty laws meet OIE standards (Score)': 0.2,
    'Any laws against animal cruelty (Score)': 0.3,
    'Support at the United Nations (Score)': 0.1
}

# Function to calculate the weighted average score for each row.
def calculate_weighted_average(row):
    total_weight = 0
    weighted_sum = 0
    for col, weight in weights.items():
        if pd.notna(row[col]):
            weighted_sum += row[col] * weight
            total_weight += weight
    if total_weight == 0:
        return None
    return weighted_sum / total_weight

# Applying the function to each row to calculate the overall score.
df['Weighted Overall Score'] = df.apply(calculate_weighted_average, axis=1)

# Saving the resulting DataFrame to a CSV file.
df.to_csv('animal_rights_by_country.csv', index=False)

print("Table saved as animal_rights_by_country.csv")