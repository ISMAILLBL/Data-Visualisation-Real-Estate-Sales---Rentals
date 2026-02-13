🏠 Moroccan Real Estate Market Analysis (Power BI + Python ETL)

A Business Intelligence project that analyzes the Moroccan real estate market using scraped property listings data and interactive dashboards built in Power BI.

The project implements a full BI pipeline:

Web Data → ETL (Python) → Star Schema → Power BI Dashboards

📊 Project Overview

The Moroccan real estate market generates a huge amount of online listings data (price, location, surface, type, etc.).
However, this data is raw, unstructured and inconsistent.

This project transforms raw listing data into decision-making insights by:

Cleaning and structuring scraped data

Building a dimensional data warehouse (Star Schema)

Creating interactive Power BI dashboards

Goal:

Help users understand price trends, compare cities, and evaluate property value.

🧱 BI Architecture
Raw Data (CSV / Scraping)
        ↓
Python ETL (combine.py)
        ↓
Star Schema (Fact + Dimensions)
        ↓
Power BI Model
        ↓
Dashboards & Insights


Layers:

Source Layer → Raw listings

ETL Layer → Cleaning & modeling

Storage Layer → Star schema tables

Analytics Layer → Power BI visualization

🗂️ Data Used

The dataset represents Moroccan real estate listings.

Each row corresponds to a property advertisement.

Main Columns
Column	Description
Category	Property type (Apartment, Villa, House…)
Type	Sale or Rent
Price	Property price
Ville	City
Secteur	District
Surface habitable	Living area
Surface totale	Total area
Chambres	Bedrooms
Salle de bain	Bathrooms
Salons	Living rooms
Standing	Property quality level
Condition	Property state
Equipments	Available equipment
Origin	Owner or agency
Year	Publication year
⚙️ ETL Process (combine.py)

The ETL script is implemented in Python using Pandas.

📄 See file: 

combine

1️⃣ Extraction

Load merged CSV dataset

Validate structure and required columns

2️⃣ Transformation
Data Cleaning

Remove spaces

Normalize accents

Fix text inconsistencies

Handle missing values

Remove duplicates

Standardization

Example normalization:

combined_data['Ville'] = combined_data['Ville'] \
    .str.strip() \
    .str.normalize('NFKD') \
    .str.encode('ascii', errors='ignore') \
    .str.decode('ascii')

Dimensional Modeling

Creates dimension tables:

dim_category

dim_condition

dim_equipments

dim_type

dim_ville

dim_secteur

dim_standing

dim_origin

dim_temps

Creates fact table:

fact_location_vente

3️⃣ Load

Exports the Star Schema into CSV files:

data/
 ├── dim_category.csv
 ├── dim_condition.csv
 ├── dim_ville.csv
 ├── dim_standing.csv
 ├── dim_temps.csv
 └── fact_location_vente.csv


These files are imported into Power BI.

⭐ Data Warehouse Model

The project uses a Star Schema:

Fact table → Property transactions

Dimension tables → descriptive attributes

This improves:

Query performance

Analytical flexibility

Dashboard responsiveness

📈 Power BI Dashboards

The dashboards provide several analytical views.

1. Market Overview

Total listings

Average price

Average price per m²

Distribution by property type

Distribution by city

2. Rent vs Sale Analysis

Listings distribution

Average price comparison

Surface vs price correlation

3. Geographic Analysis

Listings per city

Average price by city

Most expensive districts

4. Standing & Condition

Price by quality level

Price by property condition

5. Surface & Rooms

Surface vs price correlation

Bedrooms vs price evolution

📊 Power BI file included in repository
(Example dashboard structure available in report) 

Rapport PowerBI

🚀 How to Run the Project
1️⃣ Install requirements
pip install pandas

2️⃣ Run ETL

Place your dataset as:

data.csv


Then run:

python combine.py


Generated files will appear inside:

data/

3️⃣ Open Power BI

Open Power BI Desktop

Import CSV files from /data

Create relationships

Load dashboard file (.pbix)
