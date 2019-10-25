from requests import get
from bs4 import BeautifulSoup

def to_gpa(grade):
    grade = grade.lower()
    if grade == 'a+':
        return 4.00
    elif grade == 'a':
        return 3.75
    elif grade == 'a-':
        return 3.50
    elif grade == 'b+':
        return 3.25
    elif grade == 'b':
        return 3.00
    elif grade == 'b-':
        return 2.75
    elif grade == 'c+':
        return 2.50
    elif grade == 'c':
        return 2.25
    elif grade == 'd':
        return 2.00
    elif grade == 'f':
        return 0.00
    else:
        return None


def to_g_and_c(num):
    if num == 4.00:
        return ['A+', '1st Class']
    elif 3.75 <= num < 4.00:
        return ['A ', '1st Class']
    elif 3.50 <= num < 3.75:
        return ['A-', '1st Class']
    elif 3.25 <= num < 3.50:
        return ['B+', '1st Class']
    elif 3.00 <= num < 3.25:
        return ['B ', '1st Class']
    elif 2.75 <= num < 3.00:
        return ['B-', '2nd Class']
    elif 2.50 <= num < 2.75:
        return ['C+', '2nd Class']
    elif 2.25 <= num < 2.50:
        return ['C ', '2nd Class']
    elif 2.00 <= num < 2.25:
        return ['D ', '3rd Class']
    else:
        return ['F', 'None']


def welcome(name):
    return [
        {
            'text': 'Welcome {}.\n\n'
                    'This is a simple bot for finding out your result(NU Tejgaon College)\n\n'
                    '@Admin: Abdullah Zayed, Ikbal Nayem\n\n'
                    '@Bot Version - 3.0\n\n'
                    '@Main Web App: tccseresult.tk\n\n'
                    '@Contact:\n\n'
                    'http://facebook.com/ikbal.nayem/\n\n'
                    'http://facebook.com/xayed42/\n\n'
                    '@G-Mail: \n\n'
                    'xayed42@gmail.com\n\n'
                    'ikbalnayem000@gmail.com\n\n'
                    'Thank you. Enjoy.'.format(name)
        }
    ]



data={
    '16_4th': ['5614', '2018'],
    '17_2nd': ['5612', '2018']
}


def getData(reg, examCode, examYear):
    link='http://www.nu.ac.bd/results/cse/cse_result.php?roll_number=&reg_no={reg}&exm_code={examCode}&exam_year={examYear}'
    r=get(link.format(reg=reg, examCode=examCode, examYear=examYear))
    #print(r.text)
    soup=BeautifulSoup(r.text, 'html.parser')
    if soup.body.table.tr.td.text=='Error! Wrong Registration Number':
        return {'exception':'student_not_found'}
    else:
        fullList,grades=[],{}
        #print('-'*80)
        resultRows2=soup.find_all('table')[2].findAll('tr')[1:]
        resultRows1=soup.find_all('table')[1].findAll('tr')

        name=resultRows1[4].find_all('td')[2].text.strip()
        semester=resultRows1[2].td.text.strip().split()[1].lower()
        
        try:
            cgpa=float(resultRows1[9].find_all('td')[2].text.strip())
        except:
            cgpa=0

        for result in resultRows2:
            singleList=[]
            for singleResult in result.find_all('td'):
                t=singleResult.text.strip().title()
                if len(t)==4 and t.isnumeric() and t[0]=='0':
                    t='CSE_'+t[1:]
                singleList.append(t)
                #print(t, end=' '*10)
            #print()
            grades[singleList[0]]=singleList[3]
            fullList.append(singleList)
        #print('-'*80)

        finalJson={"batch":int(str(reg)[0:2])-8, "cgpa": cgpa, "courses":fullList, "exam year":examYear, 
                   "exception":"result_found", "grades":grades, "name":name, "registration": reg, 
                   "result":"PASSED" if cgpa!=0 else "FAILED", "semester":semester, 
                   "session":"20"+str(reg)[:2]+"-"+str(int(str(reg)[:2])+1)}
        #print(finalJson)
        return finalJson

def get_result(regNum, semester):
    d=str(regNum)[:2]+'_'+str(semester.lower())
    if d in data.keys():
        r=getData(regNum, data[d][0], data[d][1])
    else:
        r = get('http://iku.pythonanywhere.com/result/api/{}/{}'.format(semester, regNum)).json()
    print(r)
    if r['exception'] == 'result_found':
        part1 = 'Student Information: \n\n'
        part1 += 'Name: {name}\n\nRegistration Number: {regNum}\n\nSemester: {semester}\n\nSession: {session}\n\n' \
                 'Batch: {batch}\n\nExam Year: {year}'.format(
            name=r['name'].title(),
            regNum=regNum,
            semester=semester,
            session=r['session'],
            batch=r['batch'],
            year=r['exam year']
        )

        part2 = 'At a Glance: \n\n'
        for s in r['courses']:
            grade = r['grades'][s[0]]
            part2 += 'Course Name: {}\nCourse Code: {}\nCredit: {}\nGrade: {}\nGPA: {}\n\n' \
                     ''.format(s[1], s[0][1:] if s[0][0]=='_' else s[0], s[2], grade, to_gpa(grade))
        cgpa = r['cgpa']
        l = to_g_and_c(float(cgpa))
        part3 = 'Final Result: {}\n\nCGPA: {}\n\nGrade: {}'.format(r['result'], cgpa, l[0])
        if cgpa != 0:
            part3 += '\n\nClass: {}'.format(l[1])

        return [
            {'text': part1},
            {'text': part2},
            {'text': part3}
        ]
    else:
        return [{'text': 'Sorry. Invalid Registration or semester.'}]
