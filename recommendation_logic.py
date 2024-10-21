from functools import lru_cache
import pandas as pd
import numpy as np
import pickle
from typing import List, Dict, Union

from config import CLUSTER_PROFILE_PATH, PREFERED_COURSE_PATH, PROGRAM_SIMILARITY_PATH, PROGRAM_MEAN_PATH

# Caching data loading functions
@lru_cache(maxsize=1)
def load_cluster_profile() -> pd.DataFrame:
    return pd.read_excel(CLUSTER_PROFILE_PATH, sheet_name="Cluster_profile")

@lru_cache(maxsize=1)
def load_cluster_program_score() -> pd.DataFrame:
    return pd.read_excel(CLUSTER_PROFILE_PATH, sheet_name="Proportion Program per Cluster")

@lru_cache(maxsize=1)
def load_prefered_course_match() -> pd.DataFrame:
    return pd.read_csv(PREFERED_COURSE_PATH)

@lru_cache(maxsize=1)
def load_program_sim() -> pd.DataFrame:
    return pd.read_csv(PROGRAM_SIMILARITY_PATH)

@lru_cache(maxsize=1)
def load_program_mean() -> Dict[str, float]:
    with open(PROGRAM_MEAN_PATH, "rb") as f:
        return pickle.load(f)

# Load data
cluster_prof: pd.DataFrame = load_cluster_profile()
prefered_course_match: pd.DataFrame = load_prefered_course_match()
cluster_program_score: pd.DataFrame = load_cluster_program_score()
program_sim: pd.DataFrame = load_program_sim()
program_mean: Dict[str, float] = load_program_mean()

def proj_scaler(data: Union[np.ndarray, pd.Series], scale: str = "all") -> np.ndarray:
    """
    Scales the input data based on the specified scale type.
    
    Parameters:
    - data (Union[np.ndarray, pd.Series]): The input data to scale.
    - scale (str): The type of scaling to apply ('hs', 'sase', or 'all'). Default is 'all'.
    
    Returns:
    - np.ndarray: The scaled data.
    """
    scale_factors = {
        "hs": np.array([100, 100, 100, 100, 100, 1, 1, 1, 1]),
        "sase": np.array([1, 1, 1, 1, 1, 30, 30, 40, 80]),
        "all": np.array([100, 100, 100, 100, 100, 30, 30, 40, 80])
    }
    
    if scale not in scale_factors:
        raise ValueError(f"Invalid scale type: {scale}. Choose from 'hs', 'sase', or 'all'.")
    
    return data / scale_factors[scale]

def pred_cluster(student_info: Union[np.ndarray, pd.Series], cluster_profile: pd.DataFrame, scale: str = "hs") -> Union[int, str]:
    """
    Predicts the cluster for a student based on their information and cluster profiles.
    
    Parameters:
    - student_info (Union[np.ndarray, pd.Series]): The student's information.
    - cluster_profile (pd.DataFrame): The cluster profiles with a 'Cluster' column.
    - scale (str): The type of scaling to apply ('hs', 'sase', or 'all'). Default is 'hs'.
    
    Returns:
    - Union[int, str]: The predicted cluster for the student.
    """
    if 'Cluster' not in cluster_profile.columns:
        raise ValueError("The cluster profile must contain a 'Cluster' column.")
    
    clusters = cluster_profile['Cluster']
    student_info_scaled = proj_scaler(student_info, scale=scale)
    cluster_profile_scaled = proj_scaler(cluster_profile.drop(columns=['Cluster']), scale=scale)
    
    distances = cluster_profile_scaled.sub(student_info_scaled, axis=1).pow(2).sum(axis=1).pow(0.5)
    
    closest_cluster_index = distances.idxmin()
    
    return clusters.iloc[closest_cluster_index]

def make_partial_recommendation(student_info: pd.DataFrame, pred_list: List[str], compare_list: List[str]) -> pd.DataFrame:
    """
    Makes partial recommendations based on the student's information, predicted list, and comparison list.
    
    Parameters:
    - student_info (pd.DataFrame): The student's information DataFrame.
    - pred_list (List[str]): The list of predicted programs.
    - compare_list (List[str]): The list of programs to compare against.
    
    Returns:
    - List[str]: The list of partial recommendations.
    """
    student_info["PROG CODE"] = student_info["PROG CODE"].str.strip()
    pred_list = [prog.strip() for prog in pred_list]
    pred_scores = [student_info.loc[student_info["PROG CODE"] == prog, "Score"].values[0] for prog in pred_list]
    top_pred_df = pd.DataFrame({
        "Program":pred_list,
        "Score": pred_scores
    })
    
    if compare_list:
        common_programs = list(set(pred_list).intersection(compare_list))
        pred_list_trim = [prog for prog in pred_list if prog not in common_programs]
        compare_list_trim = [prog for prog in compare_list if prog not in common_programs]
        final_pred_list = pred_list_trim + compare_list_trim
        if 'BS EnvET' in final_pred_list:
            final_pred_list.remove('BS EnvET')
            final_pred_list.append('BSEnE')
  
        final_pred_scores = [student_info.loc[student_info["PROG CODE"] == prog, "Score"].values[0] for prog in final_pred_list]
        final_pred_df_score = pd.DataFrame({
        "Program": final_pred_list,
        "Score": final_pred_scores
        })
        # Strip whitespace from program codes in final_pred_list and ensure they match those in program_sim
        final_pred_list = [prog.strip() for prog in final_pred_list]
        cluster_model_sim = program_sim.loc[program_sim.Program.isin(final_pred_list), ["Program"] + final_pred_list]
        cluster_model_sim["mean_sim"] = cluster_model_sim.iloc[:, 1:].mean(axis=1)
        cluster_model_sim = pd.merge(cluster_model_sim, final_pred_df_score, how="left", on="Program")
        cluster_model_sim["Final_Score"] = cluster_model_sim["mean_sim"] * cluster_model_sim["Score"]
        cluster_model_sim["Final_Score"] = 1e-5 + (1-2*1e-5)*((cluster_model_sim["Final_Score"]-cluster_model_sim["Final_Score"].min())/(cluster_model_sim["Final_Score"].max()-cluster_model_sim["Final_Score"].min()))
        common_programs_df = top_pred_df.loc[top_pred_df.Program.isin(common_programs)]
        common_programs_df["Final_Score"] =  1e-5                   
        partial_recom = common_programs_df[["Program","Final_Score"]]._append(cluster_model_sim[["Program","Final_Score"]], ignore_index=True)
    else:
        partial_recom = top_pred_df = pd.DataFrame({
        "Program": pred_list,
        "Final_Score": pred_scores
    })
        partial_recom["Final_Score"] = 1e-4 + (1-2*1e-4)*((partial_recom["Final_Score"]-partial_recom["Final_Score"].min())/(partial_recom["Final_Score"].max()-partial_recom["Final_Score"].min()))
    
    return partial_recom.sort_values("Final_Score")

