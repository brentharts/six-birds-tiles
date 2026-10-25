#!/usr/bin/env python3
"""Admissible 2x2x2 vertex blocks of Chair44 tilings versus the legal substitution language.

Run from anywhere: python3 verify/hull/chair44_vertex_blocks.py [OUT.json] (default admissible_blocks.json). Uses its exact chair geometry
(simulations/explore/framed_chair.py), the 44-contact atlas (certificates/candidate_certificate.json,
legal_contacts) and the 168-label substitution (verify/substitution_modular_coincidence.py).

A block is the 8 unit cells around a lattice vertex, each labelled (frame, cell of chair). It is
*admissible* if the chair poses the labels name are consistent (a pose covering a block cell is the
pose named there), pairwise disjoint, and every adjacent pair has its relative pose in the atlas.
Every block occurring in a tiling by Q is admissible (Tsiokos: tilings by Q are registered chair
tilings with all contacts in the atlas).
"""
import itertools
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # repository root
sys.path.insert(0, str(REPO / "simulations" / "explore"))
sys.path.insert(0, str(REPO / "verify"))
import framed_chair as F  # noqa: E402
import substitution_modular_coincidence as m  # noqa: E402

cert = json.loads((REPO / "certificates" / "candidate_certificate.json").read_text())
L = {(tuple(map(tuple, g)), tuple(t)) for g, t in cert["legal_contacts"]}
L = {((tuple(g[0]), tuple(g[1])), t) for g, t in L}
assert len(L) == 44
inv_closed = all(F.normal((g, t), F.ROOT) in L for g, t in L)
print("atlas closed under inversion:", inv_closed)

BITS = tuple(itertools.product((0, 1), repeat=3))
POS = tuple(itertools.product((-1, 0), repeat=3))
frames = tuple(m.frame_from_json(r) for r in cert["orientation_group"])
children = tuple((m.frame_from_json(r[0]), tuple(r[1])) for r in cert["children"])
labels = [(f, c) for f in frames for c in m.CHAIR_CELLS]
index = {l: i for i, l in enumerate(labels)}

# legal language (as in Tsiokos' seed_language_closure.py)
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
windows = [tuple((BITS.index(tuple((o[k] + b[k]) // 2 for k in range(3))),
                  tuple((o[k] + b[k]) % 2 for k in range(3))) for b in BITS)
           for o in itertools.product(range(3), repeat=3)]
language = {tuple(phi[j, d] for d in BITS) for j in range(168)}
frontier = set(language)
while frontier:
    new = {tuple(phi[blk[i], d] for i, d in win) for blk in frontier for win in windows} - language
    language |= new
    frontier = new
print("legal blocks:", len(language))


def pose_of(cell, lab):
    """The chair pose (frame, t) whose cell `c` is the unit cell with lower corner `cell`."""
    f, c = labels[lab]
    t = tuple(cell[i] - (m.cell_lower(f, (0, 0, 0), c)[i]) for i in range(3))
    assert m.cell_lower(f, t, c) == cell
    return (f, t)


def compatible(p, q):
    if p == q:
        return True
    if F.cells(p) & F.cells(q):
        return False
    return not F.adjacent(p, q) or F.normal(p, q) in L


# sanity: framed_chair.cells agrees with m.cell_lower
for f in frames:
    for t in ((0, 0, 0), (3, -2, 5)):
        assert F.cells((f, t)) == frozenset(m.cell_lower(f, t, c) for c in m.CHAIR_CELLS)

def admissible_blocks():
    out = []
    poses = [None] * 8

    def rec(k):
        if k == 8:
            out.append(tuple(chosen))
            return
        cell = POS[k]
        for lab in range(168):
            p = pose_of(cell, lab)
            cells = F.cells(p)
            ok = True
            # consistency with cells already labelled
            for j in range(k):
                q = poses[j]
                if POS[j] in cells and q != p:
                    ok = False
                    break
                if cell in F.cells(q) and q != p:
                    ok = False
                    break
                if not compatible(p, q):
                    ok = False
                    break
            if ok:
                poses[k] = p
                chosen.append(lab)
                rec(k + 1)
                chosen.pop()
        poses[k] = None

    chosen = []
    rec(0)
    return out


adm = admissible_blocks()
admset = set(adm)
print("admissible blocks:", len(admset))
print("legal subset of admissible:", language <= admset)
extra = sorted(admset - language)
print("admissible but not legal:", len(extra))
json.dump({"admissible": sorted(admset), "extra": extra},
          open(sys.argv[1] if len(sys.argv) > 1 else "admissible_blocks.json", "w"))
ok = len(admset) == 360189 and len(language) == 1410 and language <= admset and inv_closed
print("STATUS:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
