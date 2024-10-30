import csv
import json
import random
import os

program_status = False
first_run = True


# Get class members from filepath
def get_class(cvs_file_path, dict_key, json_file_path):
    data = {}
    with open(cvs_file_path, encoding='utf-8') as file:
        content = csv.DictReader(file)
        for row in content:
            key = row[dict_key]
            data[key] = row

    with open(json_file_path, 'w', encoding='utf-8') as jsonF:
        jsonF.write(json.dumps(data, indent=4))
    return data


# Get Mentors: People that registered to be mentors
def get_mentors(cvs_file_path, dict_key, json_file_path):
    data = {}
    with open(cvs_file_path, encoding='utf-8') as file:
        content = csv.DictReader(file)
        for row in content:
            key = row[dict_key]
            data[key] = row

    with open(json_file_path, 'w', encoding='utf-8') as jsonF:
        jsonF.write(json.dumps(data, indent=4))
    return data


# Pair Mentees to Mentors
def mentor_mentee_pair(year_dict, mentors_name, mentee_list, mentors_year, mentees_to_mentor_size=2):
    mentors_dict = {}
    for mentors in year_dict:
        if len(mentee_list) > 1:
            mentees_choice = random.sample(mentee_list, mentees_to_mentor_size)
        elif len(mentee_list) == 1:
            mentees_choice = mentee_list
            print("This is the remaining mentee")
            print(mentee_list)
        else:
            print("No more Mentee")
            return False
        [mentee_list.remove(mentees) for mentees in mentees_choice]
        mentors_dict[year_dict[mentors][mentors_name]] = mentees_choice
        with open(f"../Mentor_mentee_pair/Pair_for_{mentors_year}.json", 'w', encoding='utf-8') as file:
            file.write(json.dumps(mentors_dict, indent=4))
    return mentors_dict


# Store mentees that are not yet assigned to a mentor
def store_remaining_mentees(mentee_list, remaining_mentees_filepath, mentee_year):
    remaining_mentees_dict = {}
    for remaining_mentees in mentee_list:
        for number in mentee_year:
            if remaining_mentees[1] == mentee_year[number]['Matric No']:
                remaining_mentees_dict[number] = mentee_year[number]
    with open(remaining_mentees_filepath, 'w', encoding='utf-8') as file:
        file.write(json.dumps(remaining_mentees_dict, indent=4))
    return remaining_mentees_dict


def get_class_from_remaining_mentees(filepath):
    with open(filepath) as file:
        content = json.load(file)
    return content


start = input("Do you want to start the program? ").lower()
if start == 'yes':
    program_status = True
else:
    program_status = False


year_3 = get_class("../Class/cvsFiles/300L.csv", "SN", "../Class/jsonFiles/300L.json")
year_4 = get_class("../Class/cvsFiles/400L.csv", "SN", "../Class/jsonFiles/400L.json")
year_5 = get_class("../Class/cvsFiles/500L.csv", "SN", "../Class/jsonFiles/500L.json")

year_4_mentors = get_mentors("../Registered_Mentors/cvsFiles/400L.csv", "SN",
                             "../Registered_Mentors/jsonFiles/400L.json")
year_5_mentors = get_mentors("../Registered_Mentors/cvsFiles/500L.csv", "SN",
                             "../Registered_Mentors/jsonFiles/500L.json")

while program_status is True:
    # Get mentees list
    if first_run is True:
        mentees_for_year5_list = [[year_4[no]['First Name'], year_4[no]['Matric No']] for no in year_4] + \
                                 [[year_3[no]['FULL NAMES'], year_3[no]['Matric No']] for no in year_3]
        mentees_for_year4_list = [[year_3[no]['FULL NAMES'], year_3[no]['Matric No']] for no in year_3]
    else:
        mentees_for_year5_list = [[year_4[no]['First Name'], year_4[no]['Matric No']] for no in remaining_mentees_year4] + \
                                 [[year_3[no]['FULL NAMES'], year_3[no]['Matric No']] for no in remaining_mentees_year3]
        mentees_for_year4_list = [[year_3[no]['FULL NAMES'], year_3[no]['Matric No']] for no in remaining_mentees_year3]

        print(f"New Mentee list for year 5: {mentees_for_year5_list}")
        print(f"Total number of New Mentee list for year 5: {len(mentees_for_year5_list)}")
        print(f"New Mentee list for year 4: {mentees_for_year4_list}")
        print(f"Total number of New Mentee list for year 4: {len(mentees_for_year4_list)}")

    print(f"Original Mentee list for year 5: {mentees_for_year5_list}")
    print(f"Total number of Original Mentee list for year 5: {len(mentees_for_year5_list)}")
    print(f"Original Mentee list for year 4: {mentees_for_year4_list}")
    print(f"Total number of Original Mentee list for year 4: {len(mentees_for_year4_list)}")
    print('\n')

    mentor_mentee_year5_dict = mentor_mentee_pair(year_5_mentors, "FIRST NAME AND OTHER NAME", mentees_for_year5_list, "500L")
    if mentor_mentee_year5_dict is False:
        print('END')
        program_status = False
        break
    else:
        for people in mentor_mentee_year5_dict:
            for individual in mentor_mentee_year5_dict[people]:
                if individual in mentees_for_year4_list:
                    mentees_for_year4_list.remove(individual)

    mentor_mentee_year4_dict = mentor_mentee_pair(year_4_mentors, "First Name", mentees_for_year4_list, "400L")
    if mentor_mentee_year4_dict is False:
        program_status = False
        break

    remaining_mentees_year4 = store_remaining_mentees(mentees_for_year5_list, "../Remaining_mentees/400L.json", year_4)
    remaining_mentees_year3 = store_remaining_mentees(mentees_for_year4_list, "../Remaining_mentees/300L.json", year_3)
    first_run = False

    print(f"Mentor-Mentee pair for 500L: {mentor_mentee_year5_dict}")
    print(f"Mentor-Mentee pair for 400L: {mentor_mentee_year4_dict}")
    print('\n')
    print(f"Remaining mentees in 300L: {remaining_mentees_year3}")
    print(f"The total number of mentees in 300L left is {len(remaining_mentees_year3)}")
    print(f"Remaining mentees in 400L: {remaining_mentees_year4}")
    print(f"The total number of mentees in 400L left is {len(remaining_mentees_year4)}")

    print('\n')

    contd = True
    while contd:
        to_continue = input("Do you want to continue? ").lower()
        if to_continue == 'no':
            program_status = False
            contd = False
        elif to_continue == 'yes':
            program_status = True
            contd = False
        else:
            contd = True
