var width = 760,
height = 720,
outerRadius = Math.min(width, height) / 2 - 6,
innerRadius = outerRadius - 24;
 
function formatPercent(value, total){
  var myNumber = value/total * 100
  return Math.round(myNumber * 10)/10
}          

function formatRideSclaler(value, total){
  var myScaler = value * 64.36688800
  return Math.round(myScaler * 1)/1
}
var formatNumber = d3.format(",.0f");
                 
var communityAreas = ["1","2","3","4","5","6","7","8","9", "10", 
"11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", 
"22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
"34","35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45",
"46","47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58",
"59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72",
"73", "74", "75", "76", "77"]

var colors = ["#9ACD32",
"#377DB8",
"#F5DEB3",
"#EE82EE",
"#40E0D0",
"#FF6347",
"#D8BFD8",
"#2E6D41",
"#708090",
"#87CEEB",
"#A0522D",
"#6A5ACD",
"#2E8B57",
"#F4A460",
"#245FAF",
"#FA8072",
"#9ACD32",
"#377DB8",
"#F5DEB3",
"#EE82EE",
"#40E0D0",
"#FF6347",
"#D8BFD8",
"#6A5ACD",
"#708090",
"#87CEEB",
"#A0522D",
"#FFF5EE",
"#2E8B57",
"#F4A460",
"#FA8072",
"#F4A460",
"#2E8B57",
"#A0522D",
"#6A5ACD",
"#708090",
"#40E0D0",
"#4682B4",
"#EE82EE",
"#9ACD32",
"#D2B48C",
"#D8BFD8",
"#708090",
"#00FF7F",
"#D8BFD8",
"##A4CAFA",
"#D2B48C",
"#EE82EE",
"#87CEEB",
"#377DB8",
"#9ACD32",
"#40E0D0",
"#D8BFD8",
"#6A5ACD",
"#40E0D0",
"#A0522D",
"#377DB8",
"#A0522D",
"#9ACD32",
"#377DB8",
"#F5DEB3",
"#EE82EE",
"#40E0D0",
"#A9CAFA",
"#D8BFD8",
"#D2B48C",
"#4682B4",
"#00FF7F",
"#A0522D",
"#40E0D0",
"#708090",
"#87CEEB",
"#A0522D",
"#FA8072",
"#2E8B57",
"#F4A460",
"#FA8072"]

var fill = d3.scale.ordinal()
    .domain(d3.range(communityAreas.length))
    .range(colors);
    
var arc = d3.svg.arc()
.innerRadius(innerRadius*1.01)
.outerRadius(outerRadius);
 
var layout = d3.layout.chord()
.padding(.04)
.sortChords(d3.descending);
 
var path = d3.svg.chord()
.radius(innerRadius);

var svg = d3.select("#viz").append("svg")
.attr("width", width)
.attr("height", height)
.append("g")
.attr("id", "circle")
.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

svg.append("circle")
.attr("r", outerRadius);

d3.csv("../static/data/areas.csv", function(areas) {
d3.json("../static/data/matrix.json",function(matrix) {
  console.log(matrix[0])
   console.log(areas[0])
// Compute the chord layout.
layout.matrix(matrix);

var totalAmount = 0
for (var i = 0; i < matrix.length; i++){
  var rowValue = matrix[i].reduce((a, b) => a + b, 0)
  totalAmount += rowValue
}
console.log(totalAmount);
// Add a group per neighborhood.
var group = svg.selectAll(".group")
.data(layout.groups)
.enter().append("g")
.attr("class", "group")
.on("mouseover", mouseover);
 
// Add a mouseover title.
group.append("title").text(function(d, i) {
return areas[i].name + ": " + formatPercent(d.value, totalAmount) + "% of aggregate total rides originate from this area.\n" 
+ "Roughly " +formatNumber(formatRideSclaler(d.value))+"* " + "total number of rides originated from " + areas[i].name+"."; 
});

 
// Add the group arc.
var groupPath = group.append("path")
.attr("id", function(d, i) { return "group" + i; })
.attr("d", arc)
.style("fill", function(d, i) { return areas[i].color; });
 
// Add a text label.
var groupText = group.append("text")
.attr("x", 1)
.attr("dy", 12)
 
groupText.append("textPath")
.attr("xlink:href", function(d, i) { return "#group" + i; })
.text(function(d, i) { return communityAreas[i]; });
 
// Remove the labels that don't fit. :(
groupText.filter(function(d, i) { return groupPath[0][i].getTotalLength() / 2 - 18 < this.getComputedTextLength(); })
.remove();
 
// Add the chords.
var chord = svg.selectAll(".chord")
.data(layout.chords)
.enter().append("path")
.attr("class", "chord")
.style("fill", function(d) { return areas[d.source.index].color; })
.attr("d", path);
 
// Add mouseover title for each chord.
 chord.append("title").text(function(d) {
 return areas[d.source.index].name
 + " → " + areas[d.target.index].name
 + ": " + formatPercent(d.source.value, totalAmount)
 + "% of total trips.\n" + areas[d.target.index].name
 + " → " + areas[d.source.index].name
 + ": " + formatPercent(d.target.value, totalAmount)
 + "% of total trips.";
 });
 
function mouseover(d, i) {
chord.classed("fade", function(p) {
return p.source.index != i
&& p.target.index != i;
});
}
});
});


