# Matching Algorithm for BTT Winternships

Given a set of exclusion criterion from companies, match student and employer preferences to assign students to projects per company
* Companies have students to include / exclude (see data/company_pref.csv)
* Students have companies they prefer and can rank them in order
* Also note factors like F1/J1, Gov't ID, Sponsored Companies

## Current state
* Initial pass - compare if both student and employer have a pref for each other (thus match them)
* Second pass - match those with a pref
* Third pass - match leftovers with no successful prefs
* Does not take into account individual projects within a company, only has companies listed

### Concerns / Areas to Modify
* Equity - do all students get best matches?
* Fails when there are rank orders
* Algorithm can be complicated since we want the best for everybody
* Create team diversity using:
    * Academic Standing *questionable
    * Major Type
    * Gender
* Student shouldn’t match with company that has a project in a language they don’t know
* Treat projects as individuals, rather than the companies (if company has multiple projects they might pref one for specific project)
* Possibly allow students to exclude companies (so they get rid of those that don’t know languages)
* “Weighted Lottery” -> if one project is popular, use random
* Ingests a lot of data -> try to simplify from 5 files to less. Consider not using student application

## Tasks
- [x] Understand the codebase
- [x] Make it run
- [ ] Add comments for better readability
- [ ] Refactor code
- [ ] Create synthetic data to extend the current data (can write a script for this)
- [ ] Use real data (available Oct. 8) to test out/fix up algorithm