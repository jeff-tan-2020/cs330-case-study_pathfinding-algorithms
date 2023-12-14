import time
import csv
import os
import math
import sys
import random
def read_passengers():
    # Passengers with the earliest date_time have the highest priority
    points = []
    with open(os.path.join('data', 'passengers.csv'), 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            source_lat = float(row['Source Lat'])
            source_lon = float(row['Source Lon'])
            pt = (source_lat, source_lon)
            points.append(pt)    
    return points   

    #after driver pickup have to use node and road information from adjacency, edges, and node_data to get time

def k_center(points, k):
    i = random.randint(0, len(points)-1)
    centers = [points[i]]
    while len(centers) < k:
        # continue to add points to centers
        maxdist = 0
        maxpt = None
        for p in points:
            dist = min([math.dist(p, c) for c in centers])
            if dist > maxdist:
                maxdist = dist
                maxpt = p
        centers.append(maxpt)
    return centers     

                 
def cost(points, centers):
    total_cost = 0
    for p in points:
        dist = min([math.dist(p, c) for c in centers])
        total_cost += dist
    return total_cost         

# Your main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python kcenter.py <k = # of centers>")
        sys.exit(1)
    k = int(sys.argv[1])

    if k <= 0:
        print("Please provide a positive integer for k.")
        sys.exit(1)
    
    points = read_passengers()
    start_time = time.time()
    # Running the k-center algorithm
    centers = k_center(points, k)
    end_time = time.time()
    total_time = end_time-start_time
    # Writing the centers to a CSV file
    total_cost = cost(points, centers)
    with open(os.path.join('data-analysis', f'k-centers-{k}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Lat', 'Lon'])  # Write header
        writer.writerows(centers)  # Write center coordinates
        writer.writerow([])  # Add an empty row for better separation
        writer.writerow(['Time', total_time])  # Write total cost
        writer.writerow(['Total Cost', total_cost])  # Write total cost

if __name__ == "__main__":
    main()

 