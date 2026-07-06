from ingestion.zip_extractor import ZipExtractor
from ingestion.export_loader import ExportLoader

from profiling.profile_builder import ProfileBuilder


class RecommendationPipeline:

    def __init__(
        self,
        matcher,
        recommender,
    ):

        self.matcher = matcher

        self.recommender = recommender

        self.extractor = ZipExtractor()

        self.profile_builder = ProfileBuilder()

    # =====================================================
    # Recommend
    # =====================================================

    def recommend(
        self,
        zip_file,
    ):

        # ---------------------------------------------
        # Extract Export
        # ---------------------------------------------

        export_folder = self.extractor.extract(zip_file)
        
        # ---------------------------------------------
        # Load Movies
        # ---------------------------------------------

        loader = ExportLoader(export_folder)

        movies = loader.load()

        # ---------------------------------------------
        # Match Movies
        # ---------------------------------------------

        matched_movies, unmatched_movies = (
            self.matcher.match_movies(movies)
        )

        # ---------------------------------------------
        # Build Profile
        # ---------------------------------------------

        profile = self.profile_builder.build_profile(
            matched_movies
        )

        # ---------------------------------------------
        # Watched IDs
        # ---------------------------------------------

        watched_ids = {
            movie["id"]
            for movie in matched_movies
        }

        # ---------------------------------------------
        # Recommendations
        # ---------------------------------------------

        recommendations = self.recommender.recommend(
            profile=profile,
            matched_movies=matched_movies,
            watched_ids=watched_ids,
            top_k=20,
        )

        # ---------------------------------------------
        # Return Everything
        # ---------------------------------------------

        return {
            "movies_loaded": len(movies),
            "movies_matched": len(matched_movies),
            "movies_unmatched": len(unmatched_movies),
            "matched_movies": matched_movies,
            "profile": profile,
            "recommendations": recommendations,
        }