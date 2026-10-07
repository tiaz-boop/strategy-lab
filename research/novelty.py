def novelty_score(dna, known_hashes):
    return 1.0 if dna.hash() not in known_hashes else 0.0
