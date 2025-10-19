# Name: Karen Lin
# Student ID: 07134248
# Email: linkaren@umich.edu
# Collaborators: Lilly Joelson
# Karen's Functions: calc_avg_bills() and calc_max_island_ratios()
# GenAI Statement: Used ChatGPT to assist with test cases; it provided the expected values by applying the calculations of my functions to my sample data sets (so I didn't have to manually calculate them myself)


# Name: Lillian Joelson
# Student ID: 70108944
# Email: ljoelson@umich.edu
# Collaborators: Karen Lin
# Lilly's Functions: lowest_ratio_2007() and calc_fpercent()
# GenAI Statement: Used Chat GPT to guide coding process on how to build functions in English and debug code. It also helped be build my Unit Tests by giving me ideas on what to test and guiding how to build the code

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
    species_bills = {}

    for penguin in data:
        species = penguin["species"]
        bill_length = penguin["bill_length_mm"]
        bill_depth = penguin["bill_depth_mm"]

        # skip NA entries
        if bill_length == "NA" or bill_depth == "NA":
            continue

        bill_length = float(bill_length)
        bill_depth = float(bill_depth)

        if species not in species_bills:
            species_bills[species] = {"lengths": [], "depths": []}
        species_bills[species]["lengths"].append(bill_length)
        species_bills[species]["depths"].append(bill_depth)

    avg_dict = {}
    for species, bills in species_bills.items():
        avg_length = round(sum(bills["lengths"]) / len(bills["lengths"]), 2)
        avg_depth = round(sum(bills["depths"]) / len(bills["depths"]), 2)
        avg_dict[species] = {
            "avg_bill_length_mm": avg_length,
            "avg_bill_depth_mm": avg_depth,
        }

    return avg_dict

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
        ratio = round(val["avg_bill_length_mm"] / val["avg_bill_depth_mm"],2)
        bill_ratios[species] = {"island": max_island, "ratio": ratio}

    return bill_ratios


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
    

# WRITE OUTPUT FILE
def generate_penguin_report(results):

    data = load_data('penguins.csv')
    avg_bills_all = calc_avg_bills(data)
    bill_ratios = calc_max_island_ratios(data)
    lowest_species, lowest_ratio = lowest_ratio_2007(data)
    female_percent = calc_fpercent(data)

    with open('penguins_report.txt', 'w') as file:
        # intro
        file.write("PROJECT 1 OUTPUT FILE\n")
        file.write("Dataset: penguins.csv\n\n")
        file.write("Collaborators:\n")
        file.write("- Karen Lin (linkaren@umich.edu)\n")
        file.write("- Lillian Joelson (ljoelson@umich.edu)\n\n")
        
        # karen
        file.write("Karen's Calculations:\n")
        file.write(f"1. Average Bill Lengths and Bill Depths of Each Species: \n")
        for species, values in avg_bills_all.items():
            file.write(f"   {species}: \n")
            file.write(f"    - Length = {values['avg_bill_length_mm']} mm \n")
            file.write(f"    - Depth = {values['avg_bill_depth_mm']} mm \n")
        
        file.write(f"2. Bill Ratios in the Most Frequently Occurring Island \n")
        for species, ratio in bill_ratios.items():
            file.write(f"    - {species}: Length-to-Depth Ratio = {ratio}\n")
        
        # lilly
        file.write("Lilly's Calculations:\n")
        file.write(f"1. Species with the Lowest Bill Length-to-Depth Ratio in 2007: {lowest_species}\n")
        file.write(f"   - Ratio: {lowest_ratio}\n")
        file.write(f"2. Percentage of Females in {lowest_species} (2007): {female_percent}%\n\n")


# MAIN

