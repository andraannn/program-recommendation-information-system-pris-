from typing import Callable, Dict
from functools import reduce
from rapidfuzz import process, fuzz
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline

IP_NAMES: tuple = ('Bontok', 'Balangao', 'Tonglayan', 'Sakki', 'Madukayan', 'Barlig', 'Sadanga', 'Alab', 'Isneg', 'Tinggian',
            'Adasen', 'Binongan', 'Ilaud', 'Itneg', 'Masad', 'Banao', 'Gubang', 'Mabaka', 'Maeng', 'Mayudan', 'Danak', 'Kankanaey',
            'Iyaplay', 'Kankanaey', 'Ibenguet', 'Kalanguya', 'Karao', 'Mandek-ey', 'Ibaloy', 'Ayangan', 'Tuwali', 'Banao', 'Mabaka',
            'Salegseg', 'Guilayon', 'Cagaluan', 'Guinaang', 'Balatoc', 'Lubuagan', 'Malbong', 'Naneng', 'Taloctok', 'Mangali', 
            'Lubo', 'Tinglayan', 'Tulgao', 'Butbut', 'Basao', 'Dacalan', 'Sumadel', 'Dananao', 'Apayao', 'Bago', 'Agta', 'Kalanguya', 
            'Bugkalot', 'Isinai', 'Gaddang', 'Aggay', 'Dumagat', 'Ibanag', 'Itawis', 'Ivatan', 'Aeta', 'Negrito', 'Baluga', 'Pugot', 
            'Abelling', 'Agta', 'Dumagat', 'Remontado', 'Bugkalot', 'Cimaron', 'Kabihug', 'Tabangon', 'Abiyan', 'Aeta', 'Isarog', 'Itom', 
            'Pullon', 'Agutaynon', 'Tagbanua', 'Dagayanen', 'Taot bato', 'Batak', 'Molbog', 'Iraya Mangyan', 'Hanunuo Mangyan', 'Alangan Mangyan', 
            'Buhid Mangyan', 'Tadyawan Mangyan', 'Batangan Mangyan', 'Gubatnon Mangyan', 'Ratagnon Mangyan', 'Ati', 'Cuyunon', 'Sulod', 'Antique', 
            'Magahat', 'Korolanos', 'Ata', 'Escaya', 'Badjao', 'Kongking', 'Matigsalog', 'Mandaya', 'Mansaka', 'Dibabawon', 'Banwaon', 
            'Bagobo', 'Tagakaolo', 'Talaingod', 'Langilan', 'Mamanwa', 'Higaonon', 'Blaan', 'T-boli', 'Kalagan', 'Tagabawa', 'Matigsalog', 
            'Tigawahanon', 'Sangil', 'Aromanon', 'Tiruray', 'Bagobo', 'Ubo', 'Manobo', 'North', 'Higaonon', 'Subanen', 'Meranao', 'Iranon', 'Karintik', 
            'Blaan', 'Lambangian', 'Dulangan', 'Subanen', 'Talaandig', 'Higaonon', 'Matigsalog', 'Umayamnon', 'Kamigin', 'Yakan', 'Sama', 'Badjao', 
            'Sama', 'Laut', 'Kalibugan', 'Jama', 'Mapon')

SCIENCE: tuple = tuple(pd.Series(['GenPhysics2', 'GenBio2', 'EarthAndLifeScience', 'GenPhysics1', 'PhysicalScience', 'GenChem2', 'GenBio1', 'GenChem1', 'EarthScience']).str.lower())
MATH: tuple = tuple(pd.Series(['PreCalculus', 'BasicCalculus', 'BusinessFinance', 'StatisticsAndProbability', 'GeneralMath', 'BusinessMath']).str.lower())
ENGLISH: tuple = tuple(pd.Series(['CreativeWriting', 'Reading_and_Writing', 'MediaandInformationLiteracy', 't21stCenturyLiteratureFromThePhilippinesAndTheWorld', 
           'ContemporaryPhilippineArtsFromTheRegions', 'OralCommunication', 'CreativeNonfiction']).str.lower())
