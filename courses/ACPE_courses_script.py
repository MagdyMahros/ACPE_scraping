"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 18-11-20
    * description:This script extracts the corresponding undergraduate courses details and tabulate it.
"""

import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter as dura

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/ACPE_courses_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/ACPE_courses.csv'

course_data = {'Level_Code': '', 'University': 'Australian College of Physical Education', 'City': '',
               'Country': 'Australia', 'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD',
               'Currency_Time': 'year', 'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': '', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '',
               'Prerequisite_2_grade': '6.5', 'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '',
               'Availability': '', 'Description': '', 'Career_Outcomes': '', 'Online': '', 'Offline': '',
               'Distance': 'no', 'Face_to_Face': '', 'Blended': '', 'Remarks': '',
               'Subject_Description_1': '', 'Subject_or_Unit_2': '', 'Subject_Objective_2': '',
               'Subject_Description_2': '',
               'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

possible_cities = {'online': 'Online', 'mixed': 'Online', 'sydney': 'Sydney'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    remarks_list = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE
    title = soup.find('h1')
    if title:
        course_data['Course'] = title.get_text()
        print('COURSE TITLE: ', course_data['Course'])

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_data['Course']:
                    course_data['Level_Code'] = i
        print('COURSE LEVEL CODE: ', course_data['Level_Code'])

        # DECIDE THE FACULTY
        for i in faculty_key:
            for j in faculty_key[i]:
                if j.lower() in course_data['Course'].lower():
                    course_data['Faculty'] = i
        print('COURSE FACULTY: ', course_data['Faculty'])

        # COURSE LANGUAGE
        for language in possible_languages:
            if language in course_data['Course']:
                course_data['Course_Lang'] = language
            else:
                course_data['Course_Lang'] = 'English'
        print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # DURATION
    dura_title = soup.find('strong', text=re.compile('Course duration'))
    if dura_title:
        duration = dura_title.find_next_sibling('small')
        if duration:
            duration_text = duration.get_text().lower().strip()
            if 'full time' in duration_text or 'full-time' in duration_text:
                course_data['Full_Time'] = 'yes'
            else:
                course_data['Full_Time'] = 'no'
            if 'part time' in duration_text or 'part-time' in duration_text:
                course_data['Part_Time'] = 'yes'
            else:
                course_data['Part_Time'] = 'no'
            print('FULL TIME/PART TIME: ', course_data['Full_Time'] + ' / ' + course_data['Part_Time'])
            converted_duration = dura.convert_duration(duration_text)
            if converted_duration is not None:
                duration_l = list(converted_duration)
                if duration_l[0] == 1 and 'Years' in duration_l[1]:
                    duration_l[1] = 'Year'
                if duration_l[0] == 1 and 'Months' in duration_l[1]:
                    duration_l[1] = 'Month'
                course_data['Duration'] = duration_l[0]
                course_data['Duration_Time'] = duration_l[1]
                print('COURSE DURATION: ', str(duration_l[0]) + ' / ' + duration_l[1])

    # STUDY MODE
    study_mode_title = dura_title = soup.find('strong', text=re.compile('Study mode'))
    if study_mode_title:
        study_mode = study_mode_title.find_next_sibling('small')
        if study_mode:
            study_mode_text = study_mode.get_text().lower().strip()
            if 'face to face' in study_mode_text:
                course_data['Face_to_Face'] = 'yes'
                course_data['Offline'] = 'yes'
            else:
                course_data['Face_to_Face'] = 'no'
                course_data['Offline'] = 'no'
            if 'blended' in study_mode_text:
                course_data['Blended'] = 'yes'
                actual_cities.append('mixed')
            else:
                course_data['Blended'] = 'no'
            if 'online' in study_mode_text:
                course_data['Online'] = 'yes'
                actual_cities.append('online')
            else:
                course_data['Online'] = 'no'
            print('STUDY MODE: OFFLINE / FACE TO FACE: ' + course_data['Offline'] + '/' + course_data['Face_to_Face'] +
                  ' BLENDED: ' + course_data['Blended'] + ' ONLINE: ' + course_data['Online'] + ' DISTANCE: ' +
                  course_data['Distance'])

    # DESCRIPTION
    desc_title = soup.find('h3', text=re.compile('About the course', re.IGNORECASE))
    if desc_title:
        description = desc_title.find_next('p')
        if description:
            course_data['Description'] = description.get_text().strip()
            print('DESCRIPTION: ', course_data['Description'])

    # CAREER OUTCOMES
    career_title = soup.find('h3', text=re.compile('Career opportunities', re.IGNORECASE))
    if career_title:
        career_list = []
        career_ul = career_title.find_next('ul', class_='iconlist')
        if career_ul:
            career_li = career_ul.find_all('li')
            if career_li:
                for li in career_li:
                    career_list.append(li.get_text().strip())
                career_list = ' / '.join(career_list)
                course_data['Career_Outcomes'] = career_list
                print('CAREER OUTCOMES: ', course_data['Career_Outcomes'])

    # CITY
    actual_cities.append('sydney')

    # UNITS
    sem_1 = soup.find('h4', text=re.compile('Semester 1', re.IGNORECASE))
    sem_2 = soup.find('h4', text=re.compile('Semester 2', re.IGNORECASE))
    sem_3 = soup.find('h4', text=re.compile('Semester 3', re.IGNORECASE))
    sem_4 = soup.find('h4', text=re.compile('Semester 4', re.IGNORECASE))
    sem_5 = soup.find('h4', text=re.compile('Semester 5', re.IGNORECASE))
    sem_6 = soup.find('h4', text=re.compile('Semester 6', re.IGNORECASE))
    sem_7 = soup.find('h4', text=re.compile('Semester 7', re.IGNORECASE))
    sem_8 = soup.find('h4', text=re.compile('Semester 8', re.IGNORECASE))

    i = 1
    if sem_1:
        ul = sem_1.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_2:
        ul = sem_2.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_3:
        ul = sem_3.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_4:
        ul = sem_4.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_5:
        ul = sem_5.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_6:
        ul = sem_6.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_7:
        ul = sem_7.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1
    if sem_8:
        ul = sem_8.find_next_sibling('ul')
        if ul:
            li_list = ul.find_all('li')
            for li in li_list:
                course_data['Subject_or_Unit_' + str(i)] = li.get_text()
                i += 1

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance',
                          'Face_to_Face', 'Blended', 'Remarks', 'Subject_or_Unit_1', 'Subject_Objective_1',
                          'Subject_Description_1',
                          'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('ACPE_courses_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
