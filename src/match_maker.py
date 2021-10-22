from entity_classes import Project, Student
from generate_data import *
import random
from math import inf
import csv
import sys
import os
import shutil

PASSES = 5 # Equivalent to the minimum number of preferences a student must provide

def get_interested_students(students, project, rank):
    '''
    Returns a list of names of students who have the project listed at the
    specified rank.
    '''
    students_ = sorted(list(students.values()), key=lambda x: x._score, reverse=True)
    interested = []
    for student in students_:
        if student.matched():
            continue
        if student.preferred_projects[rank] == project.organization and project.student_eligible(student):
            interested.append(student.legal_name)
    return interested

def add_matches(students, project):
    '''
    Adds the students in the given list of Student objects
    to the given Project.
    '''
    for student in students:
        if not project.reached_capacity():
            project.add_match(student)
            student.add_match(project)

def get_optimal_students(project, interested_students, iterations=10):
    '''
    A sad attempt at optimization, to gather a set of students
    that both have higher overall student scores and provide a high
    diversity score for the project. By default, stops searching
    after 10 iterations.
    '''
    if len(interested_students) == 0 or project.reached_capacity():
        return []
    num_required_students = project.capacity - len(project.student_matches)
    test_project = Project()
    optimal = -inf
    optimal_students = []
    for i in range(iterations):
        random.shuffle(interested_students)
        average_student_score = sum([student._score for student in interested_students[:num_required_students]]) / len(interested_students[:num_required_students])
        test_project.student_matches = project.student_matches + [student.legal_name for student in interested_students[:num_required_students]]
        diversity_score = test_project.diversity_score(interested_students)
        if (sum([average_student_score, diversity_score])/2) > optimal:
            optimal = sum([average_student_score, diversity_score])/2
            optimal_students = interested_students[:num_required_students]
    return optimal_students


def match_remaining_students(students, projects, unmatched):
    '''
    A function for dealing with unmatched students. For now it just randomly
    assigns students to projects until all projects are filled up.
    '''
    # Sort the students by score
    if unmatched == 0:
        return students, projects, 0
    sorted_students = sorted(list(students.values()), key=lambda x: x._score, reverse=True)
    students_left = [student.legal_name for student in sorted_students if not(student.matched())]
    unmatched = len(students_left)
    while len(students_left) != 0:
        next_student_name = students_left[0] # Get the first priority student
        # Match the student with a project
        for project in projects.values():
            if not project.reached_capacity() and project.student_eligible(students[next_student_name]):
                add_matches([students[next_student_name]], project)
                students_left.pop(0)
                unmatched -= 1
        if not(students[next_student_name].matched()):
            print("Unable to find eligible match for {}".format(next_student_name))
            students_left.pop(0)
        if [True] * len(list(projects.keys())) == [project.reached_capacity() for project in projects.values()]:
            print("Capacity per project reached.")
            print("Total spots available were {}".format(sum([project.capacity for project in projects.values()])))
            return students, projects, len(students_left)
    return students, projects, 0


def match(students, projects):
    '''
    Matching Algorithm:

    For each n in PASSES, and for each project, collect all students whose
    n'th choice is this project, eliminating students in the exclusion list
    for the project. Students that are preferred by the company are put first.
    For the rest of the empty slots, the set of students that both have the
    highest scores and make up a high diversity score are chosen.

    These scores are calculated from preconfigured priorities given
    to student-specific attributes in a config file.
    '''
    for n in range(PASSES):
        for project in projects.values():
            if project.reached_capacity():
                continue
            # Get students for whom this project is the nth choice
            interested = get_interested_students(students, project, n)
            # Immediately match any mutual preferences
            mutual_preferences = [student for student in interested if student in project.preferred_students]
            random.shuffle(mutual_preferences)
            for student_name in mutual_preferences:
                add_matches([students[student_name]], project)
                interested.remove(student_name)
            # For the rest of empty spots
            # Give priority to students with higher scores and the set of students that
            #   give highest diversity score
            optimal_students = get_optimal_students(project, [student for student in students.values() if student.legal_name in interested])
            add_matches(optimal_students, project)
    unmatched = len([student for student in students.values() if not student.matched()])
    students, projects, unmatched = match_remaining_students(students, projects, unmatched)
    return students, projects, unmatched

def load_student_data():
    students = {}

    student_apps = open('./data/student_applications.csv', newline='')
    student_enrollment = open('./data/student_enrollment.csv', newline='')
    student_preferences = open('./data/student_pref.csv', newline='')

    reader = csv.DictReader(student_apps)
    id = 0
    for row in reader:
        if id < 2:
            id += 1
            continue
        student = Student(id)
        if not student.add_application_data(row):
            continue
        students[student.legal_name] = student
        id += 1

    reader = csv.DictReader(student_enrollment)
    for row in reader:
        student = students[(row['RecipientLastName'].strip() + ", " + row['RecipientFirstName'].strip()).upper()]
        student.add_enrollment_data(row)

    reader = csv.DictReader(student_preferences)
    for row in reader:
        student = students[(row['RecipientLastName'].strip() + ", " + row['RecipientFirstName'].strip()).upper()]
        student.add_preferences(row)
    print("Total {} students.".format(len(students)))
    return students

def load_project_data():
    company_pref = open('./data/company_pref.csv', newline='')
    companies = {}
    reader = csv.DictReader(company_pref)
    id = 0
    for row in reader:
        if id < 2:
            id += 1
            continue
        project = Project(row)
        companies[project.organization] = project

    company_info = open('./data/company_info.csv', newline='')
    reader = csv.DictReader(company_info)
    id = 0
    for row in reader:
        if id < 2:
            id += 1
            continue
        companies[row['Organization']].add_project_info(row)
    print("Total {} companies.".format(len(companies)))
    return companies

def write_matches(students):
    try:
        print("Clearing old matches...")
        os.remove("./out/matches.csv")
    except FileNotFoundError:
        pass
    with open(r'./out/matches.csv', 'a', newline='') as f:
        header = ['Student', 'Project/Company']
        writer = csv.writer(f)
        writer.writerow(header)
        for student in students.values():
            writer.writerow([student.legal_name, student.project_match])
        f.close()

def generate_mock_data(num_companies=10, max_student_capacity=30):
    try:
        os.mkdir("./data/")
    except FileExistsError:
        pass
    try:
        print("Clearing old data...")
        os.remove("./data/company_pref.csv")
        os.remove("./data/company_info.csv")
        os.remove("./data/student_enrollment.csv")
        os.remove("./data/student_pref.csv")
    except FileNotFoundError:
        pass
    print("Generating mock data...")
    generate_student_enrollment_data()
    generate_student_preference_data(num_companies)
    generate_company_preference_data(num_companies)
    generate_company_info_data(num_companies, max_student_capacity)

def main():
    students = load_student_data()
    projects = load_project_data()
    students, projects, unmatched = match(students, projects)
    print("Total unmatched students: {}".format(unmatched))
    write_matches(students)

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--test':
            generate_mock_data(6, 40)
    except IndexError:
        pass
    main()
