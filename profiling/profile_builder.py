from collections import defaultdict

from profiling.profile import UserProfile


class ProfileBuilder:

    def __init__(self):

        self.profile = UserProfile()

    # =====================================================
    # Rating Weight
    # =====================================================

    def rating_weight(
        self,
        rating
    ):

        if rating is None:
            return 1.0

        if rating >= 5.0:
            return 5.0

        if rating >= 4.5:
            return 4.5

        if rating >= 4.0:
            return 4.0

        if rating >= 3.5:
            return 3.0

        if rating >= 3.0:
            return 2.0

        if rating >= 2.5:
            return 1.25

        if rating >= 2.0:
            return 1.0

        return 0.5

    # =====================================================
    # Split Helper
    # =====================================================

    def split_values(
        self,
        value
    ):

        if value is None:
            return []

        if value == "":
            return []

        separators = [
            ",",
            "-",
            "|"
        ]

        values = [str(value)]

        for separator in separators:

            new_values = []

            for item in values:

                new_values.extend(
                    item.split(separator)
                )

            values = new_values

        cleaned = []

        for value in values:

            value = value.strip()

            if value:

                cleaned.append(value)

        return cleaned

    # =====================================================
    # Add Weighted Features
    # =====================================================

    def add_feature(
        self,
        container,
        values,
        weight
    ):

        for value in values:

            container[value] += weight

    # =====================================================
    # Runtime Statistics
    # =====================================================

    def runtime_statistics(
        self,
        runtimes
    ):

        runtimes = [

            runtime

            for runtime in runtimes

            if runtime is not None

            and runtime > 0

        ]

        if not runtimes:

            return {

                "average": 0,

                "minimum": 0,

                "maximum": 0

            }

        return {

            "average":

                round(

                    sum(runtimes)

                    / len(runtimes)

                ),

            "minimum":

                min(runtimes),

            "maximum":

                max(runtimes)

        }
        # =====================================================
    # Build User Profile
    # =====================================================

    def build_profile(
        self,
        matched_movies
    ):

        profile = UserProfile()

        profile.genres = defaultdict(float)
        profile.directors = defaultdict(float)
        profile.cast = defaultdict(float)
        profile.writers = defaultdict(float)
        profile.keywords = defaultdict(float)
        profile.countries = defaultdict(float)
        profile.languages = defaultdict(float)
        profile.decades = defaultdict(float)

        runtimes = []
        ratings = []

        for movie in matched_movies:

            weight = self.rating_weight(
                movie.get("rating")
            )

            rating = movie.get("rating")

            if rating is not None:
                ratings.append(rating)

            self.add_feature(
                profile.genres,
                self.split_values(
                    movie.get("genres")
                ),
                weight
            )

            self.add_feature(
                profile.directors,
                self.split_values(
                    movie.get("director")
                ),
                weight
            )

            self.add_feature(
                profile.cast,
                self.split_values(
                    movie.get("cast")
                ),
                weight
            )

            self.add_feature(
                profile.writers,
                self.split_values(
                    movie.get("writers")
                ),
                weight
            )

            self.add_feature(
                profile.keywords,
                self.split_values(
                    movie.get("keywords")
                ),
                weight
            )

            self.add_feature(
                profile.countries,
                self.split_values(
                    movie.get(
                        "production_countries"
                    )
                ),
                weight
            )

            self.add_feature(
                profile.languages,
                self.split_values(
                    movie.get(
                        "spoken_languages"
                    )
                ),
                weight
            )

            year = movie.get("year")

            if year:

                decade = (year // 10) * 10

                profile.decades[
                    decade
                ] += weight

            runtime = movie.get("runtime")

            if runtime is not None and runtime >= 30:

                runtimes.append(runtime)

        profile.runtime = self.runtime_statistics(
            runtimes
        )

        profile.movie_count = len(
            matched_movies
        )

        if ratings:

            profile.average_rating = round(
                sum(ratings) / len(ratings),
                2
            )
            
            
        profile.genres = self.normalize_scores(profile.genres)

        profile.directors = self.normalize_scores(profile.directors)

        profile.cast = self.normalize_scores(profile.cast)

        profile.writers = self.normalize_scores(profile.writers)

        profile.keywords = self.normalize_scores(profile.keywords)

        profile.countries = self.normalize_scores(profile.countries)

        profile.languages = self.normalize_scores(profile.languages)

        profile.decades = self.normalize_scores(profile.decades)

        print("Genres:", len(profile.genres))
        print("Directors:", len(profile.directors))
        print("Cast:", len(profile.cast))
        print("Keywords:", len(profile.keywords))

        profile.directors = self.prune_scores(profile.directors, 0.20)
        profile.cast = self.prune_scores(profile.cast, 0.20)
        profile.keywords = self.prune_scores(profile.keywords, 0.20)

        print("After pruning")
        print("Genres:", len(profile.genres))
        print("Directors:", len(profile.directors))
        print("Cast:", len(profile.cast))
        print("Keywords:", len(profile.keywords))
        return profile
    
    def normalize_scores(self, scores):

        if not scores:
            return scores

        maximum = max(scores.values())

        if maximum == 0:
            return scores

        return {

            key: round(value / maximum, 4)

            for key, value in scores.items()

        }
    
    def prune_scores(self, scores, threshold=0.2):

        return {
            key: value
            for key, value in scores.items()
            if value >= threshold
        }

    # =====================================================
    # Convert Profile to Dictionary
    # =====================================================

    def to_dict(self,profile):

        return {

            "movie_count":
                profile.movie_count,

            "average_rating":
                profile.average_rating,

            "genres":
                dict(profile.genres),

            "directors":
                dict(profile.directors),

            "cast":
                dict(profile.cast),

            "writers":
                dict(profile.writers),

            "keywords":
                dict(profile.keywords),

            "countries":
                dict(profile.countries),

            "languages":
                dict(profile.languages),

            "decades":
                dict(profile.decades),

            "runtime":
                profile.runtime

        }