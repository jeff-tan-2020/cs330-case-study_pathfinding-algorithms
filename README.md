# cs330-case-study_pathfinding-algorithms
Fall 2023 Duke CS330 Case Study Project: Done with Miles Eng, Jeffery Tan, Reuben Bufffoe, and Elias Lai

## Data
Data in this case study was provided by the Duke CS330 Teaching Staff. 

## Goals
1. Given data on road networks in New York City, construct weighted undirected graphs with weights representing 
the travel time between two nodes.
- Nodes represented by their latitude and longitude
- The length of each road was given
- The travel speed down a road varied by the hour of day and whether the day was a weekday or weekend

2. Given a list of passengers and their corresponding location and destination, assign their location
and destination to nodes on the road network and put them in a priority queue based on the time they
requested their ride. 
- Starting locations and destinations were given as latitude and longitude values that needed
to be matched to the closest node in the road network based on Euclidean distance.

3.  Given a list of drivers, assign their location to a node on the road network and put them 
in a priority queue based on the time they are available to take on a passenger. 
- Drivers can re-enter the queue after dropping off a passenger, but also have a random chance
to leave the queue and stop working 

4. Implement pathfinding algorithms to calculate the travel time for a driver to pick up
and drop off their passenger

## Algorithms
### Graph generation: 
A total of 48 weighted, undirected graphs were generated with weighted edges
representing the time it took to travel down a road at a given hour in a 24 hour cycle. This
was done for data on weekdays and weekends resulting in 48 total graphs. The graph used in
the pathfinding algorithm depended on the passenger's time that they requested a ride. 

### T1: 
- Assigning passengers and drivers to nodes was done iteratively in O(n) time.
- First come first serve algorithm to match passengers with drivers. 
- Djikstra's pathfinding algorithm was used to calculate pickup and travel times.
- Each driver had a constant probability of leaving the queue.

### T2: 
- Assigning passengers and drivers to nodes was done iteratively.
- Drivers were assigned to passengers based on closest Euclidean distance. 
- Djikstra's pathfinding algorithm was used to calculate pickup and travel times.
- Each driver had a constant probability of leaving the queue.

### T3: 
- Assigning passengers and drivers to nodes was done iteratively.
- Drivers were assigned to passengers based on least pickup time by running Djikstra's algorithm. 
- Djikstra's pathfinding algorithm was used to calculate pickup and travel times.
- Each driver had a constant probability of leaving the queue.

### T4: 
- A Kd-Tree was built to assign passengers and drivers to nodes in O(log n) time. 
- Drivers were assigned to passengers based on least pickup time by running A* algorithm. 
- A*'s pathfinding algorithm was used to calculate pickup and travel times.
- Each driver had a constant probability of leaving the queue.

### T5: 
- A Kd-Tree was built to assign passengers and drivers to nodes. 
- Drivers were assigned to passengers based on closest 5 drivers based on Manhatten distance
and then the least pickup time by running A* algorithm. 
- A*'s pathfinding algorithm was used to calculate pickup and travel times.
- Each driver had a varying probability of leaving the queue, with increasing 
probability of leaving with an increasing number of driving hours, net profits, and number of rides given.

## Results