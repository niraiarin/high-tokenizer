(spec
  (type StepIndex Int (>= 1))
  (type InformationGain Int (>= 0))
  (type ViolationDensity Int (>= 0))
  (type Threshold Int (>= 0))

  (func computeInformationGain
    (input (step StepIndex))
    (output InformationGain)
    (pre (>= step 1))
    (post (>= result 0)))

  (func computeViolationDensity
    (input (step StepIndex) (constraintCount Int))
    (output ViolationDensity)
    (pre (>= step 1))
    (pre (>= constraintCount 0))
    (post (>= result 0)))

  (func optimalStop
    (input (threshold Threshold))
    (output StepIndex)
    (pre (>= threshold 0))
    (post (>= result 1)))

  (func detectOverthinking
    (input (currentStep StepIndex) (optimalStep StepIndex))
    (output Int)
    (pre (>= currentStep 1))
    (pre (>= optimalStep 1))
    (post (>= result 0))))
