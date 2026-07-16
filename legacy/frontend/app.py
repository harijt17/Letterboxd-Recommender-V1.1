import streamlit as st

from legacy.frontend.api_client import (
    upload_export,
    get_recommendations
)

st.set_page_config(
    page_title="Letterboxd Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Letterboxd Movie Recommender")

st.write(
    "Upload your Letterboxd export ZIP to receive personalized movie recommendations."
)

uploaded_file = st.file_uploader(
    "Choose your Letterboxd export",
    type=["zip"]
)

if uploaded_file:

    if st.button("Generate Recommendations"):

        with st.spinner("Analyzing your profile..."):

            upload_result = upload_export(
                uploaded_file
            )

            session_id = upload_result[
                "session_id"
            ]

            recommendations = get_recommendations(
                session_id
            )

        st.success("Recommendations generated!")

        movies = recommendations["recommendations"]

        st.subheader("🎬 Top Recommendations")

        for movie in movies:

            with st.container(border=True):

                col1, col2 = st.columns([1, 3])

                with col1:
                    poster = None

                    if movie.get("poster_path"):
                        poster = (
                            "https://image.tmdb.org/t/p/w342"
                            + movie["poster_path"]
                        )

                    if poster:
                        st.image(
                            poster,
                            width="stretch"
                        )
                    else:
                        st.image(
                            "https://placehold.co/342x513?text=No+Poster",
                            width="stretch"
                        )
                with col2:

                    st.markdown(
                        f"### {movie['title'].title()} ({movie['year']})"
                    )

                    st.write(
                        f"**Director:** {movie['director'].title()}"
                    )

                    st.write(
                        f"**Genres:** {movie['genres'].title()}"
                    )

                    st.metric(
                        "Recommendation Score",
                        f"{movie['recommendation_score']:.4f}"
                    )

                    st.progress(
                        float(movie["recommendation_score"])
                    )