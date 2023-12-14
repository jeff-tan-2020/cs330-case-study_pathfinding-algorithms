import heapq
def heuristic(start, end, speed):
  # try manhattan distance
  #Euclidean distance: return (((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5) / speed
  return (abs(end[0] - start[0]) + abs(end[1] - start[1])) / speed

def shortest_path(graph, start, end):
  pqueue = [(0, start)]

  parents = {}
  cost_so_far = {}
  parents[start] = None
  cost_so_far[start] = 0

  while pqueue:
    _, curr_node = heapq.heappop(pqueue)

    if curr_node == end:
      break

    for neighbor, travel_time, speed in graph[curr_node][1]:
      new_cost = cost_so_far[curr_node] + travel_time

      # 
      if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
        cost_so_far[neighbor] = new_cost
        priority = new_cost + heuristic(graph[neighbor][0], graph[end][0], speed)
        heapq.heappush(pqueue, (priority, neighbor))
        parents[neighbor] = curr_node

  return cost_so_far[end]