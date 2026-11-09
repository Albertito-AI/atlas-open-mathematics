import Lean.Elab.Tactic.Omega

/-
Q0001: a known linear Diophantine solvability criterion.
All variables are integers. This file extends the teaching record without
changing the fixed four-statement pilot or its acceptance checker.
-/
namespace Atlas.IntegerCriterion

theorem necessary (p q x y : Int)
    (first : 2 * x + 3 * y = p) (second : -x + 4 * y = q) :
    11 ∣ p + 2 * q := by
  refine ⟨y, ?_⟩
  omega

theorem witness (p q k : Int) (divisible : p + 2 * q = 11 * k) :
    2 * (4 * k - q) + 3 * k = p ∧ -(4 * k - q) + 4 * k = q := by
  omega

theorem solvability_iff (p q : Int) :
    (∃ x y : Int, 2 * x + 3 * y = p ∧ -x + 4 * y = q) ↔
      11 ∣ p + 2 * q := by
  constructor
  · intro solution
    cases solution with
    | intro x rest =>
      cases rest with
      | intro y equations =>
        exact necessary p q x y equations.1 equations.2
  · intro divisible
    cases divisible with
    | intro k equation =>
      exact ⟨4 * k - q, k, witness p q k equation⟩

theorem unique_solution (p q x y u v : Int)
    (first_xy : 2 * x + 3 * y = p) (second_xy : -x + 4 * y = q)
    (first_uv : 2 * u + 3 * v = p) (second_uv : -u + 4 * v = q) :
    x = u ∧ y = v := by
  omega

end Atlas.IntegerCriterion

#print axioms Atlas.IntegerCriterion.necessary
#print axioms Atlas.IntegerCriterion.witness
#print axioms Atlas.IntegerCriterion.solvability_iff
#print axioms Atlas.IntegerCriterion.unique_solution
