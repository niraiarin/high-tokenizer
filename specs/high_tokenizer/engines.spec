(spec
  (type CandidateCount Int (>= 0))
  (type ExpansionSize Int (>= 0))
  (type InputSize Int (>= 1))

  (func abstract
    (input (input_size InputSize) (context_size Int))
    (output CandidateCount)
    (pre (>= input_size 1))
    (pre (>= context_size 0))
    (post (>= result 0)))

  (func expand
    (input (term_id Int) (granularity Int))
    (output ExpansionSize)
    (pre (>= term_id 0))
    (pre (>= granularity 1))
    (post (>= result 0))))
