import pandas   as pd
import yfinance as yf

df = pd.read_csv("Data/govtrades.csv", delimiter="|") # Read in data
df = df.dropna(axis=1, how="all")                     # Drop columns where all values are NaN

df["Sector"]   = df.groupby("Symbol")["Sector"].ffill().bfill()   # Fill in sector values based on existing listed symbols
df["Industry"] = df.groupby("Symbol")["Industry"].ffill().bfill() # Fill in industry values based on existing listed symbols

symbols_with_nan = df[df["Sector"].isna()]["Symbol"].unique()

# Fetch sector and industry
def fetch_sector_industry(symbol):
    try:
        stock    = yf.Ticker(symbol)
        info     = stock.info
        sector   = info.get("sector", "Unknown")
        industry = info.get("industry", "Unknown")
        
        if sector != "Unknown" and industry != "Unknown": return sector, industry
        else: return None, None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None, None

# Loop through symbols and update DataFrame for valid data
for idx, row in df[df["Symbol"].isin(symbols_with_nan)].iterrows():
    if pd.isna(row["Sector"]) and pd.isna(row["Industry"]):
        sector, industry = fetch_sector_industry(row["Symbol"])
        if sector:   df.at[idx, "Sector"]   = sector
        if industry: df.at[idx, "Industry"] = industry

# Remaining symbols without Sector or Industry...Manually adding
sector_industry_dict = { "CCLP"    : ("Energy", "Oil & Gas Equipment & Services")
                       , "HGH"     : ("Finance", "Life Insurance")
                       , "LM09.SG" : ("Finance", "Mutual Funds")
                       , "ODMAX"   : ("Finance", "Mutual Funds")
                       , "NQCAX"   : ("Finance", "Mutual Funds")
                       , "WHIAX"   : ("Finance", "Mutual Funds")
                       , "DES"     : ("Finance", "Mutual Funds")
                       , "NUVBX"   : ("Finance", "Mutual Funds")
                       , "AFTEX"   : ("Finance", "Mutual Funds")
                       , "TZA"     : ("Finance", "Exchange Traded Funds (ETFs)")
                       , "PIOBX"   : ("Finance", "Mutual Funds")
                       , "VWO"     : ("Finance", "ETFs")
                       , "VCIFX"   : ("Finance", "Mutual Funds")
                       , "SPEU"    : ("Finance", "Mutual Funds")
                       , "AIBAX"   : ("Finance", "Mutual Funds")
                       , "BSV"     : ("Finance", "ETFs")
                       , "KSDIX"   : ("Finance", "Mutual Funds")
                       , "LSFAX"   : ("Finance", "Mutual Funds")
                       , "MUTHX"   : ("Finance", "Mutual Funds")
                       , "FRRSX"   : ("Finance", "Mutual Funds")
                       , "IYZ"     : ("Finance", "ETFs")
                       , "GHYYX"   : ("Finance", "Mutual Funds")
                       , "VVPSX"   : ("Finance", "Mutual Funds")
                       , "VGK"     : ("Finance", "ETFs")
                       , "SMLCX"   : ("Finance", "Mutual Funds")
                       , "MTLFX"   : ("Finance", "Mutual Funds")       
                       , "SHY"     : ("Finance", "ETFs")
                       , "ICRPX"   : ("Finance", "Mutual Funds")
                       , "WRK"     : ("Industrials", "Paper Packaging")
                       , "BEGBX"   : ("Finance", "Mutual Funds")
                       , "MFADX"   : ("Finance", "Mutual Funds")
                       , "COAGX"   : ("Finance", "Mutual Funds")
                       , "MNK"     : ("Health Care", "Pharmaceuticals")
                       , "DNKN"    : ("Consumer Discretionary", "Restaurants")
                       , "AT"      : ("Utilities", "Electric Utilities")
                       , "POM"     : ("Utilities", "Electric Utilities")
                       , "MXIM"    : ("Information Technology", "Semiconductors")
                       , "PRGX"    : ("Industrials", "Business Services")
                       , "CIT"     : ("Finance", "Banks")
                       , "CFX"     : ("Industrials", "Machinery")
                       , "MIK"     : ("Consumer Discretionary", "Specialty Retail")
                       , "HDS"     : ("Industrials", "Industrial Distribution")
                       , "PEY"     : ("Finance", "Mutual Funds")
                       , "VIXY"    : ("Finance", "ETFs")
                       , "MN"      : ("Finance", "Banks")
                       , "RSNRX"   : ("Finance", "Mutual Funds")
                       , "TUP"     : ("Consumer Staples", "Personal Products")
                       , "CEQP"    : ("Energy", "Oil & Gas Midstream")
                       , "WETF"    : ("Finance", "Asset Management")
                       , "MRO"     : ("Energy", "Oil & Gas Exploration & Production")
                       , "SWN"     : ("Energy", "Oil & Gas Exploration & Production")
                       , "MYL"     : ("Health Care", "Pharmaceuticals")
                       , "VCSH"    : ("Finance", "ETFs")
                       , "MCC"     : ("Finance", "Closed-End Funds")
                       , "WLL"     : ("Energy", "Oil & Gas Exploration & Production")
}

mask = df["Sector"].isna() | df["Industry"].isna()

df.loc[mask, "Sector"]   = df.loc[mask, "Symbol"].map(lambda x: sector_industry_dict.get(x, (None, None))[0])
df.loc[mask, "Industry"] = df.loc[mask, "Symbol"].map(lambda x: sector_industry_dict.get(x, (None, None))[1])

print(df.isna().sum())

df.drop_duplicates(inplace=True)

df.to_csv("Data/cleaned_govtrades.csv", index=False)