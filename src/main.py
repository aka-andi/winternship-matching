from generate_data import generate_mock_data
from file_io import read_project_data, read_student_data, write_match_data
from match_maker import match
import sys

def main():
    students = read_student_data()
    projects = read_project_data()
    students, projects, unmatched = match(students, projects)
    print("Total unmatched students: {}".format(unmatched))
    write_match_data(students)

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--test':
            generate_mock_data(6, 40)
    except IndexError:
        pass
    main()
