import pandas as pd
from pathlib import Path

#Look into the folder and find the files
listing_folders = Path("Original_Listing")
listing_files = sorted(listing_folders.glob("CRMLSListing*.csv"))

if not listing_files:
    print("No files found")
    exit()

print(f"Found {len(listing_files)} to concentrate.")

dfs = []
total_raw_rows = 0

#Go through each file and clean individually
for file in listing_files:
    print(f"Processing: {file.name}")
    df = pd.read_csv(file, low_memory=False)

    raw_count = len(df)
    total_raw_rows += raw_count

    print(f"{file.name} contains {len(df)} rows")
    dfs.append(df)

#Concentrate all the given files
concentrated_df = pd.concat(dfs,axis = 0, ignore_index = True)

print("Concentrating completed!")

#Row count of the concentrated dataset
print(f"Total rows in concentrated dataset: {len(concentrated_df)} rows")

#Track of the amount of dropped rows
total_empty_rows = 0
total_duplicate_rows = 0
total_clean_rows = 0

# Remove completely blank/empty rows (a)
pre_clean_count_a = len(concentrated_df)
concentrated_df_a = concentrated_df.dropna(how="all")

# Calculate dropped blank rows and total rows after removing blank rows
total_empty_rows = pre_clean_count_a - len(concentrated_df_a)

print(f"Total empty rows removed: {total_empty_rows} rows")
print(f"There are {len(concentrated_df_a)} rows in total after removing empty rows")

# Remove duplicate rows (b)
pre_clean_count_b = len(concentrated_df_a)
concentrated_df_b = concentrated_df_a.drop_duplicates()

#Calculate dropped duplicate rows and total rows after removing duplicate rows
total_duplicate_rows = pre_clean_count_b - len(concentrated_df_b)
print(f"Total duplicate rows removed: {total_duplicate_rows} rows")
print(f"There are {len(concentrated_df_b)} after removing duplicate rows")

#Create the frequency table of PropertyType before Residential filtering
print("\nProperty's frequency table before Residential filter:")
print((concentrated_df_b)["PropertyType"].value_counts(dropna=False))

#Filter for Residential properties only (c)
pre_clean_count_c = len(concentrated_df_b)
concentrated_df_c = concentrated_df_b[concentrated_df_b["PropertyType"]=="Residential"]

#Calculate dropped non-residential rows and total rows after filtering
total_non_residential_rows = pre_clean_count_c - len(concentrated_df_c)
print(f"Total non-residential rows removed: {total_non_residential_rows} rows")
print(f"There are {len(concentrated_df_c)} rows in total after Residential filtering")

#Save the Python script
output_path = listing_folders.parent / ("Cleaned_Listing_Dataset.csv")
print(f"Successfully saved clean dataset to {output_path}")

#Description of the dataframe
print("\n")
print(f"Original_Listing folder has: {len(listing_files)} files")
print(f"Concentrated_df has: {len(concentrated_df)} rows")
print(f"After cleaning data, the dataset has: {len(concentrated_df_b)} rows")
print(f"After Residential filtering, the dataset has: {len(concentrated_df_c)} rows")

#Export the dataframe to the csv file
concentrated_df_c.to_csv("listing.csv",index=False)
