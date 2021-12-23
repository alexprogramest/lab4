import json, pymysql, config
from abc import ABC, abstractmethod


class ITeacher(ABC):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.own_curses = []

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def surname(self):
        pass

    def __str__(self):
        temp = max(len(self.name), len(self.surname))
        return "\n\tThe name    %*s\n\tThe surname %*s\n\t" % (temp, self.name, temp, self.surname,)


class CourseTeacher(ITeacher):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, arg_name):
        self.__name = arg_name

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, arg_surname):
        self.__surname = arg_surname

    def __str__(self):
        return super().__str__() + "All courses:\n\t\t" + \
               "\n\t\t\"\"".join(['"' + own_curse + '"' for own_curse in self.own_curses])


# ------------------------------------------------------------------------------------------------------
class ICourse(ABC):
    def __init__(self, name, teacher):
        self.name = name
        self.assigned_teacher = teacher
        teacher.own_curses.append(name)

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def assigned_teacher(self):
        pass

    @abstractmethod
    def whole_program(self):
        pass


class ILocalCourse(ICourse):
    __city = "Kiev"

    def __init__(self, name, teacher):
        super().__init__(name, teacher)

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def assigned_teacher(self):
        pass

    @abstractmethod
    def whole_program(self):
        pass

    @classmethod
    def city(cls):
        return cls.__city


class IOffsiteCourse(ICourse):
    def __init__(self, name, teacher, another_city):
        super().__init__(name, teacher)
        self.__city = another_city

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def assigned_teacher(self):
        pass

    @abstractmethod
    def whole_program(self):
        pass

    def city(self):
        return self.__city


class KievCourse(ILocalCourse):
    def __init__(self, name, teacher):
        super().__init__(name, teacher)
        self.__whole_program = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, arg_name):
        self.__name = arg_name

    @property
    def assigned_teacher(self):
        return self.__assigned_teacher

    @assigned_teacher.setter
    def assigned_teacher(self, arg_assigned_teacher):
        self.__assigned_teacher = arg_assigned_teacher

    @property
    def whole_program(self):
        return self.__whole_program

    @whole_program.setter
    def whole_program(self, adding_topic):
        self.__whole_program.append(adding_topic)

    @whole_program.deleter
    def whole_program(self):
        del self.__whole_program[len(self.__whole_program) - 1]

    def __str__(self):
        length = max(len(self.name), len(self.city()))
        return "\n\nThe name of courses %*s\nThe teacher: %s\nThe whole program: %*s\nThe city: %*s" \
               % (length, self.name, self.assigned_teacher, length, "\n".join(self.whole_program), length, self.city())


class KievRegionCourse(IOffsiteCourse):
    def __init__(self, name, teacher, another_city):
        super().__init__(name, teacher, another_city)
        self.__whole_program = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, arg_name):
        self.__name = arg_name

    @property
    def assigned_teacher(self):
        return self.__assigned_teacher

    @assigned_teacher.setter
    def assigned_teacher(self, arg_assigned_teacher):
        self.__assigned_teacher = arg_assigned_teacher

    @property
    def whole_program(self):
        return self.__whole_program

    @whole_program.setter
    def whole_program(self, adding_topic):
        self.__whole_program.append(adding_topic)

    @whole_program.deleter
    def whole_program(self):
        del self.__whole_program[len(self.__whole_program) - 1]

    def __str__(self):
        length = max(len(self.name), len(self.city()))
        return "\n\nThe name of courses \"%*s\"\nThe teacher: %s\nThe whole program: %*s\nThe city: %*s" \
               % (length, self.name, self.assigned_teacher, length, "\n".join(self.whole_program), length, self.city())


class ICourseFactory(ABC):

    @classmethod
    @abstractmethod
    def create_subject(cls, whole_data, arg_choice):
        pass


