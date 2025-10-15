# Name: Karen Lin
# Student ID: 07134248
# Email: linkaren@umich.edu
# Collaborators: Lilly Joelson
# Karen's Functions:


# Name: Lillian Joelson
# Student ID: 70108944
# Email: 
# Collaborators: Karen Lin
# Lilly's Functions: 

import csv
import unittest

def load_data(filename):
    data = []
    with open(filename) as inFile:
        reader = csv.DictReader(inFile)
        next(reader)

        for row in reader:
            data.append(row)
    
    return data


# Lilly: calculate avg bill length and avg bill depth for each species in this island




# Karen: calculate avg bill length and avg bill depth for each species → calc_avg_bills
def calc_avg_bills(data):

   # make list of unique species and their bill lengths
    avg_bill_lengths = {} # output: {species1: 11, species2: 22, species3: 33}

    for penguin in data:
        species = penguin['species']
        if species not in avg_bill_lengths:
            unique_species[species] = penguin['bill_length_mm']
        else:  # if species is in unique_species
            continue
    
    # make a dictionary where key is species and value is avg bill length and avg bill depth




#    for penguin in data:
#        if penguin['island'] == max_island:
#            max_island_data.append(penguin)
#            # print(max_island_data)
#            try:
#                for penguin in max_island_data:
#                    # print(penguin)
#                    total_length += float(penguin['bill_length_mm'])
#                    total_depth += float(penguin['bill_depth_mm'])
#            except ValueError:
#                continue


#    avg_length = total_length / len(max_island_data)
#    avg_depth = total_depth / len(max_island_data)
   ratio = avg_length / avg_depth



# Karen: calculate avg bill length and avg bill depth for each species → calc_avg_bills

def calc_max_island_ratios(data):

    # get count of each island
    island_freqs = {}

    for penguin in data:
        island = penguin['island']
        if island not in island_freqs:
            island_freqs[island] = 1
        else: # the island is in the island list
            island_freqs[island] += 1 

    # get name of max island
    max_freq = 0
    max_island = ''

    for island, freq in island_freqs.items():
        if freq > max_freq:
            max_freq = freq
            max_island = island # would keep the most recent island if two have the same frequency
    
    print(f'THe most frequently occuring island is {max_island}.')


# Lilly: find the year w lowest ratio
def calc(data, max_island):

    #set up dict
   year_ratios = {}

   years = set()
   for penguin in data:
       years.add(penguin['year'])

    #set up numbers for calculating average
   for year in years:
       total_length = 0.0
       total_depth = 0.0
       count = 0


       for penguin in data:
           if penguin['island'] == max_island and penguin['year'] == year:
               if penguin['bill_length_mm'] != 'NA' and penguin['bill_depth_mm'] != 'NA':
                   try:
                       total_length += float(penguin['bill_length_mm'])
                       total_depth += float(penguin['bill_depth_mm'])
                       count += 1
                   except ValueError:
                       continue
    #calculate average, then ratio
   avg_length = total_length / count
   avg_depth = total_depth / count
   ratio = avg_length / avg_depth
   year_ratios[year] = ratio

   lowest_year = None
   lowest_ratio = None

   for year, ratio in year_ratios.items():
       if lowest_ratio is None or ratio < lowest_ratio:
           lowest_ratio = ratio
           lowest_year = year #keeps most recent year if they both have the same frequency

   print(f"Year with the lowest bill length/depth ratio is {lowest_year} with a ratio of {lowest_ratio:.2f}.")

   return lowest_year, lowest_ratio


def calc_fpercent(data, lowest_year):
    for data in lowe
    


# MAIN

def main():
    data = load_data("penguins.csv")

    most_pop_island = calculate_max_island(data)
    bill_ratio = calculate_bill_ratios(data, most_pop_island)

if __name__ == "__main__":
    main()


# KAREN'S TEST CASES

# Before you begin writing the code for your calculation functions, please write four test cases per function. 
# Two must test general/usual cases and two test edge cases
# Use a sample of your chosen csv dataset (ensure to use data that has NA/null values) rather than re-reading/reusing your entire csv file.


