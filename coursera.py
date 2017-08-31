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
    number_to_select = 20
    list_of_random_url_courses = random.sample(
        url_courses_list, number_to_select)
    return list_of_random_url_courses


def get_course_info(list_of_random_url_courses):
    courses_info = []
    val_of_week_for_grammat = 1
    for elem in list_of_random_url_courses:
        url = elem
        req_data = requests.get(url)
        soup = BeautifulSoup(req_data.text, "lxml")
        courses_name = (soup.find("h2", {
            "class": "headline-4-text course-title"})).text
        language = (
                soup.find("div", {"class": "rc-Language"})).text
        start_date = (soup.find("div", {
            "class": "startdate rc-StartDateString caption-text"})).text
        weeks_count = len(soup.find_all("div", {
            "class": "week-heading body-2-text"}))
        if weeks_count > val_of_week_for_grammat:
            duration = "{}{}".format(weeks_count, " weeks")
        else:
            duration = "{}{}".format(weeks_count, " week")
        try:
            rating = (soup.find("div", {
            	"class": "ratings-text bt3-visible-xs"})).text
        except AttributeError:
            rating = ""
        courses_info.append([courses_name, language, start_date, duration, rating])
    return courses_info


def output_courses_info_to_xlsx(courses_info, filepath):
    wb = Workbook()
    ws = wb.active
    for row in courses_info:
        ws.append(row)
    wb.save(filepath)


if __name__ == '__main__':
    _filepath_to_save = input("Enter filepath with filename for save file: ")
    print("Please wait")
    _get_full_url_courses_list = get_full_url_courses_list()
    _get_random_url_courses_list = get_random_url_courses_list(
            _get_full_url_courses_list)
    _get_course_info = get_course_info(_get_random_url_courses_list)
    _output_courses_info_to_xlsx = output_courses_info_to_xlsx(
            _get_course_info, _filepath_to_save)
    print("Work is done!")