class CourseFactory(ICourseFactory):

    @classmethod
    def create_subject(cls, arg_choice, *args):
        if not isinstance(arg_choice, int):
            raise TypeError("Choice for factory is integer!!")
        if not 1 <= arg_choice <= 6:
            raise ValueError("Value of choice for factory must be between 1 and 3!!")
        if arg_choice == 6:
            return CourseTeacher(args[0], args[1])
        if arg_choice == 4:
            return KievCourse(args[0], cls.create_subject(6))
        if arg_choice == 5:
            return KievRegionCourse(args[0], cls.create_subject(6, args[1], args[2]), args[3])
        if arg_choice == 3:
            print("Print teacher's info (name with surname)")
            temp_teacher_name = input()
            temp_teacher_surname = input()
            return CourseTeacher(temp_teacher_name, temp_teacher_surname)
        print("Well.... Could you type the name of course")
        temp_course_name = input()
        if arg_choice == 1:
            new_course = KievCourse(temp_course_name, cls.create_subject(3))
        if arg_choice == 2:
            temp_city = input("You chose the not local course. Where are these courses (city name)?\n")
            new_course = KievRegionCourse(temp_course_name, cls.create_subject(3), temp_city)

        print("Now, print the whole program of the course (when you wish to finish, please type the 'quit')")
        while True:
            answer2 = input()
            if answer2.lower() == 'quit':
                break
            new_course.whole_program = answer2
        my_bd.cursor().execute(f"""
            INSERT INTO Course(Name, City)
            VALUES (7568, {new_course.name}, {new_course.city()});
        """)
        my_bd.cursor().execute(f"""
                    INSERT INTO Teacher(Name, Surname)
                    VALUES (7568, {new_course.assigned_teacher.name}, 
                    {new_course.assigned_teacher.surname});
                """)
        return new_course


def finding_course():
    print("Print the course name, which you would like to find (the name)")
    the_name = input()
    my_bd.cursor().execute("""
        SELECT Name, (SELECT Name, Surname FROM Teacher WHERE Teacher.TeacherID =  Course.TeacherID), 
        (SELECT Surname FROM Teacher WHERE Teacher.TeacherID =  Course.TeacherID), 
        City FROM Course 
    """)
    whole_data = my_bd.cursor().fetchall()
    for temp_data in whole_data:
        if the_name == temp_data[0]:
            if temp_data[3] == "Kiev":
                new_course = CourseFactory.create_subject(4, temp_data[0],
                                                          temp_data[1], temp_data[2])

            else:
                new_course = CourseFactory.create_subject(5, temp_data[0],
                                                          temp_data[1], temp_data[2])
            return
    print("No matches....")


def choice1(arg_answer1):
    if arg_answer1 == '1':
        CourseFactory.create_subject(arg_choice=1)
    elif arg_answer1 == '2':
        CourseFactory.create_subject(arg_choice=2)
    elif arg_answer1 == '3':
        finding_course()


def creating_database():
    with my_bd.cursor() as cursor:
        cursor.execute(f"""USE {config.db_name};""")
        cursor.execute("""CREATE TABLE Teacher (
            TeacherID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(20) NOT NULL,
            Surname VARCHAR(20) NOT NULL
            );
        """)
        cursor.execute("""CREATE TABLE Course (
                    CourseID INT PRIMARY KEY AUTO_INCREMENT,
                    TeacherID INT,  
                    Name VARCHAR(20) NOT NULL,
                    City VARCHAR(20) NOT NULL
                    );
                """)
        cursor.execute("""
        ALTER TABLE Course
        ADD FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID);
        """)


if __name__ == '__main__':
    my_bd = pymysql.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    # creating_database()

    print("Hello! What would you like to do next?"
          "\n1. Add new local course"
          "\n2. Add new offsite course"
          "\n3. Find (and see) the particular one")
    asnwer1 = input("Type the number\n")
    while asnwer1 not in ['1', '2', '3']:
        print("Invalid input!")
        asnwer1 = input("Type the number")
    choice1(asnwer1)
    my_bd.close()
