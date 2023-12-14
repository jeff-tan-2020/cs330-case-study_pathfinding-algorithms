import csv
import time
import math
import heapq
from queue import Queue
from datetime import timedelta
from random import random

from buildgraph import build_graph
from passenger_driver import passenger_driver_queues
from dijkstra import travel_times

def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

def T2(trial_num):
    start_time = time.time()

    print("--- T2")

    driver_Q, passenger_Q = passenger_driver_queues()

    queue_time = time.time() - start_time
    print("--- driver and passenger queues built in " + str(queue_time) + " seconds")

    weekdays, weekends = build_graph()

    # this tracks whether the current passenger still needs to be matched
    passenger_is_unmatched = False

    # if trial_num == 1:
    #   filename = "results/t2rides_final.csv"
    # else:
    filename = "results/t2_passengers.csv"
    
    print("--- now writing to " + filename)

    # with open(filename, 'w') as file:
    #     writer = csv.writer(file)

        # writer.writerow(["passenger_start_datetime", "ride_match_datetime", "driver_to_passenger", "passenger_to_dest", "match_runtime_sec"])

        # driver profit
        #writer.writerow(["rides_completed", "driver_profit"])

        # passenger waittime
        # writer.writerow(["passenger_wait", "passenger_total"])

        #start_match_time = time.time()
        #time_to_match = 0

    while len(passenger_Q) > 0:

            # make sure there are still drivers available
            if len(driver_Q) == 0:
                print("no more drivers are available, " + str(len(passenger_Q)) + " passengers still unmatched.")
                break

            # if we matched the last passenger we get the next one, otherwise we still use the last one
            if not passenger_is_unmatched:
                start_match = time.time()
                passenger_wait_time = None
                curr_passenger = heapq.heappop(passenger_Q)
            
            closest_driver = None
            min_distance = float('inf')

            temp_driver_Q = Queue()

            while len(driver_Q) > 0:
                curr_driver = heapq.heappop(driver_Q)

                if curr_driver.date_time <= curr_passenger.date_time:

                    # break without calculating path if they are at the same node
                    if curr_driver.node == curr_passenger.source_node:
                        if min_distance < float('inf'):
                            temp_driver_Q.put(closest_driver)

                        closest_driver = curr_driver
                        min_distance = 0
                        break

                    distance = calculate_distance(curr_passenger.source_lat, curr_passenger.source_lon, curr_driver.source_lat, curr_driver.source_lon)
                    if distance < min_distance:
                        if closest_driver is not None:
                            temp_driver_Q.put(closest_driver)
                        closest_driver = curr_driver
                        min_distance = distance
                    else:
                        temp_driver_Q.put(curr_driver)
                else:
                    heapq.heappush(driver_Q, curr_driver)
                    break
            
            while not temp_driver_Q.empty():
                temp_driver = temp_driver_Q.get()
                heapq.heappush(driver_Q, temp_driver)

            if closest_driver:
                end_match = time.time()
                match_time = end_match - start_match
                match_time = timedelta(seconds=match_time).total_seconds()
                # print(f"Passenger requesting at {curr_passenger.request_date_time} is matched with driver at {curr_passenger.date_time} with distance {min_distance}")
            
                # get traffic data
                hour = curr_passenger.date_time.hour
                graph = weekdays[hour] if curr_passenger.date_time.weekday() < 5 else weekends[hour]

                # run dijkstra's to get driver to passenger, then passenger to destination
                driver_to_passenger = travel_times(graph, closest_driver.node, curr_passenger.source_node)
                passenger_to_dest = travel_times(graph, curr_passenger.source_node, curr_passenger.dest_node)
                
                elapsed_time = driver_to_passenger + passenger_to_dest

                # print(f"Wait time: {wait_time + driver_to_passenger} hours")
                # print(f"Ride time: {passenger_to_dest} hours")
                #write passenger.csv
                '''
                #Unused code
                if passenger_wait_time:
                    passenger_time = match_time + passenger_wait_time.total_seconds() + timedelta(hours=elapsed_time).total_seconds()
                    writer.writerow([match_time + passenger_wait_time.total_seconds(),passenger_time])
                else:
                    passenger_time = match_time + timedelta(hours=elapsed_time).total_seconds()
                    writer.writerow([match_time,passenger_time])
                '''
                
                # update driver attributes
                closest_driver.node = curr_passenger.dest_node
                closest_driver.date_time = curr_passenger.date_time + timedelta(hours = elapsed_time)
                closest_driver.profit = closest_driver.profit + passenger_to_dest - driver_to_passenger
                closest_driver.source_lat = curr_passenger.dest_lat
                closest_driver.source_lon = curr_passenger.dest_lon
                closest_driver.rides = closest_driver.rides + 1

                # put driver back in queue
                time_on_shift = closest_driver.date_time - closest_driver.start_date_time
                                
                if random() > 0.05 and time_on_shift < timedelta(hours = 8):
                    heapq.heappush(driver_Q, closest_driver)              

                # we matched the passenger, so we should grab the next one from the queue
                passenger_is_unmatched = False

                #time_to_match = time.time() - start_match_time
                #start_match_time = time.time()

                # writer.writerow([curr_passenger.request_date_time, curr_passenger.date_time, driver_to_passenger, passenger_to_dest, time_to_match])
            
                if len(passenger_Q) % 500 == 0:
                    print("runtime: " + str(timedelta(seconds = time.time() - start_time)))
                    print("matching passenger " + str(5001 - len(passenger_Q)) + " of 5001")

            else:
                # if there are not available drivers, then iterate the date and time of the passenger and put them back in the queue
                
                time_difference = curr_driver.date_time - curr_passenger.date_time
                curr_passenger.date_time = curr_passenger.date_time + time_difference

                # we will use this passenger again rather than grab a new one
                passenger_is_unmatched = True

    if not driver_Q and passenger_Q:
      print("no more drivers are available, " + str(len(passenger_Q)) + " passengers still unmatched.")
    else:
       print("all matches complete.")

    while driver_Q:
        driver = heapq.heappop(driver_Q)
        #writer.writerow([driver.rides, driver.profit])


    total_runtime = time.time() - start_time
    # with open("results/T2_runtime.csv", "a") as file:
    #   writer = csv.writer(file)
    #   writer.writerow([total_runtime, queue_time, build_graph_time])

    # print(f"total runtime: {total_runtime}")
    # print(f"queue build runtime: {queue_time}")
    # print(f"build_graph runtime: {build_graph_time}")

    # print('Wait average:' + str(sum(wait_times)/len(wait_times)) + ' hours')
    # print('Ride average:' + str(sum(ride_times)/len(ride_times)) + ' hours')
    # print('Total average:' + str(sum(total_times)/len(total_times)) + ' hours')
    return total_runtime, queue_time

if __name__ == "__main__":
    
    total_runtime, queue_time = T2("_test")
    print(f"total runtime: {total_runtime}")
    print(f"queue build time: {queue_time}")
