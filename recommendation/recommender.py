from recommendation.candidate_generator import CandidateGenerator
from recommendation.scorer import RecommendationScorer
from recommendation.ranker import RecommendationRanker
from recommendation.diversity import DiversityFilter
from recommendation.content_similarity import ContentSimilarity
import time
class Recommender:

    def __init__(self, repository):

        self.repository = repository

        self.candidate_generator = CandidateGenerator(
            repository
        )

        self.scorer = RecommendationScorer()

        self.content_similarity = ContentSimilarity()

        self.ranker = RecommendationRanker()

        self.diversity = DiversityFilter()
    # =====================================================
    # Generate Recommendations
    # =====================================================

    def recommend(
        self,
        profile,
        matched_movies,
        watched_ids,
        top_k=20,
        candidate_pool=5000
    ):

        # ----------------------------------------------
        # Generate Candidate Movies
        # ----------------------------------------------
        start = time.perf_counter()

        candidates = self.candidate_generator.generate_candidates(
            profile=profile,
            watched_ids=watched_ids,
            top_k=candidate_pool
        )

        print(f"Candidate Generation: {time.perf_counter()-start:.2f}s")
        start = time.perf_counter()

        if candidates.empty:
            return []

        # ----------------------------------------------
        # Metadata Score
        # ----------------------------------------------

        scored = self.scorer.score(
            candidates=candidates,
            profile=profile
        )
        print(f"Metadata Scoring: {time.perf_counter()-start:.2f}s")
        start = time.perf_counter()
        # ----------------------------------------------
        # Content Similarity
        # ----------------------------------------------

        scored = self.content_similarity.compute_similarity(
            candidates=scored,
            matched_movies=matched_movies
        )
        print(f"Content Similarity: {time.perf_counter()-start:.2f}s")
        start = time.perf_counter()
        # ----------------------------------------------
        # Final Recommendation Score
        # ----------------------------------------------

        scored["recommendation_score"] = (

            scored["metadata_score"] * 0.70 +

            scored["content_similarity"] * 0.30

        ).round(4)

        # ----------------------------------------------
        # Rank Movies
        # ----------------------------------------------

        ranked = self.ranker.rank(
            scored_movies=scored,
            top_k=candidate_pool
        )
        print(f"Ranking: {time.perf_counter()-start:.2f}s")
        start = time.perf_counter()
        
        # ----------------------------------------------
        # Apply Diversity Filter
        # ----------------------------------------------

        recommendations = self.diversity.apply(
            ranked_movies=ranked,
            top_k=top_k
        )
        print(f"Diversity Filtering: {time.perf_counter()-start:.2f}s")

        return recommendations

    # =====================================================
    # Full Recommendation Pipeline (Debug)
    # =====================================================

    def debug(
        self,
        profile,
        watched_ids,
        top_k=20,
        candidate_pool=5000
    ):

        candidates = self.candidate_generator.generate_candidates(
            profile,
            watched_ids,
            candidate_pool
        )

        scored = self.scorer.score(
            candidates,
            profile
        )

        ranked = self.ranker.rank(
            scored,
            candidate_pool
        )

        final = self.diversity.apply(
            ranked,
            top_k
        )

        return {
            "candidate_count": len(candidates),
            "scored_count": len(scored),
            "ranked_count": len(ranked),
            "final_count": len(final),
            "recommendations": final
        }