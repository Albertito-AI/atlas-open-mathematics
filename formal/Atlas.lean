import Lean.Elab.Tactic.Omega

/-
Known supporting algebra for the teaching pilot, over integers.
These statements do not certify the Python implementation or arbitrary matrices.
-/
namespace Atlas

theorem two_equation_consequences (x y s d : Int)
    (sum_eq : x + y = s) (difference_eq : x - y = d) :
    2 * x = s + d ∧ 2 * y = s - d := by
  omega

theorem two_equation_unique (x y u v s d : Int)
    (sum_xy : x + y = s) (difference_xy : x - y = d)
    (sum_uv : u + v = s) (difference_uv : u - v = d) :
    x = u ∧ y = v := by
  omega

theorem concrete_solution (x y : Int) :
    (x + y = 11 ∧ x - y = 3) ↔ (x = 7 ∧ y = 4) := by
  omega

theorem incompatible_parity :
    ¬ ∃ x y : Int, x + y = 10 ∧ x - y = 3 := by
  omega

end Atlas

#print axioms Atlas.two_equation_consequences
#print axioms Atlas.two_equation_unique
#print axioms Atlas.concrete_solution
#print axioms Atlas.incompatible_parity