# ----- calculate_max_island(data) ----- 

# test case 1 (general): generally calculate most popular island
def test_most_pop_island(self):
    sample_data = [
        {"19","Adelie","Torgersen",34.4,18.4,184,3325,"female",2007}
        {"20","Adelie","Torgersen",46,21.5,194,4200,"male",2007}
        {"21","Adelie","Biscoe",37.8,18.3,174,3400,"female",2007}
        {"22","Adelie","Biscoe",37.7,18.7,180,3600,"male",2007}
        {"23","Adelie","Biscoe",35.9,19.2,189,3800,"female",2007}
        {"24","Adelie","Biscoe",38.2,18.1,185,3950,"male",2007}
        ]
    result = calculate_max_island(sample_data)
    self.assertEqual(calculate_max_island(sample_data), 'Biscoe')

# test case 2 (general): return most recent island if each frequency is only 1
def test_single_islands(self):
    sample_data = [
        {"116","Adelie","Biscoe",42.7,18.3,196,4075,"male",2009}
        {"117","Adelie","Torgersen",38.6,17,188,2900,"female",2009}
    ]
    self.assertEqual(calculate_max_island(sample_data), 'Torgersen')

# test case 3 (edge): return most recent island if frequencies are equal
def test_tied_islands(self):
    sample_data = [
        {"275","Gentoo","Biscoe",45.2,14.8,212,5200,"female",2009}
        {"276","Gentoo","Biscoe",49.9,16.1,213,5400,"male",2009}
        {"277","Chinstrap","Dream",46.5,17.9,192,3500,"female",2007}
        {"278","Chinstrap","Dream",50,19.5,196,3900,"male",2007}
        ]
    result = calculate_max_island(sample_data)
    self.assertEqual(result, 'Dream')

# test case 4 (edge): calculate most popular island
def test_empty_islands(self):
    self.assertEqual(calculate_max_island([]), 'Lack of data provided.')


# ----- calculate_bill_ratios(data, max_island) ----- 

# test case 1 (general): calculate ratio of species in most popular island
def test_valid_island_ratio(self):
    sample_data = [
        {"19","Adelie","Torgersen",34.4,18.4,184,3325,"female",2007}
        {"20","Adelie","Torgersen",46,21.5,194,4200,"male",2007}
        {"21","Adelie","Biscoe",37.8,18.3,174,3400,"female",2007}
        {"22","Adelie","Biscoe",37.7,18.7,180,3600,"male",2007}
        {"23","Adelie","Biscoe",35.9,19.2,189,3800,"female",2007}
        {"24","Adelie","Biscoe",38.2,18.1,185,3950,"male",2007}
        ]
    most_pop_island = calculate_max_island(sample_data)
    ratio = calculate_bill_ratios(sample_data, most_pop_island)
    self.assertAlmostEqual(ratio, 2.01)

# test case 2 (general): skip rows w NA values and still compute average
def test_skip_na_values(self):
    sample_data = [
        {"270","Gentoo","Biscoe",48.8,16.2,222,6000,"male",2009}
        {"271","Gentoo","Biscoe",47.2,13.7,214,4925,"female",2009}
        {"272","Gentoo","Biscoe",NA,NA,NA,NA,NA,2009}
        {"273","Gentoo","Biscoe",46.8,14.3,215,4850,"female",2009}
        ]
    ratio = calculate_bill_ratios(sample_data, 'Biscoe')
    self.assertAlmostEqual(ratio, 3.25)

# test case 3 (edge): nonexistent island
    def test_nonexistent_island(self):
        ratio = calculate_bill_ratios(data, 'Nonexistent Test Island')
        self.assertIsNone(ratio)

# test case 4 (edge): when all values are NA
def test_no_matching_island(self):
    sample_data = [{"4","Adelie","Torgersen",NA,NA,NA,NA,NA,2007}]
    ratio = calculate_bill_ratios(sample_data, 'Adelie')
    self.assertIsNone(ratio)