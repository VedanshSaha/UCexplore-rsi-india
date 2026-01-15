# Union-Closed Families and Frankl’s Conjecture

This repository contains code for generating and analyzing **union-closed families of sets** in order to study **Frankl’s Union-Closed Sets Conjecture**.

A family \( \mathcal{F} \subseteq 2^{[n]} \) is union-closed if  
\( A,B \in \mathcal{F} \Rightarrow A \cup B \in \mathcal{F} \).

Frankl’s conjecture states that in any non-empty finite union-closed family, there exists an element that appears in at least half of the sets.

---

## Goal

The goal of this codebase is to enumerate small union-closed families under constraints, identify families where the maximum element frequency is unusually small, and study how standard compression operations affect those families.

The focus is on **near-extremal families**, meaning families where no element has frequency close to \( |\mathcal{F}|/2 \).

---

## Family generation

Families are generated over universes of size \( n \le 5 \).

The generator enforces:
- closure under union,
- inclusion of the empty set,
- optional size constraints.

Each family is represented as a bitmask over subsets of \([n]\).

---

## Isomorphism removal

Two families that differ only by a permutation of the ground set represent the same structure.

To avoid double counting, each family is converted into a canonical form using **Nauty/Traces** by encoding the incidence structure as a bipartite graph and computing a canonical labeling.

Only one representative from each isomorphism class is kept.

---

## Frequency data

For every family, the following are computed:

- frequency of each element  
- minimum element frequency  
- variance of element frequencies  
- distribution of set sizes  

These are used to detect families where all elements have low frequency relative to \( |\mathcal{F}| \).

---

## Shift and compression operations

The code implements standard shift and compression operations used in union-closed set theory.

For a given family, these operators are applied iteratively, and after each step the element-frequency data is recomputed.

This allows tracking:
- whether compression increases the minimum element frequency,
- which families remain resistant to compression,
- which structural features survive repeated shifting.

---

## Near-extremal catalog

Families are filtered by conditions such as:
- large \( |\mathcal{F}| \) relative to \( 2^n \),
- small maximum element frequency,
- high symmetry or uneven set-size distributions.

These families are stored along with their invariants, giving a reproducible catalog of difficult cases for small universes.

---

## What this repository produces

The pipeline outputs:

- all non-isomorphic union-closed families for small \(n\),
- element-frequency statistics for each family,
- compressed versions of each family,
- families that remain low-frequency after compression.

These datasets provide concrete input for testing hypotheses about why Frankl’s bound holds or where it is tight.

---

## References

- D. Reimer, *An Average Set Size Theorem*  
- H. Bruhn and O. Schaudt, *The Union-Closed Sets Conjecture* (survey)  
- J. Gilmer, *A Proof of Frankl’s Conjecture for Large Families*  
- P. Frankl, original formulation of the conjecture  
