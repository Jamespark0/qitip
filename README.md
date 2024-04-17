<div align="center"> 
    <center><h1><strong>qitip</strong> (Quantum ITIP)</h1></center> 
    </div>
     <br/> 
<div align="center">
<strong>qitip</strong> is a python package dedicated to help proving information inequalities in quantum information theory.
</div>

---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [What is **qitip**?](#what-is-qitip)
- [Features](#features)
- [Introduction](#introduction)
- [Installation (under progress)](#installation-under-progress)
- [User Guide](#user-guide)
  - [To use **qitip**](#to-use-qitip)
  - [Initialization](#initialization)
  - [Specify an inequality](#specify-an-inequality)
  - [Specify constraints](#specify-constraints)
  - [Embedding in higher-dimensional space](#embedding-in-higher-dimensional-space)
  - [Check von-Neumann type](#check-von-neumann-type)
- [Credits](#credits)
- [Warning](#warning)
- [References](#references)

## What is **qitip**?
**qitip** stands for Quantum ITIP (Information Theoretical Inequality Prover). 
This Python package not only automatically proves if a quantum information inequality can be derived from strong subadditivity and weak monotonicity in quantum information theory, but also generates readable messages to help prove or disprove the given inequality.

## Features
1. Proves if an constrained or unconstrained quantum information inequality can be derived from strong subadditivity and weak monotonicity in quantum informaiton theory.
2. Generates useful messages to help prove the inequality if it can be derived from strong subadditivity and weak monotonicity.
3. Generates hints to construct a counterexample if the inequality is unable to be derived from strong subadditivity and weak monotonicity.

## Introduction
A quantum state can be described by a density matrix $\hat{\rho}$. If we are only interested in parts of the quantum system, we can trace out the parts that do not belong in those of our interests. For example, assume we only have access to a part of a bipartite system $AB$ whose density matrix is denoted as $\hat{\rho}_{AB}$. Without loss of generality, the system accessible to us is $A$. The corresponding density matrix of system $A$ is defined as 
```math
\hat{\rho}_{A} = \mathrm{Tr}_{B}(\hat{\rho}_{AB})
```
where $\hat{\rho}_{A}$ is also called the **reduced density matrix** of $`\hat{\rho}_{AB}`$.

The quantum entropy (also known as von-Neumann entropy) of a density matrix $`\hat{\rho}`$ is defined as 

```math
S(\hat{\rho}) = -\mathrm{Tr}(\hat{\rho}\log\hat{\rho}).
```

One can also apply this formula to any reduced density matrix of some quantum system. 

There are a set of rules that a quantum system must satisfy. 
These rules are **strong sub-additivity** and **weak monotonicity**. Consider an $`n-`$party quantum system. In principle, one can index each party with an integer $i\in \set{1,2,...,n}$. Let $N$ be the set $\set{1,2,...,n}$ and $I, J\subseteq N$, the general form of strong sub-addivity and weak monotoncit [[1]](#1) is given as 
```math
\begin{cases}
S(\hat{\rho}_{I}) + S(\hat{\rho}_{J}) \geq S(\hat{\rho}_{I \cup J}) + S(\hat{\rho}_{I \cap J})\\
S(\hat{\rho}_{I}) + S(\hat{\rho}_{J}) \geq S(\hat{\rho}_{I \setminus J}) + S(\hat{\rho}_{J \setminus I})
\end{cases}.
```
The set of these inequalities are referred to as **basic inequalities**.

Information inequalities play a crucial role in information theory. 
In practice, an information inequality is the linear combination of von-Neumann entropy, conditinal entropy, mutual information and conditional mutual information. By their definitions, an information inequality can be expressed as the linear combination of marginal entropies which is called the **canonical expression**.
Proving if an inequality can be derived from the basic inequalities is no easy task in quantum information theory, and neither is its counterpart in classical information theory. 
In classical information theory, an algorithm was proposed to automate the process (Ho et all., 2020 [[2]](#2)). As far as we know, there is no such tool in quantum information theory. This package is built on top of the classical algorithm [[2]](#2), and aims to be the cornerstone to bridge the gap.

## Installation 
The package is available on [Python Package Index (PyPI)](https://pypi.org)
```
pip install qitip
```

## User Guide

### To use **qitip**
```
import qitip
```
This imports the qitip package, and one can start working with it afterwards.

To prove a quantum information inequalities, there are three things one need to specify:
1.  The number of parties in the quantum system
2.  The inequality to be proved
3.  The constraints imposed on the inequality

### Initialization<a name="initialization"></a>
Before any further actions, one has to specify the number of parties (some integer greater than 1) in the quantum system. For example, if one is to work with a tripartite system (i.e. a 3-party system), run
```Python
q3 = qitip.init(3)
```
This sets up the entropic space to work within. The information of the entries of a vector in the entropic space can be accessed by
```Python
q3.vector_entry
```
This returns a dictionary in python which maps the marginal entropy (in `frozenset`) to the index of a vector in the entropic space. 
For example, the vector entry of a tripartite system is given by 
```Python
{frozenset({1}): 0, frozenset({2}): 1, frozenset({3}): 2, frozenset({1, 2}): 3, frozenset({1, 3}): 4, frozenset({2, 3}): 5, frozenset({1, 2, 3}): 6}
```
In computer programming, indices usually starts with $0$.

Before proceeding, the information inequalities and constraints the package deals with are in **canonical expression**.

### Specify an inequality
The general form of an inequality is given as 
```math
\sum_{I\subset N} a_{I}\cdot S(I) \geq 0
```
where $a_{I}\in \mathbb{R}, \forall a_{I}$

There are two ways to specify the inequality to be proved:
1. Express the inequality in the *vector* form. The vector can be any `Sequence` type in Python such as `list` and `tuple` as long as it matches the dimension and is in the order of the `vector_entry` mentioned above.
For example, if the inequality is $I(1;2\mid 3) = S(1,3) + S(2,3) - S(1,2,3) - S(3) \geq 0$ of a tripartite system, one can create 
```Python
inequality = q3.inequality((0,0,-1, 0, 1, 1, -1))
```
2. Specify the coefficients of the inequality with a Python `dictionary`. As the number of quantum systems increases, expressing an inequality directly in the vector form is infeasible. 
By specifying the coefficients in the form
```
{(subset of the entire system): coefficient, ...}
```
To specify the subset of the entire system, just put the indices of the systems in a `list` or in a `tuple`.
Take the same example above, we can define the inequality as
```Python
inequality = q3.inequality.from_coefficients({(1, 3): 1, (2,3): 1, (1,2,3): -1, (3,):-1})
```
If one is to specify the coefficient of a marginal system with one index, the `key` of the dictinoary need not be a `list` or a `tuple`. It can be an integer as well.


### Specify constraints
One cna impose constraints on the inequality to be proved. Generally, a constraint is expressed as 
```math
\sum_{I\subset N} c_{I}\cdot S(I) = 0
```
where $c_{I}\in \mathbb{R}, \forall c_{I}$.

There are two ways to specify the constraints, very similar to that to specify an inequality.

1. Express the constraints in *matrix* form: 
Each row of the matrix represent a constraint in canonical expression; hence, the columns must match the dimensinoality of the entropic space. 
The matrix is a $2D$ `ArrayLike` object, so things like a `list` of lists or a `tuple` of tuples are all valid.

For example, if the tripartite system is *pairwise independent*, i.e. $I(i;j\mid k) = 0$, the constraints can be defined as 
```Python
constraints = q3.constraints([[-1,0,0,1,1,0,-1], [0,-1,0,1,0,1,-1], [0,0,-1,0,1,1,-1]])
```

2. Specify the coefficients of each constraint. Similar to the case when specifying an inequality of a quantum system with many parties, specifying the matrix is partically infeasible. Hence, this approach passes a `Sequence` of Python `dictionaries`.

Take the example above, one can also specify *pairwise independent* of a tripartite system using
```Python
constraints = q3.constraints.from_coefficients([{(1,2): 1, (1,3):1, (1,2,3): -1, (1):-1}, {(1,2): 1, (2,3):1, (1,2,3): -1, (2):-1}, {(1,3): 1, (2,3):1, (1,2,3): -1, (3):-1}])
```

### Embedding in higher-dimensional space
In classical information theory, Yeung has shown that an unconstrained information inequality with four random variables is actually an Shannon-type inequality with six random variables [[3]](#3). 
Therefore, I think adding the funcitonality to embed existing inequalities or constraints in a quantum system with more parties may be useful.

Assume an ineqaulity, `inequality`, and constraints, `constraints`, are defined in a quantum system with $`n-`$parties. If one is to investigate the inequality and the constraints in a quantum system with $`m-`$parties where $m > n$, one can achieve by running the code
```Python
# qn = qitip.init(n)
# qm = qitip.init(m)

new_inequality = qm.embed(inequality)
new_constraints = qm.embed(constraints)
```

### Check von-Neumann type
After specifying an inequality and constraints, one can check if the inequality, `inequality`, under the user-imposed constraints, `constraints` is von-Neumann type by 
```Python
print(qn.is_vn_type(inequality, constraints).message)
```
or
```Python
qn.check_vn_type(inequality, constraints)
```
If the inequality is unconstrained, one can passing `inequality` to `qn.is_vn_type` or to `qn.check_vn_type` without passing `constraints`.

The output message have two possible outcomes:
1. `It's von-Neumann type!` The prover shows how to construct the inequality from strong subadditivity and from weak monotonicity altogether.
2. `It's not provable by Quantum ITIP :(` This indicates that the inequality cannot be derived from basic inequalities. It also generates a list of **equalities** that the counterexample can satisfy. 
Note that the hints provided by the prover is a sufficient condition not a necessary condition and a counterexample may never be found due to the existence of non-von-Neumann type inequalities.

For example, 
1. To prove the non-negativity of quantum entropy, let's say $S(1)$, in a tripartite system, one can
```Python
import qitip

q3 = qitip.init(3)
inequality = q3.inequality.from_coefficients({1:1})

print(q3.is_vn_type(inequality).message)
```
The program generates the following outcome:
```
It's von-Neumann type inequality.

It can be proved by summing up the following:
0.5 * [- 1.0 * S(3) + 1.0 * S(1, 3) + 1.0 * S(2, 3) - 1.0 * S(1, 2, 3)] >= 0
0.5 * [1.0 * S(1) + 1.0 * S(3) - 1.0 * S(1, 3)] >= 0
0.5 * [1.0 * S(1) - 1.0 * S(2, 3) + 1.0 * S(1, 2, 3)] >= 0
```

2. Conditional entropy can be negative in quantum information theory. 
If one is to show $S(2\mid 1) \geq 0$ cannot be derived from basic inequalities, one can run some script as the following
```Python
import qitip

q3 = qitip.init(3)
inequality = q3.inequality.from_coefficients({(1,2):1, (1):-1})

print(q3.is_vn_type(inequality).message)
```
The program outputs
```text
Not provable by Quantum ITIP:(

One can try to disprove by using:
1.0 * S(1) + 1.0 * S(3) - 1.0 * S(1, 3) = 0
1.0 * S(2) + 1.0 * S(3) - 1.0 * S(2, 3) = 0
- 1.0 * S(1) + 1.0 * S(1, 2) + 1.0 * S(1, 3) - 1.0 * S(1, 2, 3) = 0
1.0 * S(1) - 1.0 * S(2, 3) + 1.0 * S(1, 2, 3) = 0
- 1.0 * S(1) - 1.0 * S(3) + 1.0 * S(1, 2) + 1.0 * S(2, 3) = 0
```

## Credits
This work is inspired by the classical ITIP formulated by Siu Wai Ho, Alex Lin Ling, Chee Wei Tan and Raymond Yeung. More information can be found from [the AITIP website](https://aitip.org).

I would like to thank Professor Mario Berta and Tobias Rippchen. This project would not be possible without their supoorts and guidance.

## Warning
This is a master-thesis project, and still has a lot of rooms for improvements.

## References
<a id="1">[1]</a> N. Pippenger, “The inequalities of quantum information theory,” IEEE Transactions on Information Theory, vol. 49, no. 4, pp. 773–789, Apr. 2003, conference Name: IEEE Transactions on Information Theory. [Online]. Available: https://ieeexplore.ieee.org/document/1193790

<a id="2">[2]</a> S.-W. Ho, L. Ling, C. W. Tan, and R. W. Yeung, “Proving and Disproving Information Inequalities: Theory and Scalable Algorithms,” IEEE Transactions on Information Theory, vol. 66, no. 9, pp. 5522–5536, Sep. 2020, conference Name: IEEE Transactions on Information Theory. [Online]. Available: https://ieeexplore.ieee.org/document/9044774

<a id="3">[3]</a> R. W. Yeung, A First Course in Information Theory, ser. Information Technology: Transmission, Processing and Storage, J. K. Wolf, Ed. Boston, MA: Springer US, 2002. [Online]. Available: http://link.springer.com/10.1007/978-1-4419-8608-5

