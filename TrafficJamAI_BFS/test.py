"""Test script for the Traffic Jam Puzzle AI for Project 1 of CSCI373 AI.
(c) 2016 Gary Chen
"""
from JamPuzzle import *
from JamAgent import *

# Initial State A
vehiclesA = [
			Vehicle((3, 0), Orientations.vertical, VehicleTypes.car),
			Vehicle((4, 0), Orientations.horizontal, VehicleTypes.car),
			Vehicle((4, 1), Orientations.horizontal, VehicleTypes.car),
			Vehicle((0, 2), Orientations.vertical, VehicleTypes.car),
			Vehicle((1, 2), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((4, 2), Orientations.horizontal, VehicleTypes.car),
			Vehicle((2, 4), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((5, 3), Orientations.vertical, VehicleTypes.car),
			]	
trafficJamA = JamPuzzle(6, 6, 5, vehiclesA)

# Initial State B
vehiclesB = [
			Vehicle((0, 0), Orientations.vertical, VehicleTypes.truck),
			Vehicle((1, 0), Orientations.vertical, VehicleTypes.truck),
			Vehicle((2, 0), Orientations.vertical, VehicleTypes.car),
			Vehicle((3, 0), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((3, 1), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((2, 2), Orientations.horizontal, VehicleTypes.car),
			Vehicle((4, 2), Orientations.horizontal, VehicleTypes.car),
			Vehicle((0, 3), Orientations.horizontal, VehicleTypes.car),
			Vehicle((4, 3), Orientations.vertical, VehicleTypes.car),
			Vehicle((2, 5), Orientations.horizontal, VehicleTypes.car),
			]	
trafficJamB = JamPuzzle(6, 6, 4, vehiclesB)

# Initial State C
vehiclesC = [
			Vehicle((0, 3), Orientations.vertical, VehicleTypes.truck),
			Vehicle((1, 2), Orientations.vertical, VehicleTypes.truck),
			Vehicle((2, 0), Orientations.vertical, VehicleTypes.truck),
			Vehicle((2, 3), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((3, 0), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((3, 1), Orientations.vertical, VehicleTypes.car),
			Vehicle((3, 4), Orientations.horizontal, VehicleTypes.truck),
			Vehicle((4, 1), Orientations.horizontal, VehicleTypes.car),
			Vehicle((5, 2), Orientations.vertical, VehicleTypes.car),
			]	
trafficJamC = JamPuzzle(6, 6, 5, vehiclesC)


def printSolution(puzzle, solution):
	"""Method that takes an initial puzzle and array of solution Move
	objects and applies the solution to the puzzle while printing out
	the state and next move details for each move.
	"""
	for m in solution:
		print(puzzle)
		print(m)
		puzzle.move(m.pos, m.moves)
	print(puzzle)
	print("Puzzle completed in " + str(len(solution)) + " moves.")


# Create AI agent and run on specified puzzles
agent = JamAgent()

solution = agent.bfs(trafficJamA)
printSolution(trafficJamA, solution)
print("Number of nodes visited in search:  " + str(agent.nodesVisited))

print("****************************************")

solution = agent.bfs(trafficJamB)
printSolution(trafficJamB, solution)
print("Number of nodes visited in search:  " + str(agent.nodesVisited))

print("****************************************")

solution = agent.bfs(trafficJamC)
printSolution(trafficJamC, solution)
print("Number of nodes visited in search:  " + str(agent.nodesVisited))