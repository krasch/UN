from collections import defaultdict
from itertools import product

import pandas as pd


# series relevant only for land-locked developing countries
only_LLDC = [8401, 8402]
# series relevant only for least-developed countries
only_LDC2014 = [8102, 8104]
# series relevant only for small-island developing countries
only_SIDS = [8501, 8502]
# series relevant only for developing countries
only_developing = [8601, 8602]


def extract_countries(df):
    countries = df.groupby("ISO3Code").first()
    countries = countries[["CountryName", "Population2012", "isMdgCountry", "IsDeveloped",
                           "IsFormer", "IsLLDC", "IsLDC2014"]]
    return countries


def extract_land_locked_developing_countries(df):
    countries = extract_countries(df)
    countries = countries[countries.IsLLDC == 1]
    return countries.index.values


def extract_least_developed_countries(df):
    countries = extract_countries(df)
    countries = countries[countries.IsLDC2014 == 1]
    return countries.index.values


def extract_developing_countries(df):
    countries = extract_countries(df)
    countries = countries[countries.IsDeveloped == 0]
    return countries.index.values


def extract_small_island_countries(df):
    return ["CPV", "COM", "GNB", "MDV", "MRT", "STP", "SYC", "SGP",
            "ATG", "BHS", "BRB", "BLZ", "CUB", "DMA", "DOM", "GRD",
            "GUY", "HTI", "JAM", "KNA", "LCA", "SUR", "TTO",
            "COK", "FJI", "KIR", "MHL", "FSM", "NRU", "NIU", "PLW",
            "PNG", "WSM", "SLB", "TLS", "TON", "TUV", "VUT"]


def configure_get_population(df):
    # most population numbers can be found in the world bank data
    populations = pd.read_csv("population.csv")
    populations = populations.set_index(["Country Code", "Year"])["Value"]
    populations = populations.to_dict()

    # some countries did not exist during some years, just return population as 0 for those years
    sudan = list(product(["SDN"], range(2012, 2016)))
    yugoslavia = list(product(["YUG"], range(2004, 2016)))
    not_exist = sudan + yugoslavia
    populations_not_exist = {t: 0 for t in not_exist}

    # rest take from 2012 data
    # missing ones are all small countries, introduces only a small error
    countries = extract_countries(df)
    populations2012 = countries["Population2012"].to_dict()

    def get_population(iso_code, year):
        # world bank has no data for 2015, use 2014 instead
        if year == 2015:
            year = 2014

        try:
            return populations[(iso_code, year)]
        except KeyError:
            try:
                return populations_not_exist[iso_code, year]
            except KeyError:
                return populations2012[iso_code]

    return get_population


def combinations_generator(df):
    years = sorted(list(df["Year"].value_counts().index.values))
    series = sorted(list(df["SeriesId"].value_counts().index.values))

    countries_all = sorted(list(df["ISO3Code"].value_counts().index.values))
    countries_LLDC = extract_land_locked_developing_countries(df)
    countries_LDC2014 = extract_least_developed_countries(df)
    countries_islands = extract_small_island_countries(df)
    countries_developing = extract_developing_countries(df)

    countries_selector = defaultdict(lambda: countries_all)  # most series are valid for all countries
    for ser in only_developing:
        countries_selector[ser] = countries_developing
    for ser in only_SIDS:
        countries_selector[ser] = countries_islands
    for ser in only_LDC2014:
        countries_selector[ser] = countries_LDC2014
    for ser in only_LLDC:
        countries_selector[ser] = countries_LLDC

    for ser in series:
        countries = countries_selector[ser]
        for country in countries:
            for year in years:
                yield ser, country, year