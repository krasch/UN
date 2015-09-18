from countries import *


def read_mdg_data(filename):
    df = pd.read_csv(filename, sep="\t")
    df["IndicatorOrderClause"] = df["IndicatorOrderClause"].astype(str)
    df["Year"] = df["Year"].astype(int)
    df = df.rename(columns={"SeriesOrderClause": "SeriesId"})
    return df


def extract_names(df):
    df = df.groupby("SeriesId").first().reset_index()
    df = df[["GoalId", "GoalName", "TargetId", "TargetName",
             "IndicatorId", "IndicatorName", "SeriesId", "SeriesName"]]
    return df


def extract_series(df):
    return sorted(list(df["SeriesId"].value_counts().index.values))


def extract_is_available(df):
    df = df.drop_duplicates(subset=["SeriesId", "ISO3Code", "Year"])
    exists = df.set_index(["SeriesId", "ISO3Code", "Year"])
    exists = pd.Series(1, index=exists.index)
    exists.name = "available"
    return exists.to_frame()


def all_combinations(df):
    years = sorted(list(df["Year"].value_counts().index.values))
    countries = sorted(list(df["ISO3Code"].value_counts().index.values))
    series = sorted(list(df["SeriesId"].value_counts().index.values))

    comb = list(product(series, countries, years))
    comb = pd.DataFrame(comb, columns=["SeriesId", "ISO3Code", "Year"])
    comb = comb.set_index(["SeriesId", "ISO3Code", "Year"]).index
    return comb

data = read_mdg_data("data.txt")

# info about all countries
countries = extract_countries(data)

# map series -> indicator -> target -> goal
names = extract_names(data)
names.to_csv("names.csv")

# all combinations of series, country, year
combinations = all_combinations(data)

# mark with "1" if data is available
available = extract_is_available(data)

# mark with "0" if data is not available
available = available.reindex(combinations).fillna(0)

# add population column
get_population = configure_get_population(countries)
available["population"] = available.apply(lambda row: get_population(iso_code=row.name[1], year=row.name[2]),
                                          axis=1)

# total number of people, per year and series
population_total = available["population"].groupby(level=[0, 2]).sum()

# number of people for which data available, per year and series
available = available["available"] * available["population"]
population_available = available.groupby(level=[0, 2]).sum()

# ratio of people for which data is available, per year and series
ratio_available = population_available / population_total
ratio_available.to_csv("aggregated.csv")