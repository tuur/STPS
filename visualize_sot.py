import argparse
from lib.TTree import TTree, read_sot, to_tuples, tuples_to_tree
from lib.utils import read_origins
import sys

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description='Visualizes a sets-of-trees file, or outputs it to latex.')
	parser.add_argument('sot', metavar='sot', type=str, 
		help='file path to the sets-of-trees file')
	parser.add_argument('-indices', metavar='-indices', type=str, default='all',
		help='give the indices of a selection of sots that are to be displayed/considered (default=all|n|n-m)')	
	parser.add_argument('-origins', metavar='origins', type=str, default=None,
		help='Will use the indices of the unlabeled trees instead, and visualize the corresponding hypotheses. Provide the file path to the origins file.')		
	parser.add_argument('-totree', metavar='-totree', type=int, default=0,
		help='If a projection was used, merge the individual branches to a new tree (for vizualization)')		
	parser.add_argument('-s', metavar='-s', type=int, default=0,
		help='Also print the leaves of the tree. For unordered trees they are printed in alphabetical order (default=0|1)')		
	parser.add_argument('-show', metavar='-show', type=int, default=1,
		help='Shows the trees of each set in an nltk display (default=1|0)')		
	parser.add_argument('-p', metavar='-p', type=int, default=1,
		help='Prints the trees in each set in ptb format (default=1|0)')		
	parser.add_argument('-latex', metavar='-latex', type=int, default=0,
		help='Prints the trees in latex (1) forest, or (2) qtree format (1|2|default=0). Forest package: https://www.ctan.org/pkg/forest?lang=en')		
			
		
	args = parser.parse_args()
	sots = read_sot(args.sot)
	
	# read the selected indices
	if '-' in args.indices:
		n,m = args.indices.split('-')
		selection = range(max(int(n),0),min(int(m)+1, len(sots)))
	elif args.indices== 'all' :
		selection = []
	else:
		n = args.indices
		selection = [int(n)]

	
	if args.origins:
		origins_from, has_hyps = read_origins(args.origins)
		selection = set([sot for i in has_hyps for sot in has_hyps[i] if i in selection or args.indices=='all'])
		
	indices = [i for i in sots.keys() if i in selection or args.indices == 'all']
	# Show the positive hypotheses
	for i in indices:
		print '---< SOT ' + str(i) + ' (contains ' + str(len(sots[i])) + ' trees) >---',
		if args.origins:
			print 'originates from ',','.join(str(tup) for tup in origins_from[i])
		else:
			print
		if args.totree:
			sots[i] = set([tuples_to_tree([t.to_tuple() for sot in sots[i] for t in sot.projection()])])				
		
		for sot in sots[i]:
		
			if args.p:
				print sot
				
			if args.s:
				print 'leaves:',sot.pprint_leaves()				

			if args.latex == 1:
				print sot.latex()
			elif args.latex == 2:
				print sot.nltklatex()
	 
			if args.show:
				sot.show()				
	
