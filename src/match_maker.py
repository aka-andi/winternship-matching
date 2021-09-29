from entity_classes import Project, Student

def get_mutually_eligible(students, projects):
    students_to_projects = {}
    for student in students:
        for proj_id in student.eligible_project_ids:
            if student in projects[proj_id]:
                students_to_projects[student] = proj_id
    return students_to_projects

def match(student_data, project_data):
    matches = {} # Dictionary mapping student full name, email with project

    projects = []
    id = 0
    for project in project_data:
        projects.append(Project(project_data[project], id=id))
        id += 1
    students = ''
    id = 0
    for student in student_data:
        students.append(Student(student_data[student], id=id))
        id += 1
    students.get_eligible(projects)
    projects.get_eligible(students)

    # Ignore preferences first, rule out immediate no-nos
    # Get entries where both project and student are eligible for one another
    student_to_project = get_mutually_eligible(students, projects)

    # Match by preference and ranking


    return matches
