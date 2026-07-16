import pandas as pd
import numpy as np

listing = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\listing.csv")

#LISTING

#Part 1: Convert date fields to datetime format
print("---|DATETIME FORMAT|---")
listing_columns = [
    'CloseDate',
    'PurchaseContractDate',
    'ListingContractDate',
    'ContractStatusChangeDate'
]

for col in listing_columns:
    if col in listing.columns:
        listing[col] = pd.to_datetime(listing[col], errors='coerce')

print(listing[listing_columns].dtypes)
print(listing[listing_columns].head(10))

#Part 2: Remove unnecessary or redundant columns
print("\n---|DETECT REDUNDANT COLUMNS|---")

threshold = 0.90
total_rows = len(listing)
dropped_columns = []

#Dropping all columns that have over 90% null data
for col in listing.columns:
    null_ratio = listing[col].isnull().mean()
    if null_ratio >= threshold:
        dropped_columns.append(col)
        print(f"{col} is {null_ratio*100:.2f}% empty")
        continue

most_repeated_ratio = 0
valid_row_count = listing[col].count()

#Dropping the columns that have over 90% of exact same data
if valid_row_count > 0:
    most_repeated_data_count = listing[col].value_counts().max()
    most_repeated_ratio = most_repeated_data_count / valid_row_count

if most_repeated_ratio >= threshold:
    most_repeated_data = listing[col].value_counts().idxmax()
    dropped_columns.append(col)
    print(f"{col} has {most_repeated_ratio*100:.2f}% repeated with mostly {most_repeated_data}.")
else:
    print("There is no highly repeated data.")

print(f"There are {len(dropped_columns)} redundant columns.")

#Part 3: Handle missing values appropriately
print("\n---|HANDLE MISSING VALUE|---")

#Select all remaining text columns
text_cols = listing.select_dtypes(include = ['object', 'category']).columns
null_count = 0

for col in text_cols:
    null_count = listing[col].isnull().sum()
    if null_count > 0:
        listing[col] = listing[col].fillna('None')
        print(f"Filled {null_count} blanks in categorical {col} with 'None'")

#Select all remaining numeric columns
numerical_cols = listing.select_dtypes(include=[np.number]).columns
null_count2 = 0

for col in numerical_cols:
    null_count2 = listing[col].isnull().sum()
    if null_count2 > 0:
        median_value = listing [col].median()
        listing[col] = listing[col].fillna(median_value)
        print(f"Filled {null_count} blanks in numerical {col} with median: {median_value}")

#PART 4: Ensure numeric fields are properly typed
print("---|PROPERLY TYPE NUMERIC FIELDS|---")
for col in listing.select_dtypes(include=[np.number]).columns:
    non_null_values = listing[col].dropna()
    if(non_null_values % 1 == 0).all():
        listing[col] = listing[col].astype('Int64')
        print(f"{col} cast to Integer")
    else:
        listing[col] = listing[col].astype(float)
        print(f"{col} cast to Float")

#Part 5: Remove or flag invalid numeric values
print("---|REMOVE INVALID NUMERIC VALUES|---")
rows_before_removed = len(listing)

if "ClosePrice" in listing.columns:
    listing = listing[listing["ClosePrice"] > 0]

if "LivingArea" in listing.columns:
    listing = listing[listing["LivingArea"] > 0]

if "DaysOnMarket" in listing.columns:
    listing = listing[listing["DaysOnMarket"] >= 0]

if "BedroomsTotal" in listing.columns:
    listing = listing[listing["BedroomsTotal"] >= 0]

if "BathroomsTotalInteger" in listing.columns:
    listing = listing[listing["BathroomsTotalInteger"] >= 0]

print("\nRows before invalid value removal:", rows_before_removed)
print("Rows after invalid value removal:", len(listing))
print("Rows removed:", rows_before_removed - len(listing))
print("\nData type confirmation:")
print(listing.dtypes)

#Date Consistency Check
print("---|DATE CONSISTENCY CHECK AND GEOGRAPHIC DATA CHECK|---")

if "ListingContractDate" in listing.columns and "CloseDate" in listing.columns:
    listing["listing_after_close_flag"] = (
        listing["ListingContractDate"] > listing["CloseDate"]
    )

if "PurchaseContractDate" in listing.columns and "CloseDate" in listing.columns:
    listing["purchase_after_close_flag"] = (
        listing["PurchaseContractDate"] > listing["CloseDate"]
    )

if "ListingContractDate" in listing.columns and "PurchaseContractDate" in listing.columns:
    listing["negative_timeline_flag"] = (
        listing["ListingContractDate"] > listing["PurchaseContractDate"]


    )

if "Latitude" in listing.columns and "Longitude" in listing.columns:
    # Flag records with missing coordinates (Latitude or Longitude is null)
    listing["missing_coords_flag"] = (
        listing["Latitude"].isnull() | listing["Longitude"].isnull()
    )
    #Flag Latitude = 0 or Longitude = 0 (sentinel null values)
    listing["senstive_null_flag"] = (
        (listing["Latitude"] == 0) | (listing["Longitude"] == 0)
    )
    #Flag Longitude > 0 errors
    listing["positive_longitude_flag"] = listing["Longitude"] > 0
    #Flag out-of-state or implausible coordinates
    #California has latitude from 32.5° N to 42.0° N and longitude from -124.5° W to -114.1° W
    listing["out_of_state_flag"] = (
            (listing["Latitude"] < 32.5) |
            (listing["Latitude"] > 42) |
            (listing["Longitude"] < -124.5) |
            (listing["Longitude"] > -114.1)
    )
flag_records_columns = [
    "listing_after_close_flag", "purchase_after_close_flag",
    "negative_timeline_flag", "missing_coords_flag",
    "senstive_null_flag", "positive_longitude_flag",
    "out_of_state_flag"
]
existing_flag_columns = [
    col for col in flag_records_columns if col in listing.columns
]
print("\nData consistency flag counts:")
for col in existing_flag_columns:
    print(f"{col}: {listing[col].sum()}")

#Create a dataframe of geographic data quality summary noting any invalid coordinate records
flag_summary = pd.DataFrame({
    "FlagColumn": existing_flag_columns,
    "FlaggedRows": [listing[col].sum() for col in existing_flag_columns]
})

flag_summary.to_csv("listing_flag_summary.csv", index=False)
print("Completed!")
