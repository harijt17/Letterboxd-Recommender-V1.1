from matching.movie_matcher import MovieMatcher
from recommendation.movie_repository import MovieRepository
from recommendation.recommender import Recommender


# ==========================================================
# Global Objects
# ==========================================================

_repository = None

_recommender = None

_matcher = None


# ==========================================================
# Repository
# ==========================================================

def get_repository():

    global _repository

    if _repository is None:

        print("=" * 60)
        print("Loading Movie Repository...")
        print("=" * 60)

        _repository = MovieRepository()

    return _repository

# ==========================================================
# Movie Matcher
# ==========================================================

def get_matcher():

    global _matcher

    if _matcher is None:

        print("=" * 60)
        print("Initializing Movie Matcher...")
        print("=" * 60)

        _matcher = MovieMatcher(

            movies_df=get_repository().movies

        )

    return _matcher

# ==========================================================
# Recommender
# ==========================================================

def get_recommender():

    global _recommender

    if _recommender is None:

        print("=" * 60)
        print("Initializing Recommender...")
        print("=" * 60)

        _recommender = Recommender(

            repository=get_repository()

        )

    return _recommender