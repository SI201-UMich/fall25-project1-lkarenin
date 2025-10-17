# Name: Karen Lin
# Student ID: 07134248
# Email: linkaren@umich.edu
# Collaborators: Lilly Joelson
# Karen's Functions: calc_avg_bills() and calc_max_island_ratios()
# GenAI Statement: Used ChatGPT to assist with test cases; it provided the expected values by applying the calculations of my functions to my sample data sets (so I didn't have to manually calculate them myself)


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

        for row in reader:
            data.append(row)
    
    return data


# Karen: calculate avg bill length and avg bill depth for each species → calc_avg_bills 
    # output: dict, key is species, value is avg bill length and avg bill depth
def calc_avg_bills(data):
    bill_stats = {}  # {species: {bill_length_mm: [], bill_depth_mm: []}}

    for penguin in data:
        species = penguin["species"]
        try:
            length = float(penguin["bill_length_mm"])
            depth = float(penguin["bill_depth_mm"])
        except ValueError: # skips null rows
            continue

        if species not in bill_stats:
            bill_stats[species] = {"bill_length_mm": [], "bill_depth_mm": []}

        bill_stats[species]["bill_length_mm"].append(length)
        bill_stats[species]["bill_depth_mm"].append(depth)

    avg_bills = {}
    for species, bills in bill_stats.items():
        avg_length = sum(bills["bill_length_mm"]) / len(bills["bill_length_mm"])
        avg_depth = sum(bills["bill_depth_mm"]) / len(bills["bill_depth_mm"])
        avg_bills[species] = {"avg_bill_length_mm": round(avg_length, 2), "avg_bill_depth_mm": round(avg_depth, 2)}

    return avg_bills


def calc_max_island_ratios(data):
    # find name of most frequently occurring island
    island_freqs = {}
    for penguin in data:
        island = penguin["island"]
        if island not in island_freqs:
            island_freqs[island] = 1
        else:
            island_freqs[island] += 1

    max_freq = 0
    max_island = ""
    for island, freq in island_freqs.items():
        if freq > max_freq:
            max_freq = freq
            max_island = island

    print(f"The most frequently occurring island is {max_island}.")

    # makes new list of all penguins' data from that island
    island_data = []
    for penguin in data:
        if penguin["island"] == max_island:
            island_data.append(penguin)

    # call calc_avg_bills() on this island’s data
    avg_bills = calc_avg_bills(island_data)

    # calculate bill length to depth ratio for each species on that island
    bill_ratios = {}
    for species, val in avg_bills.items():
        ratio = val["avg_bill_length_mm"] / val["avg_bill_depth_mm"]
        bill_ratios[species] = round(ratio, 2)

    return max_island, bill_ratios


# Lilly: find the species with the lowest ratio in 2007

def lowest_ratio_2007(data):

    penguins_2007 = []
    for penguin in data:
        if penguin['year'] != "2007":
            continue
        try:
            float(penguin["bill_length_mm"])
            float(penguin["bill_depth_mm"])
        except ValueError:
            continue
        penguins_2007.append(penguin)
    
    avg_bills_2007 = calc_avg_bills(penguins_2007)
    
    ratios = {}
    for species, stats in avg_bills_2007.items():
        ratio = stats['avg_bill_length_mm'] / stats['avg_bill_depth_mm']
        ratios[species] = round(ratio, 2)
    
    if not ratios:
        return None, None
    
    lowest_species = min(ratios, key=ratios.get)
    lowest_ratio = ratios[lowest_species]
    return lowest_species, lowest_ratio

# Lilly: find the percentage of females that make up whichever species has the lowest bill length to depth ratio in 2007

def calc_fpercent(data):

    lowest_species, _ = lowest_ratio_2007(data)

    if not lowest_species:
        return None
    
    female_count = 0
    total_count = 0
    for penguin in data:
        if penguin['year'] != "2007":
            continue
        if penguin['species'] != lowest_species:
            continue
        sex = penguin['sex'].strip().lower()
        if sex == "female":
            female_count += 1
        if sex in ("female", "male"):
            total_count += 1

    if total_count == 0:
        return 0 

    percent = (female_count / total_count) * 100
    return round(percent, 2)
    


# MAIN

def main():
    data = load_data("penguins.csv")

    avg_bills_all = calc_avg_bills(data)
    print("Average bill lengths and depths for all species:")
    for species, values in avg_bills_all.items():
        print(f"{species}: length = {values['avg_bill_length_mm']} mm, depth = {values['avg_bill_depth_mm']} mm")
    
    most_pop_island, bill_ratios = calc_max_island_ratios(data)
    print(f"The bill length-to-depth ratios for each species on {most_pop_island}:")
    for species, ratio in bill_ratios.items():
        print(f"{species}: {ratio}")


