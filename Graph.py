import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

class Graph:

	"""
		parameters of the graph:
			n - number of vertices
			m - number of edges
			edges - the adjacency list
			adj - the adjacency matrix

	"""
	def __init__(self):
		self.n = 0
		self.m = 0
		self.vertices = []
		self.all_edges = []
		self.edges = [[]]
		self.adj = [[]]

	"""
		Construct a graph from a file
			First line: n
			Next m lines:
						v1, v2, an undirected edge connecting
								v1 and v2
	"""

	def read(self, filename):
		file = open(filename, 'r')
		lines = file.readlines()
		self.n = int(lines[0])
		self.m = len(lines) - 1
		self.vertices = [i for i in range(self.n)]
		self.edges = [[] for i in range(self.n)]
		self.adj = [[False for i in range(self.n)] for j in range(self.n)]
		for i in range(self.m):
			line = lines[i+1][:-1]
			if line:
				br = line.split()
				u, v = int(br[0]), int(br[1])
				self.add(u, v)
		file.close()

	"""
		Utility function to print out the stats:
			number of vertices, edges
				and the adjacency list
	"""

	def add(self, u, v):
		self.adj[u][v] = True
		self.adj[v][u] = True
		self.all_edges.append([u, v])
		if u not in self.edges[v] and v not in self.edges[u]:
			self.edges[v].append(u)
			self.edges[u].append(v)
			self.m += 1


	def print_graph(self):
		print self.n, self.m
		for i in range(self.n):
			print i, self.edges[i]

	"""
		Assuming that C is a clique.

		Check if for some v notin C,
			v can be added to C to form a clique
	"""

	def isClique(self, v, c):
		for u in c:
			if not self.adj[u][v]:
				return False
		return True


	"""
		Procedure to greedily compute all sets of disjoint maximal
		cliques starting from v

	"""
	def find_maximal_cliques_growing(self, v):
		vertices = [i for i in range(self.n)]
		vertices.remove(v)
		ret = []
		clique = [v]
		while vertices:
			done = False
			for u in self.edges[v]:
				if self.isClique(u, clique) and u in vertices:
					clique.append(u)
					vertices.remove(u)
					done = True
					break
			if not done:
				ret.append(clique)
				v = vertices.pop(0)
				clique = [v]
		if len(clique) > 0:
			ret.append(clique)
		return ret
	

	"""
		Compute all maximal cliques using a greedy strategy
			for all incoming vertex, compute all candidate cliques
			it can be added to. Then choose uniformly from all
			such cliques.

		This method also reports the number of 

	"""
	def find_maximal_cliques_greedy(self, v):
		vertices = [i for i in range(self.n)]
		vertices.remove(v)
		cliques = [[v]]
		missing = 0
		while vertices:
			u = vertices.pop(0)
			cand = []
			for i in range(len(cliques)):
				if self.isClique(u, cliques[i]):
					cand.append(i)

			if not cand:
				cliques.append([u])
			elif len(cand) == 1:
				cliques[cand[0]].append(u)
			else:
				sizes = [len(cliques[i]) for i in cand]
				s = sum(sizes)
				import random
				prob = random.random()
				p = 0
				for i in cand:
					p +=  1.0*len(cliques[i]) / s
					if prob <= p:
						cliques[i].append(u)
						break
				missing += len(cand) - 1
		print str(missing) + " edges missing (unused)/"+str(len(self.all_edges)) 
		return cliques



	"""
		Plot the historgram for degree of vertices

	"""

	def plotDegDistribution(self):
		deg = [len(self.edges[v]) for v in range(self.n)]

		bins = np.arange(0, max(deg) + 1.5) - 0.5
		plt.hist(deg, normed=False, bins=bins)
		plt.xlabel("Vertex degree")
		plt.ylabel("Frequency")
		plt.show()


	"""
		Plot the histogram of the sizes of all maximal cliques

	"""
	def plotCliqueDistribution(self):
		c = self.find_maximal_cliques_greedy(0)
		length = [len(cc) for cc in c]
		bins = np.arange(0, max(length) + 1.5) - 0.5
		plt.hist(length, normed=False, bins=bins)
		plt.xlabel("Maximal clique size")
		plt.ylabel("Frequency")
		plt.show()

	"""
		Plot the graph.
			Dependency: matplotlib, networkx
	"""
	def drawGraph(self):
		gg = nx.Graph()
		gg.add_nodes_from(self.vertices)
		gg.add_edges_from(self.all_edges)
		nx.draw(gg, with_labels=False, node_size=10, alpha=1)	
		plt.show()



	def approximatePowerLaw(self):
		deg = [len(self.edges[v]) for v in range(self.n)]

		m = min(deg)
		M = max(deg)
		cnt = {}
		for d in deg:
			if d+1 not in cnt:
				cnt[d+1] = 1
			else:
				cnt[d+1] += 1
		logx = []
		logy = []
		x = []
		y = []
		for d in range(m, M+1):
			if d+1 in cnt:
				logx.append(math.log(d+1))
				logy.append(math.log(cnt[d+1]))
				x.append(d)
				y.append(cnt[d+1])

		logx_avg = 1.0*sum(logx)/len(logx)
		logy_avg = 1.0*sum(logy)/len(logy)

		s1 = 0
		s2 = 0
		for i in range(len(x)):
			s1 += (logx[i] - logx_avg) * (logy[i] - logy_avg)
			s2 += (logx[i] - logx_avg) * (logx[i] - logx_avg)

		b = 1.0*s1 / s2
		a = logy_avg - b * logx_avg
		  
		reg = "y = " + str(math.exp(a)) + "/x^"+str(-b)

		def f(d):
			xx = d + 1
			return math.exp(a) * xx**(b)

		plt.scatter(x,y)
		X_plot = np.linspace(m, M,100)
		plt.plot(X_plot, f(X_plot))
		plt.xlabel("Vertex degree\nPower law: "+reg)
		plt.ylabel("Frequency")
		plt.show()


"""
	Implementation of the Erdos random graph model
"""
class Erdos(Graph):
	def __init__(self, n, p):
		self.n = n
		self.m = 0
		self.vertices = [i for i in range(self.n)]
		self.edges = [[] for i in range(n)]
		self.adj = [[False for i in range(n)] for j in range(n)]
		
		for i in range(n - 1):
			for j in range(i + 1, n):
				if random.random() < p:
					self.add(i, j)


"""
	Implementation of the Power Law graph model

"""

class PowerLaw(Graph):

	def __init__(self, n, prob):
		self.n = n
		self.edges = [[] for i in range(n)]
		self.adj = [[False for i in range(self.n)] for j in range(self.n)]
		
		self.add(0, 1)
		self.add(1, 2)
		self.add(2, 3)
		self.add(3, 1)

		# import random

		# for v in range(4, n):
		# 	p = random.random()
		# 	if p <= prob:
				
		# 	else:
				



if __name__ == "__main__":
	#g = Erdos(10, 0.1)
	# g = PowerLawTree(10, 0.7)
	g = Graph()
	directory = "data/graph/"
	filename = "graph_total_778"
	g.read(directory+filename + ".txt")
	#g.drawGraph()
	g.plotCliqueDistribution()
	#g.plotDegDistribution()

	#g.approximatePowerLaw()
	