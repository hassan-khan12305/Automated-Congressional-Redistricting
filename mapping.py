# Importing required Libraries
import geopandas as gpd
import altair as alt
import pandas as pd
import json

# Reading Shapefiles
alt.renderers.enable('mimetype')
file = "ga_2016.shp"
gdf = gpd.read_file(file)

# Add Choropleth Layer and Hover Results
#"GEOID20",
choro = alt.Chart(gdf).mark_geoshape().encode(
    tooltip = ["PRECINCT_N", alt.Tooltip("PRES16DPCT", format = '%'), alt.Tooltip("PRES16RPCT", format = '%')],
    color = alt.Color("PRES16DPCT", type = "quantitative", scale = alt.Scale(scheme = 'redblue'), title = "Votes", legend = alt.Legend(format = ".00%"))
).properties(
    width = 1000,
    height = 700
)

# Producing Map
choro.show()