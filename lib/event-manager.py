
import csv
import googleapiclient
from googleapiclient.discovery import build
from mako.template import Template
from mako.runtime import Context
import os
from os import path
import time 
import config
from collections import Counter


print('\nEventManager Initialized\n')

def clean_zipcode(zc):
    return zc.rjust(5, '0')[0:5]

def clean_phone_numbers(n):
    if len(n) == 10:
        return n
    elif len(n) == 11 and n[0]==1:
        return n[1:]
    else:
        return 'Invalid Number'

def get_hour_from_timestamp(tstamp):
    return time.strptime(tstamp, r'%m/%d/%y %H:%M').tm_hour

def get_day_from_timestamp(tstamp):
    return time.strftime('%A', time.strptime(tstamp, r'%m/%d/%y %H:%M'))


def legislators_by_zipcode(zc):
    with build('civicinfo', 'v2') as service: 
        service._developerKey = config.api_key
        try:
            data = service.representatives().representativeInfoByAddress( address=zc
            , levels = 'country'
            , roles=['legislatorUpperBody', 'legislatorLowerBody']
            , includeOffices=True).execute()
            return data['officials']
        except googleapiclient.errors.HttpError as err:
            return 'You can find your representatives by visiting www.commoncause.org/take-action/find-elected-officials'



def save_thank_you_letter(person_id, form_letter):
    if not path.exists('output'): os.mkdir('output')
    filename = f'output/thanks_{person_id}.html'
    with open(filename, 'w') as file:
        file.write(form_letter)

def mailing_list_actions():

    with open('event_attendees.csv', newline='') as csvfile:
        if csv.Sniffer().has_header(csvfile.read()):
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
        else:
            reader = csv.reader(csvfile, dialect=dial)

        #Create letter template    
        letter_template = Template(filename='template_letter.html', module_directory='/tmp/mako_modules')

        #Registration Time / Date Info
        reg_time = []
        reg_day = []
        for row in reader:
            person_id = row[' ']
            reg_time.append(get_hour_from_timestamp(row['RegDate']))
            reg_day.append(get_day_from_timestamp(row['RegDate']))
            name = row['first_Name']
            zipcode = clean_zipcode(row['Zipcode'])
            legislators =  legislators_by_zipcode(zipcode)
            personal_letter = letter_template.render(name=name, legislators=legislators)
            save_thank_you_letter(person_id, personal_letter)
    return reg_time, reg_day
    
reg_time, reg_day = mailing_list_actions()
t_count = Counter(reg_time)
d_count = Counter(reg_day)
print(t_count)
print(d_count)

        

 
print('\nEventManager Finished')