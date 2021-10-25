import csv
import os
from entity_classes import Project, Student

DATA_DIR = "../data/" # Directory in which input files will be kept
RESULT_DIR = "../results" # Directory in which matches will be outputted

def get_student_name(data, lname_header='RecipientLastName', fname_header='RecipientFirstName'):
    ''' Get student name in form LNAME, FNAME from raw data '''
    return (data[lname_header].strip() + ", " + data[fname_header].strip()).upper()

def read_student_data():
    ''' Parse raw student data and return a dictionary of Student objects. '''
    students = {}
    student_enrollment = csv.DictReader(open('{}/student_enrollment.csv'.format(DATA_DIR), newline=''))
    student_apps = csv.DictReader(open('{}/student_applications.csv'.format(DATA_DIR), newline=''))
    student_preferences = csv.DictReader(open('{}/student_pref.csv'.format(DATA_DIR), newline=''))

    for data in student_enrollment:
        try:
            int(data['Progress'])
        except ValueError:
            continue
        students[get_student_name(data)] = Student()
        students[get_student_name(data)].add_enrollment_data(data)
    for data in student_apps:
        if get_student_name(data, 'Q4', 'Q2') in students:
            students[get_student_name(data, 'Q4', 'Q2')].add_application_data(data)
    for data in student_preferences:
        students[get_student_name(data)].add_preferences(data)

    print("Total {} students.".format(len(students)))
    return students

def read_project_data():
    ''' Parse raw project data and return a dictionary of Project objects. '''
    companies = {}
    company_pref = open('../data/company_pref.csv', newline='')
    company_info = open('../data/company_info.csv', newline='')

    for data in csv.DictReader(company_pref):
        try:
            int(data['V5'])
        except ValueError:
            continue
        project = Project(data)
        companies[project.organization] = project
    for data in csv.DictReader(company_info):
        try:
            companies[data['Organization']].add_project_info(data)
        except KeyError:
            continue
    print("Total {} companies.".format(len(companies)))
    return companies

def write_match_data(students):
    ''' Output match results.'''
    try:
        print("Clearing old matches...")
        os.remove("{}/matches.csv".format(RESULT_DIR))
    except FileNotFoundError:
        pass
    with open(r'{}/matches.csv'.format(RESULT_DIR), 'a', newline='') as f:
        header = ['Student', 'Project/Company']
        writer = csv.writer(f)
        writer.writerow(header)
        for student in students.values():
            writer.writerow([student.legal_name, student.project_match])
        f.close()
