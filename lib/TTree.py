import re
from nltk.tree import Tree as nltktree
from pyparsing import nestedExpr
import copy
from nltk.draw.tree import draw_trees as nltkdrawtrees
from tree_intersections import subtree

# A labeled unordered rooted tree class, using a breadth first canonical form.

class TTree:

   def __init__( self,string = "", id = -1):
      self._children = []
      self._label = ""
      self.string = string
      self._proj = False
      if id == -1:
      	id = str(self)
      self.id = id
      
      if type(string)==str and ("(" in string):
        string = string.replace('\n','')
        string = nestedExpr().parseString(string).asList()[0]
       
      if type(string)==str:
        self._label=string

      elif type(string)==list:
        self._label=string[0]
        children_string = string[1:]

        # order the children according to their labels, to achieve the cannonical form
        children_string.sort()
             
        for e in children_string:
                self._children+= [TTree(e)]
            
      else:
        print "TTREE ERROR: Syntax error in:",string," of type ",type(string)
        exit()

   def __str__( self ):
      if self.is_leaf():
        return str(self._label)
      else:
        res = "("+str(self._label)
        for child in self._children:
            res+= " "+str(child)
        return res + ")"

   def set_label(self,newlabel):
    self._label = newlabel
    return self
   
   def __hash__(self):
        return hash(str(self))

   def __eq__(self, other):
        if self._label==other.label() and len(self._children)==len(other.children()):
            for i in range(0,len(self._children)):
                if self._children[i]!=other.children()[i]:
                    return False
            return True    
        else:
            return False
            
   def __ne__(self,other):
        return not(self==other)

   def root(self):
       copied = self.copy()
       copied._children = []
       return copied
      
   def is_leaf(self):
        return self._children==[]
        
   def children(self):
        return self._children 

   def label(self):
        return self._label

   def pprint_leaves(self):
       return ' '.join(nltktree.fromstring(self.string).flatten())
     
   def leaves(self):
        if self.is_leaf():
            return [self]
        leaves = []
        for child in self._children:
            leaves += child.leaves()                    
        return leaves

   def copy(self):
        return copy.copy(self)
        
   # Insert a TTree at the end of the children of the current tree (or use position to change the input location)
   def insert(self,tree,position=False):
       if isinstance(tree,TTree):
           for i in range(0,len(self._children)):
               if TTree.label(tree) < TTree.label(self._children[i]): # insert the tree accordingly to the canonical form
                   self._children = self._children[:i]+[tree]+self._children[i:]
                   return self 
           self._children += [tree]
           return self     
       else:
           print "TTREE ERROR: incorrect type '"+str(tree)+"' is not an TTree instance but:"+str(type(tree))
           return None
       
   def latex(self):
       foreststr0 = re.sub(r' (?P<label>[^\(\) ]+) ', ' [\g<label>] ', str(self)).replace(r'-w',r'').replace(r'-pos',r'')
       foreststr1 = re.sub(r' (?P<label>[^\(\) ]+)\)', ' [\g<label>]]', foreststr0)
       foreststr2 = re.sub(r' (?P<label>[^\(\)\[\] ]+) ', ' [\g<label>] ', foreststr1)       
       foreststr3 = re.sub(r'\((?P<label>[^\(\) ]+) ', '[\g<label> ', foreststr2).replace(')',']').replace('_','-').replace('%',r'PROC').replace('drug-tag-r','drug-tag-r,ptr')
       return r"\begin{figure}[h!]\resizebox{0.9\textwidth}{!}{\begin{forest}"+foreststr3+"\end{forest}}\end{figure}"
   
   def nltklatex(self):
          return r"\begin{figure}[h!]\resizebox{0.9\textwidth}{!}{"+nltktree(str(self)).pprint_latex_qtree().replace('_','\_')+r"}\end{figure}"

   def show(self):
       nltktree.fromstring('( ' + str(self) + ')').draw()
           
   # All the tree parsing functions of nltk.tree can be integrated easily, one example is given:    
   def bracket_parse(string):
       return TTree(nltktree.bracket_parse(string).pprint())  
       
   def num_nodes(self):
    size = 1
    for c in self._children:
         size += c.num_nodes()
    return size 
   
   def node_labels(self):
    if self.is_leaf():
        return [self._label]
    else:
        res = [self._label]
        for c in self._children:
            res += c.node_labels()
        return res
   
   def set_projection(self):
    self._proj = True
    return self
   
   def is_projection(self):
    return self._proj
   
   def projection(self):
    if self.is_leaf():
        return set([self.set_projection()])
    else:
        res = set([])
        for child in self._children:
            for t in child.projection():
                c = self.root().set_projection()
                res.add(c.insert(t).set_projection())
        return res
   
   def to_tuple(self):
        if self.is_leaf():
            return (self.label(),)
        else:
            if self._proj:
                return (self.label(),)+self._children[0].to_tuple()
            else:
                print 'ERROR: cannot make tuple from non projected tree (might still have branches)'
                
def to_tuples(trees):
    """converts a tree, that has no branching to a tuple; so (A (B C)) to (A, B, C)"""
    res = set([])
    for t in trees:
         res.add(t.to_tuple()) 
    return res
    
def tuples_to_tree(tuples):
    tups = list(tuples)
    if tuples==set([]):
        return TTree('(_ empty)')
    t_init = TTree("("+str(tups[0][0])+' '+str(tups[0][1])+")")
    for tup in tups:
        add_proj_tree(t_init,tuple_to_tree(tup))
    return TTree(str(nltktree.fromstring(str(t_init))))

def add_proj_tree(t1,t2):
    match = False
    if len(t2.children())==0:
        return
    if len(t1.children())==0:
        t1.insert(t2.children()[0])  
    for c1 in t1.children():
        if c1.label()==t2.children()[0].label():
            match = True
            add_proj_tree(c1,t2.children()[0])
    if not(match):
        t1.insert(t2.children()[0])
        
        
def tuple_to_tree(tup):
    r = range(0,len(tup)-1)
    string = ""
    for i in r:
        string+= "("+str(tup[i])+" "
    string+=str(tup[len(tup)-1])+((len(tup)-1)*")")
    return TTree(string)   
    
def read_sot(file):
	with open(file) as f:
		treeSets = {}
		
		setStrings = f.read().split('\n\n\n')
		for sid in range(len(setStrings)):
			treeStrings = setStrings[sid].split('\n\n')
			for tid in range(len(treeStrings)):
				if treeStrings[tid].strip() == '':
					continue
				if sid in treeSets:
					treeSets[sid].add(TTree(treeStrings[tid], id=str(sid)+':'+str(tid)))
				else:
					treeSets[sid] = set([TTree(treeStrings[tid], id=str(sid)+':'+str(tid))])
	return treeSets


