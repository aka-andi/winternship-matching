# Matching Algorithm for BTT Winternships

## How to Run
Download files student_applications.csv, student_enrollments.csv, student_prefs.csv,
company_info.csv, and company_pref.csv. Ensure that they are under the "data"
folder. Under the "src" folder run:
> python3 main.py


The matches should appear under "results" folder.

## Configuration
The **scoring_config.json** file can be used to specify criteria by which the
algorithm will prioritize students in matching with their first preferences. For
example, by default the configuration file contains bounds for GPA. This means
that students with GPAs in that range will have a higher chance of being
matched to their top choice. The file also specifies criteria which diversity is
measured in a particular roster for a project/company. This scoring
criteria can be modified by the user to their liking.
