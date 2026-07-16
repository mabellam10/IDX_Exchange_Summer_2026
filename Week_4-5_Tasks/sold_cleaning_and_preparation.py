import pandas as pd
import numpy as np

sold = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\sold.csv")

#SOLD

#Part 1: Convert date fields to datetime format
print("---|DATETIME FORMAT|---")
sold_columns = [
    'CloseDate',
    'PurchaseContractDate',
    'ListingContractDate',
    'ContractStatusChangeDate'
]

for col in sold_columns:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors='coerce')

print(sold[sold_columns].dtypes)
print(sold[sold_columns].head(10))

#Part 2: Remove unnecessary or redundant columns
print("\n---|DETECT REDUNDANT COLUMNS|---")

threshold = 0.90
total_rows = len(sold)
dropped_columns = []

#Dropping all columns that have over 90% null data
for col in sold.columns:
    null_ratio = sold[col].isnull().mean()
    if null_ratio >= threshold:
        dropped_columns.append(col)
        print(f"{col} is {null_ratio*100:.2f}% empty")
        continue

most_repeated_ratio = 0
valid_row_count = sold[col].count()

#Dropping the columns that have over 90% of exact same data
if valid_row_count > 0:
    most_repeated_data_count = sold[col].value_counts().max()
    most_repeated_ratio = most_repeated_data_count / valid_row_count

if most_repeated_ratio >= threshold:
    most_repeated_data = sold[col].value_counts().idxmax()
    dropped_columns.append(col)
    print(f"{col} has {most_repeated_ratio*100:.2f}% repeated with mostly {most_repeated_data}.")
else:
    print("There is no highly repeated data.")

print(f"There are {len(dropped_columns)} redundant columns.")

#Part 3: Handle missing values appropriately
print("---|HANDLE MISSING VALUE|---")

#Select all remaining text columns
text_cols = sold.select_dtypes(include = ['object', 'category']).columns
null_count = 0

for col in text_cols:
    null_count = sold[col].isnull().sum()
    if null_count > 0:
        sold[col] = sold[col].fillna('None')
        print(f"Filled {null_count} blanks in categorical {col} with 'None'")

#Select all remaining numeric columns
numerical_cols = sold.select_dtypes(include=[np.number]).columns
null_count2 = 0

for col in numerical_cols:
    null_count2 = sold[col].isnull().sum()
    if null_count2 > 0:
        median_value = sold [col].median()
        sold[col] = sold[col].fillna(median_value)
        print(f"Filled {null_count2} blanks in numerical {col} with median: {median_value}")

#PART 4: Ensure numeric fields are properly typed
print("---|PROPERLY TYPE NUMERIC FIELDS|---")
for col in sold.select_dtypes(include=[np.number]).columns:
    non_null_values = sold[col].dropna()
    if(non_null_values % 1 == 0).all():
        sold[col] = sold[col].astype('Int64')
        print(f"{col} cast to Integer")
    else:
        sold[col] = sold[col].astype(float)
        print(f"{col} cast to Float")

#Part 5: Remove or flag invalid numeric values
print("\n---|REMOVE INVALID NUMERIC VALUES|---")
rows_before_removed = len(sold)

if "ClosePrice" in sold.columns:
    sold = sold[sold["ClosePrice"] > 0]

if "LivingArea" in sold.columns:
    sold = sold[sold["LivingArea"] > 0]

if "DaysOnMarket" in sold.columns:
    sold = sold[sold["DaysOnMarket"] >= 0]

if "BedroomsTotal" in sold.columns:
    sold = sold[sold["BedroomsTotal"] >= 0]

if "BathroomsTotalInteger" in sold.columns:
    sold = sold[sold["BathroomsTotalInteger"] >= 0]

print("\nRows before invalid value removal:", rows_before_removed)
print("Rows after invalid value removal:", len(sold))
print("Rows removed:", rows_before_removed - len(sold))
print("\nData type confirmation:")
print(sold.dtypes)

#Date Consistency Check
print("\n---|DATE CONSISTENCY CHECK AND GEOGRAPHIC DATA CHECK|---")

if "ListingContractDate" in sold.columns and "CloseDate" in sold.columns:
    sold["listing_after_close_flag"] = (
        sold["ListingContractDate"] > sold["CloseDate"]
    )

if "PurchaseContractDate" in sold.columns and "CloseDate" in sold.columns:
    sold["purchase_after_close_flag"] = (
        sold["PurchaseContractDate"] > sold["CloseDate"]
    )

if "ListingContractDate" in sold.columns and "PurchaseContractDate" in sold.columns:
    sold["negative_timeline_flag"] = (
        sold["ListingContractDate"] > sold["PurchaseContractDate"]
    )

if "Latitude" in sold.columns and "Longitude" in sold.columns:
    # Flag records with missing coordinates (Latitude or Longitude is null)
    sold["missing_coords_flag"] = (
        sold["Latitude"].isnull() | sold["Longitude"].isnull()
    )
    #Flag Latitude = 0 or Longitude = 0 (sentinel null values)
    sold["senstive_null_flag"] = (
        (sold["Latitude"] == 0) | (sold["Longitude"] == 0)
    )
    #Flag Longitude > 0 errors
    sold["positive_longitude_flag"] = sold["Longitude"] > 0
    #Flag out-of-state or implausible coordinates
    #California has latitude from 32.5° N to 42.0° N and longitude from -124.5° W to -114.1° W
    sold["out_of_state_flag"] = (
            (sold["Latitude"] < 32.5) |
            (sold["Latitude"] > 42) |
            (sold["Longitude"] < -124.5) |
            (sold["Longitude"] > -114.1)
    )
flag_records_columns = [
    "listing_after_close_flag", "purchase_after_close_flag",
    "negative_timeline_flag", "missing_coords_flag",
    "senstive_null_flag", "positive_longitude_flag",
    "out_of_state_flag"
]
existing_flag_columns = [
    col for col in flag_records_columns if col in sold.columns
]
print("\nData consistency flag counts:")
for col in existing_flag_columns:
    print(f"{col}: {sold[col].sum()}")

#Create a dataframe of geographic data quality summary noting any invalid coordinate records
flag_summary = pd.DataFrame({
    "FlagColumn": existing_flag_columns,
    "FlaggedRows": [sold[col].sum() for col in existing_flag_columns]
})

flag_summary.to_csv("sold_flag_summary.csv", index=False)
print("Completed!")
