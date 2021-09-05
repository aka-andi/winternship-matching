import pandas as pd
import numpy as np


def load_applications(file_path: str) -> pd.DataFrame:
    # CSV must have columns "EMPLID", "Gender", "CUNY", "Year", "CS Courses", "Govt ID", "F1/J1"
    df = pd.read_csv(file_path,
                     usecols=["EMPLID", "Gender", "CUNY", "Year", "CS Courses", "Govt ID", "F1/J1"],
                     skipinitialspace=True,
                     skiprows=[1, 2])
    df['Gender'] = df['Gender'].str.split(',')
    return df


def load_enrollment(file_path: str) -> pd.DataFrame:
    # CSV must have columns "EMPLID", "Programming Languages", "Interests"
    df = pd.read_csv(file_path,
                     usecols=["EMPLID", "Programming Languages", "Interests"],
                     skipinitialspace=True,
                     skiprows=[1, 2])
    df['Programming Languages'] = df['Programming Languages'].str.split(',')
    df['Interests'] = df['Interests'].str.split(',')
    return df


def load_student_pref(file_path: str) -> pd.DataFrame:
    # CSV must have columns "First", "Last", "EMPLID", "Preferences"
    df = pd.read_csv(file_path,
                     usecols=["First", "Last", "EMPLID", "Preferences"],
                     skipinitialspace=True,
                     skiprows=[1])
    df['Preferences'] = df['Preferences'].str.split(',')
    return df


def determine_cs_experience(num_courses: str, programming_languages: list) -> str:
    if 'None' in programming_languages or num_courses == '0':
        return 'beginner'
    if len(programming_languages) >= 5 or num_courses in ['3', '4', '5+']:
        return 'advanced'
    return 'intermediate'


def load_students(app_file, enrollment_file, pref_file) -> dict:
    app_df = load_applications(app_file)
    enrollment_df = load_enrollment(enrollment_file)
    pref_df = load_student_pref(pref_file)

    # added code to avoid error for column types below
    pref_df['EMPLID'] = pref_df['EMPLID'].astype(int)

    combined_df = pref_df.merge(enrollment_df, on='EMPLID')
    combined_df = combined_df.merge(app_df, on='EMPLID')

    combined_df.insert(0, 'LastFirst', combined_df.Last.str.title() + combined_df.First.str.title())
    combined_df = combined_df.drop_duplicates(subset=['LastFirst'])
    combined_df = combined_df.set_index('LastFirst')
    combined_df['matched_company'] = None
    combined_df.drop(columns=['CS Courses', 'Programming Languages'], inplace=True)
    combined_df.rename(columns={'First': 'first',
                                'Last': 'last',
                                'Gender': 'gender',
                                'Year': 'year',
                                'CUNY': 'cuny',
                                "Govt ID": 'govtid',
                                "F1/J1": 'f1j1',
                                'Interests': 'interests',
                                'Preferences': 'ranked_companies'}, inplace=True)
    return combined_df.to_dict(orient='index')


def load_company_info(file_path: str) -> pd.DataFrame:
    # CSV must have columns "Organization", "Number of Students", "Sponsored", "F1/J1"
    df = pd.read_csv(file_path,
                     usecols=["Organization", "Number of Students", "Sponsored", "F1/J1"],
                     skipinitialspace=True)
    df.rename(columns={'Number of Students': 'num_students',
                       'Sponsored': 'sponsored',
                       'F1/J1': 'f1_j1'}, inplace=True)
    return df


def load_company_pref(file_path: str) -> pd.DataFrame:
    # CSV must have columns "Organization", "Prefer", "Exclude"
    df = pd.read_csv(file_path,
                     usecols=["Organization", "Prefer", "Exclude"],
                     skipinitialspace=True,
                     skiprows=[1])
    df.Prefer = df.Prefer.str.title()
    df.Prefer = df.Prefer.str.replace(', ', '')
    df.Prefer = df.Prefer.str.split(' / ')

    df.Exclude = df.Exclude.str.title()
    df.Exclude = df.Exclude.str.replace(', ', '')
    df.Exclude = df.Exclude.str.split(' / ')

    df.rename(columns={'Prefer': 'prefer',
                       'Exclude': 'exclude'}, inplace=True)
    return df


def load_companies(info_file, pref_file) -> dict:
    info_df = load_company_info(info_file)
    pref_df = load_company_pref(pref_file)
    combined_df = pref_df.merge(info_df, on='Organization')
    combined_df['team'] = np.empty((len(combined_df), 0)).tolist()
    combined_df = combined_df.set_index('Organization')
    return combined_df.to_dict(orient='index')
