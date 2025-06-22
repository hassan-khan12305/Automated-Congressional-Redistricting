# importing required libraries
import statistics as stat
import numpy as np

# checks the completeness requirement by ensuring all precincts were used and assigned a district
def completeness(unused_list):
    return len(unused_list) == 0

# calculates the population deviation of the district plan using standard deviation and the target population
def popdeviation(totals_list):
    return np.std(totals_list)/691975

def distcount(repvotes_list, demvotes_list, pbcalc):
    # initialize count variables for each party and competitive
    rep = 0
    dem = 0
    comp = 0
    # checks if method is being used for partisan bias calculation
    if pbcalc:
        # counts number of districts won by each democrats and republicans
        for i in range(14):
            pct = repvotes_list[i]
            if pct >= 0.5:
                rep += 1
            else:
                dem += 1
        return [rep, dem]
    else:
        for i in range(14):
            # counts number won by each democrats and republicans by a 5% margin above 50%
            total = repvotes_list[i] + demvotes_list[i]
            pct = repvotes_list[i] / total
            if pct > 0.55:
                rep += 1
            elif pct < 0.45:
                dem += 1
            # counting the districts in the 45%-55% range as competitive
            else:
                comp += 1
        return [rep, dem, comp]

def efficiencygap(repvotes_list, demvotes_list):
    # initializing necessary variables
    repinefficient = 0
    deminefficient = 0
    totalvotes = sum(repvotes_list) + sum(demvotes_list)
    reppct = 0
    dempct = 0
    for i in range(14):
        # calculating republican and democrat vote percentage from vote numbers
        total = repvotes_list[i] + demvotes_list[i]
        reppct = repvotes_list[i]/total
        dempct = demvotes_list[i]/total
        # if district won by republicans
        if reppct >= 0.5:
            # all republican votes over 50% are counted as inefficient
            repinefficient += repvotes_list[i] * (reppct - 0.5)
            # all democratic votes are counted as inefficient
            deminefficient += demvotes_list[i]
        # repeated for districts won by democrats, the other way.
        else:
            deminefficient += demvotes_list[i] * (dempct - 0.5)
            repinefficient += repvotes_list[i]
    # calculates and returns efficiency gap
    return (deminefficient - repinefficient)/totalvotes

def partisanbias(repvotes_list, demvotes_list):
    # calculates statewide vote percentage for republicans and democrats
    reppct = sum(repvotes_list) / (sum(repvotes_list) + sum(demvotes_list))
    dempct = sum(demvotes_list) / (sum(repvotes_list) + sum(demvotes_list))
    # initializes lists for shifted vote results
    newreppct = []
    newdempct = []
    # calculates the shifter (may be negative if democrats win statewide)
    shifter = reppct - 0.5
    for i in range(14):
        # calculates vote percentages for each party for each district
        total = repvotes_list[i] + demvotes_list[i]
        reppct = repvotes_list[i]/total
        dempct = demvotes_list[i]/total
        # shifts the vote results and adds them to the list
        newreppct.append(reppct - shifter)
        newdempct.append(dempct + shifter)
    # uses the distcount method to count number of democratic and republican districts
    counts = distcount(newreppct, newdempct, True)
    # calculates and returns partisan bias
    return ((counts[0]/14) - 0.5)

def meanmediandiff(repvotes_list, demvotes_list):
    # initializes lists for vote percentages for each district
    reppct = []
    dempct = []
    for i in range(14):
        # calculates vote percentages for each party and adds to list
        total = repvotes_list[i] + demvotes_list[i]
        reppct.append(repvotes_list[i]/total)
        dempct.append(demvotes_list[i]/total)
    # calculates and returns the difference between median and mean of district vote percentages
    return stat.median(reppct) - stat.mean(reppct)

def declination(repvotes_list, demvotes_list):
    # initializes lists for vote percentages for each district
    reppct = []
    dempct = []
    for i in range(14):
        # calculates vote percentages for each party and adds to list
        total = repvotes_list[i] + demvotes_list[i]
        reppct.append(repvotes_list[i]/total)
        dempct.append(demvotes_list[i]/total)
    # calculates the mean (center of mass) for both republican vote percentages and democratic vote percentages and returns the difference
    return stat.mean(reppct) - stat.mean(dempct)