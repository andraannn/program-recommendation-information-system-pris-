import pickle
from functools import partial, lru_cache
import pandas as pd
from sklearn.pipeline import Pipeline
from typing import Dict, Any

from config import MODEL_PATH, PREPROCESSOR_PATH, ONEHOTENCODER_PATH, SCHOOL_TYPES_PATH, CITY_PROP_PATH, PROGRAMS_PATH
from utils import compose
from preprocess import *

# Filter the FutureWarning
import warnings
warnings.filterwarnings("ignore")

# Caching data loading functions
@lru_cache(maxsize=1)
def load_model() -> Pipeline:
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

@lru_cache(maxsize=1)
def load_preprocessor() -> Pipeline:
    with open(PREPROCESSOR_PATH, "rb") as f:
        return pickle.load(f)
    
@lru_cache(maxsize=1)
def load_onehotencoder() -> Pipeline:
    with open(ONEHOTENCODER_PATH, "rb") as f:
        return pickle.load(f)

@lru_cache(maxsize=1)
def load_school_types() -> Dict[str, str]:
    return pd.read_csv(SCHOOL_TYPES_PATH, usecols=["School", "Type"], index_col=0).to_dict()["Type"]

@lru_cache(maxsize=1)
def load_city_prop() -> pd.DataFrame:
    return pd.read_csv(CITY_PROP_PATH, index_col=0)

@lru_cache(maxsize=1)
def load_programs() -> pd.DataFrame:
    return pd.read_csv(PROGRAMS_PATH, index_col=0)

# Load data
model: Pipeline = load_model()
impute_pipeline: Pipeline = load_preprocessor()
onehot_encoder: Pipeline = load_onehotencoder()
SCHOOL_TYPES: Dict[str, str] = load_school_types()
CITY_PROP: pd.DataFrame = load_city_prop()
PROGRAMS: pd.DataFrame = load_programs()

def data_pipeline(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the input data dictionary through a series of preprocessing steps.
    
    Parameters:
    - data (Dict[str, Any]): The input data to process.
    
    Returns:
    - Dict[str, Any]: The processed data.
    """
    preprocess = compose(
        partial(calculate_sase_percentage),
        partial(get_school_type, school_types=SCHOOL_TYPES),
        partial(city_lumping, city_percent=CITY_PROP, tolerance=0.5),
        partial(get_ip_matched, cutoff=80),
        partial(impute_and_rarelabel_encode, pipeline=impute_pipeline),
        partial(average_science),
        partial(average_math),
        partial(average_english),
        partial(average_filipino),
        partial(average_others),
        partial(filter_data),
    )
    return preprocess(data)

def predict(data: Dict[str, Any]) -> float:
    """
    Predicts the outcome based on the input data.
    
    Parameters:
    - data (Dict[str, Any]): The input data to predict.
    
    Returns:
    - float: The prediction result.
    """
    processed_data = data_pipeline(data)
    onehot_encoded = onehot_encoder.transform(pd.DataFrame([processed_data]))
    prediction = model.predict(onehot_encoded)
    return prediction

def prediction_per_program(data: Dict[str, Any], top: int = 10) -> pd.DataFrame:
    """
    Predicts the outcome for each program based on the input data.
    
    Parameters:
    - data (Dict[str, Any]): The input data to predict.
    - top (int): The number of top results to return. Default is 10.
    
    Returns:
    - pd.DataFrame: The prediction results for each program.
    """
    processed_data = data_pipeline(data)
    expanded_data = pd.concat([pd.DataFrame([processed_data])] * len(PROGRAMS), ignore_index=True)
    expanded_data["PROG CODE"] = PROGRAMS["PROG CODE"].values
    onehot_data = onehot_encoder.transform(expanded_data)
    expanded_data["PROG NAME"] = PROGRAMS["COURSE_NAME"]
    expanded_data["PREDICTED"] = model.predict(onehot_data)
    
    return expanded_data[['Science', 'Math', 'English', 'Filipino', 'Others', 'AP', 'SC', 'MA', 'LU', 'PROG CODE', 'PROG NAME', 'PREDICTED']]