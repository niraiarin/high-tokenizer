(spec
  (type ConceptCount Int (>= 1))
  (type ComplexityCost Float (>= 0))
  (type Weight Float (>= 0))
  (type Weight Float (<= 1))

  (func estimate_concepts
    (input (concept_count ConceptCount) (context_size Int))
    (output ComplexityCost)
    (pre (>= concept_count 1))
    (pre (>= context_size 0))
    (post (>= result 0)))

  (func estimate_term
    (input (term_length Int) (type_complexity Int))
    (output ComplexityCost)
    (pre (>= term_length 0))
    (pre (>= type_complexity 0))
    (post (>= result 0))))
