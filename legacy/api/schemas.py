from pydantic import BaseModel
from typing import List, Optional


# ==========================================================
# Upload Response
# ==========================================================

class UploadResponse(BaseModel):

    session_id: str

    movies_loaded: int

    movies_matched: int

    movies_unmatched: int


# ==========================================================
# Recommendation
# ==========================================================

class Recommendation(BaseModel):

    title: str

    year: int

    recommendation_score: float

    metadata_score: float

    content_similarity: float

    genres: str

    director: str

    poster_path: Optional[str] = None


# ==========================================================
# Recommendation Response
# ==========================================================

class RecommendationResponse(BaseModel):

    recommendations: List[Recommendation]

class SessionResponse(BaseModel):

    session_id: str

    movies_loaded: int

    movies_matched: int

    movies_unmatched: int

    created_at: str