if __name__ == "__main__":
    main()


# KAREN'S TEST CASES

# Before you begin writing the code for your calculation functions, please write four test cases per function. 
# Two must test general/usual cases and two test edge cases
# Use a sample of your chosen csv dataset (ensure to use data that has NA/null values) rather than re-reading/reusing your entire csv file.


import unittest

class TestPenguinFunctions(unittest.TestCase):
    
    def setUp(self):
        # general
        self.general_sample = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.1", "bill_depth": "18.7", "flipper_length_mm": "181", "body_mass_g": "3750", "sex": "male", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.5", "bill_depth": "17.4", "flipper_length_mm": "186", "body_mass_g": "3800", "sex": "female", "year": "2007"},
            {"species": "Adelie", "island": "Dream", "bill_length_mm": "40.2", "bill_depth": "17.1", "flipper_length_mm": "193", "body_mass_g": "3400", "sex": "female", "year": "2009"},
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": "46.1", "bill_depth": "13.2", "flipper_length_mm": "211", "body_mass_g": "4500", "sex": "female", "year": "2007"}
        ]
        
        # edges
        self.edge_sample = [
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": "NA", "bill_depth": "NA", "flipper_length_mm": "NA", "body_mass_g": "NA", "sex": "NA", "year": "2009"},
            {"species": "Gentoo", "island": "Dream", "bill_length_mm": "46.5", "bill_depth": "17.9", "flipper_length_mm": "192", "body_mass_g": "3500", "sex": "female", "year": "2007"},
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50", "bill_depth": "19.2", "flipper_length_mm": "196", "body_mass_g": "3900", "sex": "male", "year": "2007"}
        ]

# ----- calc_avg_bills ----- 

    # general
    def test_calc_avg_bills_gen_1(self):
        result = calc_avg_bills(self.general_sample)
        expected = {
            "Adelie": {"avg_bill_length_mm": 39.6, "avg_bill_depth_mm": 17.33},
            "Gentoo": {"avg_bill_length_mm": 46.1, "avg_bill_depth_mm": 13.2}
        }
        self.assertEqual(result, expected)
    
    def test_calc_avg_bills_gen_2(self): # only adelie species
        data = [self.general_sample[0:2]]
        result = calc_avg_bills(data)
        expected = {"Adelie": {"avg_bill_length_mm": 39.6, "avg_bill_depth_mm": 17.33}}
        self.assertEqual(result, expected)
    
    # edge
    def test_calc_avg_bills_edge_1(self): # a penguin is missing data
        result = calc_avg_bills(self.edge_sample)
        expected = {
            "Gentoo": {"avg_bill_length_mm": 23.25, "avg_bill_depth_mm": 8.95},
            "Chinstrap": {"avg_bill_length_mm": 50, "avg_bill_depth_mm": 19.2}
        }
        self.assertEqual(result, expected)
    
    def test_calc_avg_bills_edge_2(self): # empty data set
        result = calc_avg_bills([])
        self.assertEqual(result, {})
    
# ----- calc_max_island_ratios ----
    
    # general
    def test_calc_max_island_ratios_gen_1(self):
        result = calc_max_island_ratios(self.general_sample)
        expected = {
            "Adelie": {"island": "Torgersen", "ratio": 0.67},
            "Gentoo": {"island": "Biscoe", "ratio": 1.0}
        }
        self.assertEqual(result, expected)

    def test_calc_max_island_ratios_gen_2(self):
        sample = self.general_sample[::-1]
        result = calc_max_island_ratios(sample)
        expected = {
            "Adelie": {"island": "Torgersen", "ratio": 0.67},
            "Gentoo": {"island": "Biscoe", "ratio": 1.0}
        }
        self.assertEqual(result, expected)

    # edge
    def test_calc_max_island_ratios_edge_1(self):
        result = calc_max_island_ratios(self.edge_sample)
        expected = {
            "Gentoo": {"island": "Dream", "ratio": 0.5},      # ignores NA row for Biscoe
            "Chinstrap": {"island": "Dream", "ratio": 1.0}
        }
        self.assertEqual(result, expected)

    def test_calc_max_island_ratios_edge_2(self): # test ignoring missing values (NA)
        sample = [self.edge_sample[0]]
        result = calc_max_island_ratios(sample)
        expected = {}  # no species counted
        self.assertEqual(result, expected)



