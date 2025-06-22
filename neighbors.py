import geopandas as gpd
import numpy as np

file = "ga_2016.shp"    

# open file
gdf = gpd.read_file(file)

# add NEIGHBORS column
gdf["NEIGHBORS"] = None  

for index, row in gdf.iterrows():
    #try:
        neighbors = np.array(gdf[gdf.geometry.touches(row['geometry'])].INDEX)
        overlap = np.array(gdf[gdf.geometry.overlaps(row['geometry'])].INDEX)
        neighbors = np.union1d(neighbors, overlap)
        neighbors = np.char.mod('%d', neighbors)
        #print(neighbors)
        gdf.at[index, "NEIGHBORS"] = ", ".join(neighbors)
    #except:
       # print("Error")
       # pass
   
# save GeoDataFrame as a new file
gdf.to_file("ga_2016_neighbors.shp")