def main():
    data = load_data("penguins.csv")

    avg_bills_all = calc_avg_bills(data)
    print("Average bill lengths and depths for all species:\n")
    for species, values in avg_bills_all.items():
        print(f"{species}: length = {values['avg_bill_length_mm']} mm, depth = {values['avg_bill_depth_mm']} mm")
    
    bill_ratios = calc_max_island_ratios(data)

    print("\nBill length-to-depth ratios for each species in the most frequently occurring island:\n")
    for species, ratio in bill_ratios.items():
        print(f"{species}: {ratio['ratio']}")

    lowest_species, lowest_ratio = lowest_ratio_2007(data)
    if lowest_species:
        print(f"\nIn 2007, the species with the lowest bill length-to-depth ratio is {lowest_species} with a ratio of ({lowest_ratio}).")
    else:
        print("No species data for 2007.")

    percent_females = calc_fpercent(data)
    if percent_females is not None:
        print(f"The percentage of females in species {lowest_species} in 2007 is {percent_females}%")
    else:
        print("No female data for 2007 for lowest species ratio.")


    results = {
    'avg_bills_all': calc_avg_bills,
    'bill_ratios': calc_max_island_ratios,
    'lowest_species, lowest_ratio': lowest_ratio_2007,
    'percent_females': calc_fpercent
    }
    generate_penguin_report(results)

    

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
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.1", "bill_depth_mm": "18.7", "flipper_length_mm": "181", "body_mass_g": "3750", "sex": "male", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.5", "bill_depth_mm": "17.4", "flipper_length_mm": "186", "body_mass_g": "3800", "sex": "female", "year": "2007"},
            {"species": "Adelie", "island": "Dream", "bill_length_mm": "40.2", "bill_depth_mm": "17.1", "flipper_length_mm": "193", "body_mass_g": "3400", "sex": "female", "year": "2009"},
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": "46.1", "bill_depth_mm": "13.2", "flipper_length_mm": "211", "body_mass_g": "4500", "sex": "female", "year": "2007"}
        ]
        
        # edges
        self.edge_sample = [
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": "NA", "bill_depth_mm": "NA", "flipper_length_mm": "NA", "body_mass_g": "NA", "sex": "NA", "year": "2009"},
            {"species": "Gentoo", "island": "Dream", "bill_length_mm": "46.5", "bill_depth_mm": "17.9", "flipper_length_mm": "192", "body_mass_g": "3500", "sex": "female", "year": "2007"},
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50", "bill_depth_mm": "19.2", "flipper_length_mm": "196", "body_mass_g": "3900", "sex": "male", "year": "2007"}
        ]

# ----- calc_avg_bills ----- 

    # general
    def test_calc_avg_bills_gen_1(self):
        result = calc_avg_bills(self.general_sample)
        expected = {
            "Adelie": {"avg_bill_length_mm": 39.6, "avg_bill_depth_mm": 17.73},
            "Gentoo": {"avg_bill_length_mm": 46.1, "avg_bill_depth_mm": 13.2}
        }
        self.assertEqual(result, expected)
    
    def test_calc_avg_bills_gen_2(self): # only adelie species
        data = self.general_sample[0:2]
        result = calc_avg_bills(data)
        expected = {"Adelie": {"avg_bill_length_mm": 39.3, "avg_bill_depth_mm": 18.05}}
        self.assertEqual(result, expected)
    
    # edge
    def test_calc_avg_bills_edge_1(self): # a penguin is missing data
        result = calc_avg_bills(self.edge_sample)
        expected = {
            "Gentoo": {"avg_bill_length_mm": 46.5, "avg_bill_depth_mm": 17.9},
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
            "Adelie": {"island": "Torgersen", "ratio": 2.18}
        }
        self.assertEqual(result, expected)

    def test_calc_max_island_ratios_gen_2(self):
        sample = self.general_sample[::-1]
        result = calc_max_island_ratios(sample)
        expected = {
            "Adelie": {"island": "Torgersen", "ratio": 2.18}
        }
        self.assertEqual(result, expected)

    # edge
    def test_calc_max_island_ratios_edge_1(self):
        result = calc_max_island_ratios(self.edge_sample)
        expected = {
            "Gentoo": {"island": "Dream", "ratio": 2.6},      # ignores NA row for Biscoe
            "Chinstrap": {"island": "Dream", "ratio": 2.6}
        }
        self.assertEqual(result, expected)

    def test_calc_max_island_ratios_edge_2(self): # test ignoring missing values (NA)
        sample = [self.edge_sample[0]]
        result = calc_max_island_ratios(sample)
        expected = {}  # no species counted
        self.assertEqual(result, expected)



#Lilly's Test Cases 

#Finding the species with the lowest bill length to depth ratio in 2007


