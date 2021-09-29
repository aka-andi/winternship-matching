from file_io import load_students, load_companies
from match_maker import match


def load_student_data():
    ''' Stub for loading student data '''
    return []

def load_project_data():
    ''' Stub for loading project data '''
    return []

def main():

    students = load_student_data()
    projects = load_project_data()

    students, projects = match(students, projects)


if __name__ == "__main__":
    main()
