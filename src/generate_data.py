import random
import csv
import string

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

with open(r'./../data/student_enrollment.csv', 'a', newline='') as f:
    writer = csv.writer(f)

    for i in range(300):
        row = []
        response_id = 'R_' + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        row.extend(qualtrics_fields)
        row.append(response_id)
        first_name = ''.join(random.choices(string.ascii_letters, k=10))
        last_name = ''.join(random.choices(string.ascii_letters, k=10))
        row.extend(['Person', 'BTT'])
        row.append('BTTPerson@gmu.edu')
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
