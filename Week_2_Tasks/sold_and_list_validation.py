import pandas as pd

#STRUCTURE AND VALIDATION FOR SOLD'S FILES

#Upload the combined and filtered csv file from Week 1
sold = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1_Tasks\\sold.csv")

#PART 1: Dataset structure
#Set up the structure of the dataset
print("---|STRUCTURE OF SOLD DATASET|---")

#Identify the number of rows and columns
print(f"The number of rows and columns:{sold.shape}")

#Names of each column from the dataset
print(f"All of the names of the columns: {sold.columns.tolist()}")

#Review the data type of each column from the dataset
print(f"Data types of each column:{sold.dtypes}")

print(f"Show the first rows of the dataset: {sold.head(10)}")

#PART 2: PropertyType check
print("\n---|PROPERTY TYPE CHECK|---")

#Finding unique property types
if "PropertyType" in sold.columns:
    unique_types = sold["PropertyType"].unique()
    print(f"Unique property types found are: {unique_types}")
else:
    print("No 'PropertyType' column found")

#PART 3: Missing value analysis
print("---|MISSING VALUE REPORT|---")
null_counts = sold.isnull().sum()
null_pct = ((null_counts / len(sold))*100).round(3)

#Build the dataframe from the null data
missing_report = pd.DataFrame({
    'Column': sold.columns,
    'Null count': null_counts.values,
    'Null percentage': null_pct.values
})
missing_report = missing_report[missing_report['Null count']>0].sort_values(by = "Null percentage", ascending = False)
missing_report = missing_report.reset_index(drop=True)
print(missing_report)

#Finding columns that contain over 90% missing values
print("\n---|COLUMNS CONTAINING ABOVE 90 PERCENTAGE OF NULL VALUES|---")
high_missing = missing_report[missing_report['Null percentage'] > 90]
flagged_columns = len(high_missing)
list_flagged_names = high_missing['Column'].tolist()

if high_missing.empty:
    print("There are no columns that have over 90 percentage of null values")
else:
    print(high_missing)

print(f"There are {flagged_columns} columns that have over 90 percentage of null values")
print(f"List of flagged columns: {list_flagged_names}")

#PART 4: Numeric distribution summary
print("\n---|NUMERIC DISTRIBUTION SUMMARY|---")
numeric_distribution = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
numeric_features = []

for column in numeric_distribution:
    if column in sold.columns:
        numeric_features.append(column)

if numeric_features:
    numeric_distribution_summary = sold[numeric_features].describe(
        percentiles = [0.10, 0.25, 0.50, 0.60, 0.75, 0.90, 0.95]
    )
print(numeric_distribution_summary)

#PART 5: SAVE THE CSV FILES
missing_report.to_csv("sold_missing_value_report.csv", index=False)
high_missing.to_csv("sold_high_missing.csv", index=False)

if numeric_features:
    numeric_distribution_summary.to_csv("sold_numeric_distribution_summary.csv")

print("\nStructure and validation of Sold dataset are completed!")

#STRUCTURE AND VALIDATION FOR LISTING'S FILES

#Upload the combined and filtered csv file from Week 1
listing = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1_Tasks\\listing.csv")

#PART 1: Dataset structure
#Set up the structure of the dataset
print("---|STRUCTURE OF LISTING DATASET|---")

#Identify the number of rows and columns
print(f"The number of rows and columns:{listing.shape}")

#Names of each column from the dataset
print(f"All of the names of the columns: {listing.columns.tolist()}")

#Review the data type of each column from the dataset
print(f"Data types of each column:{listing.dtypes}")

print(f"Show the first rows of the dataset: {listing.head(10)}")

#PART 2: PropertyType check
print("\n---|PROPERTY TYPE CHECK|---")

#Finding unique property types
if "PropertyType" in listing.columns:
    unique_types = listing["PropertyType"].unique()
    print(f"Unique property types found are: {unique_types}")
else:
    print("No 'PropertyType' column found")

#PART 3: Missing value analysis
print("---|MISSING VALUE REPORT|---")
null_counts = listing.isnull().sum()
null_pct = ((null_counts / len(sold))*100).round(3)

#Build the dataframe from the null data
missing_report_2 = pd.DataFrame({
    'Column': listing.columns,
    'Null count': null_counts.values,
    'Null percentage': null_pct.values
})
missing_report_2 = missing_report_2[missing_report_2['Null count']>0].sort_values(by = "Null percentage", ascending = False)
missing_report_2 = missing_report_2.reset_index(drop=True)
print(missing_report)

#Finding columns that contain over 90% missing values
print("\n---|COLUMNS CONTAINING ABOVE 90 PERCENTAGE OF NULL VALUES|---")
high_missing_2 = missing_report_2[missing_report_2['Null percentage'] > 90]
flagged_columns_2 = len(high_missing_2)
list_flagged_names_2 = high_missing_2['Column'].tolist()

if high_missing_2.empty:
    print("There are no columns that have over 90 percentage of null values")
else:
    print(high_missing_2)

print(f"There are {flagged_columns_2} columns that have over 90 percentage of null values")
print(f"List of flagged columns: {list_flagged_names_2}")

#PART 4: Numeric distribution summary
print("\n---|NUMERIC DISTRIBUTION SUMMARY|---")
numeric_distribution_2 = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
numeric_features_2 = []

for column in numeric_distribution_2:
    if column in listing.columns:
        numeric_features_2.append(column)

if numeric_features_2:
    numeric_distribution_summary_2 = listing[numeric_features_2].describe(
        percentiles = [0.10, 0.25, 0.50, 0.60, 0.75, 0.90, 0.95]
    )
print(numeric_distribution_summary_2)

#PART 5: SAVE THE CSV FILES
missing_report_2.to_csv("listing_missing_value_report.csv", index=False)
high_missing_2.to_csv("listing_high_missing.csv", index=False)

if numeric_features_2:
    numeric_distribution_summary_2.to_csv("listing_numeric_distribution_summary.csv")

print("\nStructure and validation of Listing dataset are completed!")




