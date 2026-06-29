import pandas as pd


class RecommendationRanker:

    def __init__(self):
        pass

    # =====================================================
    # Rank Recommendations
    # =====================================================

    def rank(
        self,
        scored_movies,
        top_k=100
    ):

        ranked = scored_movies.sort_values(
            by="recommendation_score",
            ascending=False
        ).reset_index(drop=True)

        return ranked.head(top_k)

    # =====================================================
    # Top N Helper
    # =====================================================

    def top_n(
        self,
        ranked_movies,
        n=20
    ):

        return ranked_movies.head(n).reset_index(
            drop=True
        )

    # =====================================================
    # Get Score Statistics
    # =====================================================

    def score_statistics(
        self,
        ranked_movies
    ):

        if ranked_movies.empty:

            return {
                "count": 0,
                "highest": 0,
                "lowest": 0,
                "average": 0
            }

        return {

            "count": len(ranked_movies),

            "highest": round(
                ranked_movies[
                    "recommendation_score"
                ].max(),
                4
            ),

            "lowest": round(
                ranked_movies[
                    "recommendation_score"
                ].min(),
                4
            ),

            "average": round(
                ranked_movies[
                    "recommendation_score"
                ].mean(),
                4
            )

        }