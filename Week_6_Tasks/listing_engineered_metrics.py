import pandas as pd

listing = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\listing.csv")
sold = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\sold.csv")

#Part 1: Feature engineering and market metrics

print("---|WEEK 6 FEATURE ENGINEERING AND MARKET METRICS||---")

#Create key metrics
date_columns = ["CloseDate", "PurchaseContractDate", "ListingContractDate"]
for col in date_columns:
    if col in listing.columns:
        listing[col] = pd.to_datetime(listing[col], errors="coerce")

#Price ratio - measures negotiation strength
if "ClosePrice" in listing.columns and "OriginalListPrice" in listing.columns:
    listing["Price_Ratio"] = (
        listing["ClosePrice"] / listing["OriginalListPrice"]
    )

#Price Per Sq Ft - normalizes price across sizes
if "ClosePrice" in listing.columns and "LivingArea" in listing.columns:
    listing["Price_Per_Sq_Ft"] = (
        listing["ClosePrice"] / listing["LivingArea"]
    )

#Year / Month / YrMo - Enables time-series analysis
if "CloseDate" in listing.columns:
    listing["CloseDate"] = pd.to_datetime(listing["CloseDate"])
    listing['Year'] = listing['CloseDate'].dt.year
    listing['Month'] = listing['CloseDate'].dt.month
    listing['YrMo'] = listing['CloseDate'].dt.strftime('%Y-%m')

#Close to Original List Ratio - Captures full price reduction history
if "ClosePrice" in listing.columns and "OriginalListPrice" in listing.columns:
    listing["Close_to_Original_List_Ratio"] = (
        listing["ClosePrice"] / listing["OriginalListPrice"]
    )

#Listing to Contract Days - Measures time from listing to accepted offer
if "PurchaseContractDate" in listing.columns and "ListingContractDate" in listing.columns:
    listing["Listing_to_Contract_Days"] = (
        listing["PurchaseContractDate"] - listing["ListingContractDate"]
    ).dt.days

#Contract to Close Days - Escrow and closing period duration
if "CloseDate" in listing.columns and "PurchaseContractDate" in listing.columns:
    listing["Contract_to_CloseDays"] = (
        listing["CloseDate"] - listing["PurchaseContractDate"]
    ).dt.days

print("Complete creating Week 6 Key metrics!")

#Part 2: Creating a dataframe from the created key metrics
key_metrics_week6 = [
    "Price_Ratio",
    "Price_Per_Sq_Ft",
    "Close_to_Original_List_Ratio",
    "Listing_to_Contract_Days",
    "Contract_to_CloseDays",
]

existing_week6_columns = [
    col for col in key_metrics_week6 if col in listing.columns
]
print("\nWeek 6 dataframe:")
print(listing[existing_week6_columns])

print("\nWeek 6 dataframe statistics:")
print(
    listing[existing_week6_columns]
    .describe()
)

#Part 3: Segment Analysis
print("---| SEGMENT ANALYSIS |---")

segment_items = [
    "PropertyType",
    "PropertySubType",
    "CountryOrParish",
    "MLSAreaMajor",
    "ListOfficeName",
    "BuyerOfficeName",
]

agg_map = {}

if "ClosePrice" in listing.columns:
    agg_map["ClosePrice"] = ["count", "mean", "median"]
if "price_per_sqft" in listing.columns:
    agg_map["price_per_sqft"] = ["mean", "median"]
if "DaysOnMarket" in listing.columns:
    agg_map["DaysOnMarket"] = ["mean", "median"]

if not agg_map:
    print("None of the metric columns exist in the DataFrame.")
else:
    for segment in segment_items:
        if segment in listing.columns:
            print(f"\nSegmented summary table of {segment}:")

            if "ClosePrice" in listing.columns:
                agg_map["ClosePrice"] = ["count", "mean", "median"]

            if "price_per_sqft" in listing.columns:
                agg_map["price_per_sqft"] = ["mean", "median"]

            if "DaysOnMarket" in listing.columns:
                agg_map["DaysOnMarket"] = ["mean", "median"]

            if agg_map:
                segment_summary = listing.groupby(segment).agg(agg_map)

            print(segment_summary.head(20))

            output_file = f"sold_segmented_summary_table_of_{segment}.csv"
            segment_summary.to_csv(output_file)
            print(f"Saved {output_file}!")

print("\nComplete week 6 segment analysis!")