This directory contains the python code necessary to calculate the aggregations for the "Behind the scenes..." 
visualization. 

## Install pre-requisites

    conda create --name UN --file requirements.conda python=2.7
    source activate UN

## Get the data

    wget http://data.okfn.org/data/core/population/r/population.csv
    wget https://unite.un.org/ideas/sites/unite.un.org.ideas/files/public/MdgDatabase_2015WSD_DataVizChallenge.zip
    unzip MdgDatabase_2015WSD_DataVizChallenge.zip
    
(Population data is based on raw data provided by the world bank [here](http://data.worldbank.org/indicator/SP.POP.TOTL).
The formatted version used in this project has been provided by [https://github.com/datasets/population](https://github.com/datasets/population).

## Run the aggregation

    python aggregate.py
    
This will generate two files: ```names.csv``` (containing a mapping from series -> indicator -> target -> goal) and
```aggregated.csv``` (containing the actual aggregated data).

