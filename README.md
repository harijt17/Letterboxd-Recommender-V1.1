# 🎬 Letterboxd Recommender

> **A standalone Windows desktop application that generates personalized movie recommendations by analyzing your Letterboxd viewing history.**

Letterboxd Recommender is a **content-based movie recommendation system** that builds a personalized movie taste profile from your Letterboxd export. Instead of recommending movies based on what similar users watch, the application learns **your individual movie preferences** by analyzing the films you've watched, your ratings, reviews, and rich movie metadata.

The recommendation engine combines **metadata similarity**, **TF-IDF content similarity**, and a **weighted scoring pipeline** to recommend movies that closely align with your unique taste.

The application is distributed as a **native Windows desktop application** with a one-click installer, automatic runtime setup, and no Python installation required.

---

## ✨ Features

### 🎬 Personalized Movie Recommendations

Generate recommendations directly from your Letterboxd export.

- Supports official Letterboxd export (.zip)
- No API keys required
- No account login required
- Completely offline after the initial runtime setup

---

### 🧠 Personalized Taste Profiling

Builds a unique movie preference profile using:

- ⭐ Movie Ratings
- 🎭 Genres
- 🎬 Directors
- 🎥 Cast Members
- ✍️ Writers
- 🏷️ Keywords
- 🌍 Production Countries
- 🗣️ Spoken Languages
- 📅 Release Decades
- ⏱️ Runtime Preferences

---

### 🔍 Intelligent Movie Matching

Automatically matches movies from your Letterboxd export using:

- Exact title matching
- Release year validation
- RapidFuzz fuzzy matching
- Automatic duplicate handling

---

### 🎯 Content-Based Recommendation Engine

Recommendations are generated using a multi-stage pipeline that includes:

- Candidate Generation
- Metadata Similarity
- TF-IDF Content Similarity
- Weighted Recommendation Scoring
- Diversity Filtering

---

### 💻 Desktop Application

- Native Windows desktop application
- Professional Windows installer
- Standalone executable
- No Python installation required
- Automatic runtime asset download
- Automatic runtime cleanup
- One-click installation

---

## 🚀 Installation

### Windows (Recommended)

1. Download the latest installer from the **Releases** page.
2. Run the installer.
3. Launch **Letterboxd Recommender**.
4. During the first launch, the application automatically downloads the required runtime assets.
5. Upload your Letterboxd export (`.zip`).
6. Generate personalized recommendations.

> **Note**
>
> Runtime assets are downloaded only once and stored locally for future use.

---

## ⚡ Quick Start

```text
Download Installer
        │
        ▼
Install Application
        │
        ▼
Launch Letterboxd Recommender
        │
        ▼
Automatic Runtime Setup
        │
        ▼
Upload Letterboxd Export (.zip)
        │
        ▼
Generate Recommendations
```

---

## 🆕 Version 2 Highlights

Version 2 introduces a complete desktop application with a redesigned recommendation pipeline and a significantly improved user experience.

### Highlights

- ✅ Native Windows desktop application
- ✅ One-click Windows installer
- ✅ Standalone executable distribution
- ✅ Automatic runtime asset download
- ✅ Automatic runtime cleanup
- ✅ Improved recommendation pipeline
- ✅ Faster application startup
- ✅ Better modular project architecture
- ✅ Professional packaging using Nuitka and Inno Setup

---

## 🔒 Privacy

Your Letterboxd export is processed **entirely on your own computer**.

The application does **not** upload your viewing history, ratings, reviews, or personal data to any external server. All recommendation generation happens locally on your machine.


---

# 🏗️ Application Workflow

The application follows a fully automated workflow from installation to recommendation generation.

```text
Start Application
        │
        ▼
Initialize Runtime Environment
        │
        ▼
Clean Temporary Runtime Files
        │
        ▼
Verify Runtime Assets
        │
        ▼
Download Missing Assets (First Launch Only)
        │
        ▼
Launch Desktop Application
        │
        ▼
Upload Letterboxd Export (.zip)
        │
        ▼
Extract Export
        │
        ▼
Match Movies
        │
        ▼
Generate User Profile
        │
        ▼
Generate Recommendations
        │
        ▼
Display Results
```

---

# 🧠 Recommendation Pipeline

The recommendation engine is built as a modular multi-stage pipeline. Each stage has a dedicated responsibility, making the system easier to maintain, optimize, and extend.

