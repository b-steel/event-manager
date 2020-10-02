
import csv
import googleapiclient
from googleapiclient.discovery import build
from mako.template import Template
from mako.runtime import Context
import os
from os import path

print('\nEventManager Initialized\n')

def clean_zipcode(zc):
    return zc.rjust(5, '0')[0:5]

def legislators_by_zipcode(zc):
    with build('civicinfo', 'v2') as service: 
        with open('key.txt', 'r') as k:
            devkey = k.read()
        service._developerKey = devkey
        try:
            data = service.representatives().representativeInfoByAddress( address=zc
            , levels = 'country'
            , roles=['legislatorUpperBody', 'legislatorLowerBody']
            , includeOffices=True).execute()
            return data['officials']
        except googleapiclient.errors.HttpError as err:
            return 'You can find your representatives by visiting www.commoncause.org/take-action/find-elected-officials'


letter_template = Template(filename='template_letter.html', module_directory='/tmp/mako_modules')

# buf = StringIO()
# ctx = Context(buf, name="jack")
# mytemplate.render_context(ctx)
# print(buf.getvalue())

with open('event_attendees.csv', newline='') as csvfile:
    if csv.Sniffer().has_header(csvfile.read()):
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)
    else:
        reader = csv.reader(csvfile, dialect=dial)

    for row in reader:
        person_id = row[' ']
        name = row['first_Name']
        zipcode = clean_zipcode(row['Zipcode'])
        legislators =  legislators_by_zipcode(zipcode)
        personal_letter = letter_template.render(name=name, legislators=legislators)

        if not path.exists('output'): os.mkdir('output')
        filename = f'output/thanks_{person_id}.html'
        with open(filename, 'w') as file:
            file.write(personal_letter)


 
print('\nEventManager Finished')