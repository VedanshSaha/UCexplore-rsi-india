# Union-Closed Sets Exploration (Frankl’s Conjecture)

This repository contains code to explore small instances of **union-closed families** in connection with **Frankl’s Union-Closed Sets Conjecture**.

The conjecture asks whether, in any finite union-closed family of sets, there must exist an element that appears in at least half of the sets. Although the statement is elementary, all known proof techniques fail on certain structured families, so small-case computation is useful for understanding what those extremal configurations look like.

The code in this repository does the following:

- Enumerates **union-closed families** by generating antichains of minimal sets and taking their union-closure.
- Uses **isomorphism reduction** (either brute-force or via Nauty/Traces) so that families differing only by relabeling elements are counted once.
- Computes **element-frequency statistics**, including minimum frequency and variance across elements.
- Implements basic **shift and compression operators** from the literature and measures how these operations change frequency distributions.
- Produces reproducible **CSV datasets** and analysis-ready outputs for small universes.

This project is designed for **small parameter regimes** (typically universes of size 4–5 on a laptop) and is meant to generate concrete examples and patterns that can guide theoretical work. It does not attempt to prove the conjecture, but to map the structure of near-extremal families and the behavior of standard compression methods.

**Main references:**
- D. Reimer, *An entropy approach to the union-closed sets conjecture* (2003)  
- H. Bruhn and O. Schaudt, *The journey of the union-closed sets conjecture* (survey)  
- J. Gilmer, *A constant lower bound for union-closed families* (2022)  
- B. McKay and A. Piperno, *Practical Graph Isomorphism II* (Nauty/Traces)
