import pandas as pd

listing = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\listing.csv")
sold = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\sold.csv")

#Part 1: Feature engineering and market metrics

print("---|WEEK 6 FEATURE ENGINEERING AND MARKET METRICS||---")

#Create key metrics
date_columns = ["CloseDate", "PurchaseContractDate", "ListingContractDate"]
for col in date_columns:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

#Price ratio - measures negotiation strength
if "ClosePrice" in sold.columns and "OriginalListPrice" in sold.columns:
    sold["Price_Ratio"] = (
        sold["ClosePrice"] / sold["OriginalListPrice"]
    )

#Price Per Sq Ft - normalizes price across sizes
if "ClosePrice" in sold.columns and "LivingArea" in sold.columns:
    sold["Price_Per_Sq_Ft"] = (
        sold["ClosePrice"] / sold["LivingArea"]
    )

#Year / Month / YrMo - Enables time-series analysis
if "CloseDate" in sold.columns:
    sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
    sold['Year'] = sold['CloseDate'].dt.year
    sold['Month'] = sold['CloseDate'].dt.month
    sold['YrMo'] = sold['CloseDate'].dt.strftime('%Y-%m')

#Close to Original List Ratio - Captures full price reduction history
if "ClosePrice" in sold.columns and "OriginalListPrice" in sold.columns:
    sold["Close_to_Original_List_Ratio"] = (
        sold["ClosePrice"] / sold["OriginalListPrice"]
    )

#Listing to Contract Days - Measures time from listing to accepted offer
if "PurchaseContractDate" in sold.columns and "ListingContractDate" in sold.columns:
    sold["Listing_to_Contract_Days"] = (
        sold["PurchaseContractDate"] - sold["ListingContractDate"]
    ).dt.days

#Contract to Close Days - Escrow and closing period duration
if "CloseDate" in sold.columns and "PurchaseContractDate" in sold.columns:
    sold["Contract_to_CloseDays"] = (
        sold["CloseDate"] - sold["PurchaseContractDate"]
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
    col for col in key_metrics_week6 if col in sold.columns
]
print("\nWeek 6 dataframe:")
print(sold[existing_week6_columns])

print("\nWeek 6 dataframe statistics:")
print(
    sold[existing_week6_columns]
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

if "ClosePrice" in sold.columns:
    agg_map["ClosePrice"] = ["count", "mean", "median"]
if "price_per_sqft" in sold.columns:
    agg_map["price_per_sqft"] = ["mean", "median"]
if "DaysOnMarket" in sold.columns:
    agg_map["DaysOnMarket"] = ["mean", "median"]

if not agg_map:
    print("None of the metric columns exist in the DataFrame.")
else:
    for segment in segment_items:
        if segment in sold.columns:
            print(f"\nSegmented summary table of {segment}:")

            if "ClosePrice" in sold.columns:
                agg_map["ClosePrice"] = ["count", "mean", "median"]

            if "price_per_sqft" in sold.columns:
                agg_map["price_per_sqft"] = ["mean", "median"]

            if "DaysOnMarket" in sold.columns:
                agg_map["DaysOnMarket"] = ["mean", "median"]

            if agg_map:
                segment_summary = sold.groupby(segment).agg(agg_map)

            print(segment_summary.head(20))

            output_file = f"sold_segmented_summary_table_of_{segment}.csv"
            segment_summary.to_csv(output_file)
            print(f"Saved {output_file}!")

print("\nComplete week 6 segment analysis!")