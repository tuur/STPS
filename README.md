## Pattern Structure of Syntactic Trees

This tool can be used for syntactic tree classification, based on the Syntax Tree Pattern Structure (STPS). It is associated with, and described in [(Leeuwenberg et al., 2015)](http://link.springer.com/chapter/10.1007%2F978-3-319-19545-2_10), where it was used for drug-drug interaction relation extraction. The ICFCA`15 conference slides can be found [here](https://github.com/tuur/STPS/raw/master/slides.pdf).
The tool includes the following functionalities:

* Tree Classification using Lazy Positive Hypothesis Classification (LPHC)
* Visualization, Penn Treebank Output, and Latex output of Trees

And will soon also include:
* Tree simplifications
* Extraction of Class-characteristic Tree Patterns
* Tree Classification based on Extracted Patterns

### Requirements
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [NLTK 3.0](http://www.nltk.org/)

### Usage

##### LPHC classification

##### Pattern Extraction

##### Classification with fixed Patterns

### File formats
We use three different data formats. Examples are given for the sentences:
* 'A relates to B .'
* 'A is not related to B .'

#####Sets of Trees (.sot)
STPS uses similarity on sets of trees. Trees are described by the Penn TreeBank format. Trees should be separated by one empty line, and sets by two empty lines. Usually sentences are represented as set containing only one tree, namely the parse tree of that sentence. For example:

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

##### Class Labels (.lab)
Labels are to be given as one label per line. For example:
```
relation
norelation
```

## Reference
```
@incollection{
author={Leeuwenberg, Artuur and Buzmakov, Aleksey and Toussaint, Yannick and Napoli, Amedeo},
title={Exploring Pattern Structures of Syntactic Trees for Relation Extraction},
year={2015},
booktitle={Formal Concept Analysis},
publisher={Springer International Publishing},
url={http://dx.doi.org/10.1007/978-3-319-19545-2_10}
}
```


