# Some functions for file reading


def read_labels(file):
	""" reads a class-label file"""	
	labels = {}
	i = 0
	with open(file) as f:
		for line in f:
			labels[i] = line.strip()
			i += 1
	return labels

def read_origins(file):
	""" reads an origin file as a dictionary of indices to sets of tuples """
	origins_from = {} # from hyp to the (unlabeled sot, labeled sot) pairs  from which it was constructed
	has_hyps = {} # from unlabeled sot to its origin sots
	with open(file) as f:
		for line in f:
			unlabeledS, labeledS, indexS = line.strip().split()
			unlabeled, labeled, index = int(unlabeledS), int(labeledS), int(indexS)
			
			if index in origins_from:
				origins_from[index].add((unlabeled, labeled))
			else:
				origins_from[index] = set([(unlabeled, labeled)])
			
			if unlabeled in has_hyps:
				has_hyps[unlabeled].add(index)
			else:
				has_hyps[unlabeled] = set([index])
	return origins_from, has_hyps
