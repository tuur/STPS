## Pattern Structure of Syntactic Trees

This tool can be used for syntactic tree classification, based on the Syntax Tree Pattern Structure (STPS). It is associated with, and described in [(Leeuwenberg et al., 2015)](http://link.springer.com/chapter/10.1007%2F978-3-319-19545-2_10), where it was used for drug-drug interaction relation extraction. The ICFCA`15 conference slides can be found [here](https://github.com/tuur/STPS/raw/master/slides.pdf).
The tool includes the following functionalities:

* Tree Classification using Lazy Positive Hypothesis Classification (LPHC) (with or withour branch projection)
* Some Visualization, Penn Treebank Output, and Latex output of Trees (using [forest](https://www.ctan.org/pkg/forest?lang=en))

And will soon also include:
* Tree simplifications
* Extraction of Class-characteristic Tree Patterns
* Tree Classification based on Extracted Patterns

The code is not very clean yet, so in case of errors or suggestions feel free to send me an e-mail.

### Requirements
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [NLTK 3.0](http://www.nltk.org/)

### Usage
A very simple demo example is included, which classifies questions.
Corresponding calls are given below. 

##### LPHC classification
The code allows classification of sets of trees (SOTS), as the similarity operator works on sets of trees. Usually sentences are represented as set containing only one tree, namely the parse tree of that sentence. Examples of the file formats are given below, and in the example folder.

To classify the set of unlabeled SOTS, stored in `example/unlabeled/unlabeled_trees.ptb`, using as example data the SOTS in `example/labeled/trees.sot` with their corresponding labels in `example/labeled/classlabels.labels` the following command is to be used:
```
python lphc.py example/unlabeled/unlabeled_trees.ptb example/labeled/trees.sot example/labeled/classlabels.labels question sentence -projection 1 -output_hypotheses 'pos_hyps.out' -output_origins 'origins.out'
```
As argument the label(s) of the positive class (here `question`), and those of the negative class (here `sentence`) should be provided. There are options for using the branch projection, outputting the positive hypotheses/patterns that were found, and the links that indicate which positive hypotheses/patterns were used to classify each unlabeled SOT.

For more information run:
```python lphc.py -h```

##### Visualization

To visualize the trees from the labeled example data (SOT 2 to 4), you can use:
```python visualize_sot.py example/labeled/trees.sot -s 1 -indices 2-4```

You can also use the script to visualize the found positive hypotheses. For example, after you run the lphc.py command mentioned above, and `pos_hyps.out` and `origins.out` are created. You can run:

```
python visualize_sot.py pos_hyps.out -origins origins.out -totree 1 -indices 2
```

This will visualize the positive hypotheses used to classify the third unlabeled SOT (index 2) as a question. Notice that the totree option merges the branches obtained after the projection to a single tree.

For more detailed information run:
```python visualize_sot -h```

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

##### Origins
These can be created by `lphc.py` during classification and contain the links between indices of the positive hypotheses that were found, and their corresponding unlabeled and labeled indices. They have the format:
```unlabeled_index <space> labeled_index <tab> positive_hypothesis_index```. 
For example:
```
0 2    0
3 2    1
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


