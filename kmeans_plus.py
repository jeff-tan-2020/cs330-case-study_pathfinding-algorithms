import time
import csv
import os
import math
import sys
import random
import numpy as np
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

def square_dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def kcenter_initialization(points, k):
    i = random.randint(0, len(points)-1)
    centers = [points[i]]
    while len(centers) < k:
        # continue to add points to centers
        d_squared = [min([square_dist(p, c) for c in centers]) for p in points]
        # Normalize the squared distances to get probabilities
        probabilities = [ds / sum(d_squared) for ds in d_squared]
        # Choose the next center with weighted probability by D^2
        next_center_index = random.choices(range(len(points)), weights=probabilities)[0]
        next_center = points[next_center_index]
        centers.append(next_center)
    return centers 

def assign_points_to_centers(points, centers):
    assignments = []
    for point in points:
        # Find the index of the nearest center
        distances = np.array([math.dist(point, center) for center in centers])
        nearest_center_index = np.argmin(distances)
        # Extract the single value
        nearest_center_index = int(nearest_center_index)
        # Append the index of the assigned center
        assignments.append(nearest_center_index)
    return np.array(assignments)

def compute_centers(points, assignments, k):
    centers = []
    for i in range(k):
        # Calculate the mean of points assigned to the i-th center
        cluster_points = [points[j] for j in range(len(assignments)) if assignments[j]==i]
        if len(cluster_points) > 0:
            new_center = tuple(np.mean(cluster_points, axis=0))
            centers.append(new_center)
    return np.array(centers)

def k_means(points, k, max_iterations=100, tolerance=0.1):
    # 1: Initialize centers
    centers = kcenter_initialization(points, k)
    
    for _ in range(max_iterations): #Trials
        # 2. Assign points to nearest center
        assignments = assign_points_to_centers(points, centers)
        
        # 3. Recompute centers as mean of assigned points
        new_centers = compute_centers(points, assignments, k)
        
        # Threshold value for convergence
        if sum(square_dist(new_centers[i], centers[i]) for i in range(k)) < tolerance:
            break
        # Update centers
        centers = new_centers
    
    return centers, assignments

def cost(points, centers, assignments):
    total_cost = 0
    for i in range(len(points)):
        p = points[i]
        c = centers[assignments[i]]
        total_cost += math.dist(p, c)
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
    centers, assignments = k_means(points, k)
    end_time = time.time()
    total_time = end_time-start_time
    # Writing the centers to a CSV file
    total_cost = cost(points, centers, assignments)
    with open(os.path.join('data-analysis', f'k-means_pp-{k}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Lat', 'Lon'])  # Write header
        writer.writerows(centers)  # Write center coordinates
        writer.writerow([])  # Add an empty row for better separation
        writer.writerow(['Time', total_time])  # Write total cost
        writer.writerow(['Total Cost', total_cost])  # Write total cost

if __name__ == "__main__":
    main()

 