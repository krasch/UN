function parseNames(names) {
    var parsed = {};

    var goalNames = d3.nest()
        .key(function(d) {return d.GoalId})
        .rollup(function(d) {return d[0].GoalName})
        .map(names);
    parsed["goals"] = goalNames;

    var targetNames = d3.nest()
       .key(function(d) {return d.TargetId})
       .rollup(function(d) {return d[0].TargetName})
       .map(names);
    parsed["targets"] = targetNames;

    var indicatorNames = d3.nest()
       .key(function(d) {return d.IndicatorId})
       .rollup(function(d) {return d[0].IndicatorName})
       .map(names);
    parsed["indicators"] = indicatorNames;

    var seriesNames = d3.nest()
          .key(function(d) {return d.SeriesId})
          .rollup(function(d) {return d[0].SeriesName})
          .map(names);
    parsed["series"] = seriesNames;

    var seriesToGoal = d3.nest()
        .key(function(d) {return d.SeriesId})
        .rollup(function(d) {return d[0].GoalId;})
        .map(names);
    parsed["seriesToGoal"] = seriesToGoal;

    var mapping = d3.nest()
       .key(function(d) {return d.GoalId})
       .key(function(d) {return d.TargetId})
       .key(function(d) {return d.IndicatorId})
       .key(function(d) {return d.SeriesId})
       .entries(names);
    parsed["mapping"] = mapping;

    return parsed; 
}


function weightedAverage(seriesData) {
    function weight(year) {
        if ((year<1990) || (year==2015))
            return 0.0 
        if (year >= 2010)
            return 0.1
        else
           return 0.5/20.0;
    }
    weightedPercentages = seriesData.map(function(d) {return weight(d.Year)*d.Ratio});
    return d3.sum(weightedPercentages);
}

function configureGoalColors(colorList) {
    function configure(color) {
       return {"color": color,
                "scale": d3.scale.linear()
                         .domain([0, 1])
                         .range(["seashell", color])};
    }

    var colors = {};
    colorList.forEach(function(d, i) {colors[i+1] = configure(d);});

    return colors;  
}
