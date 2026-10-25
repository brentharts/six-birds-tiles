# Hull and symmetry of Chair44 tilings

These scripts give computer-assisted answers to Open Problems 1 and 2 of arXiv:2609.19214 (§10).

An **atlas tiling** is a tiling of R³ by chairs in poses (proper frames, integer translations) in which every
face-adjacent pair has its relative pose in the 44-contact atlas A44.

- **Hull.** Every atlas tiling lies in the substitution hull Ω_σ.
  - So Ω_σ, which is minimal, uniquely ergodic, pure point, and the hull of a regular model set over Z₂³, contains every
    atlas tiling.
  - Every atlas tiling is pure point diffractive.
  - Only 30 of the 44 contacts ever occur.
- **Symmetry.** The symmetry group of an atlas tiling is conjugate to exactly one of 1, C2 (about a face-diagonal axis),
  C4 and D4, and each occurs. So |Sym(T)| ≤ 8.
- **For tilings by the solid Q**, both statements follow from **Tsiokos's registration theorem** (Thm 5.6, Lemma 5.3):
  every tiling by Q is, up to an isometry, an atlas tiling.
  - Its proof has been audited independently. Every written step was checked, every finite input recomputed in
    exact arithmetic, and each of the 5,273 witnesses in `certificates/companion_collision_certificate.json` checked.
    See [`independent/REGISTRATION_AUDIT.md`](independent/REGISTRATION_AUDIT.md).
  - It has not been refereed.
- **Not claimed:** that the space of *all* tilings by Q is minimal (it is the union of the translates gΩ_σ), or that every
  element of Ω_σ is limit-periodic.

The scripts use only the Python standard library and this repository's own data:
- `certificates/candidate_certificate.json` (the 44-contact atlas and the children);
- `simulations/explore/framed_chair.py`;
- `verify/substitution_modular_coincidence.py`.

```
python3 verify/hull/chair44_vertex_blocks.py   blocks.json   # admissible 2x2x2 vertex blocks: 360189   (~8 min)
python3 verify/hull/chair44_hull_prune.py      blocks.json   # Win(sigma(admissible)) = the 1410 legal blocks
python3 verify/hull/chair44_symmetry_census.py               # groups 1, C2(diag), C4, D4; consistency checks on real patches
```

Each script ends with `STATUS: PASS` or `FAIL`.

## Argument

1. **Blocks.** A *block* is the labelling of the 8 unit cells at a lattice vertex.
   - It is *admissible* if the chairs it names are consistent and disjoint, and all face contacts are in A44. Every block
     of an atlas tiling is admissible.
   - It is *legal* if it occurs in some σⁿ(j).
2. **Lemma (computed).** Every window of σ(b), for b admissible, is legal. There are 360,189 admissible blocks in 15,214
   O-orbits.
3. **Hierarchy (H).** Every atlas tiling T satisfies T = σ(D(T)), where D(T) is again an atlas tiling.
   - This is Kamenetsky's Prop. 7.1 (arXiv:2610.00916). It follows from three finite conditions: coarsening closure
     30 → 44 with Σ(P\*) = 2P\*; tight facet rules; unique parents for the 33 first-shell enclosures.
   - All three were reproduced by independent code. Tsiokos proves the same for tilings by Q (Thms 6.4–6.5).
4. **Hull.**
   - Every patch of T lies in σⁿ(β) for a block β of Dⁿ(T).
   - β is a window of σ(β′) with β′ admissible, so β is legal by the lemma.
   - Hence every patch of T is legal. No exhaustion of space by one supertile is used, so tilings with fault planes are
     covered.
5. **Symmetry.**
   - Symmetries map poses to poses, so they are proper, with integer translation parts, and Sym(T) embeds in O.
   - No element of order 3: a point of its axis with all coordinates in (1/100, 99/100) mod 1 is interior to a chair,
     which the rotation would fix. So Sym(T) ≤ D4.
   - Point groups fix a vertex of every supertile lattice L_n. Take a block that recurs after the stabilisers settle. It is
     periodic under the central window, so it is one of the 27 fixed seeds, with stabiliser 1 or D4. Neither Klein group
     occurs.
   - Cyclic groups: the axis, with direction e, meets every L_n, although no single point of it need be a vertex of every
     L_n. The group K occurs iff a certain graph has a strongly connected component using two different axial window
     shifts. Its vertices are the legal blocks whose stabiliser meets the rotations about e in exactly K; their full
     stabiliser may be larger. That holds for C2(diag) and C4, but not for C2 about a coordinate axis.
   - The patches built by `chair44_symmetry_census.py` are consistency checks. The exclusion of further symmetries rests on
     the argument.
6. **Independent checks** ([`independent/`](independent/), standard library, reads only this repository's data).
   - An adversarial referee re-derived every number with separately written code, including A44 from the pyramid
     geometry and from the eight children alone. It also wrote an O-orbit certificate of the lemma
     (`lemmaA_orbits.json`) with a stand-alone verifier (`c44lemma_cert.py`).
   - `registration_audit.py` recomputes the finite inputs of the registration theorem: the mesh, the census
     6,862 → 5,317, and every collision witness.
   - The lemma depends on the exact atlas: enlarging A44 by the five non-atlas contacts of one violating block gives 24
     failures.
   - The referee report is [`independent/INDEPENDENT_REVIEW.md`](independent/INDEPENDENT_REVIEW.md). Commands are in
     [`independent/README.md`](independent/README.md).
   - Brent Hartshorn's `spectre` repository regenerates the tile and its atlas with independent code on the same eight
     children (`symchair44.py`, `chair44_hull_admissible.py`) and gets the same counts.

Paper draft: T. Romanov, *The hull and the symmetry groups of Chair44 tilings* (2026). It is computer-assisted and not yet refereed.
