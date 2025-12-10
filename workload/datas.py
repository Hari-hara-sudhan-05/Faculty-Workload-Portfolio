import mysql.connector
import datetime as dt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="workload"
)

print(mydb.is_connected())

c = mydb.cursor()

def authenticate(email,password):
    q = f"SELECT f_name FROM Users WHERE faculty_id = %s AND password = %s"
    c.execute(q,(email,password))
    name = c.fetchone()
    return name

def isAdmin(email):
    a = f"SELECT entity from users where faculty_id = '{email}'"
    c.execute(a)
    admin = c.fetchone()
    if admin[0] == 'admin':
        return True
    return False


def get_faculty_details(faculty_id):
    lst = [[None, 0, 0, 0]]
    
    q1 = f"SELECT f_name FROM Users WHERE faculty_id = '{faculty_id}'"
    c.execute(q1)
    name = c.fetchone()
    
    if name is None:
        return None
    
    lst[0][0] = name[0]

    q2 = f"SELECT t.course_code, tc.course_name, t.day_of_the_week, t.hour_of_the_week, t.section, t.handled_duration FROM Theory t JOIN TheoryCourse tc ON t.course_code = tc.course_code WHERE t.faculty_id = '{faculty_id}' and t.sessionn = 'feb-jul'"
    c.execute(q2)
    theory_courses = c.fetchall()
    lst[0][1] = len(theory_courses)
    lst.append(theory_courses)

    q3 = f"SELECT p.course_code, pc.course_name, p.day_of_the_week, p.hour_of_the_week_start, p.hour_of_the_week_end, p.section, p.handled_duration FROM Practical p JOIN PracticalCourse pc ON p.course_code = pc.course_code WHERE p.faculty_id = '{faculty_id}' and p.sessionn='feb-jul'"
    c.execute(q3)
    practical_courses = c.fetchall()
    lst[0][2] = len(practical_courses)
    lst.append(practical_courses)

    q4 = f"SELECT p.course_code, p.course_name, p1.day_of_the_week, p1.hour_of_the_week_start, p1.hour_of_the_week_end, p1.section, p1.handled_duration FROM project p1 join projectcourse p ON p.course_code = p1.course_code WHERE p1.faculty_id = '{faculty_id}' and p.sessionn= 'feb-jul'"
    c.execute(q4)
    projects = c.fetchall()
    lst[0][3] = len(projects)
    lst.append(projects)

    return lst


def faculty_courses(faculty_id):
    lst=[]
    q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}' and Theory.sessionn = 'feb-jul'"
    c.execute(q1)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)

    q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' and p.sessionn = 'feb-jul' UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' and p.sessionn='feb-jul'"
    c.execute(q2)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)
    return lst

def faculty_courses_sort(faculty_id,session):
    if session =='All_Session':
        lst=[]
        q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}'"
        c.execute(q1)
        out=c.fetchall()
        tup=()
        for i in range(len(out)):
            tup+=(out[i][0],)
        lst.append(tup)

        q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}'UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}'"
        c.execute(q2)
        out=c.fetchall()
        tup=()
        for i in range(len(out)):
            tup+=(out[i][0],)
        lst.append(tup)
        return lst
    
    
    lst=[]
    q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}' AND Theory.sessionn = '{session}'"
    c.execute(q1)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)

    q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' AND p.sessionn = '{session}' UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' AND p.sessionn = '{session}'"
    c.execute(q2)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)
    return lst

def getAllFaculty():
    lst = []
    q1 = f"select faculty_id, f_name from users"
    c.execute(q1)
    output = c.fetchall()
    lst.extend(output)
    return lst

def getAllCourse():
    course_code = []
    course_name = []
    q1 = f"select course_code from theoryCourse"
    c.execute(q1)
    course_code.extend(c.fetchall())

    q2 = f"select course_code from PracticalCourse"
    c.execute(q2)
    course_code.extend(c.fetchall())

    q3 = f"select course_name from theoryCourse"
    c.execute(q3)
    course_name.extend(c.fetchall())

    q4 = f"select course_name from PracticalCourse"
    c.execute(q4)
    course_name.extend(c.fetchall())
    return course_code,course_name

def getvac():
    course_code = []
    course_name = []
    q1 = f"select course_code from VAC"
    c.execute(q1)
    course_code.extend(c.fetchall())

    q2 = f"select course_name from VAC"
    c.execute(q2)
    course_name.extend(c.fetchall())
    return course_code,course_name

