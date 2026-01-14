#!/usr/bin/env python3

import subprocess
import tempfile
import os
import sys
import json


def family_to_dreadnaut(family_masks, n):
    sets = list(sorted(family_masks))
    m = len(sets)
    total = m + n

    adj = [[] for _ in range(total)]
    for i, S in enumerate(sets):
        for e in range(n):
            if (S >> e) & 1:
                adj[i].append(m + e)
                adj[m + e].append(i)

    edges = []
    for u in range(total):
        for v in adj[u]:
            if u < v:
                edges.append((u, v))

    lines = []
    lines.append(f"n={total}")
    lines.append("g " + " ".join(f"{u} {v}" for u, v in edges) + " .")

    sets_list = " ".join(str(i) for i in range(m))
    elements_list = " ".join(str(i) for i in range(m, m + n))

    lines.append(f"c {sets_list} ;")
    lines.append(f"c {elements_list} ;")
    lines.append("x")
    lines.append("Q")
    lines.append(".")

    return "\n".join(lines)


def canonicalize_with_dreadnaut(family_masks, n, dreadnaut_path="dreadnaut"):
    script = family_to_dreadnaut(family_masks, n)

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tf:
        tf.write(script)
        fname = tf.name

    try:
        proc = subprocess.run(
            [dreadnaut_path],
            input=script.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        return proc.stdout.decode("utf-8", errors="ignore")
    except Exception:
        return None
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass


if __name__ == "__main__":
    fam = {1 << 0, (1 << 1) | (1 << 2)}
    out = canonicalize_with_dreadnaut(fam, 3)
    if out:
        print(out[:200])
