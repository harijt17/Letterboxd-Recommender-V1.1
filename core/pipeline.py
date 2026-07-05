from ingestion.zip_extractor import ZipExtractor
from ingestion.export_loader import ExportLoader
import time
from matching.movie_matcher import MovieMatcher

from profiling.profile_builder import ProfileBuilder

from recommendation.recommender import Recommender


class RecommendationPipeline:

    def __init__(
        self,
        matcher,
        recommender,
        session_manager
    ):

        self.matcher = matcher

        self.recommender = recommender

        self.session_manager = session_manager

        self.extractor = ZipExtractor()

        self.profile_builder = ProfileBuilder()



    # =====================================================
    # Run Pipeline
    # =====================================================

    def run(
        self,
        zip_file,
        session_id
    ):


        # ---------------------------------------------
        # Extract Export
        # ---------------------------------------------

        export_folder = self.extractor.extract(
            zip_file,
            session_id
        )

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
            top_k=20
        )

        # ---------------------------------------------
        # Save Results
        # ---------------------------------------------

        self.session_manager.save_object(
            session_id,
            "matched_movies.pkl",
            matched_movies
        )

        self.session_manager.save_object(
            session_id,
            "profile.pkl",
            profile
        )

        self.session_manager.save_object(
            session_id,
            "recommendations.pkl",
            recommendations
        )

        self.session_manager.save_metadata(
            session_id,
            {
                "session_id": session_id,
                "movies_loaded": len(movies),
                "movies_matched": len(matched_movies),
                "movies_unmatched": len(unmatched_movies)
            }
        )

        # ---------------------------------------------
        # Return Summary
        # ---------------------------------------------

        return {
            "movies_loaded": len(movies),
            "movies_matched": len(matched_movies),
            "movies_unmatched": len(unmatched_movies)
        }