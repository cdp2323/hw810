import os
from prettytable import PrettyTable

class Student:
    def __init__(self,id, name, dept):
        self.CWID = id
        self.Name = name
        self.Deptt = dept
        self.Course = {}
        self.Completed_Course = []


class Instructor:
    def __init__(self, id, name, dept):
        self.CWID = id
        self.Name = name
        self.Dept = dept
        self.Course = {}
    
class University:
    def __init__(self, path):
        self.student_file = os.path.join(path,'students.txt')
        self.instructors_file = os.path.join(path,'instructors.txt')
        self.grade_file = os.path.join(path,'grades.txt')
        self.students = dict()
        self.instructors = dict()
        self.read_students()
        self.read_instructors()
        self.read_grades()
        self.student_prettytable()
        self.instructors_prettytable()
        
    def read_students(self):
        for id, name, dept in self.file_reading_gen(self.student_file, 3):
            student_id = Student(id,name,dept)
            self.students[id] = student_id
    
    def read_instructors(self):
        for id, name, dept in self.file_reading_gen(self.instructors_file,3):
            instructor_id = Instructor(id,name,dept)
            self.instructors[id] = instructor_id
    
    def read_grades(self):
        for student_id, course_name, grade, instructor_id in self.file_reading_gen(self.grade_file,4):
            self.students[student_id].Course[course_name] = grade
            if grade:
                self.students[student_id].Completed_Course.append(course_name)
            if not course_name in self.instructors[instructor_id].Course:
                self.instructors[instructor_id].Course[course_name] = 1
            else:
                self.instructors[instructor_id].Course[course_name] += 1

    def student_prettytable(self):
        student_table = PrettyTable(field_names = ["CWID","NAME","Completed Course"])
        for CWID in self.students:
            student_table.add_row([CWID,self.students[CWID].Name, sorted(self.students[CWID].Completed_Course)])
        print('Student Summary')
        print(student_table)
    
    def instructors_prettytable(self):
        instructors_table = PrettyTable(field_names = ["CWID","NAME","Dept","Course","students"])
        for CWID in self.instructors:
            for course in self.instructors[CWID].Course:
                instructors_table.add_row([CWID,self.instructors[CWID].Name, self.instructors[CWID].Dept, course,self.instructors[CWID].Course[course]])
        print('Instructors Summary')
        print(instructors_table)

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

if __name__ == "__main__":
    path = '/Users/acai/Desktop/hw810'
    Cai_University = University(path)
    a =1
    