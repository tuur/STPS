## Pattern Structure of Syntactic Trees

This tool can be used for syntactic tree classification, based on the Syntax Tree Pattern Structure (STPS). This method is associated with, and described in [(Leeuwenberg et al., 2015)](link.springer.com/chapter/10.1007/978-3-319-19545-2_10). The ICFCA`15 conference slides can be found [here](https://github.com/tuur/STPS/raw/master/slides.pdf).
The tool includes the following functionalities:

* Tree Classification using Lazy Pattern Structure Classification
* Class-characteristic Tree pattern extraction
* Tree Classification based on Extracted Patterns

### Requirements
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [NLTK 3.0](http://www.nltk.org/)

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
}
```


