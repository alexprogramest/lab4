import json
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
    """
    We have the abstract factory, which consists of three methods.
    Every of them returns abstract type (in reality just involve it)
    There I used the annotations for the class and methods for better
    understanding.
    """

    @abstractmethod
    def create_local_course(self, course_name, main_teacher) -> ILocalCourse:
        pass

    @abstractmethod
    def create_offsite_course(self, course_name, course_city, main_teacher) -> IOffsiteCourse:
        pass

    @abstractmethod
    def create_teacher(self, name, surname) -> ITeacher:
        pass


class CourseFactory(ICourseFactory):

    def create_local_course(self, course_name, main_teacher):
        return KievCourse(course_name, main_teacher)

    def create_offsite_course(self, course_name, course_city, main_teacher):
        return KievRegionCourse(course_name, main_teacher, course_city)

    def create_teacher(self, name, surname):
        return CourseTeacher(name, surname)


def adding_new_course(type_of_course, whole_data):
    print("Well.... Could you type the name of course and the teacher's info (name with surname)")
    temp_course_name = input()
    temp_teacher_name = input()
    temp_teacher_surname = input()
    if type_of_course:
        temp_city = input("You chose the not local course. Where are these courses (city name)?\n")
        new_course = main_factory.create_offsite_course(temp_course_name, temp_city,
                                                        main_factory.create_teacher(temp_teacher_name,
                                                                                    temp_teacher_surname))

    else:
        new_course = main_factory.create_local_course(temp_course_name,
                                                      main_factory.create_teacher(temp_teacher_name,
                                                                                  temp_teacher_surname))
    print("Now, print the whole program of the course (when you wish to finish, please type the 'quit')")

    while True:
        answer2 = input()
        if answer2.lower() == 'quit':
            break
        new_course.whole_program = answer2

    whole_data.append({"name": new_course.name, "city": new_course.city(),
                       "teacher name": new_course.assigned_teacher.name,
                       "teacher surname": new_course.assigned_teacher.surname,
                       "whole program": new_course.whole_program})

    with open("Courses.json", 'w') as fi:
        json.dump(whole_data, fi)


def finding_course(whole_data):
    print("Print the course, which you would like to find (the name)")
    the_name = input()
    for temp_data in whole_data:
        if the_name == temp_data["name"]:
            if temp_data["city"] == "Kiev":
                new_course = main_factory.create_local_course(temp_data["name"],
                                                              main_factory.create_teacher(temp_data["teacher name"],
                                                                                          temp_data["teacher surname"]))
            else:
                new_course = \
                    main_factory.create_offsite_course(temp_data["name"],
                                                       temp_data["city"],
                                                       main_factory.create_teacher(temp_data["teacher name"],
                                                                                   temp_data["teacher surname"]))
            for temp_temp in temp_data["whole program"]:
                new_course.whole_program = temp_temp
            print(new_course)
            return
    print("No matches....")


def choice1(arg_answer1, whole_data):
    if arg_answer1 == '1':
        adding_new_course(None, whole_data)
    elif arg_answer1 == '2':
        adding_new_course(1, whole_data)
    elif arg_answer1 == '3':
        finding_course(whole_data)


if __name__ == '__main__':
    main_factory = CourseFactory()
    with open("Courses.json", 'r') as f:
        data = json.load(f)
    print("Hello! What would you like to do next?"
          "\n1. Add new local course"
          "\n2. Add new offsite course"
          "\n3. Find (and see) the particular one")
    asnwer1 = input("Type the number\n")
    while asnwer1 not in ['1', '2', '3']:
        print("Invalid input!")
        asnwer1 = input("Type the number")
    choice1(asnwer1, data)
