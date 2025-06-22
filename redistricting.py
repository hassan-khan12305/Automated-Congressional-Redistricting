# importing required libraries
import geopandas as gpd
import pandas as pd
import random
import altair as alt
from altair_saver import save
import csv
import metrics

# opening a csv file to write data for district plans
f = open('results.csv', 'a', newline = '')
writer = csv.writer(f)

# iterate for the amount of desired plans
for plannumber in range(201, 202):
    # establishes all necessary variables for a single district
    rep_pop = 0
    dem_pop = 0
    tot_pop = 0
    # establishes lists to compile data for each district in the district plan
    rep_pops = []
    dem_pops = []
    tot_pops = []
    # create necessary lists to retrieve data from the dataframe of the shapefile
    precincts = []
    used = []
    neighbors = []
    rep_list = []
    dem_list = []
    tot_list = []
    rand_neighbors = []
    # creates a list composed of precincts in a singular district and a list of each district's list
    district = []
    districts = []
    dist = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14"]

    # opens the shapefile created by neighbors.py and creates a column for a district identifier
    file = "ga_2016_neighbors.shp"    
    gdf = gpd.read_file(file)
    gdf["DIST"] = None

    # iterates through the dataframe to collect necessary information for each precinct and stores in respective list
    for index, row in gdf.iterrows():
        precincts.append(str(gdf.at[index, "INDEX"]))
        neighbors.append(gdf.at[index, "NEIGHBORS"])
        rep_list.append(gdf.at[index, "PRES16R"])
        dem_list.append(gdf.at[index, "PRES16D"])
        tot_list.append(gdf.at[index, "TOTPOP"])

    # selects a random precinct and collects its attributes to establish a beginning point for the algorithm
    rand = random.randrange(0, len(precincts))
    index = random.randrange(0, len(precincts))
    current = precincts[index]
    district.append(current)
    used.append(current)
    gdf.at[index, "DIST"] = "D1"
    rep_pop += rep_list[index]
    dem_pop += dem_list[index]
    tot_pop += tot_list[index]
    rand_neighbors = neighbors[index].split(", ")
    previous = current
    i = 0
    num = 0

    # creates a loop to continue drawing districts until 14 are drawn and the plan is completed
    while len(districts) < 14:
        # initializes variables for a singular district
        district = []
        rep_pop = 0
        dem_pop = 0
        tot_pop = 0
        count = 0
        # selects a random precinct by index and splits its neighbors into a list
        index = random.randrange(0, len(precincts)) 
        rand_neighbors = neighbors[index].split(", ") 
        # creates a loop to continue drawing the district until the target population is met or surpassed
        while tot_pop < 691975:
            for p in rand_neighbors:
                current = p
                i += 1
                # adds the current precinct and respective data to the district if not already used
                if current not in used:
                    district.append(current)
                    used.append(current)
                    index = precincts.index(current)
                    gdf.at[index, "DIST"] = dist[num]
                    rep_pop += rep_list[index]
                    dem_pop += dem_list[index]
                    tot_pop += tot_list[index]
                # selects another precinct from the district or previous precinct to continue drawing
                else:
                    if len(district) != 0:
                        index = precincts.index(district[random.randrange(0, len(district))])
                    else:
                        index = precincts.index(previous)
                    rand_neighbors = neighbors[index].split(", ")
            # counts how many times the program is attempting to continue drawing
            count = count + 1
            # stops after 500 attempts in order to prevent an infinite loop
            if count > 500:
                break
        # after the district is created, it and its respective attributes are saved in lists.
        if tot_pop > 0:
            districts.append(district)
            tot_pops.append(tot_pop)
            rep_pops.append(rep_pop)
            dem_pops.append(dem_pop)
            previous = rand_neighbors[random.randrange(0, len(rand_neighbors))]
            num += 1

    # after all districts are drawn, finds all the precincts that are not assigned to any district
    unused = list(set(precincts)-set(used))
    while len(unused) > 0:
        unused = list(set(precincts)-set(used))
        # iterates through unused precincts
        for p in unused:
            neighbor_districts = []
            index = precincts.index(p)
            rand_neighbors = neighbors[index].split(", ")
            # finds which districts the precinct's neighbors are in, if any
            for n in rand_neighbors:
                index = precincts.index(n)
                neighbor_districts.append(gdf.at[index, "DIST"])
            index = precincts.index(p)
            neighbor_districts = list(filter(lambda item: item is not None, neighbor_districts))
            # selects a random district that borders the unused precinct and adds the precinct to that district
            if len(neighbor_districts) > 0:
                randdist = neighbor_districts[random.randrange(0, len(neighbor_districts))]
                gdf.at[index, "DIST"] = randdist
                # updates respective attributes of the district with precinct data
                tot_pops[dist.index(randdist)] = tot_pops[dist.index(randdist)] + tot_list[index]
                rep_pops[dist.index(randdist)] = rep_pops[dist.index(randdist)] + rep_list[index]
                dem_pops[dist.index(randdist)] = dem_pops[dist.index(randdist)] + dem_list[index]
                used.append(p)

    # prints the plan and its ID after it is complete
    print(f'Plan {plannumber:03d}')

    # metrics for the plan are calculated using the methods defined in metrics.py
    completeness = (metrics.completeness(unused))
    popdeviation = ("{:.2%}".format(metrics.popdeviation(tot_pops)))
    distcount = (metrics.distcount(rep_pops, dem_pops, False))
    efficiencygap = ("{:.2%}".format(metrics.efficiencygap(rep_pops, dem_pops)))
    partisanbias = ("{:.2%}".format(metrics.partisanbias(rep_pops, dem_pops)))
    meanmeadiandiff = ("{:.2%}".format(metrics.meanmediandiff(rep_pops, dem_pops)))
    declination = ("{:.2%}".format(metrics.declination(rep_pops, dem_pops)))

    # FOR TESTING
    print(f'Total Populations: {tot_pops}')
    print(f'Republican Populations: {rep_pops}')
    print(f'Democratic Populations: {dem_pops}')
    print(f'Population Deviation: {popdeviation}')
    print(f'District Counts: {distcount}')
    print(f'Efficiency Gap: {efficiencygap}')
    print(f'Partisan Bias: {partisanbias}')
    print(f'Mean-Median Difference: {meanmeadiandiff}')
    print(f'Declination: {declination}')

    # a row is written in the csv for each plan and its calculated metrics
    writer.writerow([plannumber, completeness, popdeviation, distcount[0], distcount[1], distcount[2], efficiencygap, partisanbias, meanmeadiandiff, declination])
    
    #gdf.to_file(f'plan{plannumber:03d}.shp') optional line to save plans as shapefiles

    # saves the plan as an html file to view the district plan and save as an image if needed
    alt.Chart(gdf).mark_geoshape().encode(
    color = alt.Color("DIST", type = "nominal", scale = alt.Scale(scheme = 'category20'))
    ).show()#save(f'plan{plannumber:03d}.html')

# prints Done when all 200 plans have been created
print("Done")