from core.dependencies import (
    get_matcher,
    get_recommender,
)

from core.pipeline import RecommendationPipeline
from core.session_manager import SessionManager
from download_dataset import download_dataset


class RecommendationEngine:

    def __init__(self):

        download_dataset()

        self.session_manager = SessionManager()

        self.pipeline = RecommendationPipeline(
            matcher=get_matcher(),
            recommender=get_recommender(),
            session_manager=self.session_manager
        )

    def recommend(self, zip_path):

        session_id, _ = self.session_manager.create_session()

        summary = self.pipeline.run(
            zip_file=zip_path,
            session_id=session_id
        )

        recommendations = self.session_manager.load_object(
            session_id,
            "recommendations.pkl"
        )

        summary["recommendations"] = recommendations

        return summary