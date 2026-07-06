from core.dependencies import (
    get_matcher,
    get_recommender,
)

from core.pipeline import RecommendationPipeline

from download_dataset import download_dataset


class RecommendationEngine:

    def __init__(self):

        download_dataset()

        self.pipeline = RecommendationPipeline(
            matcher=get_matcher(),
            recommender=get_recommender(),
        )

    def recommend(
        self,
        zip_path,
    ):

        return self.pipeline.recommend(
            zip_path
        )