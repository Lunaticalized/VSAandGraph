class Graph:
	def __init__(self):
		self.n = 0
		self.m = 0
		self.edges = [[]]
		self.adj = [[]]

	def read(self, filename):
		file = read(filename, 'r')
		line = file.readline()
		br = line.split()
		self.n, self.m = int(br[0]), int(br[1])
		edge = [[] for i in range(n)]
		self.adj = [[False for i in range(n)] for j in range(n)]
		for i in range(m):
			line = file.readline()
			br = line.split()
			u, v = int(br[0]), int(br[1])
			edge[u].append(v)
			edge[v].append(u)
			self.adj[u][v] = self.adj[v][u] = True
		self.edges = edge
		file.close()

	def print_graph(self):
		print self.n, self.m
		for i in range(self.n):
			print i, self.edges[i]

	def erdos(self, n, p):
		self.n = n
		import random
		edge = [[] for i in range(n)]
		self.adj = [[False for i in range(n)] for j in range(n)]
		cnt = 0

		for i in range(n - 1):
			for j in range(i + 1, n):
				if random.random() < p:
					edge[i].append(j)
					edge[j].append(i)
					self.adj[i][j] = self.adj[j][i] = True
					cnt += 1
		self.m = cnt
		self.edges = edge

	def powerLawTree(self, n, p):
		self.n = n
		import random
		degs = [0 for i in range(n)]
		points = [-1 for i in range(n)]
		points[0] = 0
		for i in range(1, n):
			j = int(random.random() * i)
			if random.random() <= p:
				points[i] = j
			else:
				points[i] = points[j]
		points[0] = -1
		edges = [[] for i in range(n)]
		adj = [[False for i in range(n)] for j in range(n)]
		cnt = 0
		for i in range(n):
			if points[i] >= 0:
				edges[i].append(points[i])
				edges[points[i]].append(i)
				adj[i][points[i]] = True
				adj[points[i]][i] = True
				cnt += 1

		self.edges = edges
		self.m = cnt
		self.adj = adj


	def isClique(self, v, c):
		for u in c:
			if not self.adj[u][v]:
				return False
		return True
	def find_maximal_cliques(self, v):
		vertices = [i for i in range(self.n)]
		vertices.remove(v)
		ret = []
		clique = [v]
		while len(vertices) > 0:
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
			


if __name__ == "__main__":
	g = Graph()
	#g.erdos(1000, 0.1)
	#g.print_graph()
	g.powerLawTree(100, 0.9)
	g.print_graph()
	print g.find_maximal_cliques(0)