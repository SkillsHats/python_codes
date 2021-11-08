from typing import List


# A class to store a Trie node
class TrieNode:
	def __init__(self):
		# each node stores a dictionary to its child nodes
		self.child = {}

		# keep track of the total number of times the current node is visited
		# while inserting data in Trie
		self.freq = 0


# Function to insert a given string into a Trie
def insert(root: TrieNode, word: str) -> None:

	# start from the root node
	curr = root
	for c in word:
		# create a new node if the path doesn't exist
		curr.child.setdefault(c, TrieNode())

		# increment frequency
		curr.child[c].freq += 1

		# go to the next node
		curr = curr.child[c]


# Function to recursively traverse the Trie in a preorder fashion and
# print the shortest unique prefix for each word in the Trie
def printShortestPrefix(root: TrieNode, word_so_far: str):
	if root is None:
		return

	# print `word_so_far` if the current Trie node is visited only once
	if root.freq == 1:
		print(word_so_far)
		return

	# recur for all child nodes
	for k, v in root.child.items():
		printShortestPrefix(v, word_so_far + k)


# Find the shortest unique prefix for every word in a given array
def findShortestPrefix(words: List[str]) -> None:

	# construct a Trie from the given items
	root = TrieNode()
	for s in words:
		insert(root, s)

	# Recursively traverse the Trie in a preorder fashion to list all prefixes
	printShortestPrefix(root, '')


if __name__ == '__main__':

	words = ['DOG', 'APRIL', 'CAT', 'APPLE', 'FISH']
	findShortestPrefix(words)
