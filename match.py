from typing import Tuple
from random import shuffle
import pandas as pd

def is_good_fit(new_student: dict, team: list , students: dict) -> bool:
    """TO DO"""
    if 'Male' in new_student['gender'] and 'Male' in [students[name]['gender'] for name in team]:
        return False

    if [students[name]['cuny'] for name in team].count(new_student['cuny']) == 3:
        return False

    if [students[name]['year'] for name in team].count(new_student['year']) == 3:
        return False

    # if [students[name]['cs_experience'] for name in team].count(new_student['cs_experience']) == 3:
    #     return False

    return True

def match_mutual(students: dict, companies: dict) -> Tuple[dict, dict]:
    """Match based on student rankings and company preferences"""
    #turning students.keys() into a list to squash dict obj not iterable bug
    #old code
    #all_students = students.keys()
    #new code
    all_students = list(students.keys())
    shuffle(all_students)
    for name in all_students:
        student = students[name]
        for company_name in student['ranked_companies']:
            company = companies[company_name]
            if len(company['team']) < int(company['num_students']) and name in company['prefer'] and is_good_fit(student, company['team'], students):
                students[name]['matched_company'] = company_name
                companies[company_name]['team'].append(name)
                break

    return students, companies

def match_student_pref(students, companies) -> Tuple[dict, dict]:
    """Match based on student rankings"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    shuffle(unmatched_students)
    for name in unmatched_students:
        student = students[name]
        for company_name in student['ranked_companies']:
            company = companies[company_name]
            #testing errors below
            #print(len(company['team']), type(len(company['team'])))
            #print(int(company['num_students']), type(int(company['num_students'])))
            #print(name, company)
            #print(name not in company['exclude'], type(name not in company['exclude']))
            #print(is_good_fit(student, company['team'], students), type(is_good_fit(student, company['team'], students)))
            #conclusion: name not in company['exclude'] may throw an error if exclude is left blank
            #set blank excludes or prefers to random letter like x to get around this
            if len(company['team']) < int(company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
                students[name]['matched_company'] = company_name
                #print('!!!!!!!',students[name],[company_name])
                companies[company_name]['team'].append(name)
                break
    return students, companies

def match_team_fit(students: dict, companies: dict) -> Tuple[dict, dict]:
    """Match based on team fit"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    shuffle(unmatched_students)
    for name in unmatched_students:
        student = students[name]
        #print(companies)
        for company in companies:
            #print("test",companies[company]['team'])
            #print(companies[company]['num_students'], type(companies[company]['num_students']))
            #old code, couldn't index using company['team'] like we did before because we set company to something different here
            #if len(company['team']) < int(company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
            #solution: properly index to find the company team length, new code line 75
            if len(companies[company]['team']) < int(companies[company]['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
                students[name]['matched_company'] = company.key
                companies[company.key]['team'].append(name)
                break
    return students, companies

def match(students: dict, companies: dict) -> Tuple[dict, dict]:
    """"""
    students, companies = match_mutual(students, companies)
    students, companies = match_student_pref(students, companies)
    students, companies = match_team_fit(students, companies)
    return students, companies

def valid_match(students: dict, companies: dict) -> bool:
    """"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    print(students)
    print(len(unmatched_students))
    if len(unmatched_students) > 0:
        return False
    return True
