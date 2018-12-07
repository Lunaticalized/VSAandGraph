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
		test if it is a clique
	"""

	def checkClique(self):
		for u in self.vertices:
			for v in self.vertices:
				if u != v:
					if not self.adj[u][v]:
						return False
		return True


	def checkClique(self, set):
		for u in set:
			for v in set:
				if u != v:
					if not self.adj[u][v]:
						return False
		return True

	"""
		compute the maximum clique

	"""

	def checkMaxClique(self, k):
		import itertools

		for subset in itertools.combinations(self.vertices, k):
			if self.checkClique(subset):
				return True
		return False


	def findMaxClique(self):
		for k in range(1, self.n+1):
			if not self.checkMaxClique(k):
				return k - 1
		return self.n


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

		This method also reports the number of missing programs

		flag:
			0 - default order
			1 - random order
			2 - deg descending order
			3 - deg descending with median first

	"""
	def find_maximal_cliques_greedy(self, v, flag=1):
		vertices = [i for i in range(self.n)]
		degs = [len(self.edges[vv]) for vv in self.vertices]
		
		if flag == 1:
			def compare(x, y):
				return degs[y] - degs[x]

			vertices.sort(cmp=compare)


		if flag == 2:
			import random
			random.shuffle(vertices)

		v = vertices[0]
		vertices.remove(v)
		cliques = [[v]]
		
		

		while vertices:
			import random
			v = vertices.pop(0)
			u = v
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
				
				prob = random.random()
				p = 0
				for i in cand:
					p +=  1.0 * len(cliques[i]) / s
					if prob <= p:
						cliques[i].append(u)
						break
		return cliques



	"""
		cnt missing programs for a given cluster

	"""

	def countMissingPrograms(self, cliques):
		missing = 0
		for v in self.vertices:
			cnt = 0
			for c in cliques:
				if self.checkClique(c + [v]):
					cnt += 1
			missing += (cnt - 1)
		return missing


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
		  
		reg = "y = " + str("{0:.2f}".format(round(math.exp(a),2))) + "/x^"+str("{0:.2f}".format(round(-b,2)))

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
	The graph class with multiple edges of color


"""

class GraphColor(Graph):
	def __init__(self):
		self.n = 0
		self.m = 0
		self.colors = []
		self.vertices = []
		self.all_edges = []
		# neighbors
		self.edges = [{}]
		
		# adjacency matrix
		self.adj = [[]]



	def add(self, u, v, c):
		self.adj[u][v] = True
		self.adj[v][u] = True
		self.all_edges.append([u, v])
		if c not in self.edges[v]:
			self.edges[v][c] = []
		if c not in self.edges[u]:
			self.edges[u][c] = []

		if u not in self.edges[v][c] and v not in self.edges[u][c]:
			self.edges[v][c].append(u)
			self.edges[u][c].append(v)
			self.m += 1
			if c not in self.colors:
				self.colors.append(c)

	def read(self, filename):
		file = open(filename, 'r')
		lines = file.readlines()
		self.n = int(lines[0])
		self.m = len(lines) - 1
		self.vertices = [i for i in range(self.n)]
		self.edges = [{} for i in range(self.n)]
		self.adj = [[False for i in range(self.n)] for j in range(self.n)]
		
		for i in range(self.m):
			line = lines[i+1][:-1]
			if line:
				br = line.split()
				u, v, c = int(br[0]), int(br[1]), int(br[2])
				self.add(u, v, c)
		file.close()

	def printGraph(self):
		print self.vertices
		for e in self.edges:
			print e


	def countProgramLoss(self):
		cnt = 0
		for v in self.vertices:
			cnt += len(self.edges[v]) - 1
		return cnt

	def countTotalProgram(self):
		cnt = 0
		for v in self.vertices:
			cnt += len(self.edges[v])
		return cnt

	def metric1(self):
		if self.countTotalProgram() == 0:
			return 0
		return 1.0 * self.countProgramLoss() /self.countTotalProgram()

	def metric2(self):
		avg = 0
		cnt = 0
		for v in self.vertices:
			a = len(self.edges[v]) - 1
			if a == -1:
				val = 0
			else:
				val = 1.0 * a / (a + 1)
			avg = (avg * cnt + val) / (cnt + 1)
			cnt += 1
		return avg

	def metric3(self):
		ret = 0
		
		for v in self.vertices:
			a = len(self.edges[v]) - 1
			if a == -1:
				val = 0
			else:
				val = 1.0 * a / (a + 1)
			ret = max(ret, val)
		return ret

def tryTheSeq():
	g = Graph()
	directory = "data/graph/"
	filename = "feed_sampled1_1_345"
	g.read(directory+filename + ".txt")
	#g.drawGraph()
	avg0 = 0
	for i in range(1000):
		c = g.find_maximal_cliques_greedy(0, 0)
		missing = g.countMissingPrograms(c)
		avg0 = 1.0 * (avg0 * i + missing) / (i + 1)

	avg2 = 0
	for i in range(1000):
		c = g.find_maximal_cliques_greedy(0, 1)
		missing = g.countMissingPrograms(c)
		avg2 = 1.0 * (avg2 * i + missing) / (i + 1)

	print avg0, avg2
	

if __name__ == "__main__":
	tryTheSeq()
	
	

	
	#g.plotDegDistribution()

	#g.approximatePowerLaw()
	