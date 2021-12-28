# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 09:19:23 2021

@author: benjaminas
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os

def make_dict(names, months, years, max_wind, area, dmg, deaths):
    res = {}
    for  i,name in enumerate(names):
        res [name] = {'Name': name, 'Month': months[i], 'Year': years[i], 'Max Sustained Wind': max_wind[i], 'Areas Affected': area[i], 'Damage': dmg[i], 'Deaths': deaths[i]}
    return res


def org_by_(mdict, key= 'Year'):
    """
    organise dictionary by the key provided
    """
    res = {}
    for k,v in mdict.items():
        res[v[key]] = v
    return res

def org_by_mortality(mdict, key ="mortality_scale"):
    '''
    organise by mortality scale or damage scale
    '''
    res = {1 : {}, 2 : {}, 3 : {}, 4 : {}, 0 : {}}
    for k,v in mdict.items():
        if key in v:
          res[v[key]][k] = v
    return res

def clean_numbers(mlist):
    '''
    remove and replace chars in the strings to numbers
    '''
    res = []
    for item in mlist:
        if item =="Damages not recorded":
            res.append(item)
        elif 'B' in item:
            res.append(float(item[:-1])*1e9)
        elif 'M' == item[-1]:
            res.append(float(item[:-1])*1e6)    
    return res

def worst_hit(areas):
    """
    Parameters
    ----------
    areas : dict of areas and amount of times it was hit

    Returns
    -------
    str, int of the worst hit area and the amount of times it was hit

    """
    wh_area = max(areas, key=areas.get)
    return wh_area, areas.get(wh_area)

def count_areas(mdict):
    """
    Parameters
    ----------
    mdict : dictionary containing information about the hurricanes
        

    Returns 
    -------
    dict each area as a key containing the number of counts it has been hit

    """
    
    res = {}
    
    for val in mdict.values():
       for area in val["Areas Affected"]:
        if area not in res.keys():
            res[area] = 0
        else:
            res[area] += 1
    return res


def find_max_value(mdict, mkey= 'Deaths'):
    mdead = {}
    for key, value in mdict.items():
        if value[mkey] == 'Damages not recorded':
                print("we skip")
        else:
            mdead.update({key : value[mkey]})
            
    deadliest_hurricane = max(mdead, key=mdead.get)
    return deadliest_hurricane, mdead.get(deadliest_hurricane)  

def add_mortality_scale(mdict ):
    mortality_scale = {0: 0,
                   1: 100,
                   2: 500,
                   3: 1000,
                   4: 10000}
    res = {}
    for key, value in mdict.items():
        for key2,value2 in mortality_scale.items():
            if value['Deaths'] > value2:
                res[key] = ({'mortality_scale' : key2})
        
        
    for key in res.keys():
        mdict[key].update(res[key])    
    return  0


def add_damage_scale(mdict ):
    damage_scale = {0: 0,
                1: 100000000,
                2: 1000000000,
                3: 10000000000,
                4: 50000000000}
    res = {}
    for key, value in mdict.items():
       if  value['Damage'] != 'Damages not recorded': 
        
        for key2,value2 in damage_scale.items():
            if value['Damage'] > value2:
                res[key] = ({'damage scale' : key2})
                print()
        
        
    for key in res.keys():
        mdict[key].update(res[key])   
        print(mdict[key])
    return  0
# names of hurricanes
names = ['Cuba I', 'San Felipe II Okeechobee', 'Bahamas', 'Cuba II', 'CubaBrownsville', 'Tampico', 'Labor Day', 'New England', 'Carol', 'Janet', 'Carla', 'Hattie', 'Beulah', 'Camille', 'Edith', 'Anita', 'David', 'Allen', 'Gilbert', 'Hugo', 'Andrew', 'Mitch', 'Isabel', 'Ivan', 'Emily', 'Katrina', 'Rita', 'Wilma', 'Dean', 'Felix', 'Matthew', 'Irma', 'Maria', 'Michael']

# months of hurricanes
months = ['October', 'September', 'September', 'November', 'August', 'September', 'September', 'September', 'September', 'September', 'September', 'October', 'September', 'August', 'September', 'September', 'August', 'August', 'September', 'September', 'August', 'October', 'September', 'September', 'July', 'August', 'September', 'October', 'August', 'September', 'October', 'September', 'September', 'October']

# years of hurricanes
years = [1924, 1928, 1932, 1932, 1933, 1933, 1935, 1938, 1953, 1955, 1961, 1961, 1967, 1969, 1971, 1977, 1979, 1980, 1988, 1989, 1992, 1998, 2003, 2004, 2005, 2005, 2005, 2005, 2007, 2007, 2016, 2017, 2017, 2018]

# maximum sustained winds (mph) of hurricanes
max_sustained_winds = [165, 160, 160, 175, 160, 160, 185, 160, 160, 175, 175, 160, 160, 175, 160, 175, 175, 190, 185, 160, 175, 180, 165, 165, 160, 175, 180, 185, 175, 175, 165, 180, 175, 160]

