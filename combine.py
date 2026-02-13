import pandas as pd

# Step 1: Load the uploaded data (assuming it's a CSV file)
file_path_combined = 'data.csv'  # Path to the combined data file
combined_data = pd.read_csv(file_path_combined)

# Step 2: Inspect columns to check the name
print("Columns in the data:", combined_data.columns)

# Strip any leading/trailing spaces from column names
combined_data.columns = combined_data.columns.str.strip()

# Normalize text columns by stripping spaces and handling special characters
combined_data['Category'] = combined_data['Category'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
combined_data['Type'] = combined_data['Type'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
combined_data['Ville'] = combined_data['Ville'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
combined_data['Condition'] = combined_data['Condition'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
combined_data['Standing'] = combined_data['Standing'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
combined_data['Origin'] = combined_data['Origin'].str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')

# Debugging step: Check the exact content of the 'Category' column
print(f"Column names before merging: {combined_data.columns.tolist()}")
print(f"Unique values in 'Category' column: {combined_data['Category'].unique()}")
print(f"Check for hidden spaces in 'Category': '{combined_data['Category'][0]}'")

# Ensure that all necessary columns exist after cleaning
required_columns = ['Category', 'Condition', 'Equipments', 'Type', 'Year', 'Ville', 'Secteur', 'Standing', 'Origin', 
                    'Price', 'Surface habitable', 'Surface totale', 'Chambres', 'Salle de bain', 'Salons']

# Check for missing columns
missing_columns = [col for col in required_columns if col not in combined_data.columns]

if missing_columns:
    print(f"Error: The following columns are missing: {missing_columns}")
else:
    print("All required columns are present.")

    # Step 3: Create Dimension Tables for all categorical fields

    # Dimension table for Category
    dim_category = combined_data[['Category']].drop_duplicates().reset_index(drop=True)
    dim_category['DimCategoryID'] = dim_category.index + 1

    # Dimension table for Condition
    dim_condition = combined_data[['Condition']].drop_duplicates().reset_index(drop=True)
    dim_condition['DimConditionID'] = dim_condition.index + 1

    # Dimension table for Equipments
    dim_equipments = combined_data[['Equipments']].drop_duplicates().reset_index(drop=True)
    dim_equipments['DimEquipmentsID'] = dim_equipments.index + 1

    # Dimension table for Property Type
    dim_type = combined_data[['Type']].drop_duplicates().reset_index(drop=True)
    dim_type['DimTypeID'] = dim_type.index + 1

    # Dimension table for Ville (City)
    dim_ville = combined_data[['Ville']].drop_duplicates().reset_index(drop=True)
    dim_ville['DimVilleID'] = dim_ville.index + 1

    # Dimension table for Secteur (Sector)
    dim_secteur = combined_data[['Secteur']].drop_duplicates().reset_index(drop=True)
    dim_secteur['DimSecteurID'] = dim_secteur.index + 1

    # Dimension table for Standing
    dim_standing = combined_data[['Standing']].drop_duplicates().reset_index(drop=True)
    dim_standing['DimStandingID'] = dim_standing.index + 1

    # Dimension table for Origin
    dim_origin = combined_data[['Origin']].drop_duplicates().reset_index(drop=True)
    dim_origin['DimOriginID'] = dim_origin.index + 1

    # Step 4: Create Dimension Table for Temps (Time) based on Year
    dim_temps = combined_data[['Year']].drop_duplicates().reset_index(drop=True)
    dim_temps['DimTempsID'] = dim_temps.index + 1

    # Step 5: Create Fact Table (Include 'Type' to differentiate between Location and Vente)
    fact_location_vente = combined_data[['Price', 'Surface habitable', 'Surface totale', 'Chambres', 'Salle de bain', 'Salons', 
                                        'Year', 'Category', 'Condition', 'Equipments', 'Type', 'Ville', 'Secteur', 'Standing', 'Origin']].copy()

    # Merge fact table with dimension tables to create the star schema 
    fact_location_vente = fact_location_vente.merge(dim_category[['Category', 'DimCategoryID']], on='Category', how='left')
    fact_location_vente = fact_location_vente.merge(dim_condition[['Condition', 'DimConditionID']], on='Condition', how='left')
    fact_location_vente = fact_location_vente.merge(dim_equipments[['Equipments', 'DimEquipmentsID']], on='Equipments', how='left')
    fact_location_vente = fact_location_vente.merge(dim_type[['Type', 'DimTypeID']], on='Type', how='left')
    fact_location_vente = fact_location_vente.merge(dim_ville[['Ville', 'DimVilleID']], on='Ville', how='left')
    fact_location_vente = fact_location_vente.merge(dim_secteur[['Secteur', 'DimSecteurID']], on='Secteur', how='left')
    fact_location_vente = fact_location_vente.merge(dim_standing[['Standing', 'DimStandingID']], on='Standing', how='left')
    fact_location_vente = fact_location_vente.merge(dim_origin[['Origin', 'DimOriginID']], on='Origin', how='left')
    fact_location_vente = fact_location_vente.merge(dim_temps[['Year', 'DimTempsID']], on='Year', how='left')  # Merged dimTemps

    # Step 6: Save the Dimension and Fact Tables as CSV files for Power BI

    # Save the dimension tables and fact table
    dim_category.to_csv('data/dim_category.csv', index=False)
    dim_condition.to_csv('data/dim_condition.csv', index=False)
    dim_equipments.to_csv('data/dim_equipments.csv', index=False)
    dim_type.to_csv('data/dim_type.csv', index=False)
    dim_ville.to_csv('data/dim_ville.csv', index=False)
    dim_secteur.to_csv('data/dim_secteur.csv', index=False)
    dim_standing.to_csv('data/dim_standing.csv', index=False)
    dim_origin.to_csv('data/dim_origin.csv', index=False)
    dim_temps.to_csv('data/dim_temps.csv', index=False)  # Save dimTemps
    fact_location_vente.to_csv('data/fact_location_vente.csv', index=False)

    # Return the file paths for download
    file_paths = {
        "dim_category": "data/dim_category.csv",
        "dim_condition": "data/dim_condition.csv",
        "dim_equipments": "data/dim_equipments.csv",
        "dim_type": "data/dim_type.csv",
        "dim_ville": "data/dim_ville.csv",
        "dim_secteur": "data/dim_secteur.csv",
        "dim_standing": "data/dim_standing.csv",
        "dim_origin": "data/dim_origin.csv",
        "dim_temps": "data/dim_temps.csv",  # Added file path for dimTemps
        "fact_location_vente": "data/fact_location_vente.csv"
    }

    file_paths
