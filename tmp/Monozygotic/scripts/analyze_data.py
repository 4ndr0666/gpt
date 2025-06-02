#!/usr/bin/env python3
"""
analyze_data.py

A simple script to analyze sample interaction data from the Quantum-Linked Twin Interaction Study.
"""

import csv
import statistics
from collections import defaultdict

DATA_FILE = '../data/sample_data.csv'

def load_data(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def analyze_interactions(data):
    # Example analysis: Count interactions per location
    interactions_per_location = defaultdict(int)
    for row in data:
        interactions_per_location[row['Location']] += 1
    return interactions_per_location

def main():
    data = load_data(DATA_FILE)
    interactions = analyze_interactions(data)
    print("Interactions per Location:")
    for location, count in interactions.items():
        print(f"{location}: {count}")

if __name__ == '__main__':
    main()
