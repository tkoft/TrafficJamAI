"""This module includes the JamAgent class, which represents an AI search agent to 
solve the traffic jam puzzle.  Assumes valid puzzle with solution.

It also includes a BfsNode class as a data structure for the AI's BFS search, and
a Move class to represent a single move on a puzzle.

(c) 2016 Gary Chen
"""
from JamPuzzle import *
from collections import deque
import copy
import heapq
import queue

class JamAgent:
	"""Represents AI search agent that will solve a traffic jam puzzle

	bfs(self, puzzle):  runs BFS search on a given JamPuzzle
	"""
	def __init__(self):
		# Count for performance evaluation; incremented every time goal tested (won() called)
		self.nodesVisited = 0

	def bfs(self, puzzle):
		"""Performs a BFS by creating BfsNode objects for the puzzle
		and all its subsequent states for every action at each state.
		
		Args:
			puzzle (JamPuzzle):  the initial puzzle state
		Return:  
			Moves[]: list of Move objects representing solution to puzzle
		"""

		# Queue to hold untraversed nodes
		bfsQueue = queue.PriorityQueue(0)

		# The current node/state
		current = BfsNode(puzzle, [])

		# Reset goal test counter
		self.nodesVisited = 0
		
		# Track seen puzzle states in a hashtable to prevent loops in BFS
		# Hash from str(JamPuzzle.getGrid()) --> ref to node (in the queue o) where it already exists
		seenPuzzleStates = {}
		seenPuzzleStates[str(current.puzzle.getGrid())] = current;

		# Goal test and count
		while not current.puzzle.won():
			self.nodesVisited += 1

			# Look at every possible move from current state
			for m in current.getPossibleMoves():

				# Duplicate node, perform a move on puzzle, add move to movesSoFar
				newState = copy.deepcopy(current)
				newState.puzzle.move(m.pos, m.moves)
				newState.movesSoFar += [m]
				
				# If new state is unseen or has fewer moves than when previously seen, add to queue and update seen states list
				if not str(newState.puzzle) in seenPuzzleStates: 
					bfsQueue.put(newState)
					seenPuzzleStates[str(newState.puzzle)] = newState
				elif len(newState.movesSoFar) < len(seenPuzzleStates[str(newState.puzzle)].movesSoFar):
					seenPuzzleStates[str(newState.puzzle)].movesSoFar = newState.movesSoFar

			# Get next best move from priority queue
			current = bfsQueue.get();

		return current.movesSoFar

class BfsNode:
	"""Represents a single state of the BFS

	Attributes:
		puzzle (JamPuzzle):  the puzzle state this node represents
		movesSoFar (Move[]):  array of moves taken to get to the current
				state.  Holds the solution at the end, since BFs itself
				doesn't track moves so far for each state.

	getPossibleMoves(self): retrieves list of all valid moves from this
			node's state
	"""

	def __init__(self, puzzle, movesSoFar):
		"""Constructor takes a puzzle state and list of moves taken
		so far to get there.
		"""
		self.puzzle = puzzle
		self.movesSoFar = movesSoFar

	def getPossibleMoves(self):
		"""Find the moveRange() of each vehicle in puzzle state and
		adds every move (except 0 moves) in the range for each vehicle
		to a result list of Move objects

		Return: 
			Move[]: the array of all valid moves for this node's state
		"""
		results = []
		current = self.puzzle
		for v in current.vehicles:
			for i in current.moveRange(v):
				# Don't move if move length is 0
				if not i == 0:
						results += [Move(v.pos, i)]
		return results

	def numBlocked(self):
		"""Heuristic function: count number of vehicles between door and solution vehicle.  
		Blocking vehicles must be horizontal, and assumes there is a solution vehicle.
		"""
		# Number of blocking vehicles so far
		count = 0
		# y-coordinate to check
		y = 0
		# Get vehicle at current coordinate (could be none)
		currentVeh = self.puzzle.getVehicleAt((self.puzzle.doorPos, y))
		# Check until vertical vehicle found; also allow None vehicle found to prevent exception
		while (currentVeh == None or currentVeh.orientation == Orientations.horizontal):
			if not currentVeh == None:
				count += 1
			y += 1
			currentVeh = self.puzzle.getVehicleAt((self.puzzle.doorPos, y))
		return count

	def heuristic(self):
		# Not actually the heuristic, but the entire A* evaluation function.
		# f(n) = g(n) + h(n); moves so far plus heuristic
		return len(self.movesSoFar)+self.numBlocked()

	def __lt__(self, b):
		# Needed for the pirority queue to order nodes by f(n)
		return (self.heuristic()) < (b.heuristic())


class Move:
	"""Class to represent a single move, just to make things cleaner
	
	Attributes:
		pos ((int, int)): tuple of two ints representing location on
				grid of the vehicle to move
		moves (int):  the number of steps to move it in the direction
				of its orientation (can be negative or zero)
	"""
	def __init__(self, pos, moves):
		self.pos = pos;
		self.moves = moves;

	def __str__(self):
		return "Move car at "+str(self.pos)+" by "+str(self.moves)