```text
Letterboxd Export (.zip)
            │
            ▼
      Export Loader
            │
            ▼
      Movie Matcher
            │
            ▼
     Profile Generator
            │
            ▼
   Candidate Generator
            │
            ▼
    Metadata Scoring
            │
            ▼
  Content Similarity
            │
            ▼
         Ranking
            │
            ▼
 Diversity Filtering
            │
            ▼
 Final Recommendations
```

---

# ⚙️ Recommendation Methodology

## 1. Export Loading

The application reads the official Letterboxd export and extracts the user's movie history.

Information extracted includes:

- Watched Movies
- Ratings
- Reviews
- Watch Dates
- Rewatch Information
- Tags

---

## 2. Movie Matching

Every movie from the Letterboxd export is matched against the processed movie dataset.

Matching strategy:

1. Exact Title Matching
2. Release Year Validation
3. RapidFuzz Fuzzy Matching
4. Automatic Duplicate Resolution

This process significantly improves matching accuracy while minimizing false positives.

---

## 3. User Profile Generation

Once the watched movies are matched, the application constructs a personalized movie taste profile.

Each watched movie contributes weighted preferences based on its rating.

The profile captures preferences across multiple metadata dimensions:

- Genres
- Directors
- Cast
- Writers
- Keywords
- Production Countries
- Spoken Languages
- Release Decades
- Runtime

Higher-rated movies contribute more strongly to the final preference profile.

---

## 4. Candidate Generation

Instead of comparing against the entire movie database, the recommendation engine first generates a focused pool of candidate movies.

Candidates are selected using metadata relationships derived from the user's profile, greatly reducing the search space while preserving recommendation quality.

Movies already watched by the user are automatically excluded.

---

## 5. Recommendation Scoring

Each candidate movie receives a weighted recommendation score based on multiple independent components.

### Metadata Similarity

Measures how closely a movie matches the user's learned metadata preferences.

### Content Similarity

Uses a TF-IDF representation of movie content to compare semantic similarity between watched movies and candidate movies.

### Final Recommendation Score

The metadata and content similarity scores are combined into a single recommendation score used for ranking.

---

## 6. Ranking & Diversity

The highest-scoring candidates are ranked before applying a diversity filter.

The diversity stage prevents recommendations from becoming overly repetitive by introducing variation while maintaining recommendation quality.

The final output is a ranked list of personalized movie recommendations tailored to the user's viewing history.

---

# 🖥️ System Architecture

The project follows a modular architecture that separates the desktop interface, recommendation engine, data processing, and runtime management into independent components.

```text
                 Desktop Application (NiceGUI)
                           │
                           ▼
                 Recommendation Engine
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Movie Repository    User Profile      Recommendation Pipeline
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                  Processed Movie Dataset
                           │
                           ▼
                 TF-IDF Content Similarity
```

---

# 📂 Runtime Data Management

The application separates permanent assets from temporary runtime files.

## Application Files

Installed under:

```text
Program Files/
└── Letterboxd Recommender/
```

Contains:

- Desktop application
- Python runtime
- Required libraries
- Application resources

---

## Runtime Assets

Stored under:

```text
%LOCALAPPDATA%/
└── Letterboxd Recommender/
```

Contains:

```text
processed/
    movies.parquet
    tfidf/
        matrix.npz
        vectorizer.joblib

uploads/
extracted/
raw/
```

### Runtime Behavior

- Processed assets are downloaded automatically during the first launch.
- Runtime assets are reused in future sessions.
- Temporary folders (`uploads`, `extracted`, and `raw`) are automatically cleaned each time the application starts.
- User recommendation data is never stored permanently after the application session ends.

---

# 📁 Project Structure

The project is organized into independent modules, each responsible for a specific stage of the recommendation pipeline or desktop application.

```text
Letterboxd-Recommender/

├── build/                 # Build scripts
├── config/                # Application configuration
├── core/                  # Recommendation engine orchestration
├── desktop/               # NiceGUI desktop application
├── ingestion/             # Letterboxd export loading
├── installer/             # Inno Setup installer
├── matching/              # Movie matching engine
├── preprocessing/         # Dataset preprocessing utilities
├── profiling/             # User profile generation
├── recommendation/        # Recommendation pipeline
├── utils/                 # Shared utilities

├── launcher.py            # Desktop application entry point
├── download_dataset.py    # Runtime dataset downloader
├── requirements.txt
└── README.md
```

---

# 📦 Dataset

The recommendation engine uses a processed movie metadata dataset built from the **Ultimate 1 Million Movies Dataset (TMDB + IMDb)**.

The processed runtime assets include:

- Movie Metadata Dataset (`movies.parquet`)
- TF-IDF Matrix (`matrix.npz`)
- TF-IDF Vectorizer (`vectorizer.joblib`)

