(spec
  (type SExprInput String (>= 1))
  (type SExprOutput Int (>= 0))
  (type SpecASTOutput Int (>= 0))

  (func parseSExpr
    (input (source SExprInput))
    (output SExprOutput)
    (pre (>= source 1))
    (post (>= result 0)))

  (func parseSpec
    (input (sexpr SExprOutput))
    (output SpecASTOutput)
    (pre (>= sexpr 0))
    (post (>= result 0))))
