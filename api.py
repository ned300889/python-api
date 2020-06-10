import requests
import mysql.connector
import numpy as np
import json
import filecmp
import os
import shutil
from os import path


def touch(location):
    with open(location, 'a'):
        os.utime(location, None)


old = '/tmp/response.json.bak'
new = '/tmp/response.json'
touch(new)

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
if path.exists(new):
    os.rename('/tmp/response.json', '/tmp/response.json.bak')

url = ""

payload = "{\n\t\"api_key\": \"\n}"
headers = {
    'Content-Type': 'application/json'
}
try:
    response = requests.request("POST", url, headers=headers, data=payload)
    with open('/tmp/response.json', 'w') as outfile:
        outfile.write(response.text)
        outfile.close()
except (IndexError, KeyError, TypeError):
    quit()

if filecmp.cmp(old, new, shallow=False):
    print("There are no new changes to be made")
    quit()
else:
    with open('/tmp/response.json') as json_file:
        data = json.load(json_file)
mycursor = mydb.cursor()

Applicant1 = (data["data"]["TermLife"]["Applicant1"])
Applicant2 = (data["data"]["TermLife"]["Applicant2"])
CI_Applicant1 = (data["data"]["CriticalInsurance"]["Applicant1"])
CI_Applicant2 = (data["data"]["CriticalInsurance"]["Applicant2"])

id_matrix = np.array([[Applicant1, 767, 768, 769, 770, 771],
                      [Applicant1, 419, 420, 421, 422, 423],
                      [Applicant1, 557, 558, 559, 560, 561],
                      [Applicant2, 781, 782, 783, 784, 785],
                      [Applicant2, 426, 427, 428, 429, 430],
                      [Applicant2, 564, 565, 566, 567, 568],
                      [CI_Applicant1, 774, 775, 776, 777, 778],
                      [CI_Applicant1, 607, 608, 609, 610, 611],
                      [CI_Applicant1, 640, 641, 642, 643, 644],
                      [CI_Applicant2, 788, 789, 790, 791, 792],
                      [CI_Applicant2, 666, 667, 668, 669, 670],
                      [CI_Applicant2, 647, 648, 649, 650, 651],
                      ])

counter = 0
for i in range(len(id_matrix)):
    for x in (range(1, 6)):
        mycursor.execute("UPDATE wphm_frm_fields SET description = %s WHERE id = %s", (id_matrix[i][0][counter]["html_content"], (id_matrix[i][x])))
        counter += 1
        if counter == 5:
            counter = 0
mydb.commit()
