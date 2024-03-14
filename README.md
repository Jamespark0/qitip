<div align="center"> 
    <center><h1>Quantum Information Theoretic Inequality Prover (Quantum ITIP)</h1></center> 
    </div>
     <br/> 
<div align="center">
An information inequality prover dedicated to quantum information theory.
</div>

---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [What is Quantum ITIP?](#what-is-quantum-itip)
- [Features](#features)
- [Introduction](#introduction)
- [Quickstart](#quickstart)
- [Usages](#usages)
  - [Initialization](#initialization)
  - [Choose actions](#choose-actions)
    - [Add inequality](#add-inequality)
    - [Add one constraint](#add-one-constraint)
    - [Clear constraints](#clear-constraints)
    - [Check von-Neumann type](#check-von-neumann-type)
    - [End prover](#end-prover)
- [Credits](#credits)
- [Warning](#warning)
- [References](#references)

## What is Quantum ITIP?
Quantum ITIP automatically proves if a quantum information inequality can be derived from strong subadditivity and weak monotonicity in quantum information theory. If this is the case, this prover generates a set of inequalities that can be used to prove the inequality; otherwise, it generates a set of equalities to help build a counterexample to "disprove" the inequality. Note that a counterexample may not be found due to the nature of quantum information inequality.

## Features
1. The inequality to be proved can have additional constraints imposed by the user.
2. The prover helps prove and disprove the given inequality.

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

One can also apply this formula to any reduced density matrix of some quantum system. There are a set of rules that a quantum system must satisfy. These rules are **strong sub-additivity** and **weak monotonicity**. Consider an $`n-`$party quantum system. Let $N$ be the set $\set{1,2,...,n}$ and $I, J\subseteq N$, the general form of strong sub-addivity and weak monotoncity[[1]](#1) is given as 
```math
\begin{cases}
S(\hat{\rho}_{I}) + S(\hat{\rho}_{J}) \geq S(\hat{\rho}_{I \cup J}) + S(\hat{\rho}_{I \cap J})\\
S(\hat{\rho}_{I}) + S(\hat{\rho}_{J}) \geq S(\hat{\rho}_{I \setminus J}) + S(\hat{\rho}_{J \setminus I})
\end{cases}.
```
The set of these inequalities are referred to as **basic inequalities**.

Information inequalities play a crucial role in information theory. Proving if an inequality can be derived from the basic inequalities is no easy task in quantum information theory, and neither is its counterpart in classical information theory. In classical information theory, there are a lot of tools to help do the job. As far as we know, there is no such tool in quantum information theory. This prover hopes to be the cornerstone to bridge the gap.

## Quickstart
Download the entire directory. Install all the dependencies with `requirements.txt`. Navigate to the directory from the terminal and run
```
python -m src.mini_app
```

## Usages<a name="usages"></a>
### Initialization<a name="initialization"></a>
Before entering the main page, the prover asks the number of quantum systems to be worked with. Enter an integer greater than 2. For example, if we are to work with 4 quantum systems:

![init](https://imgur.com/TOzrWY2.png)

### Choose actions<a name="choose-actions"></a>
The homepage shows a list of actions that a user can choose from:

1. add/update an inequality
2. impose a constraint on the inequality
3. clear all constraints
4. check if the inequality is von-Neumann type
5. end the prover

![homepage](https://imgur.com/oQDe4Ju.png)
The action is activated by typing in the index next to the action. For example, 

`Pick an action: 1` prompts the user to add or update the inequality to be proved.

`Pick an action: q` ends the prover.

#### Add inequality<a name="add-inequality"></a>
![add\update inequality](https://imgur.com/8i5FcVY.png)
The inequality should be expressed in terms of the marginal entropies, and takes the form:

`[A linear combination of marginal entropis] >= 0`

 To assign the coefficient value for a certain marginal entropy, the indices of the systems in the marginal entropy is separated by spaces, and the assignment is followed by '->'.

`[indices of the systems] -> [coefficient value]`

If the inequality has more than one coefficient to assign (which is often the case), each assignment is separated by ';'. Those coefficients not specified by the user will be set to $0$.

For example, if the inequality to be checked is 
```math
I(1;2\mid 3) = S(1, 3) + S(2, 3) - S(1,2,3) - S(3) \geq 0,
```

one should input something like:

```
1 3 -> 1; 2 3 -> 1; 1 2 3 -> -1; 3 -> -1
```

where the order does not matter.

#### Add one constraint<a name="add-one-constraint"></a>
This prover current allows only adding **one equality constraint** at a time. The constraint is expressed in the form of marginal entropies just like the inequality to be proved, and the equality constraint takes the form:

`[linear combination of marginal entropies] = 0`.

The way to assign the coefficients in the constraint is identical to assigning the coefficients in the inequality.

![add one constraint](https://imgur.com/TFT9vUE.png)

#### Clear constraints<a name="clear-constraints"></a>
This clears all the constraints provided by the user. 

#### Check von-Neumann type<a name="check-type"></a>
By choosing this functionality, the prover check if the given inequality, under the imposed constraints, can be derived from the basic inequalities. The program returns one of the two possible outcomes:

1. `It's von-Neumann type!` The prover shows how to construct the inequality from strong subadditivity and from weak monotonicity altogether.
2. `It's not provable by Quantum ITIP :(` This indicates that the inequality cannot be derived from basic inequalities. It also generates a list of **equalities** that the counterexample can satisfy. Note that the hints provided by the prover is a sufficient condition not a necessary condition.

For example, 
1. The non-negativity of quantum entropy. Let's say to prove the marginal entropy $S(1)$ which indicates the quantum entropy of system $1$ is non-negative, the prover generates the following result

![non-negativity of quantum entropy](https://imgur.com/BrXJBBb.png)

2. Conditional entropy can be negative in quantum information theory. If we are to show $S(1\mid 2) \geq 0$ cannot be derived from basic inequalities, the prover suggests the following result to disprove the inequality

![negativity of conditional entropy](https://imgur.com/gCZsFvI.png)

#### End prover<a name="end"></a>
This terminates the program.

## Credits
This work is inspired by the classical ITIP formulated by Siu Wai Ho, Alex Lin Ling, Chee Wei Tan and Raymond Yeung. More information can be found from [the AITIP website](https://aitip.org).

I would like to thank Professor Mario Berta and Tobias Rippchen. This project would not be possible without their supoorts and guidance.

## Warning
This is a master-thesis project, and still has a lot of rooms for improvements.

## References
<a id="1">[1]</a> N. Pippenger, “The inequalities of quantum information theory,” IEEE Transactions on Information Theory, vol. 49, no. 4, pp. 773–789, Apr. 2003, conference Name: IEEE Transactions on Information Theory. [Online]. Available: https://ieeexplore.ieee.org/document/1193790
