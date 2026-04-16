(spec
  (type TypeSpec Int (>= 0))
  (type FuncSpec Int (>= 0))
  (type ConstraintSpec Int (>= 0))

  (func refines
    (input (f FuncSpec) (g FuncSpec))
    (output Bool)
    (pre (>= f 0))
    (pre (>= g 0)))

  (func testSet
    (input (spec FuncSpec))
    (output Int)
    (pre (>= spec 0))
    (post (>= result 0))))
