"""Auto-generated implementation skeletons from DSL specification.

TDD: all functions raise NotImplementedError.
Run auto-generated tests, then implement until green.
"""

from __future__ import annotations

# Type: StepIndex = Int with constraints: (>= 1)
type StepIndex = int

# Type: InformationGain = Int with constraints: (>= 0)
type InformationGain = int

# Type: ViolationDensity = Int with constraints: (>= 0)
type ViolationDensity = int

# Type: Threshold = Int with constraints: (>= 0)
type Threshold = int


def computeInformationGain(step: StepIndex) -> InformationGain:
    """Auto-generated skeleton for computeInformationGain.

    Pre-conditions:
        (>= step 1)
    Post-conditions:
        (>= result 0)

    Computes the marginal information gain at a given inference step.
    Per spec 5.5.6: delta_I(s) = I(X; E_s(T)) - I(X; E_{s-1}(T))
    Information gain decreases as step increases (diminishing returns).
    """
    # Information gain is inversely proportional to step number.
    # At step 1, gain is maximal. As steps increase, gain diminishes.
    # Using integer division: gain = max(0, 1/step) approximated as
    # a decreasing function.
    if step <= 0:
        return 0
    # Simple model: gain decreases. For integer result, use floor(100/step).
    return max(0, 100 // step)


def computeViolationDensity(step: StepIndex, constraintCount: int) -> ViolationDensity:
    """Auto-generated skeleton for computeViolationDensity.

    Pre-conditions:
        (>= step 1)
        (>= constraintCount 0)
    Post-conditions:
        (>= result 0)

    Computes the constraint violation density at a given step.
    Per spec 5.5.6: V(s) = |{c in Gamma | E_s(T) not models c}| / |Gamma|
    Violation density tends to increase beyond the optimal step.
    """
    # When there are no constraints, there are no violations.
    if constraintCount == 0:
        return 0
    # Violation density increases with step (beyond optimal, more violations).
    # Simple model: violations grow linearly with step, bounded by constraintCount.
    return min(step, constraintCount)


def optimalStop(threshold: Threshold) -> StepIndex:
    """Auto-generated skeleton for optimalStop.

    Pre-conditions:
        (>= threshold 0)
    Post-conditions:
        (>= result 1)

    Finds the optimal stopping step s* where information gain
    drops below the threshold.
    Per spec 5.5.6: s* = min{s >= 1 | delta_I(s) < delta_I}
    """
    # Find the first step where information gain < threshold.
    # computeInformationGain(step) = 100 // step
    # We need 100 // step < threshold
    # If threshold is 0, gain never goes below 0 for finite steps,
    # but we need result >= 1, so return a large step.
    if threshold <= 0:
        return 1
    # 100 // step < threshold  =>  step > 100 / threshold
    # smallest integer step > 100/threshold
    step = (100 // threshold) + 1
    return max(1, step)


def detectOverthinking(currentStep: StepIndex, optimalStep: StepIndex) -> int:
    """Auto-generated skeleton for detectOverthinking.

    Pre-conditions:
        (>= currentStep 1)
        (>= optimalStep 1)
    Post-conditions:
        (>= result 0)

    Detects overthinking (over-expansion beyond optimal step).
    Per spec 5.5.6: overthinking occurs when:
      (i) s > s*
      (ii) delta_I(s) < delta_I
      (iii) V(s) > V(s*)
    Returns the degree of overthinking (0 = no overthinking).
    """
    # Overthinking degree = max(0, currentStep - optimalStep)
    # If current step exceeds optimal, the excess is the overthinking amount.
    return max(0, currentStep - optimalStep)
