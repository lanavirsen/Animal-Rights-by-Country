# :paw_prints: Visualization: Animal Rights by Country

## Introduction

In this personal mini-project, I created a visualization to show how animal rights are recognized around the world.

I utilized the "Principal laws on animal rights" table published on a [Wikipedia](https://en.wikipedia.org/wiki/Animal_rights_by_country_or_territory) page, which provides comprehensive coverage on the subject.

For each of the 93 countries in the table, the following five questions are addressed:

- Recognition of animal sentience
- Recognition of animal suffering
- Anti-cruelty laws meet OIE* standards
- Any laws against animal cruelty
- Support at the United Nations

*OIE: the **World Organisation for Animal Health** (**WOAH**), formerly the **Office International des Epizooties** (**OIE**), is an intergovernmental organisation founded in 1924, coordinating, supporting and promoting animal disease control.

### Tools

- **Python**: A versatile programming language for data manipulation and analysis.
- **Pandas**: A library for data analysis and manipulation.
- **Re**: A library for regular expression operations.
- **Jupyter Notebook**: An interactive environment for running and documenting code.
- **Tableau**: A tool for creating interactive data visualizations.

### Data Source

- [en.wikipedia.org/wiki/Animal_rights_by_country_or_territory](https://en.wikipedia.org/wiki/Animal_rights_by_country_or_territory)
- Date: the 12th of July, 2024
- Permission is granted to copy, distribute and/or modify Wikipedia's text under the terms of the Creative Commons Attribution-ShareAlike 4.0 International License and, *unless otherwise noted*, the GNU Free Documentation License, unversioned, with no invariant sections, front-cover texts, or back-cover texts.

### Outcome

![Figure 1](https://github.com/lanavirsen/Animal-Rights-by-Country/blob/main/Figure_1.png)

*Figure 1: Screenshot of the visualization.*

[Click here to view the interactive Tableau visualization](https://public.tableau.com/views/AnimalRightsbyCountry/MasterView?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) 

Hovering over a country reveals a tooltip displaying the following details:

- Recognition of animal sentience
- Recognition of animal suffering
- Anti-cruelty laws meet OIE standards
- Any laws against animal cruelty
- Support at the United Nations

![Figure 2](https://github.com/lanavirsen/Animal-Rights-by-Country/blob/main/Figure_2.png)

*Figure 2: Example of tooltips for different countries.*

## Table of Contents

- [Data Preprocessing](#data-preprocessing)
  - [Importing the Necessary Libraries](#importing-the-necessary-libraries)
  - [Scraping the Data from Wikipedia](#scraping-the-data-from-wikipedia)
  - [Cleaning the Data](#cleaning-the-data)
  - [Converting String Values to Numerical Scores](#converting-string-values-to-numerical-scores)
  - [Saving the Result to a CSV File](#saving-the-result-to-a-csv-file)
- [Creating an Interactive Visualization](#creating-an-interactive-visualization)

## Project Workflow

### Data Preprocessing

#### Importing the Necessary Libraries

```python
# pandas library for data manipulation and analysis.
import pandas as pd

# re (regular expression) library for string matching.
import re
```

#### Scraping the Data from Wikipedia

The data is structured as a table on a Wikipedia page. I use the `pandas` library to scrape it.

```python
# URL of the page.
url = 'https://en.wikipedia.org/wiki/Animal_rights_by_country_or_territory'

# Using pandas to read the tables directly from the page.
tables = pd.read_html(url)

# The table of interest is the forty-first on the page.
df = tables[40]

# Displaying the first several rows to see the result of scraping.
display(df.head())
```

Output:

|     |         Country | Recognition of animal sentience | Recognition of animal suffering | Anti-cruelty laws meet OIE standards[10] | Any laws against animal cruelty |                   Support at the United Nations [a] |
| --- | --------------: | ------------------------------: | ------------------------------: | ---------------------------------------: | ------------------------------: | --------------------------------------------------: |
| 0   | Algeria[11][12] |                              No |                              No |                                       No |                 Yes -unenforced |                                                  No |
| 1   |      Angola[13] |                              No |                              No |                                       No |                              No |                                                  No |
| 2   |   Argentina[14] |                             Yes |                             Yes |                                      Yes |                             Yes |                                                  No |
| 3   |   Australia[15] |                             Yes |                             Yes |              Partial - varies internally |                             Yes |                                                  No |
| 4   |     Austria[16] |                             Yes |                             Yes |                                      Yes |                             Yes | Partial - support from various internal departments |

#### Cleaning the Data

The original table contains footnotes and references, such as `[11]` and `[a]`. These are preserved in the scraped data. I will remove them for clarity.

```python
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

# Displaying the first several rows to see the result.
display(df.head())
```

Output:


|     |   Country | Recognition of animal sentience | Recognition of animal suffering | Anti-cruelty laws meet OIE standards | Any laws against animal cruelty |                       Support at the United Nations |
| --- | --------: | ------------------------------: | ------------------------------: | -----------------------------------: | ------------------------------: | --------------------------------------------------: |
| 0   |   Algeria |                              No |                              No |                                   No |                 Yes -unenforced |                                                  No |
| 1   |    Angola |                              No |                              No |                                   No |                              No |                                                  No |
| 2   | Argentina |                             Yes |                             Yes |                                  Yes |                             Yes |                                                  No |
| 3   | Australia |                             Yes |                             Yes |          Partial - varies internally |                             Yes |                                                  No |
| 4   |   Austria |                             Yes |                             Yes |                                  Yes |                             Yes | Partial - support from various internal departments |

#### Converting String Values to Numerical Scores

To assign colors to the countries in Tableau, I need to convert the string values to numerical scores and calculate an "average score".  I decide to use a weighted average for the score.

```python
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

# Displaying the first several rows to see the result of the calculations.
display(df.head())
```

Output:

|  | Country | Recognition of animal sentience | Recognition of animal suffering | Anti-cruelty laws meet OIE standards | Any laws against animal cruelty | Support at the United Nations | Recognition of animal sentience (Score) | Recognition of animal suffering (Score) | Anti-cruelty laws meet OIE standards (Score) | Any laws against animal cruelty (Score) | Support at the United Nations (Score) | Weighted Overall Score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | Algeria | No | No | No | Yes -unenforced | No | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.15 |
| 1 | Angola | No | No | No | No | No | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.00 |
| 2 | Argentina | Yes | Yes | Yes | Yes | No | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.90 |
| 3 | Australia | Yes | Yes | Partial - varies internally | Yes | No | 1.0 | 1.0 | 0.5 | 1.0 | 0.0 | 0.80 |
| 4 | Austria | Yes | Yes | Yes | Yes | Partial - support from various internal departments | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 0.95 |

#### Saving the Result to a CSV File

The result looks satisfactory, so I save it to a CSV file.

```python
df.to_csv('animal_rights_by_country.csv', index=False)

print("Table saved as animal_rights_by_country.csv")
```

### Creating an Interactive Visualization

The resulting Tableau dashboard consists of a single world map visualization, with country colors determined by their weighted average score.

Hovering over a country reveals a tooltip displaying the following details:

- Recognition of animal sentience
- Recognition of animal suffering
- Anti-cruelty laws meet OIE standards
- Any laws against animal cruelty
- Support at the United Nations

To enhance the user experience, the values for each feature are conditionally colored: "Yes" is green, "No" is red, most other values are yellow, and "Unknown" is gray. This effect is achieved by creating calculated fields for each feature that output the value based on its content.

Example of a calculated field formula: 

```
IF CONTAINS(ATTR([Recognition of animal sentience]), "Partial")
THEN ATTR([Recognition of animal sentience])
END
```

The tooltip example:

![Tooltip](https://github.com/lanavirsen/Animal-Rights-by-Country/blob/main/Tooltip.png)

The finished visualization:

![Screenshot](https://github.com/lanavirsen/Animal-Rights-by-Country/blob/main/Figure_1.png)

[Click here to view the interactive Tableau visualization](https://public.tableau.com/views/AnimalRightsbyCountry/MasterView?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) 
