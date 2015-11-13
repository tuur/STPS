## Pattern Structure of Syntactic Trees

Tool for syntax tree classification, based on the Syntax Tree Pattern Structure (STPS), which was used for extraction of drug-drug interactions from biomedical texts as described in the ICFCA 2015 paper.

This tool includes the following functionalities:

* Tree Classification using Lazy Pattern Structure Classification
* Class-characteristic Tree pattern extraction
* Tree Classification based on Extracted Patterns

If you use this tool, please refer to the ICFCA`15 paper.

### Requires
* Python2.7
* nltk (tested on X)


### Usage

#### lpsc_classify

#### extract_patterns

#### pattern_classify

### Data file formats
We use three different data formats. Examples are given for the sentences:
* 'A relates to B .'
* 'A is not related to B'

####data.trees
The trees should be given in Penn Treebank bracketing style, and should be separated by an empty line.
For the example:
```
(ROOT
  (S
    (NP (NNP A))
    (VP (VBZ relates)
      (PP (TO to)
        (NP (NNP B))))
    (. .)))
    
(ROOT
  (S
    (NP (NNP A))
    (VP (VBZ is) (RB not)
      (ADJP (VBN related)
        (PP (TO to)
          (NP (NNP B)))))
    (. .)))
```

#### data.labels
Labels are to be given as one label per line. For example:
```
relation
norelation
```

####data.patterns
Patterns are sets of trees, which are described by the Penn TreeBank format. Tree should be separated by one empty line, and sets by two empty lines. For example:
```
(ROOT
  (S
    NP
    (VP (VBZ relates)
      (PP (TO to)
        NP))
    (. .)))


(ROOT
  (S
    NP
    (VP (VBZ is) (RB not)
      (ADJP (VBN related)
        (PP (TO to)
          NP)))
    (. .)))

(ROOT
  (S
    NP
    (VP (VBZ does) (RB not)
      (VP (VB relate)
        (PP (TO to)
          NP)))
    (. .)))
```

## Reference
```
@incollection{
author={Leeuwenberg, Artuur and Buzmakov, Aleksey and Toussaint, Yannick and Napoli, Amedeo},
title={Exploring Pattern Structures of Syntactic Trees for Relation Extraction},
year={2015},
booktitle={Formal Concept Analysis},
volume={9113},
series={Lecture Notes in Computer Science},
publisher={Springer International Publishing},
pages={153-168},
}
```
