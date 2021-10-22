import math
import json
from statistics import stdev
from math import floor

SCORING_CRITERIA = json.load(open("scoring_config.json"))
SENTIMENT_TO_VALUE = {
    "strongly disagree" : 1,
    "somewhat disagree": 2,
    "neither agree nor disagree": 3,
    "somewhat agree": 4,
    "strongly agree": 5,
    "not at all likely": 1,
    "a little likely": 2,
    "somewhat likely": 3,
    "likely": 4,
    "very likely": 5
}

class Project:

    def __init__(self, preference_data=None, capacity=30):
        if preference_data == None:
            self.organization = ""
            self.preferred_students = []
            self.excluded_students = []
        else:
            self.organization = preference_data['Organization']
            self.preferred_students = preference_data['Prefer'].split(" / ")
            for i in range(len(self.preferred_students)):
                self.preferred_students[i] = self.preferred_students[i].upper()
            self.excluded_students = preference_data['Exclude'].split(" / ")
        self.capacity = capacity
        self.supports_f1j1 = False
        self.student_matches = []

    def add_match(self, student):
        if len(self.student_matches) + 1 <= self.capacity:
            self.student_matches.append(student.legal_name)
            self.student_matches = list(set(self.student_matches))

    def add_project_info(self, project_info_data):
        self.capacity = int(project_info_data['Number of Students'].strip())
        self.supports_f1j1 = True if project_info_data['F1/J1'].strip() == "True" else False


    def diversity_score(self, students):
        '''
        A measure of how diverse the current set of students is. Can and
        should be modified to include more criteria.
        '''
        min_comfort_level = int(SCORING_CRITERIA["DIVERSITY-SCORING"]["overall_comfort_level"]["min"])
        max_comfort_level = int(SCORING_CRITERIA["DIVERSITY-SCORING"]["overall_comfort_level"]["max"])
        comfort_levels = [student.overall_comfort_level for student in students if student.legal_name in self.student_matches]
        frequencies = [comfort_levels.count(x) for x in range(min_comfort_level, max_comfort_level + 1)]
        return stdev(frequencies) / (stdev([self.capacity] + ([0] * (max_comfort_level - min_comfort_level))))

    def reached_capacity(self):
        return len(self.student_matches) == self.capacity

    def student_eligible(self, student):
        if student.legal_name in self.excluded_students:
            return False
        if (('F1' in student.visa_status or 'J1' in student.visa_status) and not self.supports_f1j1):
            return False
        return True

