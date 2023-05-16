# -*- coding: utf-8 -*-
"""AI assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GMtc7Phlogz20c0SqWAwcLhEMCnDz62K
"""

# This is my goal state(final state)
goal_state = [[1,2,3],[4,5,6],[7,8,0]]

# Define a function here to move my empty bar in different directions
def move(state, direction):
  # copying the state, and not changing state everytime
  new_state = [row[:] for row in state]
  for i in range(len(new_state)):
    for j in range(len(new_state[i])):
      # checking if the box we are trying to move is 0 block
      if new_state[i][j] == 0:
        if direction == "up":
          #swapping i,j block with i-1,j block and return the state if there is block above
          if i > 0:
            temp=new_state[i][j]
            new_state[i][j]=new_state[i-1][j]
            new_state[i-1][j]=temp
            return new_state
        elif direction == "down":
          #swapping i,j block with i+1,j block and return the state if there is block below
          if i < len(new_state) - 1:
            temp=new_state[i][j]
            new_state[i][j]=new_state[i+1][j]
            new_state[i+1][j]=temp
            return new_state
        elif direction == "left":
          #swapping i,j block with i,j-1 block and return the state if there is block to the left
          if j > 0:
            temp=new_state[i][j]
            new_state[i][j]=new_state[i][j-1]
            new_state[i][j-1]=temp
            return new_state
        elif direction == "right":
          #swapping i,j block with i,j+1 block and return the state if there is block to the right
          if j < len(new_state[i]) - 1:
            temp=new_state[i][j]
            new_state[i][j]=new_state[i][j+1]
            new_state[i][j+1]=temp
            return new_state
  #return None if blocks to a particular direction doesn't exist
  return None

# Defining the cost function for A* with the Misplaced Tile heuristic
#returns no of misplaced blocks compared to goal state
def cost_misplaced(state):
  total_cost = 0
  for i in range(len(state)):
    for j in range(len(state[i])):
      if state[i][j] != goal_state[i][j]:
        total_cost += 1
  return total_cost

# Define the cost function for A* with Manhattan Distance heuristic
#returns the sum of manhattan distances of the blocks that are misplaced from goal state
def cost_misplaced_man(state):
  total_cost = 0
  for i in range(len(state)):
    for j in range(len(state[i])):
      if state[i][j] != goal_state[i][j]:
        for k in range(len(state)):
          for l in range(len(state[k])):
            if goal_state[k][l] == state[i][j]:
              total_cost += abs(i-k)+abs(j-l)
  return total_cost

#function which returns cost based on the costfunction provided
def calculate_cost(cost,state,costfunction,depth):
  if costfunction=='uniform':
    return cost+1
  if costfunction=='misplaced':
    return depth+cost_misplaced(state)
  if costfunction=='misplaced_with_manhattan':
    return depth+cost_misplaced_man(state)

# Define the uniform cost search algorithm
def general_search(initial_state,cost='uniform'):
  #stores - cost,current state, path followed by 0, states in btw inital & current state, depth
  queue = [(0, initial_state, [],[],0)]
  #set to store all the states that are already explored to avoid infinite recurssion
  explored = set()
  while queue:
    # Sort the queue by cost so far to replicate priority queue poping and return the state with least cost and add to explored
    queue.sort()
    cost_so_far, current_state, path_so_far,states,depth = queue.pop(0)
    explored.add(tuple(map(tuple, current_state)))
    # Check if the current state is the goal state and return it
    if current_state == goal_state:
      return cost_so_far, path_so_far,states,len(explored)

    # Add the current state to the explored set
    # explored.add(tuple(map(tuple, current_state)))

    # Generate all possible un-explored states from the current state
    for direction in ["up", "down", "left", "right"]:
      new_state = move(current_state, direction)
      if new_state is not None and tuple(map(tuple, new_state)) not in explored:

        # Calculate the cost of the new state based on costfunction and it to frontier along with its data
        new_cost = calculate_cost(cost_so_far,current_state,cost,depth)
        new_path = path_so_far + [direction]
        new_states = states + [new_state]
        queue.append((new_cost, new_state, new_path, new_states,depth+1))
  return None

# function to print the state as a 3x3 matrix form for interpretation of solution
def print_as_matrix(states):
  for state in states:
    for row in state:
      print(row)
    print('------------')

# Prompt the user to enter the initial state
initial_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
print("Enter the numbers for the initial state of the puzzle:")
for i in range(len(initial_state)):
  row_input = input("Enter the numbers for row {} separated by commas: ".format(i))
  row_numbers = []
  row_numbers = [int(n) for n in row_input.split(",")]
  initial_state[i] = row_numbers

#Asking the user for their choice on selecting the Search Algorithm
print("Enter 0 for Uniform Cost Search")
print("Enter 1 for A* with the Misplaced Tile heuristic")
print("Enter 2 for A* with the Manhattan Distance heuristic")
method=input()
cost1=""
if method=='0':
  cost1="uniform"
elif method=='1':
  cost1="misplaced"
elif method=='2':
  cost1="misplaced_with_manhattan"

# Testing the algorithm on the user-provided initial state
print("Initial state:")
for row in initial_state:
    print(row)

#call the general-search function for solution with the user provided data and preferred costfunction
cost, path,states,explored = general_search(initial_state,cost=cost1)

#print the solution and other related data
print("Cost to reach goal state:", cost)
print("Path to reach goal state:", path)
print('Number of nodes explored:',explored)
print(print_as_matrix(states))