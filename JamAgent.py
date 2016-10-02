"""This module includes the JamAgent class, which represents an AI search agent to 
solve the traffic jam puzzle.

It also includes a BfsNode class as a data structure for the AI's BFS search, and
a Move class to represent a single move on a puzzle.

(c) 2016 Gary Chen
"""
from JamPuzzle import *
from collections import deque
import copy

class JamAgent:
	"""Represents AI search agent that will solve a traffic jam puzzle

	bfs(self, puzzle):  runs BFS search on a given JamPuzzle
	"""
	def __init__(self):
		pass

	def bfs(self, puzzle):
		"""Performs a BFS by creating BfsNode objects for the puzzle
		and all its subsequent states for every action at each state.
		
		Args:
			puzzle (JamPuzzle):  the initial puzzle state
		Return:  
			Moves[]: list of Move objects representing solution to puzzle
		"""
		# Queue to hold untraversed nodes
		bfsQueue = deque([])

		# The current node/state
		current = BfsNode(puzzle, [])
		
		# Track seen puzzle states in a hashtable to prevent loops in BFS
		# Hash from str(JamPuzzle.getGrid()) --> True if seen before, None if not
		seenPuzzleStates = {}
		seenPuzzleStates[str(current.puzzle.getGrid())] = True;

		while not current.puzzle.won():

			for m in current.getPossibleMoves():

				# Duplicate puzzle state and perform a move
				newState = copy.deepcopy(current)
				newState.puzzle.move(m.pos, m.moves)

				# If new state is unseen, add to queue and seen states list
				if (seenPuzzleStates.get(str(newState.puzzle)) == None):
					bfsQueue.append(BfsNode(newState.puzzle, current.movesSoFar + [m]))
					seenPuzzleStates[str(newState.puzzle)] = True;

			current = bfsQueue.popleft()

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