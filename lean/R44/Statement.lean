import R44

/-! Referee statement. These are aliases of canonical definitions. All
isometries, including reflections, are allowed. No lattice, face-to-face,
common orientation or local finiteness restriction is imposed. -/
noncomputable section
namespace Chair44
abbrev Space := R44.E3
/-- The exact rational solid, with its signed features. -/
abbrev Solid : Set Space := R44.Q
/-- Disjoint tile interiors and coverage of every point. -/
abbrev Tiling := R44.Tiling Solid
/-- Translation vectors preserving the tile family. -/
abbrev Periods (T : Tiling) := R44.Per T
/-- The subgroup of isometries preserving the tile family. -/
abbrev Symmetries (T : Tiling) := R44.Sym T
/-- Registered 2^n chair poses with the eight-child nesting relation.
The historical parameter is an empty record, instantiated by its constructor. -/
abbrev Hierarchy (T : Tiling) := R44.GeometricHierarchy ⟨⟩ T

/-- CLAIMS F2--F6. Uniqueness is among nested registered hierarchies.
Supertiles need not exhaust space; substitution hull membership is not asserted.
The symmetry bound also excludes symmetries of infinite order. -/
theorem chair44 : Nonempty Tiling ∧ ∀ T : Tiling,
    Periods T = {0} ∧ (Set.univ : Set (Symmetries T)).encard ≤ 24 ∧
    (∀ g h : R44.RigidMotion, g ∈ T.placements → h ∈ T.placements →
      R44.handedness g = R44.handedness h) ∧
    ∃ K : Hierarchy T, ∀ K' : Hierarchy T, K = K' :=
  ⟨R44.r44_einstein.1, fun T =>
    ⟨(R44.r44_einstein.2 T).1, (R44.r44_einstein.2 T).2,
      R44.tiling_homochiral ⟨⟩ T,
      ⟨(R44.carrierHierarchy ⟨⟩ T).toGeometric,
        R44.geometric_hierarchy_unique ⟨⟩ T _⟩⟩⟩

/-- The landed main theorem, with definition aliases. -/
theorem aperiodic : Nonempty Tiling ∧ ∀ T : Tiling,
    Periods T = {0} ∧ (Set.univ : Set (Symmetries T)).encard ≤ 24 :=
  R44.r44_einstein

#print axioms Space
#print axioms Solid
#print axioms Tiling
#print axioms Periods
#print axioms Symmetries
#print axioms Hierarchy
#print axioms chair44
#print axioms aperiodic
end Chair44