#Unit Test 1 (general) Tests the general ratio with no odd elements:
    def test_lowest_ratio_2007_1(self):

        data = [
            {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2007'},
            {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.5', 'bill_depth_mm': '17.4', 'flipper_length_mm': '186', 'body_mass_g': '3800', 'sex': 'female', 'year': '2007'},
            {'species': 'Gentoo', 'island': 'Biscoe',    'bill_length_mm': '46.1', 'bill_depth_mm': '13.2', 'flipper_length_mm': '211', 'body_mass_g': '4500', 'sex': 'female', 'year': '2007'},
            {'species': 'Gentoo', 'island': 'Biscoe',    'bill_length_mm': '50.0', 'bill_depth_mm': '16.3', 'flipper_length_mm': '230', 'body_mass_g': '5700', 'sex': 'male', 'year': '2007'},
        ]
        
        species, ratio = lowest_ratio_2007(data)
        self.assertEqual(species, 'Adelie')
        self.assertAlmostEqual(ratio, 2.18, places=2)


    #Unit Test 2 (general) Tests only from the same species:
    def test_lowest_ratio_2007_2(self):
    
        data = [
            {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2007'},
            {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.5', 'bill_depth_mm': '17.4', 'flipper_length_mm': '186', 'body_mass_g': '3800', 'sex': 'female', 'year': '2007'},
        ]
        species, ratio = lowest_ratio_2007(data)
        self.assertEqual(species, 'Adelie')
        self.assertAlmostEqual(ratio, 2.18, places=2)
    


    # Unit Test 3 (Edge Case): attempts to calculate if there is no 2007 in the data set
    def test_lowest_ratio_2007_3(self):
        data = [
            {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2008'},
            {'species': 'Gentoo', 'island': 'Biscoe',    'bill_length_mm': '46.1', 'bill_depth_mm': '13.2', 'flipper_length_mm': '211', 'body_mass_g': '4500', 'sex': 'female', 'year': '2009'},
        ]
        species, ratio = lowest_ratio_2007(data)
        self.assertIsNone(species)
        self.assertIsNone(ratio)


    # Unit Test 4 (Edge Case): attempts to calculate if there are missing part of bill length and depth data
    def test_lowest_ratio_2007_4(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "NA", "bill_depth_mm": "18.7", "flipper_length_mm": "181", "body_mass_g": "3750", "sex": "male", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.1", "bill_depth_mm": "NA", "flipper_length_mm": "186", "body_mass_g": "3800", "sex": "female", "year": "2007"},
        ]
        species, ratio = lowest_ratio_2007(data)
        self.assertIsNone(species)
        self.assertIsNone(ratio)


    #Calculates the fercent of the species from the previous function that is female
    
    #Unit Test 1 (general): Tests the percentage of females with some sex data that is neither male nor female
    def test_calc_fpercent_1(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "40.3", "bill_depth_mm": "18", "flipper_length_mm": "195", "body_mass_g": "3250", "sex": "female", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "NA", "bill_depth_mm": "NA", "flipper_length_mm": "NA", "body_mass_g": "NA", "sex": "NA", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "36.7", "bill_depth_mm": "19.3", "flipper_length_mm": "193", "body_mass_g": "3450", "sex": "female", "year": "2007"},
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50.2", "bill_depth_mm": "18.8", "flipper_length_mm": "202", "body_mass_g": "3800", "sex": "male", "year": "2009"},
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50.5", "bill_depth_mm": "19.6", "flipper_length_mm": "201", "body_mass_g": "4050", "sex": "male", "year": "2007"},
        ]
        self.assertAlmostEqual(calc_fpercent(data), 100.0, places=2)
        
    #Unit Test 2 (general): Tests the percentage of females when there is only one species
    def test_calc_fpercent_2(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "36.7", "bill_depth_mm": "19.3", "flipper_length_mm": "193", "body_mass_g": "3450", "sex": "female", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.3", "bill_depth_mm": "20.6", "flipper_length_mm": "190", "body_mass_g": "3650", "sex": "male", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "38.9", "bill_depth_mm": "17.8", "flipper_length_mm": "181", "body_mass_g": "3625", "sex": "female", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "39.2", "bill_depth_mm": "19.6", "flipper_length_mm": "195", "body_mass_g": "4675", "sex": "male", "year": "2007"},
        ]
        self.assertEqual(calc_fpercent(data), 50.0)


    #Unit Test 3 (edge case): Tests the percentage of females when no data from 2007 is found
    def test_calc_fpercent_3(self):
        data = [
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50.2", "bill_depth_mm": "18.8",
            "flipper_length_mm": "202", "body_mass_g": "3800", "sex": "male", "year": "2009"},
            {"species": "Adelie", "island": "Dream", "bill_length_mm": "38.9", "bill_depth_mm": "18.8",
            "flipper_length_mm": "190", "body_mass_g": "3600", "sex": "female", "year": "2008"},
            {"species": "Adelie", "island": "Dream", "bill_length_mm": "35.7", "bill_depth_mm": "18",
            "flipper_length_mm": "202", "body_mass_g": "3550", "sex": "female", "year": "2008"}
        ]
        self.assertIsNone(calc_fpercent(data))
    
    #Unit Test 4 (edge case): Tests the percentage of females when there is no data on the sexes of the species
    def test_calc_fpercent_4(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "40.3", "bill_depth_mm": "18",
                "flipper_length_mm": "195", "body_mass_g": "3250", "sex": "NA", "year": "2007"}, 
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "NA", "bill_depth_mm": "NA",
                "flipper_length_mm": "NA", "body_mass_g": "NA", "sex": "NA", "year": "2007"}, 
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "36.7", "bill_depth_mm": "19.3",
                "flipper_length_mm": "193", "body_mass_g": "3450", "sex": "NA", "year": "2007"}, 
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50.2", "bill_depth_mm": "18.8",
                "flipper_length_mm": "202", "body_mass_g": "3800", "sex": "NA", "year": "2009"}, 
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": "50.5", "bill_depth_mm": "19.6",
                "flipper_length_mm": "201", "body_mass_g": "4050", "sex": "NA", "year": "2007"}
        ]
        self.assertEqual(calc_fpercent(data), 0)

if __name__ == '__main__':
    unittest.main()
