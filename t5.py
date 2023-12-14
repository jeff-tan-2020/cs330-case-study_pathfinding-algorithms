# A* Algorithm faster than Djikstra
# Heuristic H based on Euclidean distance 

import time
import csv
import heapq
from datetime import timedelta
#from random import random
from queue import PriorityQueue
from probability_distributions import calculate
from buildgraph_v2 import build_graph
from A_star import shortest_path
from passenger_driver import passenger_driver_queues_t4

def manhattan(lat1, lon1, lat2, lon2):
    return abs(lat1-lat2) + abs(lon1-lon2) 

def T5(trial_num):

    start_time = time.time()

    print("--- T5")

    driver_queue, passenger_queue = passenger_driver_queues_t4()

    queue_time = time.time() - start_time
    print("--- driver and passenger queues built in " + str(queue_time) + " seconds")

    weekdays, weekends = build_graph()

        # this tracks whether the current passenger still needs to be matched
    passenger_is_unmatched = False

    if trial_num == 1:
      filename = "results/t5rides_final.csv"
    else:
      filename = "results/t5_passengers.csv"
    
    print("--- now writing to " + filename)

    with open(filename, 'w') as file:
        writer = csv.writer(file)

        # writer.writerow(["passenger_start_datetime", "ride_match_datetime", "driver_to_passenger", "passenger_to_dest", "match_runtime_sec"])

        start_match_time = time.time()
        time_to_match = 0

        while len(passenger_queue) > 0:

            # make sure there are still drivers available
            if len(driver_queue) == 0:
                print("no more drivers are available, " + str(len(passenger_queue)) + " passengers still unmatched.")
                break

            # if we matched the last passenger we get the next one, otherwise we still use the last one
            if not passenger_is_unmatched:
                curr_passenger = heapq.heappop(passenger_queue)

                # get traffic data
                hour = curr_passenger.date_time.hour
                graph = weekdays[hour] if curr_passenger.date_time.weekday() < 5 else weekends[hour]
            
            closest_driver = None

            temp_driver_queue = PriorityQueue()
            
            while driver_queue:
                curr_driver = heapq.heappop(driver_queue)
                print(len(driver_queue))
                if curr_driver.date_time <= curr_passenger.date_time:
                    #put drivers in priority queue based on Manhatten distance
                    temp_driver_queue.put((manhattan(curr_driver.source_lat, curr_driver.source_lon,
                                                      curr_passenger.source_lat, curr_passenger.source_lon), curr_driver))
                else:
                    #driver is late to get the first passenger
                    heapq.heappush(driver_queue, curr_driver)
                    break
            #get top 5 drivers to find min distance
            top_five = []
            
            while not temp_driver_queue.empty():
                _, temp_driver = temp_driver_queue.get()
                if len(top_five) < 5:
                    top_five.append(temp_driver)
                else:
                    heapq.heappush(driver_queue, temp_driver)
            min_distance = float('inf')
            for driver in top_five:
                distance = shortest_path(graph, driver.node, curr_passenger.source_node)
                if distance < min_distance:
                    min_distance = distance
                    closest_driver = driver
            #put back other 2 drivers
            for driver in top_five:
                if driver != closest_driver and driver.node != closest_driver.node:
                    heapq.heappush(driver_queue, driver)
            #if there is closest_driver
            if closest_driver:
                # print(f"Passenger requesting at {curr_passenger.request_date_time} is matched with driver starting at {closest_driver.date_time} with distance {min_distance}")
                # run astar to get driver to passenger, then passenger to destination
                # maybe we could use the original dijkstra for this since it only happens once
                driver_to_passenger = min_distance
                passenger_to_dest = shortest_path(graph, curr_passenger.source_node, curr_passenger.dest_node)
                
                elapsed_time = driver_to_passenger + passenger_to_dest
                
                # wait_time = curr_passenger.date_time - curr_passenger.request_date_time

                # print(f"Wait time: {wait_time + timedelta(hours = driver_to_passenger)} hours")
                # print(f"Ride time: {passenger_to_dest} hours")

                # update driver attributes
                closest_driver.node = curr_passenger.dest_node
                closest_driver.date_time = curr_passenger.date_time + timedelta(hours = elapsed_time)
                closest_driver.profit = closest_driver.profit + passenger_to_dest - driver_to_passenger
                closest_driver.source_lat = curr_passenger.dest_lat
                closest_driver.source_lon = curr_passenger.dest_lon
                closest_driver.rides = closest_driver.rides + 1

                # calculate probability based on number of rides and time on shift
                time_on_shift = closest_driver.date_time - closest_driver.start_date_time

                if calculate(closest_driver.rides, time_on_shift, closest_driver.profit):
                  heapq.heappush(driver_queue, closest_driver)

                # we matched the passenger, so we should grab the next one from the queue
                passenger_is_unmatched = False

                time_to_match = time.time() - start_match_time
                start_match_time = time.time()

                # writer.writerow([curr_passenger.request_date_time, curr_passenger.date_time, driver_to_passenger, passenger_to_dest, time_to_match])

                if len(passenger_queue) % 50 == 0:
                    print("runtime: " + str(timedelta(seconds = time.time() - start_time)))
                    print("matching passenger " + str(5001 - len(passenger_queue)) + " of 5001")
            #else no closest driver, update passenger time
            else:
                # if there are not available drivers, then iterate the date and time of the passenger
                time_difference = curr_driver.date_time - curr_passenger.date_time
                curr_passenger.date_time = curr_passenger.date_time + time_difference
                # we will use this passenger again rather than grab a new one
                passenger_is_unmatched = True

    if not driver_queue and not passenger_queue:
      print("no more drivers are available, " + str(len(passenger_queue)) + " passengers still unmatched.")
    else:
       print("all matches complete.")

    total_runtime = time.time() - start_time
#   with open("results/T5_runtime.csv", "a") as file:
#       writer = csv.writer(file)
#       writer.writerow([total_runtime, queue_time, build_graph_time])

#   print(f"total runtime: {total_runtime}")
#   print(f"queue runtime: {queue_time}")

    return total_runtime, queue_time

if __name__ == "__main__":

    total_runtime, queue_time = T5("_test")
    print(f"total runtime: {total_runtime}")
    print(f"queue runtime: {queue_time}")
