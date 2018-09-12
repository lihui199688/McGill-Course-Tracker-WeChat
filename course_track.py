# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import itchat

# load user info

with open('username_pswd_crs.txt') as f:
    lines = f.readlines()

itchat.auto_login()



while True:

    # get to course page
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(30)
    course_db = dict()
    driver.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")
    driver.find_element_by_id("mcg_un").click()
    driver.find_element_by_id("mcg_un").clear()
    driver.find_element_by_id("mcg_un").send_keys(lines[0].lstrip().rstrip())
    driver.find_element_by_id("mcg_pw").click()
    driver.find_element_by_id("mcg_pw").clear()
    driver.find_element_by_id("mcg_pw").send_keys(lines[1].lstrip().rstrip())

    # Select Term: current term only
    driver.find_element_by_id("mcg_un_submit").click()
    driver.find_element_by_link_text("Student Menu").click()
    driver.find_element_by_link_text("Registration Menu").click()
    driver.find_element_by_link_text("Step 2: Search Class Schedule and Add Course Sections").click()
    driver.find_element_by_xpath("/html/body/div[3]/form/input[3]").click()

    # select department
    driver.find_element_by_xpath("//option[@value='"+lines[4].lstrip().rstrip()+"']").click()
    driver.find_element_by_xpath("/html/body/div[3]/form/input[17]").click()

    # select course
    rows = driver.find_elements_by_tag_name("tr")
    i=-4
    for row in rows:
        try:
            course_num = row.text.split()[0]
        except IndexError:
            continue

        if course_num == lines[5].lstrip().rstrip():
            row.find_elements(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr['+str(i)+']/td[3]/form/input[30]')[0].click()
            break
        i=i+1

    # select crn
    rows = driver.find_elements_by_tag_name("tr")
    info_dict = {}

    for row in rows:
        if lines[6].rstrip().lstrip() in row.text:
            #get info from data row
            rem = row.find_elements_by_tag_name("td")[12].text
            status = row.find_elements_by_tag_name("td")[19].text
            info_dict["spots"] = rem
            info_dict["status"] = status

    print(info_dict)

    # send wechat
    users = itchat.search_friends(name=u'{}'.format(lines[3].lstrip().rstrip()))
    userName = users[0]['UserName']
    itchat.send('course: {} {}, remaining: {}, status: {}'.format(lines[4].lstrip().rstrip(), lines[5], info_dict["spots"], info_dict["status"]), toUserName=userName)

    # turn off browser
    driver.quit()
    time.sleep(int(lines[2]))

