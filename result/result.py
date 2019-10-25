#!/usr/bin/env python3

import sys
import json
import requests as rq

def grades(data):
    grade = ""
    for semester in data:
        # print(semester["semester"])
        grade += f"\nSemester: {semester['semester']}\nCGPA: {round(semester['sgpa'], 3)}\n"
        # print("Semester: ", semester["semester"], "\nCGPA: ", semester["sgpa"])
        for sub in semester["subject"]:
            # grade[semester["semester"]]["Subject"] = sub["subject_name"]
            # grade[semester["semester"]]["Result"] = sub["result"]
            # print("Subject: ", sub["subject_name"], "\nResult: ", sub["result"])
            grade += f"Subject: {sub['subject_name']}\nResult: {sub['result']}\n"
            pass
    print(grade)
    return grade

def result(reg):
    try:
        header = {
            "Authorization": "5988dfdd7fc53c255a38f2d4786779a1",
            "Host": "nuresult.megaminds.co",
            "User-Agent": "okhttp/3.12.0"
        }
        api = "http://nuresult.megaminds.co/api/results/" + str(reg)
        resp = rq.get(api, headers=header)
        data = json.loads(resp.text)
        name = data['name']
        regn = data['registration_number']
        college = data['college']
        sems = data['semesters']
        # return [{
        #     "text": f"{name}\nREG:{regn}\nCollege: {college}\n"
        # }]
        grade = grades(data["semesters"])
        return [{
            "text": f"{name}\nREG:{regn}\nCollege: {college}\n{grade}"
        }]
    except IndexError:
        print("Reg not Found!")
        pass
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit()
    except Exception:
        return [{
            "text": "Please check your Registration number again!"
        }]
