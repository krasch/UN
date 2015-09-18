from countries import *


def read_mdg_data(filename):
    df = pd.read_csv(filename, sep="\t")
    df["IndicatorOrderClause"] = df["IndicatorOrderClause"].astype(str)
    df["Year"] = df["Year"].astype(int)
    df["SeriesName"] = df["SeriesName"].str.replace("&quot;", "'")
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
    comb = list(combinations_generator(df))
    comb = pd.DataFrame(comb, columns=["SeriesId", "ISO3Code", "Year"])
    c = comb[comb.SeriesId==8601]
    #print (c)
    comb = comb.set_index(["SeriesId", "ISO3Code", "Year"]).index
    return comb

data = read_mdg_data("data.txt")

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
get_population = configure_get_population(data)
available["population"] = available.apply(lambda row: get_population(iso_code=row.name[1], year=row.name[2]),
                                          axis=1)

# total number of people, per year and series
population_total = available["population"].groupby(level=[0, 2]).sum()

# number of people for which data available, per year and series
available = available["available"] * available["population"]
population_available = available.groupby(level=[0, 2]).sum()

# ratio of people for which data is available, per year and series
ratio_available = population_available / population_total
ratio_available.name = "Ratio"
ratio_available.reset_index().to_csv("aggregated.csv", index=False)

s = data.groupby(["SeriesId", "SeriesName"]).first().reset_index()[["SeriesId", "SeriesName"]]
s.to_csv("s.csv")