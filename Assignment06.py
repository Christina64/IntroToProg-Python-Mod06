# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   CAlvarez,11/20/2024,Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.
student_data: dict = {}  # one row of student data
students: list = []  # a table of student data
csv_data: str = ''  # Holds combined string data separated by a comma.
json_data: str = ''  # Holds combined string data in a json format.
file = None  # Holds a reference to an opened file.
menu_choice: str  # Hold the choice made by the user.

# Processing ________________________________________
class FileProcessor:
    """
    A collection of processing layer of functions that work with Json files

    ChangeLog: (Who, When, What)
    CAlvarez,11.18.2024,Created class
    """
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from json file and loads into a list of dictionaries

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created function

        :return: list
         """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file.closed == False:
                file.close()
        return student_data

    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to json file

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created function

        :return: none
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            IO.output_student_and_course_name(student_data=student_data)
        except Exception as e:
            message = "Error: There is a problem with writing to file.\n"
            message += "Please check that the file is not open in another program."
            IO.output_error_messages(message=message, error=e)

        finally:
            if file.closed == False:
                file.close()

# Presentation _______________________________________
class IO:
    """
    A collection of presentation layer functions that manage user input and output.

    ChangeLog: (Who, When, What)
    CAlvarez,11.18.2024,Created Class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error message to the user

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created function

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("--Technical Error Message--")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user.

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created Class

        :return: None
        """
        print() # Space added for aesthetics
        print(menu)
        print() # Space added for aesthetics

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user.

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created Class

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):
                raise Exception("Please, choose only 1,2,3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__()) # Not passing e to avoid technical message

        return choice

    @staticmethod
    def output_student_and_course_name(student_data: list):
        """ This function displays the student and course name

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created Class

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]}'
              f'{student["LastName"]} is enrolled in {student["CourseName"]}')
            print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the first name, last name and a course name.

        ChangeLog: (Who, When, What)
        CAlvarez,11.18.2024,Created Class

        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Enter the course name. ")
            student = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="Please check data entered one of the values was incorrect.", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with the data entered", error=e)
        return student_data

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students=IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":

        IO.output_student_and_course_name(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":

        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
