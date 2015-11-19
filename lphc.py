__author__= 'Artuur Leeuwenberg'

import argparse
from lib.TTree import TTree, read_sot, to_tuples, tuple_to_tree
from lib.utils import read_labels
from lib.tree_intersections import similarity, subsumption

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description='Makes a binary classification (positive or negative) of sets of trees based on the lazy positive hypothesis classification with the syntactic tree pattern structure.')
	parser.add_argument('unlabeled_trees', metavar='unlabeled_trees', type=str, help='File path to the unlabeled sets of trees.')	
	parser.add_argument('labeled_trees', metavar='labeled_trees', type=str, help='File path to the sets of labeled trees.')
	parser.add_argument('labels', metavar='labels', type=str, help='File path to the class labels.')
	parser.add_argument('positive', metavar='positive', type=str, help='Indicate the positive labels (string separated by ;).')
	parser.add_argument('negative', metavar='negative', type=str, help='Indicate the negative labels (string separated by ;).')
	parser.add_argument('-projection', metavar='projection', default=1, type=int, help='Use the maximal branch projection (default=1|0).')   
	parser.add_argument('-output', metavar='output', default='./out.labs', type=str, help='File where the output labels should be written to (default=./out.labs).')
	parser.add_argument('-min_pos_hypotheses', metavar='min_pos_hypotheses', default=1, type=int, help='Number of positive hypotheses needed for a positive classification (default=1).')	
	parser.add_argument('-min_counterexamples', metavar='min_counterexamples', default=1, type=int, help='Number of negative counter examples that are to be found before a hypothesis is rejected (default=1).')
	parser.add_argument('-output_hypotheses', metavar='output_hypotheses', default=None, type=str, help='Output the positive hypotheses that are found and used for positive classifications. Provide the file path (default=None).')
	parser.add_argument('-output_origins', metavar='output_origins', default=None, type=str, help='outputs pairs of unlabeled and labeled object indices for which a positive hypothesis is found, and maps them to their corresponding index of the output_hypotheses file (in the format (unlabled,labeled):output_hypothesis_index). Provide the output file path (default=None).')
	args = parser.parse_args()
	
	unlabeled_trees = read_sot(args.unlabeled_trees)
	labeled_trees = read_sot(args.labeled_trees)
	labels = read_labels(args.labels)
	positive_labels = set(args.positive.split(';'))
	negative_labels = set(args.negative.split(';'))
	constraints = lambda x: True
	
	
	# Object descriptions are sets of trees, or sets of maximal branches the projection is used.
	if args.projection:
		describe = lambda treeSet: set([branch for tree in treeSet for branch in to_tuples(tree.projection())])
		op = 'branches'
	else:
		describe = lambda treeSet: treeSet
		op = 'trees'
	object_descriptions = {i:describe(treeSet) for i,treeSet in labeled_trees.items()}

	
	# Taking the set of positive and negative examples (indices)
	positive_examples = set(index for index in labels if labels[index] in positive_labels)
	negative_examples = set(index for index in labels if labels[index] in negative_labels)

	print 'POSITIVE:',len(positive_examples), '(' + ', '.join(positive_labels) + ')'
	print 'NEGATIVE:',len(negative_examples), '(' + ', '.join(negative_labels) + ')'


	if args.output_hypotheses:
		output_hypotheses = open(args.output_hypotheses, 'w')
		out_hyp_index = 0
	if args.output_origins:
		output_origins = open(args.output_origins, 'w')	

	# ------ Start Lazy Positive Hypothesis Classification ----- #
	with open(args.output, 'w') as out:
		for i,unlabeled_sot in unlabeled_trees.items():
			print 'SENTENCE',str(i) + ':', ' |&| '.join(unlabeled_tree.pprint_leaves() for unlabeled_tree in unlabeled_sot),			
			unlabeled_object_description = describe(unlabeled_sot)
			
			# Starts finding positive hypotheses
			positive_hypotheses = []
			for positive_index in positive_examples:
				similarity_pos = similarity(unlabeled_object_description, object_descriptions[positive_index], constraints, op=op)
				counterexamples = []
				for negative_index in negative_examples:
					similarity_neg = similarity(unlabeled_object_description, object_descriptions[negative_index], constraints, op=op)
				
					# When a counterexample is found
					if subsumption(similarity_pos, similarity_neg, op=op):
						counterexamples.append(negative_index)
					if len(counterexamples) >= args.min_counterexamples:
						break

				# When a positive hypothesis is found		
				if len(counterexamples) < args.min_counterexamples:
					positive_hypotheses.append(positive_index)
					
					# Output the origin of the found positive hypothesis (labeled tree and unlabeled sot indices)
					if args.output_origins:
						output_origins.write(str(i) + ' ' + str(positive_index) + '\t' + str(out_hyp_index) + '\n')
					
					# Output the actual positive hypothesis pattern 
					if args.output_hypotheses:
						if args.projection:
							output_hypotheses.write('\n\n'.join(str(tuple_to_tree(t)) for t in similarity_pos))
						else:
							output_hypotheses.write('\n\n'.join(str(t) for t in similarity_pos))
						output_hypotheses.write('\n\n\n')
						out_hyp_index += 1

				# Stop searching when enough positive hypotheses are found		
				if len(positive_hypotheses) >= args.min_pos_hypotheses:
					break
				
			# Classify
			if len(positive_hypotheses) >= args.min_pos_hypotheses:
				out.write('positive\n')
				print '<< positive'
			else:
				out.write('negative\n')
				print '<< negative'
				
	if args.output_hypotheses:
		output_hypotheses.close()
	if args.output_origins:
		output_origins.close()		
			