def make_final_recommendation(partial_rec: pd.DataFrame, pref_course: List[str]) -> pd.DataFrame:
    """
    Makes the final recommendation based on the partial recommendations and preferred courses.
    
    Parameters:
    - partial_rec (List[str]): The list of partial recommendations.
    - pref_course (List[str]): The list of preferred courses.
    
    Returns:
    - List[str]: The list of final recommendations.
    """
    pref_course = [prog.strip() for prog in pref_course]
    common_programs = list(set(partial_rec.Program.to_list()).intersection(pref_course))
    final_pred_list = [prog for prog in partial_rec.Program.to_list() if prog not in common_programs]
  
    if len(common_programs) > 0:
        common_programs_df = pd.DataFrame({
            "Program":common_programs,
            "Min_Score":[0]*len(common_programs)})
        cluster_model_sim = program_sim.loc[program_sim.Program.isin(final_pred_list), ["Program"] + pref_course]
        
        cluster_model_sim["Min_Score"] = cluster_model_sim.iloc[:, 1:].min(axis=1)
        cluster_model_sim = common_programs_df._append(cluster_model_sim[["Program","Min_Score"]],ignore_index=True)
    else:
        cluster_model_sim = program_sim.loc[program_sim.Program.isin(final_pred_list), ["Program"] + pref_course]
        cluster_model_sim["Min_Score"] = cluster_model_sim.iloc[:, 1:].min(axis=1)
        cluster_model_sim = cluster_model_sim[["Program","Min_Score"]]
    
    
    cluster_model_sim = pd.merge(cluster_model_sim,partial_rec, on="Program")
    cluster_model_sim["Final_Score"] = cluster_model_sim["Min_Score"]*cluster_model_sim["Final_Score"]
      
    cluster_model_sim["Final_Score"] = 1e-5 + (1-2*1e-5)*((cluster_model_sim["Final_Score"]-cluster_model_sim["Final_Score"].min())/(cluster_model_sim["Final_Score"].max()-cluster_model_sim["Final_Score"].min()))
    
    return cluster_model_sim.sort_values("Final_Score")

def recommend_program(student_info: pd.DataFrame, prefered_course: List[str], scale_hs: bool = True, scale_sase: bool = False, n_rec: int = 10) -> pd.DataFrame:
    """
    Recommends programs for a student based on their information and preferences.
    
    Parameters:
    - student_info (pd.DataFrame): The student's information DataFrame.
    - prefered_course (List[str]): The list of preferred courses.
    - scale_hs (bool): Whether to use high school scaling. Default is True.
    - scale_sase (bool): Whether to use SASE scaling. Default is False.
    - n_rec (int): The number of recommendations to make. Default is 10.
    
    Returns:
    - List[str]: The list of final program recommendations.
    """
    hs_col = ["Science", "Math", "English", "Filipino", "Others"]
    sase_col = ["AP", "SC", "MA", "LU"]
    num_cols = hs_col + sase_col
    
    student_info['Mean_GPA'] = student_info['PROG CODE'].map(program_mean)
    student_info["Score"] = np.abs(student_info["Mean_GPA"] - student_info["PREDICTED"])
    student_info_num = student_info[num_cols].iloc[0]
    
    if scale_hs and scale_sase:
        predicted_cluster = pred_cluster(student_info_num, cluster_prof, scale="all")
    elif scale_hs:
        predicted_cluster = pred_cluster(student_info_num, cluster_prof, scale="hs")
    elif scale_sase:
        predicted_cluster = pred_cluster(student_info_num, cluster_prof, scale="sase")
    
    top_pred = student_info[["PROG CODE", "Score"]].sort_values("Score", ascending=True).head(n=n_rec)["PROG CODE"]
    
    if predicted_cluster == 2:
        partial_recom = make_partial_recommendation(student_info, top_pred.tolist(), [])
    else:
        cluster_top_list = cluster_program_score[cluster_program_score.cluster == predicted_cluster].sort_values("proportion", ascending=False).head(n=n_rec)["progcode"].tolist()
        partial_recom = make_partial_recommendation(student_info, top_pred.tolist(), cluster_top_list)
    
    prefered_course_code = prefered_course_match[prefered_course_match.Progcode.isin(prefered_course)]["Progcode"].unique().tolist()

    
    if prefered_course_code:
        output= make_final_recommendation(partial_recom, prefered_course_code)
    else:
        output = partial_recom
        
    output.reset_index(inplace=True,drop=True)
    output["Cluster"]=predicted_cluster
    output["Org_rank"] = [i+1 for i in output.index]
    return output
