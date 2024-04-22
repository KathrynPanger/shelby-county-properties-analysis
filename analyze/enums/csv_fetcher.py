from enum import Enum
import pandas as pd
class CSV(Enum):
    data_path = "../../data/processed/"
    s1_2019 = "s1_2019.csv"
    s1_2020 = "s1_2020.csv"
    s1_2021 = "s1_2021.csv"
    s1_2022 = "s1_2022.csv"
    s2 = "s2_in_lieu_contracts_by_owner.csv"
    s3 = "s3_2022_icc_contracts.csv"
    s4 = 's4_2022_idb_contracts.csv'
    s5 = 's5_2022_iph.csv'
    s6 = 's6_2022_ihe.csv'
    s7 = 's7_2022_city_county_contracts.csv'
    s8 = 's8_2022_imc_contracts.csv'
    s9 = 's9_2022_idb_arlington.csv'
    s10 = 's10_2022_idb_bartlett.csv'
    s11 = 's11_2022_idb_colierville.csv'
    s12 = 's12_2021_idb_germantown.csv'
    s13 = 's13_2021_idb_millington.csv'
    s14 = 's14_pilot_extension_fund_contracts.csv'
    s15 = 's_15_in_lieu_delinquent_notices.csv'
    all_properties = "all_properties.csv"

def read_csv(csv_path: CSV) -> pd.DataFrame:
    path = CSV.data_path.value + csv_path.value
    df = pd.read_csv(path)
    return df
