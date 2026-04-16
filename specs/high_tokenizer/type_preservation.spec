(spec
  (type ConceptId Int (>= 0))
  (type DepthBound Int (>= 0))
  (type CompressionRatio Int (>= 2))

  (func checkTypePreservation
    (input (conceptId ConceptId) (constraintCount Int))
    (output Int)
    (pre (>= conceptId 0))
    (pre (>= constraintCount 0))
    (post (>= result 0))
    (post (<= result 1)))

  (func computeExpansionDepth
    (input (complexity Int) (compressionRatio CompressionRatio))
    (output DepthBound)
    (pre (>= complexity 1))
    (pre (>= compressionRatio 2))
    (post (>= result 0)))

  (func checkCompositional
    (input (concept1 ConceptId) (concept2 ConceptId))
    (output Int)
    (pre (>= concept1 0))
    (pre (>= concept2 0))
    (post (>= result 0))
    (post (<= result 1))))
