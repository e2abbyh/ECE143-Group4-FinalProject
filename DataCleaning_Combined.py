import pandas as pd

# GovTrades Data Setup
df_govtrades = pd.read_csv("Data/cleaned_govtrades.csv")
df_govtrades["Estimated Holdings"] = df_govtrades["Estimated Holdings"].str[1:].str.replace(",", "")
df_govtrades["Estimated Holdings"] = df_govtrades["Estimated Holdings"].astype(int)
df_govtrades["Party"] = df_govtrades["Senator"].str[-5]
df_govtrades["State"] = df_govtrades["Senator"].str[-3:-1]
df_govtrades["Symbol"] = df_govtrades["Symbol"].str.strip()

# Stanford CA Data Setup
df_stanford = pd.read_csv("../Private Data/cleaned_stanford.csv")
df_stanford[df_stanford["company_ticker_symbol"].isin(df_govtrades["Symbol"].tolist())]
df_combined = pd.merge(df_stanford, df_govtrades, how="inner", left_on="company_ticker_symbol", right_on="Symbol")

# List of companies that do not match across both data. The ones marked 'same' are companies which have
# merged/acquired and hences are valid data. Some of companies need not be fixed due to data subset.
#same # Block, Inc. | Square, Inc.
#same # Valaris plc | Ensco plc
#same # Amplify Energy Corp. | Midstates Petroleum
#same # Life Time Fitness, Inc. | Latam GP LP
#same # Rosetta Stone, Inc. | RST Inc
#same # Stryker Corporation | Concentric Medical Inc
# Complete Management, Inc. : Stock, Debentures or Bonds | Cummins Inc
# Department 56, Inc. | Discover Financial Services
# Washington Mutual, Inc. | Waste Management, Inc.
# EQM Midstream Partners, LP | EQT Midstream Partners, LP
# SeaCube Container Leasing Ltd. | Box, Inc.
# Western Gas Partners, LP | WDE Partners LP
# Pan Am Corporation | Plains All American Pipeline
# EnergySolutions, Inc. | Eversource Energy
# Morgan Stanley Capital I Inc. : Mortgage Pass-Through Certificates | Dean Witter
# Morgan Stanley & Co., Inc. : Auction Rate Securities | Dean Witter
# Morgan Stanley | Dean Witter
# Milestone Scientific, Inc. | Dean Witter
# European Aeronautic Defence & Space Company (EADS) | Wells Fargo Income Opportunities Fund
# ICF Kaiser International, Inc. | iShares Cohen & Steers REIT

# Command used to find the companies to manually filer (the one which give before list)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     df_compare = df_combined[["composite_litigation_name", "Company"]].drop_duplicates()
#     print(df_compare.to_string())


# Basic Cleaning before comparison
df_combined["composite_litigation_name"] = df_combined["composite_litigation_name"].str.strip()
df_combined["Company"] = df_combined["Company"].str.strip()

# Final List Combined Pairs to Drop
drop_composite_litigation_name_list = ["SeaCube Container Leasing Ltd.", "Western Gas Partners, LP", "Pan Am Corporation"
                                       ,"Complete Management, Inc. : Stock, Debentures or Bonds", "Department 56, Inc." 
                                       , "Washington Mutual, Inc.", "EQM Midstream Partners, LP"]
drop_company_list = ["Box, Inc.", "WDE Partners LP", "Plains All American Pipeline"
                     , "Cummins Inc", "Discover Financial Services"
                     , "Waste Management, Inc.", "EQT Midstream Partners, LP"]
# Dropping ill-matched data - Note both conditions have to be checked together or we may lose valid data unneccesarily
for i in range(len(drop_composite_litigation_name_list)):
    df_combined = df_combined.drop(df_combined[(df_combined["composite_litigation_name"] == drop_composite_litigation_name_list[i])
                & (df_combined["Company"] == drop_company_list[i])].index)

# Re-shifting Columns
df_combined = df_combined[["Senator", "Estimated Holdings", "Symbol", "Company", "Sector", "Industry", "Party", "State",
'index_number', 'composite_litigation_name', 'company_ticker_symbol',
'cld_fic_filing_dt', 'cld_fic_class_start_dt', 'cld_fic_class_end_dt',
'comp_classification_sector_luv', 'comp_classification_indust_luv',
'issuer_comp_citizen_hq', 'issuer_comp_citizen_jurisdict',
'cld_fic_court_usdc_luv', 'company_market', 'company_market_status',
'cld_case_status_gen_luv', 'cld_flag_case_ever_go_trial', 'case_last_stage_date'
]]
df_combined.to_csv("../Private Data/cleaned_combined_data.csv")
