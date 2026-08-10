import pandas as pd

#SOLD
#Part 1: Read the cleaned dataset
file = "D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_2\\sold_cleaned.csv"
sold_cleaned = pd.read_csv(file)

print("\n---|WEEK 7 OUTLIER DETECTION AND DATA QUALITY|---")

#Create a copy to keep raw records while adding flags
sold_flagged = sold_cleaned.copy()
target_cols = ["ClosePrice",
               "LivingArea",
               "DaysOnMarket"]

#Part 2: Flag extreme values using IQR
for col in target_cols:
    if col in sold_flagged.columns:
        Q1 = sold_flagged[col].quantile(0.25)
        Q3 = sold_flagged[col].quantile(0.75)
        IQR = Q3-Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        flag_column = f"{col}_outlier_flag"

        sold_flagged[flag_column] = (
        (sold_flagged[col] < lower_bound) |
        (sold_flagged[col] > upper_bound)
        )

        #Calculate percentiles (1st, 5th, 95th, 99th) to guide decision-making
        p1 = sold_flagged[col].quantile(0.01)
        p5 = sold_flagged[col].quantile(0.05)
        p95 = sold_flagged[col].quantile(0.95)
        p99 = sold_flagged[col].quantile(0.99)

        #Print outlier & percentile Summary
        print(f"\n{col} outlier summary:")
        print(f"Q1: {Q1}")
        print(f"Q3: {Q3}")
        print(f"IQR: {IQR}")
        print(f"Lower bound: {lower_bound}")
        print(f"Upper bound: {upper_bound}")
        print(f"1st Percentile: {p1}")
        print(f"5th Percentile: {p5}")
        print(f"95th Percentile: {p95}")
        print(f"99th Percentile: {p99}")
        print(f"Flagged rows: {sold_flagged[flag_column].sum()}")

#Part 3: Apply business rules
sold_flagged["invalid_close_price"] = sold_flagged["ClosePrice"] <= 0
sold_flagged["invalid_dom"] = sold_flagged["DaysOnMarket"] < 0

print("Successfully created flag columns!")

#Part 4: Combine all flag values into one column
flag_cols = [f"{col}_outlier_flag" for col in target_cols] + ["invalid_close_price", "invalid_dom"]
sold_flagged["flag_cols"] = sold_flagged[flag_cols].any(axis=1)

sold_filtered = sold_flagged[sold_flagged["flag_cols"] == False].copy()

#Part 5: Data Quality check and Stat comparison summary
print("\nDataset size and metric comparison (before vs. after)")
print(f"Original Row Count: {len(sold_flagged):,}")
print(f"Filtered Row Count: {len(sold_filtered):,}")
print(f"Total Rows Removed : {len(sold_flagged) - len(sold_filtered):,}")

comparison_rows = []

for col in target_cols:
    if col in sold_filtered.columns:
        before_median = sold_flagged[col].median()
        after_median = sold_filtered[col].median()
        before_mean = sold_flagged[col].mean()
        after_mean = sold_filtered[col].mean()

        print(f"\n[{col}]")
        print(f"  Median Before: {before_median:,.2f} | After: {after_median:,.2f}")
        print(f"  Mean Before: {before_mean:,.2f} | After: {after_mean:,.2f}")

        comparison_rows.append({
            "Column": col,
            "Median_before": before_median,
            "Median_after": after_median,
            "Mean_before": before_mean,
            "Mean_after": after_mean,
        })

sold_flagged.to_csv("sold_flagged.csv", index=False)
sold_filtered.to_csv("sold_filtered.csv", index=False)
pd.DataFrame(comparison_rows).to_csv("sold_comparison.csv", index=False)

print("\nSuccessfully saved deliverables:")
print("1. sold_flagged.csv ")
print("2. sold_filtered.csv ")
print("3. sold_comparison.csv")


#LISTING
#Part 1: Read the cleaned dataset
file = "D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_2\\listing_cleaned.csv"
listing_cleaned = pd.read_csv(file)

print("\n---|WEEK 7 OUTLIER DETECTION AND DATA QUALITY|---")

#Create a copy to keep raw records while adding flags
listing_flagged = listing_cleaned.copy()
target_cols = ["ClosePrice",
               "LivingArea",
               "DaysOnMarket"]

#Part 2: Flag extreme values using IQR
for col in target_cols:
    if col in listing_flagged.columns:
        Q1 = listing_flagged[col].quantile(0.25)
        Q3 = listing_flagged[col].quantile(0.75)
        IQR = Q3-Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        flag_column = f"{col}_outlier_flag"

        listing_flagged[flag_column] = (
        (listing_flagged[col] < lower_bound) |
        (listing_flagged[col] > upper_bound)
        )

        #Calculate percentiles (1st, 5th, 95th, 99th) to guide decision-making
        p1 = listing_flagged[col].quantile(0.01)
        p5 = listing_flagged[col].quantile(0.05)
        p95 = listing_flagged[col].quantile(0.95)
        p99 = listing_flagged[col].quantile(0.99)

        #Print outlier & percentile Summary
        print(f"\n{col} outlier summary:")
        print(f"Q1: {Q1}")
        print(f"Q3: {Q3}")
        print(f"IQR: {IQR}")
        print(f"Lower bound: {lower_bound}")
        print(f"Upper bound: {upper_bound}")
        print(f"1st Percentile: {p1}")
        print(f"5th Percentile: {p5}")
        print(f"95th Percentile: {p95}")
        print(f"99th Percentile: {p99}")
        print(f"Flagged rows: {listing_flagged[flag_column].sum()}")

#Part 3: Apply business rules
listing_flagged["invalid_close_price"] = listing_flagged["ClosePrice"] <= 0
listing_flagged["invalid_dom"] = listing_flagged["DaysOnMarket"] < 0

print("Successfully created flag columns!")

#Part 4: Combine all flag values into one column
flag_cols = [f"{col}_outlier_flag" for col in target_cols] + ["invalid_close_price", "invalid_dom"]
listing_flagged["flag_cols"] = sold_flagged[flag_cols].any(axis=1)

sold_filtered = sold_flagged[sold_flagged["flag_cols"] == False].copy()

#Part 5: Data Quality check and Stat comparison summary
print("\nDataset size and metric comparison (before vs. after)")
print(f"Original Row Count: {len(sold_flagged):,}")
print(f"Filtered Row Count: {len(sold_filtered):,}")
print(f"Total Rows Removed : {len(sold_flagged) - len(sold_filtered):,}")

comparison_rows = []

for col in target_cols:
    if col in sold_filtered.columns:
        before_median = sold_flagged[col].median()
        after_median = sold_filtered[col].median()
        before_mean = sold_flagged[col].mean()
        after_mean = sold_filtered[col].mean()

        print(f"\n[{col}]")
        print(f"  Median Before: {before_median:,.2f} | After: {after_median:,.2f}")
        print(f"  Mean Before: {before_mean:,.2f} | After: {after_mean:,.2f}")

        comparison_rows.append({
            "Column": col,
            "Median_before": before_median,
            "Median_after": after_median,
            "Mean_before": before_mean,
            "Mean_after": after_mean,
        })

sold_flagged.to_csv("sold_flagged.csv", index=False)
sold_filtered.to_csv("sold_filtered.csv", index=False)
pd.DataFrame(comparison_rows).to_csv("sold_comparison.csv", index=False)

print("\nSuccessfully saved deliverables:")
print("1. sold_flagged.csv ")
print("2. sold_filtered.csv ")
print("3. sold_comparison.csv")

