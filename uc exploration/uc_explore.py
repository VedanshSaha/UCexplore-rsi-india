#!/usr/bin/env python3

import itertools
import json
import csv
import argparse
from collections import defaultdict


def mask_from_set(s):
    m = 0
    for x in s:
        m |= 1 << x
    return m


def set_from_mask(m, n):
    return [i for i in range(n) if (m >> i) & 1]


def popcount(m):
    return bin(m).count("1")


def enum_antichains(n):
    universe = list(range(1, 1 << n))
    universe.sort(key=lambda m: (popcount(m), m))
    N = len(universe)

    def backtrack(start, current):
        if current:
            yield list(current)
        for i in range(start, N):
            m = universe[i]
            bad = False
            for c in current:
                if (c & m) == c or (c & m) == m:
                    bad = True
                    break
            if bad:
                continue
            current.append(m)
            yield from backtrack(i + 1, current)
            current.pop()

    yield from backtrack(0, [])


def closure_of_antichain(A):
    A_list = list(A)
    res = {0}
    for r in range(1, len(A_list) + 1):
        for comb in itertools.combinations(A_list, r):
            u = 0
            for x in comb:
                u |= x
            res.add(u)
    return res


def canonical_form_family_bruteforce(family_masks, n):
    fam_sorted = sorted(family_masks)
    best = None

    for perm in itertools.permutations(range(n)):
        perm_map = {i: perm[i] for i in range(n)}
        permuted = []

        for m in fam_sorted:
            s = set_from_mask(m, n)
            new_mask = mask_from_set(perm_map[i] for i in s)
            permuted.append(new_mask)

        permuted.sort()
        tup = tuple(permuted)

        if best is None or tup < best:
            best = tup

    return best


def element_freqs(family_masks, n):
    counts = [0] * n
    for m in family_masks:
        for i in range(n):
            if (m >> i) & 1:
                counts[i] += 1

    size = len(family_masks)
    freqs = [c / size for c in counts]
    return freqs, counts, size


def variance(xs):
    if not xs:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def compress_Cij(family_masks, i, j):
    fam = set(family_masks)
    out = set()

    for S in fam:
        if (S >> j) & 1 and not ((S >> i) & 1):
            Sprime = (S & ~(1 << j)) | (1 << i)
            out.add(Sprime)
        else:
            out.add(S)

    return out


def compress_until_stable(family_masks, n, max_iter=20):
    F = set(family_masks)

    for _ in range(max_iter):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                F2 = compress_Cij(F, i, j)
                if F2 != F:
                    F = F2
                    changed = True
        if not changed:
            break

    return F


def enumerate_unique_union_closed(n, max_families=None):
    seen = set()
    result = []

    for ant in enum_antichains(n):
        F = closure_of_antichain(ant)
        canon = canonical_form_family_bruteforce(F, n)

        if canon in seen:
            continue

        seen.add(canon)
        result.append((ant, F))

        if max_families and len(result) >= max_families:
            break

    return result


def run_experiment(n, max_families=None, output_csv="uc_results_n.csv"):
    data = []
    families = enumerate_unique_union_closed(n, max_families)

    for idx, (ant, F) in enumerate(families):
        fam_sorted = sorted(F)

        freqs_before, _, size_before = element_freqs(fam_sorted, n)
        var_before = variance(freqs_before)
        min_freq_before = min(freqs_before) if freqs_before else 0.0

        F_comp = compress_until_stable(F, n)
        freqs_after, _, _ = element_freqs(sorted(F_comp), n)
        var_after = variance(freqs_after)
        min_freq_after = min(freqs_after) if freqs_after else 0.0

        data.append({
            "index": idx,
            "antichain_minimals": [set_from_mask(m, n) for m in ant],
            "family_size": size_before,
            "min_freq_before": round(min_freq_before, 6),
            "var_before": round(var_before, 6),
            "compressed_changed": F_comp != F,
            "min_freq_after": round(min_freq_after, 6),
            "var_after": round(var_after, 6),
            "freqs_before": [round(x, 6) for x in freqs_before],
            "freqs_after": [round(x, 6) for x in freqs_after],
        })

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "index",
            "antichain_minimals",
            "family_size",
            "min_freq_before",
            "var_before",
            "compressed_changed",
            "min_freq_after",
            "var_after",
            "freqs_before",
            "freqs_after",
        ])

        for r in data:
            writer.writerow([
                r["index"],
                json.dumps(r["antichain_minimals"]),
                r["family_size"],
                r["min_freq_before"],
                r["var_before"],
                r["compressed_changed"],
                r["min_freq_after"],
                r["var_after"],
                json.dumps(r["freqs_before"]),
                json.dumps(r["freqs_after"]),
            ])

    print(f"Wrote {len(data)} canonical families to {output_csv}")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--max", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    out = args.out or f"uc_results_n{args.n}.csv"
    run_experiment(args.n, args.max, out)


if __name__ == "__main__":
    main()
