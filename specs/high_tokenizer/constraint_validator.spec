(spec
  (type ValidationScore Int (>= 0))
  (type ValidationScore Int (<= 1))
  (type ViolationCount Int (>= 0))

  (func validate_term
    (input (term_id Int) (context_size Int))
    (output ValidationScore)
    (pre (>= term_id 0))
    (pre (>= context_size 0))
    (post (>= result 0))
    (post (<= result 1)))

  (func validate_expansion
    (input (expansion_size Int) (context_size Int))
    (output ViolationCount)
    (pre (>= expansion_size 0))
    (pre (>= context_size 0))
    (post (>= result 0))))
