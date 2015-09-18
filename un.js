
// some series are only relevant for some countries
restricted_series = {8401: " (using only data for land-locked developing countries)",
                     8402: " (using only data for land-locked developing countries)",
                     8102: " (using only data for least-developed countries)",
                     8104: " (using only data for least-developed countries)",
                     8501: " (using only data for small-island developing countries)",
                     8502: " (using only data for small-island developing countries)",
                     8601: " (using only data for developing countries)",
                     8602: " (using only data for developing countries)"
                    }

function visualization(data, names) {

    this.makeStructure = function() {
        
        // one div for every goal
        var goalDivs = d3.select(".visualization").selectAll("div")
	      .data(names.mapping)
	      .enter().append("div")
	      .attr("id", function(d){return "goal" + d.key;})
              .attr("class", "goal");

        // name of goals as heading
        var goalHeader = goalDivs.append("h1").attr("class", "goalHeader");
        goalHeader.append("span").text(function(d){return names.goals[d.key].split(".")[0]})
                  .style('color', function(d){return goalColors[d.key].color;})
                  .style('text-transform', "uppercase"); 
        goalHeader.append("span").text(function(d){return names.goals[d.key].split(".")[1]}) 
                  .style('color', function(d){return goalColors[d.key].color;})  

        // one div for every target
        var targetDivs = goalDivs.selectAll("div")
             .data(function(d) {return d.values})
             .enter()
             .append("div")
             .attr("id", function(d){return "target"+d.key})
             .attr("class", "target")
             .style("display", "inline"); 

        // one div for every indicator
        var indicatorDivs = targetDivs.selectAll("div")
             .data(function(d) {return d.values})
             .enter()
             .append("div")
             .attr("id", function(d){return "indicator"+d.key})
             .attr("class", "indicator")
             .style("display", "inline"); 

        // one div for every series
        indicatorDivs.selectAll("div")
           .data(function(d) {return d.values})
           .enter()
           .append("div")
           .attr("id", function(d){return "series"+d.key})
           .attr("class", "series")
           .style("display", "inline");  
    }

    this.showCircles = function() {

         data = d3.nest()
               .key(function(d) {return d.SeriesId})
               .map(data);
        
        function circleColor(series) {
           var avg = weightedAverage(data[series]);
           var goal = names.seriesToGoal[series];
           return goalColors[goal].scale(avg);
        }

        // one svg element for every series
        var svg = d3.selectAll(".series")
                  .append("svg")
                  .attr("width", circle.width)
                  .attr("height", circle.height);

       // one circle to be used as marker if series has been selected
       svg.append("circle")
           .attr("class", "circle-border")
           .attr("r", circle.radius + 4)
           .attr("cx", circle.cx) 
           .attr("cy", circle.cy)
           .attr('fill-opacity', 0)
           .style("stroke", function(d) {return circleColor(d.key);})
           .style("stroke-width", 3)
           .style("display", "none");

        // one circle for every series
        svg.append("circle")
           .attr("class", "circle")
           .attr("r", circle.radius)
           .attr("cx", circle.cx) 
           .attr("cy", circle.cy)
           .style("fill", function(d) {return circleColor(d.key);})
           .on('click', function(d) {showDetails(d.key);})
           .append("title").text(function (d){return seriesTitle(d.key);});

    }

    this.showDetails = function(series) {
      
        // remove previous details
        d3.select(".details").remove();
        d3.select("#series"+detailsSelected).select(".circle-border").style("display", "none");

        // same series as previously was selected -> unselect
        if (detailsSelected === series) {
            detailsSelected = "";
            return;
        }
        else
            detailsSelected = series;       

        // make a border around the selected circle
        d3.select("#series"+series).select(".circle-border").style("display", "inline");

        // which goal does this series belong to? make a div under this goal
        var goal = names.seriesToGoal[series];
        var detailsDiv = d3.select("#goal"+goal)
             .append("div")
             .attr("class", "details");

        // put barplot into this div
        var color = goalColors[goal].color;
        var title = seriesTitle(series);
        makeBarplot(detailsDiv, data[series], title, color);
    }

    function makeBarplot(div, seriesData, title, color) {

        // configure x axis
        var x = d3.scale.ordinal()
                .rangeRoundBands([0, bar.width], .3);
        x.domain([  //1983, 1984, 1985, 1986, 1987, 1988, 1989, 
                    1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 
                    2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                    2010, 2011, 2012, 2013, 2014, 2015]);
        var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .tickValues([1990, 1995, 2000, 2005, 2010, 2015]);

        // configure y axis
        var y = d3.scale.linear()
                .range([bar.height, 0]);
        y.domain([0, 100]);
        var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickValues([0, 50, 100], "%");

        // make svg for plot
        var svg = div.append("svg")
           .attr("width", bar.width + bar.margin.left + bar.margin.right)
           .attr("height", bar.height + bar.margin.top + bar.margin.bottom)
           .append("g")
           .attr("transform", "translate(" + bar.margin.left + "," + bar.margin.top + ")");

        // plot x axis 
        svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + bar.height + ")")
           .call(xAxis);

        // plot y axis 
        var yElement = svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
        yElement.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", -55)
          .style("text-anchor", "end")
          .text("Percentage of population")
          .attr("class", "y-title");
         yElement.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", -40)
          .style("text-anchor", "end")
          .text("for which data is available")
          .attr("class", "y-title");

        // plot bars 
        svg.selectAll(".bar")
           .data(seriesData)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) {return x(d.Year); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.Ratio * 100.0); })
           .attr("height", function(d) { return bar.height - y(d.Ratio*100.0); })
           .style("fill", color)
           .append("svg:title").text(function(d) { return Math.round(d.Ratio*100.0) +"%" });

        // plot title
        div.append("div")
          .attr('class', 'bar-title')
          .append("text")
          .text(title);
    }

    this.seriesTitle = function(series) {
       title = names.series[series];
       if (series in restricted_series)
          title += restricted_series[series]
       return title
    }

    return this;

}
