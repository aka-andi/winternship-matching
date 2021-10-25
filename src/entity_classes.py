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
        ''' Project constructor. '''
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
        ''' Add given student to project's roster. '''
        if len(self.student_matches) + 1 <= self.capacity:
            self.student_matches.append(student.legal_name)
            self.student_matches = list(set(self.student_matches))

    def add_project_info(self, data):
        ''' Add data from "company_pref.csv" to the project. '''
        self.capacity = int(data['Number of Students'].strip())
        self.supports_f1j1 = True if data['F1/J1'].strip() == "True" else False


    def diversity_score(self, students):
        ''' Return a score that represents the diversity of the current
            student roster. Tunable to include other criteria. '''
        min_comfort_level = int(SCORING_CRITERIA["DIVERSITY-SCORING"]["overall_comfort_level"]["min"])
        max_comfort_level = int(SCORING_CRITERIA["DIVERSITY-SCORING"]["overall_comfort_level"]["max"])
        comfort_levels = [student.overall_comfort_level for student in students if student.legal_name in self.student_matches]
        frequencies = [comfort_levels.count(x) for x in range(min_comfort_level, max_comfort_level + 1)]
        return stdev(frequencies) / (stdev([self.capacity] + ([0] * (max_comfort_level - min_comfort_level))))

    def reached_capacity(self):
        ''' Return true if the project has reached its limit for its roster. '''
        return len(self.student_matches) == self.capacity

    def student_eligible(self, student):
        ''' Determine if the given student is eligible to participate in
            the project.'''
        if student.legal_name in self.excluded_students:
            return False
        if (('F1' in student.visa_status or 'J1' in student.visa_status) and not self.supports_f1j1):
            return False
        return True

class Student:

    def __init__(self):
        # Student application information
        self.legal_name =  ""
        self.student_id = ""
        self.degree = ""
        self.credits_range = (0, 120) # (min, max)
        self.graduation_year = ""
        self.majors = []
        self.gpa_range = (2.0, 3.0) # (min, max)
        self.num_cs_courses = 0
        self.experience = False
        self.residency_status = ""
        self.commitment = False
        self.visa_status = ""
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

    def add_application_data(self, data):
        ''' Add student data from "student_applications.csv" '''
        if data['Q4'].strip() == '' or data['Q2'].strip() == '':
            return False
        self.legal_name = (", ".join([data['Q4'].strip(), data['Q2'].strip()])).upper().strip()
        self.student_id = data['Q7'].replace("G", "")
        self.degree = data['Q10']
        self.visa_status = ' '.join([data['Q32'].upper().strip(), data['Q32_4_TEXT'].upper().strip()])
        try:
            if "More than" in data['Q11']:
                self.credits_range = (91, math.inf)
            else:
                self.credits_range = (
                    int(data['Q11'].strip().replace("-", " ").split(" ")[0]),
                    int(data['Q11'].strip().replace("-", " ").split(" ")[1])
                    )
            self.gpa_range = (
                float(data['Q17'].split(" ")[0]),
                float(data['Q17'].split(" ")[2])
            )
        except ValueError as e:
            # print("No credits/GPA for student: {}".format(self.legal_name))
            pass

        self.graduation_year = data['Q12'].split(" ")[0]
        self.majors = list(set(data['Q14'].split(",") + [data['Q14_7_TEXT']] + [data['Q15']] + [data['Q15_12_TEXT']]))
        if "Other" in self.majors:
            self.majors.remove("Other")
        if "Other declared major; please specify:" in self.majors:
            self.majors.remove("Other declared major; please specify:")
        if "" in self.majors:
            self.majors.remove("")
        try:
            self.num_cs_courses = int(data['Q18'])
        except:
            self.num_cs_courses = 0
        self.experience = True if data['Q20'] == 'Yes' else False
        self.residency_status = data['Q32'] # One of: {US Citizen, permanent resident, F1 or J1, Other}
        self.commitment = True if data['Q29'].strip() != '' else False
        self.eligibility = True if data['Q39'].strip() != '' else False
        self.score()
        return True

    def add_enrollment_data(self, data):
        ''' Add student data from "student_enrollments.csv" '''
        comfort_levels = [
            SENTIMENT_TO_VALUE[data["Q11"].strip().lower()],
            SENTIMENT_TO_VALUE[data["Q12"].strip().lower()],
            6 - SENTIMENT_TO_VALUE[data["Q13"].strip().lower()],
            SENTIMENT_TO_VALUE[data["Q14"].strip().lower()],
            SENTIMENT_TO_VALUE[data["Q16"].strip().lower()],
            SENTIMENT_TO_VALUE[data["Q17"].strip().lower()],
            SENTIMENT_TO_VALUE[data["Q18"].strip().lower()]
        ]
        self.overall_comfort_level = floor(float(sum(comfort_levels)) / len(comfort_levels))
        self.available = True if len(data["Q22"]) != 0 else False
        self.score()

    def add_preferences(self, data):
        ''' Add student's preferences from "student_prefs.csv" '''
        self.preferred_projects = data['Preferences'].split(",")
        self.score()

    def score(self):
        ''' Return a score for the student (used to prioritize which students
            get their first preferences). Tweakable to include other criteria. '''

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
        ''' Assign the given project to the student. '''
        self.project_match = project.organization

    def matched(self):
        ''' Return true if the student has already been matched. '''
        return self.project_match != ""
