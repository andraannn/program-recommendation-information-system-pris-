from pathlib import Path

__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent

MODEL_PATH = BASE_DIR / f"models/ardregressor-{__version__}.pkl"
PREPROCESSOR_PATH = BASE_DIR / f"transformers/preprocess-{__version__}.pkl"
ONEHOTENCODER_PATH = BASE_DIR / f"transformers/onehotencoder-{__version__}.pkl"
SCHOOL_TYPES_PATH = BASE_DIR / "transformers/School_type.csv"
CITY_PROP_PATH = BASE_DIR / "transformers/city_percentage.csv"
PROGRAMS_PATH = BASE_DIR / "transformers/programs.csv"

CLUSTER_PROFILE_PATH = BASE_DIR / "transformers/Clusters.xlsx"
PREFERED_COURSE_PATH = BASE_DIR / "transformers/programs_matching.csv"
PROGRAM_SIMILARITY_PATH = BASE_DIR / "transformers/eucdist_matrix.csv"
PROGRAM_MEAN_PATH = BASE_DIR / "transformers/program_mean_gpa.pkl"