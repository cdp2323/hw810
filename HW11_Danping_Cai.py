import os
from prettytable import PrettyTable
import sqlite3

class Student:
    #student information structure
    def __init__(self,id, name, dept):
        self.CWID = id
        self.Name = name
        self.Deptt = dept
        self.Course = {}
        self.Completed_Course = []


class Instructor:
    #instructor information structure
    def __init__(self, id, name, dept):
        self.CWID = id
        self.Name = name
        self.Dept = dept
        self.Course = {}


class Major:
    #major information structure
    def __init__(self, name):
        self.name = name
        self.require_course = set()
        self.elective_course = set()


class University:
    #university information structure
    def __init__(self, path, db_path):
        self.student_file = os.path.join(path,'students.txt')
        self.instructors_file = os.path.join(path,'instructors.txt')
        self.grade_file = os.path.join(path,'grades.txt')
        self.major_file = os.path.join(path,'majors.txt')
        self.students = dict()
        self.instructors = dict()
        self.major_dict = dict()
        self.read_students()
        self.read_instructors()
        self.read_grades()
        self.read_major()
        self.major_prettytable()
        self.student_prettytable()
        self.instructors_prettytable()
        self.instructors_prettytable_sql(db_path)
        
    def read_major(self):
        #read major file and create major instance
        for major, RorE, course in self.file_reading_gen(self.major_file, 3,header=True):
            if not major in self.major_dict:
                m = Major(major)
                self.major_dict[major] = m
                if RorE == 'R':
                    self.major_dict[major].require_course.add(course)
                elif RorE == 'E':
                    self.major_dict[major].elective_course.add(course)
            else:
                if RorE == 'R':
                    self.major_dict[major].require_course.add(course)
                elif RorE == 'E':
                    self.major_dict[major].elective_course.add(course)

    def read_students(self):
        #read student file and create student instance and univerisity dictionary
        for id, name, dept in self.file_reading_gen(self.student_file, fields =3):
            if id == 'CWID':
                continue
            student_id = Student(id,name,dept)
            self.students[id] = student_id
    
    def read_instructors(self):
        #read instructor file and create instructor instance and univerisity dictionary
        for id, name, dept in self.file_reading_gen(self.instructors_file,fields = 3):
            if id == 'CWID':
                continue
            instructor_id = Instructor(id,name,dept)
            self.instructors[id] = instructor_id
    
    def read_grades(self):
        #read grades and add course information into instructor instance
        for student_id, course_name, grade, instructor_id in self.file_reading_gen(self.grade_file,fields = 4):
            
            if student_id == 'StudentCWID':
                continue
            self.students[student_id].Course[course_name] = grade
            if grade:
                self.students[student_id].Completed_Course.append(course_name)
            if not course_name in self.instructors[instructor_id].Course:
                self.instructors[instructor_id].Course[course_name] = 1
            else:
                self.instructors[instructor_id].Course[course_name] += 1

    def student_prettytable(self):
        #print student prettytable
        student_table = PrettyTable(field_names = ["CWID","NAME","Completed Course"])
        for CWID in self.students:
            student_table.add_row([CWID,self.students[CWID].Name, sorted(self.students[CWID].Completed_Course)])
        print('Student Summary')
        print(student_table)
    
    def instructors_prettytable(self):
        #print instructor prettytable
        instructors_table = PrettyTable(field_names = ["CWID","NAME","Dept","Course","students"])
        for CWID in self.instructors:
            for course in self.instructors[CWID].Course:
                instructors_table.add_row([CWID,self.instructors[CWID].Name, self.instructors[CWID].Dept, course,self.instructors[CWID].Course[course]])
        print('Instructors Summary')
        print(instructors_table)

    def instructors_prettytable_sql(self, db_path):
        #print instructor prettytable

        db = sqlite3.connect(db_path)
        instructors_table_sql = PrettyTable(field_names = ["CWID","NAME","Dept","Course","students"])
        
        query = "select CWID, Name, Dept, Course, count(StudentCWID) from instructors join grades on CWID = InstructorCWID group by Course"
        
        for row in db.execute(query):

            instructors_table_sql.add_row(list(row))
        
        print('Instructors Summary2')
        print(instructors_table_sql)

    def file_reading_gen(self, path, fields, sep='\t', header=False):
        """
        read field-separated text files and yield a tuple with all of the values from a single line in the file 
        """
        try:
            file = open(path, "r")
        except FileNotFoundError:
            print('file not found!!!!')
        else:
            if header == True:
                next(file)
            number = 0
            for line in file:
                number += 1
                line = line.rstrip()
                line = line.split(sep)
                if len(line) != fields:
                    raise ValueError(f"{path} has {len(line)} on line {number} but expected 3Rds ")
                else:
                    yield tuple(line)
    
    def major_prettytable(self):
        #print major prettytable
        majors_table = PrettyTable(field_names = ["Dept","Required","Electives"])
        for dept in self.major_dict:
            majors_table.add_row([dept,sorted(self.major_dict[dept].require_course),sorted(self.major_dict[dept].elective_course)])
        print('Majors Summary')
        print(majors_table)

if __name__ == "__main__":
    path = '/Users/acai/Desktop/810/hw11'
    db_path = '/Users/acai/Desktop/810/hw11/810_startup.db'
    Cai_University = University(path, db_path)