# areas affected by each hurricane
areas_affected = [['Central America', 'Mexico', 'Cuba', 'Florida', 'The Bahamas'], ['Lesser Antilles', 'The Bahamas', 'United States East Coast', 'Atlantic Canada'], ['The Bahamas', 'Northeastern United States'], ['Lesser Antilles', 'Jamaica', 'Cayman Islands', 'Cuba', 'The Bahamas', 'Bermuda'], ['The Bahamas', 'Cuba', 'Florida', 'Texas', 'Tamaulipas'], ['Jamaica', 'Yucatn Peninsula'], ['The Bahamas', 'Florida', 'Georgia', 'The Carolinas', 'Virginia'], ['Southeastern United States', 'Northeastern United States', 'Southwestern Quebec'], ['Bermuda', 'New England', 'Atlantic Canada'], ['Lesser Antilles', 'Central America'], ['Texas', 'Louisiana', 'Midwestern United States'], ['Central America'], ['The Caribbean', 'Mexico', 'Texas'], ['Cuba', 'United States Gulf Coast'], ['The Caribbean', 'Central America', 'Mexico', 'United States Gulf Coast'], ['Mexico'], ['The Caribbean', 'United States East coast'], ['The Caribbean', 'Yucatn Peninsula', 'Mexico', 'South Texas'], ['Jamaica', 'Venezuela', 'Central America', 'Hispaniola', 'Mexico'], ['The Caribbean', 'United States East Coast'], ['The Bahamas', 'Florida', 'United States Gulf Coast'], ['Central America', 'Yucatn Peninsula', 'South Florida'], ['Greater Antilles', 'Bahamas', 'Eastern United States', 'Ontario'], ['The Caribbean', 'Venezuela', 'United States Gulf Coast'], ['Windward Islands', 'Jamaica', 'Mexico', 'Texas'], ['Bahamas', 'United States Gulf Coast'], ['Cuba', 'United States Gulf Coast'], ['Greater Antilles', 'Central America', 'Florida'], ['The Caribbean', 'Central America'], ['Nicaragua', 'Honduras'], ['Antilles', 'Venezuela', 'Colombia', 'United States East Coast', 'Atlantic Canada'], ['Cape Verde', 'The Caribbean', 'British Virgin Islands', 'U.S. Virgin Islands', 'Cuba', 'Florida'], ['Lesser Antilles', 'Virgin Islands', 'Puerto Rico', 'Dominican Republic', 'Turks and Caicos Islands'], ['Central America', 'United States Gulf Coast (especially Florida Panhandle)']]

# damages (USD($)) of hurricanes
damages = ['Damages not recorded', '100M', 'Damages not recorded', '40M', '27.9M', '5M', 'Damages not recorded', '306M', '2M', '65.8M', '326M', '60.3M', '208M', '1.42B', '25.4M', 'Damages not recorded', '1.54B', '1.24B', '7.1B', '10B', '26.5B', '6.2B', '5.37B', '23.3B', '1.01B', '125B', '12B', '29.4B', '1.76B', '720M', '15.1B', '64.8B', '91.6B', '25.1B']

# deaths for each hurricane
deaths = [90,4000,16,3103,179,184,408,682,5,1023,43,319,688,259,37,11,2068,269,318,107,65,19325,51,124,17,1836,125,87,45,133,603,138,3057,74]

# 1
# Update Recorded Damages
conversion = {"M": 1000000,
              "B": 1000000000}

# test function by updating damages
damages = clean_numbers(damages)


# 2 
# Create a Table

# Create and view the hurricanes dictionary
mdict = make_dict(names, months, years, max_sustained_winds, areas_affected, damages, deaths)
# 3
# Organizing by Year

# create a new dictionary of hurricanes with year and key
mdict_y = org_by_(mdict)


# 4
# Counting Damaged Areas

# create dictionary of areas to store the number of hurricanes involved in
area_dict = count_areas(mdict)


# 5 
# Calculating Maximum Hurricane Count

# find most frequently affected area and the number of hurricanes involved in

print(worst_hit(area_dict))
# 6
# Calculating the Deadliest Hurricane
print(find_max_value(mdict))
# find highest mortality hurricane and the number of deaths

# 7
# Rating Hurricanes by Mortality
add_mortality_scale(mdict)

# categorize hurricanes in new dictionary with mortality severity as key

mdict_m = org_by_mortality(mdict)
# 8 Calculating Hurricane Maximum Damage

# find highest damage inducing hurricane and its total cost

print(find_max_value(mdict,"Damage"))
# 9
# Rating Hurricanes by Damage
add_damage_scale(mdict)
mdict_dmg = org_by_mortality(mdict,key = 'damage scale' ) 
  
# categorize hurricanes in new dictionary with damage severity as key
