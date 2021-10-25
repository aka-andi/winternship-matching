import random
import csv
import string
import os

num_enrolled_students = 40
qualtrics_fields = ['9/1/2020  9:17:00 PM', '9/1/2020  9:18:00 PM', 'Survey Preview', '*******', '100', '63', 'TRUE',
                    '9/1/2020  9:18:00 PM']
languages = ['CSS', 'C++', 'C#', 'HTML', 'Java', 'Javascript', 'Objective-C', 'Perl', 'PHP', 'Python', 'Ruby',
             'Scala', 'Swift']
technical_areas = ['Cybersecurity', 'Data Analysis', 'IT Support', 'Machine Learning or AI',
                   'Market Research or Strategy', 'Program Management', 'Product Design', 'Product Management',
                   'Software Engineering']
agreement_levels = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree',
                    'Somewhat agree', 'Strongly Agree']
likelihood_levels = ['Not at all likely', 'A little likely', 'Somewhat likely', 'Likely', 'Very Likely']
pronouns = ['she/her/hers', 'he/his/him', 'they/them/their', 'ze/zir/zis']

DATA_DIR = "../data"

def get_students():
    students = []
    student_applications = csv.DictReader(open('{}/student_applications.csv'.format(DATA_DIR), newline=''))
    for data in student_applications:
        name = (data['Q4'].strip() + ", " + data['Q2'].strip()).upper()
        try:
            int(data['Progress'])
        except ValueError:
            continue
        if name not in students:
            students.append(name)
    return students[:num_enrolled_students]


def generate_student_enrollment_data():
    with open(r'../data/student_enrollment.csv', 'w', newline='') as f:
        print("Writing student_enrollment.csv...")
        writer = csv.writer(f)
        students = get_students()
        header = ['StartDate','EndDate','Status','IPAddress','Progress','Duration (in seconds)','Finished','RecordedDate','ResponseId','RecipientLastName','RecipientFirstName','RecipientEmail','ExternalReference','LocationLatitude','LocationLongitude','DistributionChannel','UserLanguage','EMPLID','Q3','Q4','Q4_5_TEXT','Q5','Q6','Q7','Programming Languages','Q8_15_TEXT','Interests','Q9_10_TEXT','Q11','Q12','Q13','Q14','Q16','Q17','Q18','Q19','Q20_1','Q20_2','Q20_3','Q20_4','Q21','Q22','Q23']
        writer.writerow(header)
        for i in range(len(students)):
            row = []
            response_id = 'R_' + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            row.extend(qualtrics_fields)
            row.append(response_id)
            first_name = students[i].split(", ")[1]
            last_name = students[i].split(", ")[0]
            row.extend([last_name, first_name])
            row.append(first_name[0] + last_name + '@gmu.edu')
            row.extend(['******', '53.1234', '18.1234', 'preview', 'EN', '23701129', first_name[0] + last_name + '@gmu.edu'])
            row.extend([random.choice(pronouns), '', 'No', 'No', 'No'])
            num_languages = random.randint(0, 6)
            if num_languages > 0:
                row.extend([random.choices(languages, k=num_languages), ''])
            else:
                row.extend(['None', ''])
            row.extend([random.choices(technical_areas, k=random.randint(1, 7)), ''])
            row.extend([random.choice(agreement_levels), random.choice(agreement_levels), random.choice(agreement_levels),
                        random.choice(agreement_levels)])
            row.extend(
                [random.choice(likelihood_levels), random.choice(likelihood_levels), random.choice(likelihood_levels)])
            row.append(first_name + '.' + last_name + '@gmail.com')
            row.extend(['Point OfContact', 'pointofcontact@gmail.com', '789-456-1230', '123-456-7890'])
            row.extend([first_name + ' ' + last_name, first_name + ' ' + last_name, ''])
            writer.writerow(row)
        f.close()

