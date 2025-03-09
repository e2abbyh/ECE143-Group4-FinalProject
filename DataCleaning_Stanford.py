import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_excel("../Private Data/Satriya_UCSD_DATA_2025.xlsx")
useful_cols = ['index_number', 'composite_litigation_name', 'company_ticker_symbol',
       'cld_fic_filing_dt', 'cld_fic_class_start_dt', 'cld_fic_class_end_dt', 'comp_classification_sector_luv',
       'comp_classification_indust_luv', 'issuer_comp_citizen_hq',
       'issuer_comp_citizen_jurisdict', 'cld_fic_court_usdc_luv',
       'company_market', 'company_market_status', 'cld_case_status_gen_luv', 'cld_flag_case_ever_go_trial', 'case_last_stage_date']
df_sub = df[useful_cols]
df_sub = df_sub[(df_sub["cld_fic_class_start_dt"] <="2020-06-09") 
                & (df_sub["cld_fic_class_start_dt"] >="2010-01-01")].reset_index(drop=True)
df_sub["company_ticker_symbol"] = df_sub["company_ticker_symbol"].str.strip()
df_sub["composite_litigation_name"] = df_sub["composite_litigation_name"].str.strip()
df_sub.to_csv("../Private Data/cleaned_stanford.csv")