#Lilly's Test Cases 

#Finding the species with the lowest bill length to depth ratio in 2007

# test case 1 (general): generally calculate the lowest ratio in 2007

def lowest_ratio_2007(self):
    sample_data = [
        {"267", "Gentoo", "Biscoe", 46.2,14.1,2175,	"female", 2009}
        {"268", "Gentoo", "Biscoe", 55.1,16,230,5850, "male", 2009}
        {"3", "Adelie",	"Torgersen",	40.3,18,195,3250, "female", 2007}
        {"4", "Adelie", "Torgersen", NA,NA,NA,NA, NA, 2007}
        {"5", "Adelie", "Torgersen"	36.7,19.3,193,3450, "female", 2007} 
    ]
    result = lowest_ratio_2007(sample_data)
    self.assertEqual(lowest_ratio_2007(sample_data), 'Biscoe')

 # test case 2 (general): calculates the lowest ratio if there is no 2007 in the data set

def lowest_ratio_2007(self):
    sample_data = [
        {"267", "Gentoo", "Biscoe", 46.2,14.1,2175,	"female", 2009}
        {"268", "Gentoo", "Biscoe", 55.1,16,230,5850, "male", 2009}
        {"61", "Adelie", "Biscoe", 35.7,16.9,185,3150, "female"	2008}
        {"62", "Adelie" "Biscoe" 41.3,21.1,195,4400, "male", 2008}
        {"63", "Adelie", "Biscoe", 37.6,17,185,3600, "female", 2008}
    ]
    result = lowest_ratio_2007(sample_data)
    self.assertEqual(lowest_ratio_2007(sample_data), 'Biscoe')


#Finding the percentage fo female penguins that make up the population of the penguin species with the lowest bill length to depth ratio in 2007

class TestCalcFPercent(unittest.TestCase):
    def test_general_1(self):
        data = [
            {"3", "Adelie", "Torgersen", 40.3,18,195,3250, "female", 2007}
            {"4", "Adelie", "Torgersen", NA	NA	NA	NA	NA	2007}
            {"5", "Adelie", "Torgersen", 36.7,19.3,193,3450, "female", 2007}
            {}
5	Adelie	Torgersen	36.7	19.3	193	3450	female	2007
6	Adelie	Torgersen	39.3	20.6	190	3650	male	2007
7	Adelie	Torgersen	38.9	17.8	181	3625	female	2007
8	Adelie	Torgersen	39.2	19.6	195	4675	male	2007,
        ]
        self.assertEqual(calc_fpercent(data), 50.0)
        
    def test_general_2(self):
        data = [
            {'species': 'Chinstrap', 'year': '2007', 'bill_length_mm': '48.7', 'bill_depth_mm': '17.4', 'sex': 'female'},
            {'species': 'Chinstrap', 'year': '2007', 'bill_length_mm': '46.5', 'bill_depth_mm': '16.0', 'sex': 'male'},
            {'species': 'Chinstrap', 'year': '2007', 'bill_length_mm': '46.5', 'bill_depth_mm': '16.0', 'sex': 'female'},
            {'species': 'Chinstrap', 'year': '2007', 'bill_length_mm': '50.0', 'bill_depth_mm': '18.0', 'sex': 'male'},
        ]
        # Chinstrap is only species, females=2, total=4  => 2/4*100=50.0%
        self.assertEqual(calc_fpercent(data), 50.0)

    # EDGE CASES
    def test_edge_none_found(self):
        # No 2007 data
        data = [
            {'species': 'Adelie', 'year': '2008', 'bill_length_mm': '33.1', 'bill_depth_mm': '16.1', 'sex': 'female'},
            {'species': 'Gentoo', 'year': '2008', 'bill_length_mm': '45.0', 'bill_depth_mm': '14.0', 'sex': 'male'},
        ]
        self.assertIsNone(calc_fpercent(data))
    
    def test_edge_all_missing_sex(self):
        data = [
            {'species': 'Adelie', 'year': '2007', 'bill_length_mm': '39', 'bill_depth_mm': '18', 'sex': 'NA'},
            {'species': 'Adelie', 'year': '2007', 'bill_length_mm': '37', 'bill_depth_mm': '17', 'sex': ''},
            {'species': 'Adelie', 'year': '2007', 'bill_length_mm': '35', 'bill_depth_mm': '16', 'sex': ' '},
        ]
        # species found, but none have valid sex fields; total = 0
        self.assertEqual(calc_fpercent(data), 0)