FILIPINO: tuple = tuple(pd.Series(['KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino', 'PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik', 
            'CreativeWriting_Malikhaing_Pagsulat']).str.lower())
OTHERS: tuple = tuple(pd.Series(['PhilippinePoliticsandGovernance', 'PhysicalEducationandHealth3', 'PrinciplesOfMarketing', 'F1_FundamentalsOfAccountancyBusinessAndManagement1',
           'UnderstandingCultureSocietyAndPolitics', 'Community_EngagementSolidarityAndCitizenship', 'DisciplinesAndIdeasInTheSocialSciences', 
           'Humanities1_Politics', 'OrganizationAndManagement2', 'IntroductionToThePhilosophyOfTheHumanPerson', 'PhysicalEducationAndHealth', 
           'BusinessMarketing', 'PhysicalEducationAndHealth2', 'AppliedEconomicsBusiness', 'PhilippinePiliticsAndGovernance', 'AppliedEconomics2', 
           'FundamentalsOfCoaching', 'EthicsAndSocial_Responsibility', 'PersonalDevelopment', 'SocialScience1', 'IntroToWorldReligionsAndSytemBeliefs', 
           'HumanMovement', 'PhysicalEducationAndHealth4', 'SafetyAndFirstAid', 'F2_FundamentalsofAccountancyBusinessAndManagement2', 'OrganizationAndManagement', 
           'BusinessEnterpriseAndSimulation', 'Humanities2_intro', 'DisasterReadinessAndRisk_Reduction', 'IntroductionToWorldReligionsAndBeliefSystems']).str.lower())

COLUMNS: list = ['NAME_HS', 'FATHER_TRIBE', 'MOTHER_TRIBE', 'AP', 'LU', 'MA', 'SC', 'PROG CODE', 'School_Type', 'HOME_ADDRESS', 
           'FATHER_TRIBE_ip_matched', 'MOTHER_TRIBE_ip_matched', 'FATHER_TRIBE_na', 'MOTHER_TRIBE_na',
           'Track', 'Science', 'Math', 'English', 'Filipino', 'Others']

COLUMNS_MAP: dict = {'name_hs': 'NAME_HS', 
               'father_tribe': 'FATHER_TRIBE', 
               'mother_tribe': 'MOTHER_TRIBE', 
               'ap': 'AP', 
               'lu': 'LU', 
               'ma': 'MA', 
               'sc': 'SC', 
               'prog code': 'PROG CODE', 
               'school_type': 'School_Type', 
               'home_address': 'HOME_ADDRESS', 
               'father_tribe_ip_matched': 'FATHER_TRIBE_ip_matched', 
               'mother_tribe_ip_matched': 'MOTHER_TRIBE_ip_matched', 
               'father_tribe_na': 'FATHER_TRIBE_na', 
               'mother_tribe_na': 'MOTHER_TRIBE_na', 
               'track': 'Track', 
               'science': 'Science', 
               'math': 'Math', 
               'english': 'English', 
               'filipino': 'Filipino', 
               'others': 'Others'}

def calculate_sase_percentage(data: dict) -> dict:
    """
    Calculate the percentage scores for the 'MA', 'SC', 'AP', and 'LU'
    """

    # Divide the 'MA', 'SC', 'AP', 'LU', and 'GR' columns by their maximum scores
    data["ma"] = data["ma"] / 40
    data["sc"] = data["sc"] / 30
    data["ap"] = data["ap"] / 30
    data["lu"] = data["lu"] / 80

    return data

def get_school_type(data: dict, school_types: dict) -> dict:
    """
    Maps the school type to the NAME_HS data
    """

    data["school_type"] = school_types.get(data["name_hs"], "Public")
    return data

def city_lumping(data: dict, city_percent : pd.DataFrame ,tolerance: int = 0.5) -> dict:
    """
    Home address of the applicant
    """

    above_tol_names = city_percent[city_percent >= tolerance].index

    if data["city_home"] in above_tol_names:
        data["home_address"] = data["city_home"]
    else:
        data["home_address"] = data["province_home"]

    return data


