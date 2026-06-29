from dataclasses import dataclass, field


@dataclass
class UserProfile:

    genres: dict = field(default_factory=dict)

    directors: dict = field(default_factory=dict)

    cast: dict = field(default_factory=dict)

    writers: dict = field(default_factory=dict)

    keywords: dict = field(default_factory=dict)

    countries: dict = field(default_factory=dict)

    languages: dict = field(default_factory=dict)

    decades: dict = field(default_factory=dict)

    runtime: dict = field(default_factory=dict)

    movie_count: int = 0

    average_rating: float = 0.0