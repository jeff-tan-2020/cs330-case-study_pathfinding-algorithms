#T1 baseline queue
#First come first serve
import time
import csv
import heapq
from random import random
from datetime import timedelta
from passenger_driver import passenger_driver_queues
from buildgraph import build_graph
from dijkstra import travel_times

#after driver pickup have to use node and road information from adjacency, edges, and node_data to get time
def T1(trial_num):
    start_time = time.time()

    print("--- T1")

    driver_queue, passenger_queue = passenger_driver_queues()

    queue_time = time.time() - start_time
    print("--- driver and passenger queues built in " + str(queue_time) + " seconds")
    #update graph based on driver time
    weekdays, weekends = build_graph() ## -- assume build_graph returns list of all graphs for every hour
    #all_graphs[(0,1)][hour] where 0 = weekday and 1 = weekend

   #  if trial_num == 1:
   #    filename = "results/t1rides_final.csv"
   #  else:
    filename = "results/t1_passengers.csv"
    
    print("--- now writing to " + filename)

    with open(filename, 'w') as file:
      writer = csv.writer(file)

      # writer.writerow(["passenger_start_datetime", "ride_match_datetime", "driver_to_passenger", "passenger_to_dest", "match_runtime_sec"])

      # driver profit
      # writer.writerow(["match_wait_time", "passenger_time"])

      #start_match_time = time.time()
      #time_to_match = 0

      while passenger_queue and driver_queue:
         passenger_wait_time = None
         start_match = time.time()
         # Get the current passenger and driver
         curr_passenger = heapq.heappop(passenger_queue)
         curr_driver = heapq.heappop(driver_queue)
         end_match = time.time()
         match_time = end_match - start_match
         match_time = timedelta(seconds=match_time).total_seconds()
         if len(passenger_queue) % 500 == 0:
            print("runtime: " + str(timedelta(seconds = time.time() - start_time)))
            print("matching passenger " + str(5001 - len(passenger_queue)) + " of 5001")
         
         #if passenger request before driver is ready
         if curr_passenger.date_time < curr_driver.date_time:
               passenger_wait_time = curr_driver.date_time - curr_passenger.date_time
               curr_passenger.date_time = curr_driver.date_time
               

         #Pickup time 
         # Get the weekday as an integer (Monday is 0, Sunday is 6)
         hour = curr_passenger.date_time.hour
         graph = weekdays[hour] if curr_passenger.date_time.weekday() < 5 else weekends[hour]

         # run dijkstra's to get driver to passenger, then passenger to destination
         driver_to_passenger = travel_times(graph, curr_driver.node, curr_passenger.source_node)
         passenger_to_dest = travel_times(graph, curr_passenger.source_node, curr_passenger.dest_node)
         
         elapsed_time = driver_to_passenger + passenger_to_dest

         if curr_passenger.date_time < curr_driver.date_time:
            passenger_wait = curr_driver.date_time - curr_passenger.date_time
            passenger_time = match_time + passenger_wait + elapsed_time
            # writer.writerow([match_time + passenger_wait,passenger_time])
         if passenger_wait_time:
            passenger_time = match_time + passenger_wait_time.total_seconds() + timedelta(hours=elapsed_time).total_seconds()
            # writer.writerow([match_time + passenger_wait_time.total_seconds(),passenger_time])
         else:
            passenger_time = match_time + elapsed_time 
            # writer.writerow([match_time,passenger_time])
         # print(f"Passenger requesting at {curr_passenger.request_date_time} is matched with driver at {curr_passenger.date_time} with distance {driver_to_passenger}")
         
         # update driver attributes
         curr_driver.node = curr_passenger.dest_node
         curr_driver.date_time = curr_passenger.date_time + timedelta(hours = elapsed_time)
         curr_driver.profit = curr_driver.profit + passenger_to_dest - driver_to_passenger
         curr_driver.source_lat = curr_passenger.dest_lat
         curr_driver.source_lon = curr_passenger.dest_lon
         curr_driver.rides = curr_driver.rides + 1

         time_on_shift = curr_driver.date_time - curr_driver.start_date_time

         # drivers leave with probability 5% or after 8 hours
         if random() > 0.05 and time_on_shift < timedelta(hours = 8):
            heapq.heappush(driver_queue, curr_driver)
         else:
            # driver profit csv
            continue
            #writer.writerow([curr_driver.rides, curr_driver.profit])

         #time_to_match = time.time() - start_match_time
         #start_match_time = time.time()

         # writer.writerow([curr_passenger.request_date_time, curr_passenger.date_time, driver_to_passenger, passenger_to_dest, time_to_match])

    total_runtime = time.time() - start_time
   #  with open("results/T1_runtime.csv", "a") as file:
   #    writer = csv.writer(file)
   #    writer.writerow([total_runtime, queue_time, build_graph_time])

   #  print(f"total runtime: {total_runtime}")
   #  print(f"queue build time: {queue_time}")


    if not driver_queue and passenger_queue:
      print("no more drivers are available, " + str(len(passenger_queue)) + " passengers still unmatched.")
    else:
       print("all matches complete.")

    while driver_queue:
        driver = heapq.heappop(driver_queue)
        #writer.writerow([driver.rides, driver.profit])
        break

    return total_runtime, queue_time

if __name__ == "__main__":
  
  total_runtime, queue_time = T1("_test")
  print(f"total runtime: {total_runtime}")
  print(f"queue build time: {queue_time}")