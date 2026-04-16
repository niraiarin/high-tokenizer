(spec
  (type SExprInput String (>= 1))
  (type SExprOutput Int (>= 0))

  (func parse_sexpr
    (input (source SExprInput))
    (output SExprOutput)
    (pre (>= source 1))
    (post (>= result 0))))
