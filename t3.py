import time
import csv
import heapq
from datetime import timedelta
from random import random
from queue import Queue

from buildgraph import build_graph
from dijkstra import travel_times
from passenger_driver import passenger_driver_queues

def T3(trial_num):

    start_time = time.time()

    print("--- T3")

    driver_queue, passenger_queue = passenger_driver_queues()

    queue_time = time.time() - start_time
    print("--- driver and passenger queues built in " + str(queue_time) + " seconds")

    weekdays, weekends = build_graph()

    # this tracks whether the current passenger still needs to be matched
    passenger_is_unmatched = False

    if trial_num == 1:
      filename = "results/t3rides_final.csv"
    else:
      filename = "results/t3_test.csv"
    
    print("--- now writing to " + filename)

    with open(filename, 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["passenger_start_datetime", "ride_match_datetime", "driver_to_passenger", "passenger_to_dest", "match_runtime_sec"])
       
        start_match_time = time.time()
        time_to_match = 0

        while passenger_queue:

            # make sure there are still drivers available
            if not driver_queue:
                print("no more drivers are available, " + str(len(passenger_queue)) + " passengers still unmatched.")
                break

            # if we matched the last passenger we get hte next one, otherwise we still use the last one
            if not passenger_is_unmatched:
                start_match = time.time()
                passenger_wait_time = None
                curr_passenger = heapq.heappop(passenger_queue)

                # get traffic data
                hour = curr_passenger.date_time.hour
                graph = weekdays[hour] if curr_passenger.date_time.weekday() < 5 else weekends[hour]
            
            closest_driver = None
            min_distance = float('inf')

            temp_driver_queue = Queue()

            while driver_queue:
                curr_driver = heapq.heappop(driver_queue)

                if curr_driver.date_time <= curr_passenger.date_time:
                    
                    # break without calculating path if they are at the same node
                    if curr_driver.node == curr_passenger.source_node:
                        if min_distance < float('inf'):
                            temp_driver_queue.put(closest_driver)

                        closest_driver = curr_driver
                        min_distance = 0
                        break
                    
                    distance = travel_times(graph, curr_driver.node, curr_passenger.source_node)

                    if distance < min_distance:
                        if min_distance < float('inf'):
                            temp_driver_queue.put(closest_driver)

                        closest_driver = curr_driver
                        min_distance = distance
                    else:
                        temp_driver_queue.put(curr_driver)
                else:
                    passenger_wait_time = curr_driver.date_time - curr_passenger.date_time
                    heapq.heappush(driver_queue, curr_driver)
                    break
            
            while not temp_driver_queue.empty():
                temp_driver = temp_driver_queue.get()
                heapq.heappush(driver_queue, temp_driver)

            if closest_driver:
                end_match = time.time()
                match_time = end_match - start_match
                match_time = timedelta(seconds=match_time).total_seconds()
                # print(f"Passenger requesting at {curr_passenger.request_date_time} is matched with driver at {curr_passenger.date_time} with distance {min_distance}")

                # run dijkstra's to get driver to passenger, then passenger to destination
                driver_to_passenger = min_distance
                passenger_to_dest = travel_times(graph, curr_passenger.source_node, curr_passenger.dest_node)
                
                elapsed_time = driver_to_passenger + passenger_to_dest

                # print(f"Wait time: {wait_time + driver_to_passenger} hours")
                # print(f"Ride time: {passenger_to_dest} hours")
                
                # update driver attributes
                closest_driver.node = curr_passenger.dest_node
                closest_driver.date_time = curr_passenger.date_time + timedelta(hours = elapsed_time)
                closest_driver.profit = closest_driver.profit + passenger_to_dest - driver_to_passenger
                closest_driver.source_lat = curr_passenger.dest_lat
                closest_driver.source_lon = curr_passenger.dest_lon
                closest_driver.rides = closest_driver.rides + 1

                time_on_shift = closest_driver.date_time - closest_driver.start_date_time

                # reinsert with probability 95%
                if random() > 0.05 and time_on_shift < timedelta(hours = 8):
                  heapq.heappush(driver_queue, closest_driver)

                # we matched the passenger, so we should grab the next one from the queue
                passenger_is_unmatched = False

                time_to_match = time.time() - start_match_time
                start_match_time = time.time()

                writer.writerow([curr_passenger.request_date_time, curr_passenger.date_time, driver_to_passenger, passenger_to_dest, time_to_match])

                if len(passenger_queue) % 50 == 0:
                    print("runtime: " + str(timedelta(seconds = time.time() - start_time)))
                    print("matching passenger " + str(5001 - len(passenger_queue)) + " of 5001")

            else:
                # if there are not available drivers, then iterate the date and time of the passenger
                time_difference = curr_driver.date_time - curr_passenger.date_time
                curr_passenger.date_time = curr_passenger.date_time + time_difference
                # we will use this passenger again rather than grab a new one
                passenger_is_unmatched = True

    if not driver_queue and passenger_queue:
      print("no more drivers are available, " + str(len(passenger_queue)) + " passengers still unmatched.")
    else:
       print("all matches complete.")

    total_runtime = time.time() - start_time
#   with open("results/T3_runtime.csv", "a") as file:
#       writer = csv.writer(file)
#       writer.writerow([total_runtime, queue_time, build_graph_time])

    # print(f"total runtime: {total_runtime}")
    # print(f"queue build runtime: {queue_time}")
    # print(f"build_graph runtime: {build_graph_time}")

    return total_runtime, queue_time

if __name__ == "__main__":

    total_runtime, queue_time = T3("_test")

    print(f"total runtime: {total_runtime}")
    print(f"queue build runtime: {queue_time}")
