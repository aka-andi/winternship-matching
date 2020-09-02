from typing import Tuple
from random import shuffle

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
    all_students = students.keys()
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
            if len(company['team'] < company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
                students[name]['matched_company'] = company_name
                companies[company_name]['team'].append(name)
                break
    return students, companies

def match_team_fit(students: dict, companies: dict) -> Tuple[dict, dict]:
    """Match based on team fit"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    shuffle(unmatched_students)
    for name in unmatched_students:
        student = students[name]
        for company in companies:
            if len(company['team'] < company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
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
    
        
    