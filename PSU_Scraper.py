#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 22:56:38 2019

@author: Austin
@purpose: Scrape all PSU Major, Minor and Certificate information 
"""
#!!! OPEN UP README DOCUMENT 
#Libraries
from bs4 import BeautifulSoup as bsp
import requests
import pandas as pd
import names
import re
import urllib2
import os
import cPickle as pickle
import time
start = time.time()

base_url = 'https://bulletins.psu.edu/undergraduate/colleges/'
output_directory = "data/"
#----------------------------------------------------
os.chdir("/Users/Austin/Documents/AIODA/Scraping")

#Some Notes!!!
#CAPITAL == Harrisburg
#----------------------------------------------------
''' Collect all course links from HTML using base_url '''
# connect to server, randomize user-agent tag to enable prolonged iterations
req = requests.get(base_url, headers=({'User-Agent' : names.get_full_name()}))
# get the html content from the webpage
r = req.content
# 'soup' it
soup = bsp(r, 'lxml')
# grab only the "a" tags in the code, loop through them
course_url_list = []
for x in soup.find_all('a'):
    try:
        # if the link is a valid university course description link, append it
        if re.match('/undergraduate/colleges/',x['href']):
            course_url_list.append(x['href'])
    except:
        # if it is not a valid university course description link, skip it
        continue

course_url_list.pop(0)

#Add the rest of the url name 
extenstion = "#majorsminorsandcertificatestext"
college_list= []
for i in range(0,len(course_url_list)):
    y = course_url_list[i] + extenstion
    college_list.append(y)
 
 

#Collects All Major/Minor/Certificate/Associate Degree Links 
''' Collect all course links from HTML using base_url '''
# connect to server, randomize user-agent tag to enable prolonged iterations
base_url = 'https://bulletins.psu.edu'
# begin loop through the subjectS links
urls = []
for link in college_list:
    url = base_url + link
    urls.append(url)
    
degree_list = []
for link in urls:
    req = requests.get(link , headers=({'User-Agent' : names.get_full_name()}))
# get the html content from the webpage
    r = req.content
# 'soup' it
    soup = bsp(r, 'lxml')



# begin loop through the subjects links
    for j in course_url_list:
        for x in soup.find_all('a'):
            try:
        # if the link is a valid university course description link, append it
                if re.match(j,x['href']):
                    degree_list.append(x['href'])
            except:
        # if it is not a valid university course description link, skip it
                continue
                   
#----------------------------------------------------
         
#link to get you to program requirements for each major/minor/cert

program_req = "#programrequirementstext"
program_req_list =[]
for r in degree_list:
    y = r + program_req
    program_req_list.append(y)

#Assigning URL Link 
base_url = 'https://bulletins.psu.edu'
# begin loop through the subjectS links
urls_major_minor = []
for link in program_req_list:
    url = base_url + link
    urls_major_minor.append(url)
    
#to print out only n amount
#degree_url=urls_major_minor[3000:5000] 

new_dict = {}

for course in urls_major_minor:
    course_list=[]
    list_page_details=[]
    
    page = urllib2.urlopen(course)
    soup = bsp(page, 'html.parser')
    
    #get Major/Minor/Certificate Names
    name_box = soup.find('h1', attrs={'class': 'page-title'}) #Credits for minor
    minor_name = name_box.text.strip() # strip() is used to remove starting and trailing
    course_list.append(minor_name)
    
    #get credits for minor - NOT WORKING 
    #name_box = soup.find('td', attrs={'class': 'column1'})
    #credits_minor = name_box.text.strip()
    
    #Get Minor Info
    #list_page_details=[]
    for tr in soup.find_all('tr')[2:]:
        tds = tr.find_all('td')
        elem = tr.text.strip()
        elem = elem.replace(u'\xa0', u' ')
        elem = elem.replace(u'\u2020', u' ')
        elem = elem.replace(u'\u2021', u' ')
        elem = elem.replace(u'\u201c', u' ')
        elem = elem.replace(u'\u201d', u' ')
        elem = elem.replace(u'\u201e', u' ')
        elem = elem.replace(u'\u201f', u' ')
        elem = elem.replace(u'\xbf', u' ')
        elem = elem.replace(u'\u2019', u' ')
        elem = elem.replace(u'\xbf', u' ')
        elem = elem.replace(u'\u2013', u' ')
        elem=str(elem)
        list_page_details.append(elem)
    #degree_credits = list_page_details[1]
    
    #get prescribed courses
    #Try to make dictionary
    for i in list_page_details:
        if 'Prescribed Courses' in i: 
            key = i 
            course_list.append(i) 
            
        if 'Additional Courses' in i: 
            key = i
            course_list.append(i)

        if "Select" in i:
            key = i
            course_list.append(i)
        
        #Below works ok
        match = re.findall("[A-Z\s](?:.{4}|.{5}|.{3}|.{2})\d{1,}", i)
        
        #match = re.findall("[A-Z\s](?:.{4}|.{5}|.{3}|.{2})\d{}", i)

        course_list.append(match)
                       
       
    
    
    #Clean Up List
    course_list = filter(None, course_list)
    degree_name = course_list[0]
    
    test_list = str(course_list).strip(',')
    test_list = test_list.replace("Course3", "")
    test_list = test_list.replace("Course13", "")
    test_list = test_list.replace("[", "")
    test_list = test_list.replace("]", "")
    test_list = test_list.replace("Making4", "")
    test_list = test_list.replace("System3", "")
    test_list = test_list.replace("  33", "")
    test_list = test_list.replace("100","")
    test_list = test_list.replace(" ","")
    test_list = test_list.replace("'", '')
    test_list = test_list.split(",")
    test_list = filter(None, test_list)
    
    #Take Uppercase values only
    
    trial = []
    for t in test_list:
        if (t.isupper() ==True):
            trial.append(t)
    
    trial_list= list(set(trial))
    
    
    
    d1 = {degree_name: trial_list}
    # adds element with key 3
    new_dict.update(d1)

pickle.dump(new_dict, open( "Courses.p", "wb" ))
#----------------------------------------------------
     
#----------------------------------------------------

''' Loop through each subject link, save the major information '''
base_url = 'https://bulletins.psu.edu'
# begin loop through the subjectS links
for link in college_list:
    url = base_url + link
    #print(url)
    major = url.split("/")[-2:][0].upper()
    print "Getting data from {}".format(major)
    # connect to server, randomize user-agent tag to enable prolonged iterations (makes it harder for bots to detect)
    req = requests.get(url, headers=({'User-Agent':names.get_full_name()}))
    # get the html content from the webpage
    r = req.content
    # 'soup' it
    soup = bsp(r, 'lxml')
    # Get Degree information
    degree_info = soup.find_all('div', class_='courseblock')






end = time.time()
print(end - start,"seconds")