def get_ip_matched(data: dict, cutoff: int = 80) -> dict:
    """
    Fuzzy match the father and mother's tribe names to the IP names
    """

    # Match the father's tribe name to the IP names using rapidfuzz
    matched_name = process.extractOne(
        data["father_tribe"], IP_NAMES, score_cutoff=cutoff
    )
    data["father_tribe_ip_matched"] = matched_name[0] if matched_name else "Non-IP"

    # Match the mother's tribe name to the IP names using rapidfuzz
    matched_name = process.extractOne(
        data["mother_tribe"], IP_NAMES, score_cutoff=cutoff
    )
    data["mother_tribe_ip_matched"] = matched_name[0] if matched_name else "Non-IP"

    return data

def impute_and_rarelabel_encode(data: dict, pipeline: Pipeline) -> dict:
    """
    Use a pretrained pipeline with feature-engine transformers to impute and rarelabel encode the data
    """

    # Make 'NAME_HS', 'FATHER_TRIBE', 'MOTHER_TRIBE', and 'TRACK/STRAND' from the data as a DataFrame
    df = pd.DataFrame({
        "NAME_HS": [data["name_hs"]],
        "FATHER_TRIBE": [data["father_tribe"]],
        "MOTHER_TRIBE": [data["mother_tribe"]],
        "TRACK/STRAND": [data["track"]]
    })

    # Use the pipeline to transform the data
    update_data = {k.lower(): v for k, v in pipeline.transform(df).to_dict("records")[0].items()}

    # Rename 'TRACK/STRAND' to 'Track'
    # TODO: Re-train the transformer to avoid this
    update_data["track"] = update_data.pop("track/strand")

    # Update the data with the transformed data
    data.update(update_data)

    return data

def average_science(data: dict) -> dict:
    """
    Calculate the average score for the science subjects
    """

    # Since all of the science subjects in the tuple are not guaranteed to be not nan, average only the subjects that are not missing using numpy
    science_subjects = [data[subject] for subject in SCIENCE if data[subject] >= 0]

    # Calculate the average score for the science subjects
    data["science"] = np.mean(science_subjects)

    return data

def average_math(data: dict) -> dict:
    """
    Calculate the average score for the math subjects
    """

    # Since all of the science subjects in the tuple are not guaranteed to be not nan, average only the subjects that are not missing using numpy
    math_subjects = [data[subject] for subject in MATH if data[subject] >= 0]

    # Calculate the average score for the science subjects
    data["math"] = np.mean(math_subjects)

    return data

def average_english(data: dict) -> dict:
    """
    Calculate the average score for the english subjects
    """

    # Since all of the science subjects in the tuple are not guaranteed to be not nan, average only the subjects that are not missing using numpy
    english_subjects = [data[subject] for subject in ENGLISH if data[subject] >= 0]

    # Calculate the average score for the science subjects
    data["english"] = np.mean(english_subjects)

    return data

def average_filipino(data: dict) -> dict:
    """
    Calculate the average score for the math subjects
    """

    # Since all of the science subjects in the tuple are not guaranteed to be not nan, average only the subjects that are not missing using numpy
    filipino_subjects = [data[subject] for subject in FILIPINO if data[subject] >= 0]

    # Calculate the average score for the science subjects
    data["filipino"] = np.mean(filipino_subjects)

    return data

def average_others(data: dict) -> dict:
    """
    Calculate the average score for the math subjects
    """

    # Since all of the science subjects in the tuple are not guaranteed to be not nan, average only the subjects that are not missing using numpy
    subjects = [data[subject] for subject in OTHERS if data[subject] >= 0]

    # Calculate the average score for the science subjects
    data["others"] = np.mean(subjects)

    return data

def filter_data(data: dict) -> dict:
    """
    Get only the relevant data for the model
    """

    _data = {}
    # Get only the relevant data for the model
    # COLUMNS object contains the relevant data

    for low, orig in COLUMNS_MAP.items():
        if orig == 'PROG CODE':
            _data[orig] = ''
            continue
        _data[orig] = data[low]
        
    return _data