def generate_student_preference_data(num_companies):
    companies = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_companies]
    for i in range(len(alphabet)):
        companies.append("Company {}".format(alphabet[i]))
    with open(r'../data/student_pref.csv', 'w', newline='') as f:
        print("Writing student_pref.csv...")
        students = get_students()
        writer = csv.writer(f)
        header = ['StartDate','EndDate','Status','IPAddress','Progress','Duration (in seconds)','Finished','RecordedDate','ResponseId','RecipientLastName','RecipientFirstName','RecipientEmail','ExternalReference','LocationLatitude','LocationLongitude','DistributionChannel','UserLanguage','First','Last','EMPLID','Email','Preferences','Q6_0_42_RANK','Q6_0_43_RANK','Q6_0_44_RANK','Q6_0_45_RANK','Q6_0_46_RANK','Q6_0_47_RANK','Q6_0_48_RANK','Q6_0_49_RANK','Q6_0_50_RANK','Q6_0_51_RANK']
        writer.writerow(header)
        for i in range(len(students)):
            row = []
            response_id = 'R_' + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            row.extend(qualtrics_fields)
            row.append(response_id)
            first_name = students[i].split(", ")[1]
            last_name = students[i].split(", ")[0]
            row.extend([last_name, first_name])
            row.append(first_name[0] + last_name + '@gmu.edu')
            row.extend(['******', '53.1234', '18.1234', 'preview', 'EN', first_name, last_name, '23701129', first_name[0] + last_name + '@gmu.edu'])

            random.shuffle(companies)
            rankings = companies[:random.choice(range(5, 11))]
            prefs = ",".join(rankings)
            row.append(prefs)
            row.extend(['', '', '', '', '', '', '', '', '', ''])
            writer.writerow(row)

        f.close()

def generate_company_preference_data(num_companies):
    companies = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_companies]
    for i in range(len(alphabet)):
        companies.append("Company {}".format(alphabet[i]))
    students = get_students()

    with open(r'../data/company_pref.csv', 'w', newline='') as f:
        print("Writing company_pref.csv...")
        header = ['V1','V2','V3','V4','V5','Q1','Q2','Q3','Organization','Prefer','Exclude']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(header)
        writer.writerow(header)
        for company in companies:
            row = []
            row.extend(['R_2zJc453NsdZgPPU', 'Default Response Set', '9/1/2020 20:11', '9/1/2020 20:19', '1', '1', 'Zahin Faruque', 'zfaruqu@gmu.edu', company])
            random.shuffle(students)
            idx = random.choice(range(1, 20))
            prefs = " / ".join(students[:idx])
            exclude = " / ".join(students[idx:random.choice(range(1, 20))])
            row.append(prefs)
            row.append(exclude)
            writer.writerow(row)
        f.close()

def generate_company_info_data(num_companies, max_student_capacity):
    companies = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_companies]
    for i in range(len(alphabet)):
        companies.append("Company {}".format(alphabet[i]))
    with open(r'../data/company_info.csv', 'w', newline='') as f:
        print("Writing company_info.csv...")
        header = ['Organization', 'Number of Students', 'Sponsored', 'F1/J1']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(header)
        for company in companies:
            writer.writerow([
                company,
                random.choice(range(1, max_student_capacity + 1)),
                random.choice(['True', 'False']),
                random.choice(['True', 'False'])
                ])
        f.close()

def generate_mock_data(num_companies=10, max_student_capacity=30):
    try:
        os.mkdir(DATA_DIR)
    except FileExistsError:
        pass
    try:
        print("Clearing old data...")
        os.remove("{}/company_pref.csv".format(DATA_DIR))
        os.remove("{}/company_info.csv".format(DATA_DIR))
        os.remove("{}/student_enrollment.csv".format(DATA_DIR))
        os.remove("{}/student_pref.csv".format(DATA_DIR))
    except FileNotFoundError as e:
        print(e)
        pass
    print("Generating mock data...")
    generate_student_enrollment_data()
    generate_student_preference_data(num_companies)
    generate_company_preference_data(num_companies)
    generate_company_info_data(num_companies, max_student_capacity)
