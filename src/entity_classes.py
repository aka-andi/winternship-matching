class Project:

    def __init__(self, data, id):
        self.id = id

        # Project information
        self.organization = data['organization']
        self.location = data['location'] # GPS coordinates
        self.remote = data['remote'] # True or false

        # Project constraints
        self.max_students = data['constraints']['max-students']
        self.major_constraints= data['constraints']["majors"]
        self.skillset_constraints = data['constraints']["skillsets"]
        self.class_constraints = data['constraints']["classes"]
        self.school_constraints = data['constraints']["schools"]
        self.gpa_constraints = data['constraints']["min-GPA"]

        # Match results
        self.current_student_ids = []
        self.eligible_student_ids = []

    def major_ok(self, major):
        return True

    def skillset_ok(self, skillset):
        return True

    def year_ok(self, year):
        # year = (1, 2, 3 or 4) = (freshman, sophomore, junior, senior)
        return True

    def school_ok(self, school):
        return True

    def gpa_ok(self, GPA):
        return True

    def get_eligible(self, students):
        for student in students:
            evaluation = [
                self.major_ok(student.major),
                self.skillset_ok(student.skillset),
                self.year_ok(student.year),
                self.school_ok(student.school),
                self.gpa_ok(student.GPA)
            ]
            if evaluation == [True, True, True, True, True]:
                self.eligible_student_ids.append(student.id)

class Student:

    def __init__(self, data, id):
        self.id = id

        # Student information
        self.name = data['name']
        self.school = data['school']
        self.major = data['major']
        self.year = data['year']
        self.gpa = data['GPA']
        self.highest_math = data['highest_math']

        # Student constraints
        self.location_constraints = data['constraints']['location']
        self.pay_constraints = data['constraints']['pay']
        self.remote_work = data['constraints']['remote']

        # Match results
        self.eligible_project_ids = []


    def location_ok(self, project):
        return True

    def pay_ok(self, project):
        return True

    def remote_work_ok(self, project):
        return True

    def get_eligible(self, projects):
        for project in projects:
            evaluation = [
                self.location_ok(project),
                self.pay_ok(project),
                self.remote_work_ok(project)
            ]
            if evaluation == [True, True, True]:
                self.eligible_project_ids.append(project.id)
