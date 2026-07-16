from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from legacy.api.schemas import (
    UploadResponse,
    RecommendationResponse,
    SessionResponse
)

from legacy.api.dependencies import (
    get_matcher,
    get_recommender
)

from legacy.api.pipeline import RecommendationPipeline

from legacy.api.session_manager import SessionManager


router = APIRouter()

session_manager = SessionManager()


# ==========================================================
# Health
# ==========================================================

@router.get("/health")
def health():

    return {

        "status": "ok"

    }

# ==========================================================
# Get Recommendations
# ==========================================================

@router.get(
    "/recommend/{session_id}",
    response_model=RecommendationResponse
)
def get_recommendations(
    session_id: str
):

    recommendations = session_manager.load_object(

        session_id,

        "recommendations.pkl"

    )

    return RecommendationResponse(
        recommendations=recommendations.to_dict(orient="records")
        )

# ==========================================================
# Session Information
# ==========================================================

@router.get(
    "/session/{session_id}",
    response_model=SessionResponse
)
def get_session(
    session_id: str
):

    metadata = session_manager.load_metadata(
        session_id
    )

    return SessionResponse(
        **metadata
    )

# ==========================================================
# Upload Letterboxd Export
# ==========================================================

@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_export(

    file: UploadFile = File(...)

):

    # ---------------------------------------------
    # Validate File
    # ---------------------------------------------

    if not file.filename.endswith(".zip"):

        raise HTTPException(

            status_code=400,

            detail="Please upload a ZIP export."

        )

    # ---------------------------------------------
    # Create Session
    # ---------------------------------------------

    session_id, _ = (

        session_manager.create_session()

    )

    # ---------------------------------------------
    # Save ZIP
    # ---------------------------------------------

    zip_path = session_manager.save_upload(

        session_id,

        file

    )

    # ---------------------------------------------
    # Run Recommendation Pipeline
    # ---------------------------------------------

    pipeline = RecommendationPipeline(
        matcher=get_matcher(),
        recommender=get_recommender(),
        session_manager=session_manager
    )

    result = pipeline.run(

        zip_file=zip_path,

        session_id=session_id

    )

    # ---------------------------------------------
    # Response
    # ---------------------------------------------

    return UploadResponse(

        session_id=session_id,

        movies_loaded=result["movies_loaded"],

        movies_matched=result["movies_matched"],

        movies_unmatched=result["movies_unmatched"]

    )