These assets are **not stored inside the GitHub repository** because of their size.

Instead, they are hosted externally and downloaded automatically during the application's first launch.

This approach keeps the installer significantly smaller while allowing the recommendation engine to work completely offline after the initial setup.

---

# ⚡ Building From Source

## Clone the Repository

```bash
git clone https://github.com/harijt17/Letterboxd-Recommender.git

cd Letterboxd-Recommender
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python launcher.py
```

During the first launch, the application automatically downloads the required runtime assets.

---

# 🏗️ Building the Desktop Application

The project uses **Nuitka** to package the application into a standalone Windows executable.

Development build:

```powershell
.\build\build_dev.ps1
```

Release build:

```powershell
.\build\build_release.ps1
```

Clean previous build:

```powershell
.\build\clean.ps1
```

The generated application is located in:

```text
dist/
└── launcher.dist/
```

---

# 📀 Windows Installer

The desktop installer is built using **Inno Setup**.

Installer configuration:

```text
installer/
└── Letterboxd_Recommender.iss
```

The generated installer is placed inside:

```text
release/
└── Letterboxd_Recommender_Setup_v2.0.0.exe
```

The installer provides:

- Professional installation wizard
- Start Menu shortcut
- Optional Desktop shortcut
- Automatic uninstaller
- Standalone desktop application

---

# 🛠️ Technologies Used

## Programming Language

- Python

---

## Desktop Application

- NiceGUI

---

## Data Processing

- Pandas
- NumPy
- PyArrow

---

## Recommendation Engine

- Content-Based Filtering
- TF-IDF
- RapidFuzz
- Scikit-learn
- SciPy

---

## Packaging

- Nuitka
- Inno Setup

---

## Dataset

- TMDB
- IMDb

---

# 📈 Performance

Typical recommendation workflow using the processed movie dataset.

| Stage | Approximate Time |
|------------------------------|----------------:|
| Runtime Initialization | ~1 s |
| Runtime Asset Verification | Cached after first launch |
| Letterboxd Export Loading | ~0.2 s |
| Movie Matching | ~8–12 s |
| User Profile Generation | <0.1 s |
| Candidate Generation | ~2–3 s |
| Recommendation Scoring | ~2–3 s |
| Final Ranking | <1 s |

> **Note**
>
> Runtime assets are downloaded only during the first launch. Subsequent launches reuse the locally cached dataset, significantly reducing startup time.


---

# 🚀 Roadmap

The project will continue to evolve with a focus on improving recommendation quality, application performance, and user experience.

## Version 2.1

### Recommendation Engine

- [ ] Improve recommendation quality using hybrid scoring
- [ ] Explain why each movie was recommended
- [ ] Smarter diversity optimization
- [ ] Better candidate generation

### Performance

- [ ] Faster application startup
- [ ] Reduced installer size
- [ ] Lower memory usage
- [ ] Recommendation engine optimization

### Desktop Application

- [ ] Better recommendation filtering
- [ ] Search and sorting improvements
- [ ] Export recommendations
- [ ] Enhanced user interface

---

## Future Plans

- Public Letterboxd profile import
- Cross-platform desktop support
- Automatic application updates
- Additional recommendation models
- Improved dataset update workflow

---

# 🤝 Contributing

Contributions, feature suggestions, and bug reports are always welcome.

If you have an idea that could improve the recommendation engine or the desktop application, feel free to open an issue or submit a pull request.

---

# ⭐ Support the Project

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

# 🙏 Acknowledgements

This project would not have been possible without the following open-source projects and datasets.

### Datasets

- TMDB (The Movie Database)
- IMDb
- The Ultimate 1 Million Movies Dataset

### Libraries

- NiceGUI
- Pandas
- NumPy
- SciPy
- Scikit-learn
- RapidFuzz
- PyArrow
- Nuitka
- Inno Setup

A huge thanks to the maintainers and contributors of these projects.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# 👨‍💻 Author

## Hari Prasath JT

Developer of **Letterboxd Recommender**.

### Connect with me

- GitHub: https://github.com/harijt17
- LinkedIn: https://linkedin.com/in/hari-jt17

---

## 🎬 Final Notes

Letterboxd Recommender began as an exploration into **content-based recommendation systems** and evolved into a fully packaged Windows desktop application with an end-to-end recommendation pipeline.

The project demonstrates the complete software development lifecycle—from data preprocessing and recommendation engine design to desktop application development, packaging, and distribution.

I hope this project helps movie enthusiasts discover films they'll love, while also serving as a useful reference for developers interested in building recommendation systems with Python.

Thank you for checking out the project!
