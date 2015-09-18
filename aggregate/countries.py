from collections import defaultdict
from itertools import product

import pandas as pd


def extract_countries(data):
    countries = data.groupby("ISO3Code").first()
    countries = countries[["CountryName", "Population2012", "isMdgCountry", "IsDeveloped", "IsFormer", "IsLLDC"]]
    return countries


def configure_get_population(countries):
    # most population numbers can be found in the world bank data
    populations = pd.read_csv("population.csv")
    populations = populations.set_index(["Country Code", "Year"])["Value"]
    populations = populations.to_dict()

    # rest take from 2012 data
    populations2012 = countries["Population2012"].to_dict()

    def get_population(iso_code, year):
        try:
            return populations[(iso_code, year)]
        except KeyError:
            return populations2012[iso_code]

    return get_population


def generate_country_year_combinations(countries):
    # some countries did not exist for all of the years the data was collected
    years = defaultdict(lambda: range(1990, 2015))
    years["SDN"] = range(1990, 2012)
    years["YUG"] = range(1990, 2004)

    for country in countries:
        for year in years[country]:
            yield country, year


def generate_series_country_year_combinations(series, countries):
    for ser in series:
        for country, year in generate_country_year_combinations(countries):
            yield ser, country, year