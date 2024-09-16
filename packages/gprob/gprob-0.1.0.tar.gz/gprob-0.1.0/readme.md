# gprob
gprob is a probabilistic programming language for Gaussian random variables with exact conditioning, implemented as a python package.

A brief example:
```python
from gprob import normal

# Initializing two independent normal variables.
x = normal(0, 1)
y = normal(0, 1)

# The joint distribution of x and y under the contition that 
# their sum is zero is obtained as 
z = (x & y) | {x-y: 0}

z.cov()
```



## Requirements
* python >= 3.7
* [numpy](https://numpy.org/)

## Installation

```
pip install gprob
```

## Acknowledgements
gprob was inspired by [GaussianInfer](https://github.com/damast93/GaussianInfer), an accompaniment for the paper

D. Stein and S. Staton, "Compositional Semantics for Probabilistic Programs with Exact Conditioning," 2021 36th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS), Rome, Italy, 2021, pp. 1-13, doi: 10.1109/LICS52264.2021.9470552

