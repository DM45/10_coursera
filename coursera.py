import requests
import random
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_full_url_courses_list():
    url_courses_list = []
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    req_data = requests.get(url)
    courses_data = etree.fromstring(req_data.content)
    for up_elem in courses_data.getchildren():
        for down_elem in up_elem.getchildren():
            if down_elem.text:
                url_courses_list.append(down_elem.text)
    return url_courses_list


def get_random_url_courses_list(url_courses_list):
    number_to_select = 2
    list_of_random_url_courses = random.sample(
        url_courses_list, number_to_select)
    return list_of_random_url_courses


def get_courses_info(list_of_random_url_courses):
    full_courses_info = []
    for elem in list_of_random_url_courses:
        url = elem
        req_data = requests.get(url)
        full_courses_info.append(req_data.text)
    return full_courses_info


def get_nesessary_part_of_courses_info(courses_info):
    nesessary_courses_info = []
    for course in courses_info:
        soup = BeautifulSoup(course, "lxml")
        courses_name = (soup.find("h2", {
            "class": "headline-4-text course-title"})).text
        language = (
                soup.find("div", {"class": "rc-Language"})).text
        start_date = (soup.find("div", {
            "class": "startdate rc-StartDateString caption-text"})).text
        duration = "{}{}".format(len(soup.find_all("div", {
            "class": "week-heading body-2-text"})), ' week(s)')
        try:
            rating = (soup.find("div", {
                "class": "ratings-text bt3-visible-xs"})).text
        except AttributeError:
            rating = ""
        nesessary_courses_info.append(
                [courses_name, language, start_date, duration, rating])
    return nesessary_courses_info


def output_courses_info_to_xlsx(courses_info):
    filepath_to_save = 'courses_info.xlsx'
    wb = Workbook()
    ws = wb.active
    for row in courses_info:
        ws.append(row)
    wb.save(filepath_to_save)


if __name__ == '__main__':
    print("Please wait")
    full_url_courses_list = get_full_url_courses_list()
    random_url_courses_list = get_random_url_courses_list(
            full_url_courses_list)
    full_courses_info = get_courses_info(random_url_courses_list)
    nesessary_part_of_courses_info = get_nesessary_part_of_courses_info(
            full_courses_info)
    courses_info_to_xlsx = output_courses_info_to_xlsx(
            nesessary_part_of_courses_info)
    print("Work is done!")
