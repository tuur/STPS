# (Un)ordered Tree Intersection
# Author: Artuur Leeuwenberg
# Date: June 2014

# I tried to follow the metacode in the following article, where the unordered tree intersection is described
# REF: Jose L. Balcazar, Albert Bifet and Antoni Lozano, "Intersection Algorithms and a Closure Operator on Unordered Trees"

# external sources
import itertools
import time
from itertools import *
import sys
import collections

sys.setrecursionlimit(10000)
# ============================ The important functions


def similarity(l1,l2, constraints, op='branches'):
	if op == 'branches':
		sim = tuple_similarity(l1, l2)
	elif op == 'trees':
		sim = tree_similarity(l1, l2)
	
	if constraints(sim):
		return sim
	else:
		return set([])

def subsumption(l1, l2, op='branches'):
	if op=='trees':
		return tree_subsumption(l1, l2)
	elif op=='branches':
		return tuple_subsumption(l1, l2)

def tree_similarity(s1, s2):
    res = set([])
    for t1 in s1:
        for t2 in s2:
            inters = tree_intersection(t1,t2)
            res = add_maximal_trees(inters, res)
    return res  

def tuple_similarity(s1,s2):
    res = set([])
    for t1 in s1:
        for t2 in s2:
            inters = tuple_intersection(t1,t2)
            res = add_maximal_tuple(inters,res)  
    return res 

def tree_subsumption(l1, l2):
		for t1 in l1:
			subtree_found = False
			for t2 in l2:
				if subtree(t1,t2):
					subtree_found = True
			if not subtree_found:
				return False
		return True


def tree_intersection(r,t):

    if not(r.label()==t.label()):
        return set([])    
    elif r.is_leaf():
        return set([r])
    elif t.is_leaf():
        return set([t])
    elif r == t:
        return set([r])
    else: # in case the roots are equal and both not leaves:
        s = set([r.root()])
        ch_r = r.children()
        ch_t = t.children()
        temp_dict={}
        matches = matchings(range(0,len(ch_r)),range(0,len(ch_t)))    
        for config in matches:
            mTrees = set([r.root()])
            for i,j in config:
                if (i,j) in temp_dict:
                    cTrees = temp_dict[(i,j)]
                else:    
                    cTrees = tree_intersection(ch_r[i],ch_t[j])
                    temp_dict[(i,j)]=cTrees
                if len(cTrees)!=0:
                    mTrees = cross(mTrees,cTrees)
                    s = max_subtrees(s,mTrees)
        return s            
                
def max_subtrees(s1,s2):
    marked = set([])
    for r in s1:    
        for t in s2:
            if  not(r in marked) and subtree(r,t) and t!=r:
                marked.add(r)
                
            elif not(t in marked) and subtree(t,r) and t!=r:
                marked.add(t)

    return set([tr for tr in s1.union(s2) if not(tr in marked)])

   
def subtree(r,t):
        if r.label()!=t.label():
            return False
        if r.is_leaf():
            return True
        if len(r.children())>len(t.children()):
            return False
        elif not(r.label()==t.label()) or r.num_nodes() > t.num_nodes():
            return False
        if t!=r:
            return True
        else:
            ch_r = r.children()
            ch_t = t.children()
            temp_dict={}

            matches = matchings(range(0,len(ch_r)),range(0,len(ch_t)))    
            for config in matches:
                sub = 0
                for i,j in config:
                    if subtree(r.children()[i],t.children()[j]):
                        sub+=1
                    else:
                        break
                if sub==len(config):
                    return True
            return False

        
def matchings(a,b): # builds the possible connections between the elements of set a and set b  
        if len(a)<len(b):
            small = a
            big = b
            switch = False
        else:
            small = b
            big = a
            switch = True
     
        result = []
        for combi in itertools.combinations(big, len(small)):
            for perm in itertools.permutations(combi):
                if switch:
                    result += [[(perm[i],small[i]) for i in range(0,len(small))]]
                else:
                    result += [[(small[i],perm[i]) for i in range(0,len(small))]]
        
        return result

def cross(l1,l2):
    crossed=set([])
    for t1 in l1:
        for t2 in l2:
        	crossed.add(t1.copy().insert(t2))
    return crossed  
 
      
def add_maximal_trees(trees, s):
	"""adds a set of maximal trees to another set of maximal trees, such that it results again in a set of maximal trees"""
	sc = s.copy()
	for t1 in trees:
		add = True
		for t2 in sc:
			sim = tree_intersection(t1, t2)
			if sim == set([t1]): # t1  is a subtree of t2
				add = False
				break
			if t2 in s and sim == set([t2]): # t2 is a subtree of t1
				s.remove(t2)
		if add:
			s.add(t1)
	return s

				
def add_maximal_tuple(tup, s):
	"""adds a tuple to a set of maximal tuples, such that is is again a set of maximal tuples"""
	for t in s.copy():
		sim = tuple_intersection(tup, t)
		if sim == tup: # tup is a subtuple of t
			return s
		if sim == t:
			s.remove(t) # t is a subtuple of tup
	s.add(tup)
	return s

	
          
def tuple_intersection(t1,t2): #sim((1,2,3,4),(1,2,3))=(1,2,3), and sim((1,2,3),(1,1,1))=(1,)
    if len(t1)==0 or len(t2)==0:
        return ()     
    if t1[0]==t2[0]:
        if len(t1)>1 and len(t2)>1:            
            return t1[:1] + tuple_intersection(t1[1:],t2[1:])
        else:
            return (t1[0],)
    else:
        return ()

def subtuple(r,t): # (1,2,3) is a subtuple of (1,2,3,4,5..), (1,2,4) is not
    if len(r)>len(t):
        return False
    else:
        return t[:len(r)]==r

def tuple_subsumption(s1,s2):
    for t1 in s1:
        go = False
        for t2 in s2:
            if subtuple(t1,t2):
                go=True
                break        
        if go==False:
            return False
    return True