class Student:

    def __init__(self, id):
        self.id = id

        # Student application information
        self.legal_name =  ""
        self.gnumber = ""
        self.degree = ""
        self.credits_range = (0, 120) # (min, max)
        self.graduation_year = ""
        self.majors = []
        self.gpa_range = (2.0, 3.0) # (min, max)
        self.num_cs_courses = 0
        self.experience = False
        self.residency_status = ""
        self.commitment = False
        self.eligibility = False

        # Student enrollment information
        self.programming_languages = []
        self.interests = []
        self.overall_comfort_level = 3 # On a scale of 1 - 5, an average derived from sentiment questions
        self.available = False

        # Student preferences for projects
        self.preferred_projects = []
        self.project_match = ""
        self._score = 0

    def add_application_data(self, application_data):
        if application_data['Q4'].strip() == '' or application_data['Q2'].strip() == '':
            return False
        self.legal_name = (", ".join([application_data['Q4'].strip(), application_data['Q2'].strip()])).upper().strip()
        self.gnumber = application_data['Q7'].replace("G", "")
        self.degree = application_data['Q10']
        self.visa_status = ' '.join([application_data['Q32'].upper().strip(), application_data['Q32_4_TEXT'].upper().strip()])
        try:
            if "More than" in application_data['Q11']:
                self.credits_range = (91, math.inf)
            else:
                self.credits_range = (
                    int(application_data['Q11'].strip().replace("-", " ").split(" ")[0]),
                    int(application_data['Q11'].strip().replace("-", " ").split(" ")[1])
                    )
            self.gpa_range = (
                float(application_data['Q17'].split(" ")[0]),
                float(application_data['Q17'].split(" ")[2])
            )
        except ValueError as e:
            # print("No credits/GPA for student: {}".format(self.legal_name))
            pass

        self.graduation_year = application_data['Q12'].split(" ")[0]
        self.majors = list(set(application_data['Q14'].split(",") + [application_data['Q14_7_TEXT']] + [application_data['Q15']] + [application_data['Q15_12_TEXT']]))
        if "Other" in self.majors:
            self.majors.remove("Other")
        if "Other declared major; please specify:" in self.majors:
            self.majors.remove("Other declared major; please specify:")
        if "" in self.majors:
            self.majors.remove("")
        try:
            self.num_cs_courses = int(application_data['Q18'])
        except:
            self.num_cs_courses = 0
        self.experience = True if application_data['Q20'] == 'Yes' else False
        self.residency_status = application_data['Q32'] # One of: {US Citizen, permanent resident, F1 or J1, Other}
        self.commitment = True if application_data['Q29'].strip() != '' else False
        self.eligibility = True if application_data['Q39'].strip() != '' else False
        self.score()
        return True

    def print_student_info(self):
        print("------------ STUDENT {} ------------".format(self.id))
        print("Legal name: {}".format(self.legal_name))
        print("G-Number: {}".format(self.gnumber))
        print("Degree: {}".format(self.degree))
        print("Credits: {}".format(self.credits_range))
        print("Graduation year: {}".format(self.graduation_year))
        print("Majors: {}".format(self.majors))
        print("GPA range: {}".format(self.gpa_range))
        print("Number of CS courses taken: {}".format(self.num_cs_courses))
        print("Previous experience at computing internship: {}".format(self.experience))
        print("Overall comfort level: {}".format(self.overall_comfort_level))
        print("Employer preferences: {}".format(self.preferred_projects))

    def add_enrollment_data(self, enrollment_data):
        comfort_levels = [
            SENTIMENT_TO_VALUE[enrollment_data["Q11"].strip().lower()],
            SENTIMENT_TO_VALUE[enrollment_data["Q12"].strip().lower()],
            6 - SENTIMENT_TO_VALUE[enrollment_data["Q13"].strip().lower()],
            SENTIMENT_TO_VALUE[enrollment_data["Q14"].strip().lower()],
            SENTIMENT_TO_VALUE[enrollment_data["Q16"].strip().lower()],
            SENTIMENT_TO_VALUE[enrollment_data["Q17"].strip().lower()],
            SENTIMENT_TO_VALUE[enrollment_data["Q18"].strip().lower()]
        ]
        self.overall_comfort_level = floor(float(sum(comfort_levels)) / len(comfort_levels))
        self.available = True if len(enrollment_data["Q22"]) != 0 else False
        self.score()

    def add_preferences(self, preference_data):
        self.preferred_projects = preference_data['Preferences'].split(",")
        self.score()

    def score(self):
        ''' A measure of how much priority a student should be given to
            be matched to their preferences (to break ties) '''

        total_points = len(SCORING_CRITERIA["STUDENT-SCORING"].keys())
        points = 0
        if "degrees" in SCORING_CRITERIA["STUDENT-SCORING"] and self.degree in SCORING_CRITERIA["STUDENT-SCORING"]["degrees"]:
            points += 1
        if "credits" in SCORING_CRITERIA["STUDENT-SCORING"] and self.credits_range[0] >= SCORING_CRITERIA["STUDENT-SCORING"]["credits"]["min"]:
            points += 1
        if "graduation_year" in SCORING_CRITERIA["STUDENT-SCORING"] and self.graduation_year in SCORING_CRITERIA["STUDENT-SCORING"]["graduation_year"]:
            points += 1
        if "major" in SCORING_CRITERIA["STUDENT-SCORING"] and True in (major in SCORING_CRITERIA["STUDENT-SCORING"]["major"] for major in self.majors):
            points += 1
        if "gpa" in SCORING_CRITERIA["STUDENT-SCORING"] and self.gpa_range[0] >= SCORING_CRITERIA["STUDENT-SCORING"]["gpa"]["min"]:
            points += 1
        if "number_cs_courses" in SCORING_CRITERIA["STUDENT-SCORING"] and self.num_cs_courses in range(SCORING_CRITERIA["STUDENT-SCORING"]["number_cs_courses"]["min"], SCORING_CRITERIA["STUDENT-SCORING"]["number_cs_courses"]["max"] + 1):
            points += 1
        if "experience" in SCORING_CRITERIA["STUDENT-SCORING"] and self.experience == SCORING_CRITERIA["STUDENT-SCORING"]["experience"]:
            points += 1
        return float(points) / total_points

    def add_match(self, project):
        self.project_match = project.organization

    def matched(self):
        return self.project_match != ""
