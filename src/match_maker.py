from generate_data import generate_mock_data
from file_io import read_project_data, read_student_data, write_match_data
from entity_classes import Project, Student
import random
from math import inf
import sys

PASSES = 5 # Equivalent to the minimum number of preferences a student must provide

def get_interested_students(students, project, rank):
    ''' Returns a list of names of students who prefer the given project
        at the specified rank. '''
    students_ = sorted(list(students.values()), key=lambda x: x._score, reverse=True)
    interested = []
    for student in students_:
        if student.matched():
            continue
        if student.preferred_projects[rank] == project.organization and project.student_eligible(student):
            interested.append(student.legal_name)
    return interested

def add_matches(students, project):
    ''' Match the given students with the given project, while is available. '''
    for student in students:
        if not project.reached_capacity():
            project.add_match(student)
            student.add_match(project)

def get_optimal_students(project, interested_students, iterations=10):
    ''' Return the students that yield best overall student and diversity
        score for the project. '''
    if len(interested_students) == 0 or project.reached_capacity():
        return []
    num_required_students = project.capacity - len(project.student_matches)
    test_project = Project()
    optimal = -inf
    optimal_students = []
    for i in range(iterations):
        random.shuffle(interested_students)
        test_project.student_matches = project.student_matches + [student.legal_name for student in interested_students[:num_required_students]]
        average_student_score = sum([student._score for student in interested_students[:num_required_students]]) / len(interested_students[:num_required_students])
        diversity_score = test_project.diversity_score(interested_students)
        if (sum([average_student_score, diversity_score])/2) > optimal:
            optimal = sum([average_student_score, diversity_score])/2
            optimal_students = interested_students[:num_required_students]
    return optimal_students


def match_remaining_students(students, projects, unmatched):
    ''' Deal with unmatched students. '''
    # Sort the students by score
    if unmatched == 0:
        return students, projects, 0
    sorted_students = sorted(list(students.values()), key=lambda x: x._score, reverse=True)
    students_left = [student.legal_name for student in sorted_students if not(student.matched())]
    unmatched = len(students_left)
    while len(students_left) != 0:
        next_student_name = students_left[0] # Get the first priority student
        # Match the student with the first available and eligible project
        for project in projects.values():
            if not project.reached_capacity() and project.student_eligible(students[next_student_name]):
                add_matches([students[next_student_name]], project)
                students_left.pop(0)
                unmatched -= 1
        if not(students[next_student_name].matched()):
            students_left.pop(0)
    return students, projects, 0


def match(students, projects):
    ''' Run the matching algorithm on the given students and projects. '''
    # For each pass
    for n in range(PASSES):
        # For each available project
        for project in projects.values():
            if project.reached_capacity():
                continue
            # Grab all students that prefer project at rank n
            interested = get_interested_students(students, project, n)
            # Mutual preferences get priority
            mutual_preferences = [student for student in interested if student in project.preferred_students]
            random.shuffle(mutual_preferences)
            for student_name in mutual_preferences:
                add_matches([students[student_name]], project)
                interested.remove(student_name)
            # For the rest of available seats, find optimal students
            optimal_students = get_optimal_students(project, [student for student in students.values() if student.legal_name in interested])
            add_matches(optimal_students, project)
    # Deal with any unmatched students here
    unmatched = len([student for student in students.values() if not student.matched()])
    students, projects, unmatched = match_remaining_students(students, projects, unmatched)
    return students, projects, unmatched
