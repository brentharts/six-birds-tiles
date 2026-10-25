#!/usr/bin/env python3
"""Hierarchical pruning of admissible 2x2x2 blocks (Tsiokos Open Problem 2: is every Chair44 tiling in
the substitution hull?).

Usage: python3 verify/hull/chair44_hull_prune.py [admissible_blocks.json] (output of chair44_vertex_blocks.py).

Let A be the set of 2x2x2 vertex blocks that occur in some tiling by Q. Every tiling T by Q is
hierarchical: its parent tiling D(T) is again a tiling by Q (registered on a lattice of spacing 2) and
T = sigma(D(T)). Every vertex block of T is one of the 27 windows of sigma(b) for a vertex block b of
D(T). Hence A is contained in Adm and in Win(sigma(A)), so A is contained in the limit of
X_0 = Adm, X_{k+1} = Adm & Win(sigma(X_k)). If that limit is the legal language, every block of every
tiling by Q is legal, and every tiling by Q lies in the substitution hull.
"""
import itertools
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # repository root
sys.path.insert(0, str(REPO / "verify"))
import substitution_modular_coincidence as m  # noqa: E402

cert = json.loads(m.CERTIFICATE.read_text())
BITS = tuple(itertools.product((0, 1), repeat=3))
frames = tuple(m.frame_from_json(r) for r in cert["orientation_group"])
children = tuple((m.frame_from_json(r[0]), tuple(r[1])) for r in cert["children"])
labels = [(f, c) for f in frames for c in m.CHAIR_CELLS]
index = {l: i for i, l in enumerate(labels)}
phi = {}
for frame in frames:
    owners = {}
    for cf, co in m.child_poses(frame, children):
        for cell in m.CHAIR_CELLS:
            owners.setdefault(m.cell_lower(cf, co, cell), []).append((cf, cell))
    for cell in m.CHAIR_CELLS:
        src = m.cell_lower(frame, m.ORIGIN, cell)
        for d in BITS:
            (tl,) = owners[m.add(m.scale(2, src), d)]
            phi[index[(frame, cell)], d] = index[tl]
WIN = [tuple((BITS.index(tuple((o[k] + b[k]) // 2 for k in range(3))),
              BITS.index(tuple((o[k] + b[k]) % 2 for k in range(3)))) for b in BITS)
       for o in itertools.product(range(3), repeat=3)]
PHI = [[phi[j, d] for d in BITS] for j in range(168)]


def windows_of(blk):
    return {tuple(PHI[blk[i]][d] for i, d in win) for win in WIN}


language = set()
frontier = {tuple(PHI[j]) for j in range(168)}
while frontier:
    language |= frontier
    frontier = {w for b in frontier for w in windows_of(b)} - language
print("legal blocks:", len(language))

BLOCKS = sys.argv[1] if len(sys.argv) > 1 else "admissible_blocks.json"
adm = {tuple(b) for b in json.load(open(BLOCKS))["admissible"]}
print("admissible blocks:", len(adm), "legal inside:", language <= adm)
X = adm
k = 0
while True:
    img = set()
    for b in X:
        img |= windows_of(b)
    Y = X & img
    k += 1
    print(f"round {k}: {len(Y)} blocks survive", flush=True)
    if Y == X:
        break
    X = Y
print("fixpoint size:", len(X), "equals legal language:", X == language)
extra = sorted(X - language)
print("surviving non-legal blocks:", len(extra))
ok = X == language
print("STATUS:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
