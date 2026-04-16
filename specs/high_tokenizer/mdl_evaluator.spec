(spec
  (type MDLScore Float (>= 0))
  (type CandidateCount Int (>= 0))
  (type RankPosition Int (>= 1))

  (func score_candidate
    (input (source_cost Float) (candidate_cost Float) (violation_penalty Float))
    (output MDLScore)
    (pre (>= source_cost 0))
    (pre (>= candidate_cost 0))
    (pre (>= violation_penalty 0))
    (post (>= result 0)))

  (func rank_candidates
    (input (candidate_count CandidateCount))
    (output RankPosition)
    (pre (>= candidate_count 1))
    (post (>= result 1))
    (post (<= result candidate_count))))
