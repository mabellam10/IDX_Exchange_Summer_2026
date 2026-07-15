#PART 1: Fetch the mortgage rate data from FRED
import pandas as pd

listing = pd.read_csv("D:\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\listing.csv")
sold = pd.read_csv("D:\\MAIQUAN_Internships\\IDX_Exchange_Summer_2026\\Week_1\\sold.csv")

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

#PART 2: Resample weekly rates to monthly averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
mortgage.groupby('year_month')['rate_30yr_fixed']
.mean()
.reset_index()
)

#PART 3: Create a matching year_month key on the MLS datasets

# Sold dataset — key off CloseDate
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

# Listings dataset — key off ListingContractDate
listing['year_month'] = pd.to_datetime(
listing['ListingContractDate']
).dt.to_period('M')

#PART 4: Merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listing_with_rates = listing.merge(mortgage_monthly, on='year_month', how='left')

#PART 5: Validate the merge
# Check for any unmatched rows
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listing_with_rates['rate_30yr_fixed'].isnull().sum())

#PART 6: Preview
print("\n---|PREVIEW|---")
print(
sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
    ].head()
)

#PART 7: Save into csv files
listing_with_rates.to_csv("listing_mortage_rates.csv", index = False)
sold_with_rates.to_csv("sold_mortgage_rates.csv", index = False)