def add_course(course_code,course_name,semester,session):
    q1=f"INSERT INTO VAC VALUES ('{course_code}','{course_name}',{int(semester)},'{session}')"
    c.execute(q1)
    c.execute('commit')
  
def remove_course(course_code,course_name,semester):
    q1=f"SELECT * FROM VAC WHERE COURSE_CODE='{course_code}'"
    c.execute(q1)
    out=c.fetchall()
    if len(out)!=0:
        q2=f"DELETE FROM VAC WHERE COURSE_CODE='{course_code}' and COURSE_NAME = '{course_name}' and SEMESTER = '{int(semester)}'"
        c.execute(q2)
        c.execute('commit')

def assign_courses_tt(type,faculty_id,course_code,day_of_the_week,section,sessionn,hour_of_the_week_start,hour_of_the_week_end=None,handled_duration=dt.datetime.now().year):
    if type=="Theory":
        q1=f"INSERT INTO THEORY VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q1)
        c.execute('commit')
    if type=="Practical":
        q2=f"INSERT INTO PRACTICAL VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{hour_of_the_week_end}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q2)
        c.execute('commit')
    if type=="Project":
        q3=f"INSERT INTO PROJECT VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{hour_of_the_week_end}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q3)
        c.execute('commit')

def remove_assigned_courses(type,faculty_id,course_code):
    if type=="Theory":
        q1=f"DELETE FROM THEORY WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    elif type=="Practical":
        q1=f"DELETE FROM PRACTICAL WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    elif type=="Project":
        q1=f"DELETE FROM PROJECT WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    c.execute(q1)
    c.execute('commit')  


def department_duties(faculty_id):
    q1 = f"select responsibilty from dept_duty where faculty_id = '{faculty_id}'"
    c.execute(q1)
    lst = c.fetchall()
    l=[]
    for i in lst:
        for j in i:
            l.append(j)
    return l

def assign_new_duty(faculty_id,Responsibilty):
    q1 = f"insert into dept_duty values ('{faculty_id}','{Responsibilty}')"
    c.execute(q1)
    c.execute('commit')

def remove_duty(faculty_id,duty):
    q1=f"DELETE FROM dept_duty WHERE Responsibilty='{duty}' AND faculty_id='{faculty_id}'"
    c.execute(q1)
    c.execute('commit')

def calculate_num_classes(faculty_id,session):
    if session =='All_Session':
        lst=[]
        q1=f"SELECT COUNT(*) FROM THEORY WHERE faculty_id='{faculty_id}'"
        c.execute(q1)
        t=c.fetchall()
        for i in t:
            for j in i:
                lst.append(j)

        q2=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PRACTICAL WHERE faculty_id='{faculty_id}'"
        c.execute(q2)
        pra=c.fetchall()
        pcount=0
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)

        q3=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PROJECT WHERE faculty_id='{faculty_id}'"
        c.execute(q3)
        pra=c.fetchall()
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)
        lst.append(pcount)
        return lst
    
    elif session =='sep-dec':
        lst=[]
        q1=f"SELECT COUNT(*) FROM THEORY WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q1)
        t=c.fetchall()
        for i in t:
            for j in i:
                lst.append(j)

        q2=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PRACTICAL WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q2)
        pra=c.fetchall()
        pcount=0
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)

        q3=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PROJECT WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q3)
        pra=c.fetchall()
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)
        lst.append(pcount)
        return lst
    
    elif session =='feb-jul':
        lst=[]
        q1=f"SELECT COUNT(*) FROM THEORY WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q1)
        t=c.fetchall()
        for i in t:
            for j in i:
                lst.append(j)

        q2=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PRACTICAL WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q2)
        pra=c.fetchall()
        pcount=0
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)

        q3=F"SELECT hour_of_the_week_start,hour_of_the_week_end FROM PROJECT WHERE faculty_id='{faculty_id}' and sessionn='{session}'"
        c.execute(q3)
        pra=c.fetchall()
        for cla in pra:
            s=cla[0]+":00"
            e=cla[1]+":00"
            start = dt.datetime.strptime(s, "%H:%M:%S") 
            end = dt.datetime.strptime(e, "%H:%M:%S") 
            difference = end - start 
            seconds = difference.total_seconds() 
            minutes = seconds / 60
            classes=minutes//50
            pcount+=int(classes)
        lst.append(pcount)
        return lst
    
def view_full(faculty_id,session,detail):
    if detail=="Academic":
        lst = faculty_courses_sort(faculty_id, session)
    else:
        lst=department_duties(faculty_id)
    return lst


