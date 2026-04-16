(spec
  (type ConceptId Int (>= 0))
  (type FeatureCount Int (>= 0))
  (type RelationCount Int (>= 0))
  (type Confidence Float (>= 0))
  (type Confidence Float (<= 1))

  (type SymbolLength Float (>= 0))
  (type StructuralCost Float (>= 0))
  (type DependencyCost Float (>= 0))
  (type TotalCost Float (>= 0))

  (type ModelCost Float (>= 0))
  (type DataCost Float (>= 0))
  (type PenaltyCost Float (>= 0))
  (type MDLTotalCost Float (>= 0)))
