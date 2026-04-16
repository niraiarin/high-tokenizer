(spec
  (type TypeId Int (>= 0))
  (type SubtypeResult Int (>= 0))
  (type SubtypeResult Int (<= 1))

  (func infer_term_type
    (input (term_id TypeId) (context_size Int))
    (output TypeId)
    (pre (>= term_id 0))
    (pre (>= context_size 0))
    (post (>= result 0)))

  (func validate_assignment
    (input (term_id TypeId) (expected_type TypeId))
    (output SubtypeResult)
    (pre (>= term_id 0))
    (pre (>= expected_type 0))
    (post (>= result 0))
    (post (<= result 1)))

  (func is_subtype
    (input (actual TypeId) (expected TypeId))
    (output SubtypeResult)
    (pre (>= actual 0))
    (pre (>= expected 0))
    (post (>= result 0))
    (post (<= result 1))))
