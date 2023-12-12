import certifi as certifi
import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from validators import *
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """

    valid_department = False
    collection = db["departments"]
    while not valid_department:
        # Create a "pointer" to the students collection within the db database.
        # unique_name: bool = False
        # unique_abbreviation: bool = False
        # unique_chair_name: bool = False
        # unique_building_office: bool = False
        # unique_description: bool = False

        name: str = ''
        abbreviation: str = ''
        chair_name: str = ''
        building: str = ''
        office: int = 0
        description: str = ''

        # while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        # name_count: int = collection.count_documents({"name": name})
        # unique_name = name_count == 0
        # if not unique_name:
        #    print("We already have a department by that name.  Try again.")

        # if unique_name:
        #    abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
        #    unique_abbreviation = abbreviation_count == 0
        #    if not unique_abbreviation:
        #        print("We already have a department with that abbreviation.  Try again.")
        # while not unique_chair_name:
        chair_name = input("Department chair name--> ")
        # chair_name_count = collection.count_documents({"chair_name": chair_name})
        # unique_chair_name = chair_name_count == 0
        # if not unique_chair_name:
        #    print("We already have a department with that chair name. Try again.")

        # while not unique_building_office:
        building = input("Department building--> ")
        office = int(input("Department Office--> "))
        # building_office_count: int = collection.count_documents({"building": building, "office": office})
        # unique_building_office = building_office_count == 0
        # if not unique_building_office:
        #    print("We already have a department by that office in that building. Try again.")

        # while not unique_description:
        description = input("Department description--> ")
        # description_count: int = collection.count_documents({"description": description})
        # unique_description = description_count == 0
        # if not unique_description:
        #    print("We already have a department by that description. Try again.")

        # Build a new departments document preparatory to storing it
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description
        }
        try:
            collection.insert_one(department)
            valid_department = True
        except Exception as exception:
            print("We got the following exception from a bad input:")
            print(exception)
            print("Please re-enter your values")


def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    name: str = ''
    abbreviation: str = ''
    while not found:
        name = input("Department's name--> ")
        abbreviation = input("Department's abbreviation--> ")
        name_count: int = collection.count_documents({"name": name, "abbreviation": abbreviation})
        found = name_count == 1
        if not found:
            print("No department found by that name and abbreviation.  Try again.")
    found_department = collection.find_one({"name": name, "abbreviation": abbreviation})
    return found_department


def delete_department(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING),
                                                   ("abbreviation", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)




def add_enrollment(db):

    #access the collection where enrollment object resides
    collection = db['students']

    #gather student information
    first_name = input("Student first name: ")
    last_name = input("Student last name: ")
    email = input("Student email: ")

    #gather the section's information of which the student will be enrolled in
    department_abbreviation = input("(string) Department abbreviation: ")
    course_number = int(input("(int) Course number: "))  # Convert to integer
    section_number = int(input("(int) Section number: "))  # Convert to integer
    semester = input("(string) Semester: ")
    section_year = int(input("(int) Section Year: "))  # Convert to integer

    #after getting input, insert into the sections detail object
    section_details = {
        "department_abbreviation": department_abbreviation,
        "course_number": course_number,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year
    }


    #gather some information about enrollment
    enrollment_type = input("(string) Choose an enrollment type (letter_grade / pass_fail): ")
    enrollments = {
        "type": enrollment_type,
        "section_details": section_details

    }

    #specify additional information based on selected enrollment type
    #if letter_grade type, then add  a min_satisfactory letter grade
    #if pass_fail type, then add an application date for the enrollment
    if enrollment_type == "letter_grade":
        letter_grade = input("Specify the minimum letter grade to pass (A/B/C): ")
        enrollments["letter_grade"] ={"min_satisfactory": letter_grade}
    elif enrollment_type == "pass_fail":
        application_date = input("Specify the Pass/Fail appilcation date (DD-MM-YYYY): ")
        enrollments["pass_fail"] ={"application_date": application_date}

    #now that we have our objects, we need to find the student we are adding the enrollment to
    #use the information gathered about the student in the beginning
    #then update the existing student record by adding an enrollment.
    try:
        update_result = collection.update_one(
            #does the updating to the enrollment object within students object
            {"first_name": first_name, "last_name": last_name, "email": email},
            {"$push": {"enrollments": enrollments}}
        )
        if update_result.matched_count == 0: #if student object is found, then this should = 1
            print("No matching student found. Check student details entered")
        elif update_result.modified_count == 0: #if changes were made/added, then this should = 1, if 0 then something went wrong  due to duplicates.
            print("Enrollment data was not added. Duplicate information error")
        else:
            print("Enrollment was added successfully")
    except Exception as exception:
        print("Error adding enrollment")
        print(exception)


def list_enrollment(db):
    collection = db['students']

    first_name: str = ''
    last_name: str = ''
    email: str = ''


    #gather some information about the student
    print("Give student details to list their enrollments")
    first_name = input("Student's first name: ")
    last_name = input("Student's last name: ")
    email = input("Student's email: ")

    #Find student in the collection
    student = collection.find_one(
        {"first_name": first_name, "last_name": last_name, "email": email}
    )

    #Now check if the student was found
    if student:
        print(f"\nListing enrollments for {first_name}  {last_name} ({email}):")
        enrollments = student.get('enrollments', [])
        if enrollments:
            for i, enrollment in enumerate(enrollments, 1):
                print(f"\nEnrollment {i}:")
                for key, value in enrollment.items():
                    print(f"  {key}: {value}")
        else:
            print("No enrollments found for this student.")
    else:
        print("Student not found. Please check the entered details.")




def delete_enrollment(db):
    collection = db['students']

    #get some infomration about the student
    first_name = input("Student's first name: ")
    last_name = input("Student's last name: ")
    email = input("Student's email: ")


    #get some info about the section to identify the enrollment to delete
    department_abbreviation = input("(string) Department abbreviation: ")
    course_number = int(input("(int) Course number: "))  # Convert to integer
    section_number = int(input("(int) Section number: "))  # Convert to integer
    semester = input("(string) Semester: ")
    section_year = int(input("(int) Section Year: "))  # Convert to integer

    #create the section details object to find
    section_details = {
        "department_abbreviation": department_abbreviation,
        "course_number": course_number,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year
    }


    #find student and delete specific enrollment
    try:
        update_result = collection.update_one(
            {"first_name": first_name, "last_name": last_name, "email": email},
            {"$pull": {"enrollments": {"section_details": section_details}}}
        )
        if update_result.matched_count == 0: #check if student found
            print("No matching student found. Check the entered student details")
        elif update_result.modified_count == 0: #check for enrollment (pulled out nothing)
            print("Enrollment data was not found or not removed.")
        else:   #success
            print("Enrollment was deleted successfully.")
    except Exception as exception:
        print("Error deleting enrollment")
        print(exception)

def add_student(db):
    valid_student = False
    collection = db["students"]
    while not valid_student:
        # Create a "pointer" to the students collection within the db database.
        unique_email_student: bool = False

        last_name: str = ''
        first_name: str = ''
        email: str = ''

        while not unique_email_student:
            last_name = input("Student last name--> ")
            first_name = input("Student first name--> ")

            email = input("Student email--> ")

            name_email_count: int = collection.count_documents(
                {"first_name": first_name, "last_name": last_name, "email": email})
            unique_email_student = name_email_count == 0
            if not unique_email_student:
                print("We already have a student by that name.  Try again.")

        # Build a new departments document preparatory to storing it
        student = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
        try:
            collection.insert_one(student)
            valid_student = True
        except Exception as exception:
            print("We got the following exception from a bad input:")
            print(exception)
            print("Please re-enter your values")


def select_student(db):
    collection = db["students"]
    found: bool = False
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    while not found:
        first_name = input("Student's first name--> ")
        last_name = input("Student's last name--> ")
        email = input("Student's email--> ")
        name_email_count: int = collection.count_documents(
            {"first_name": first_name, "last_name": last_name, "email": email})
        found = name_email_count == 1
        if not found:
            print("No student found by that name and email.  Try again.")
    # found_department = collection.find_one({"name": name, "abbreviation": abbreviation})
    found_student = collection.find_one(
        {"first_name": first_name, "last_name": last_name, "email": email})
    return found_student


def delete_student(db):
    student = select_student(db)
    students = db["students"]
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments.")


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [username] -->')
    project: str = input('Mongo project name [cecs-323-fall] -->')
    hash_name: str = input('7-character database hash [44qveqy] -->')
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster, tlsCAFile=certifi.where())

    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.

    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # Students Collection
    if 'students' not in db.list_collection_names():
        db.create_collection('students', check_exists=True)

    students = db['students']
    student_majors = {
        'major_name': 'CS',
        'declaration_date': '10/30/10'
    }

    section_details = {
        'department_abbreviation': 'MED',
        'course_number': 1,
        'section_number': 1,
        'semester': 'Fall',
        'section_year': 2023,
    }

    enrollment = {
        'type': 'letter_grade',
        'section_details': section_details,
        'letter_grade': {'min_satisfactory': 'B'}
    }

    student = {
        'first_name': "Jane",
        'last_name': "Smith",
        'email': "email@mail.com",
        'enrollments': [enrollment],
        'student_majors': [student_majors]
    }
    # db.create_collection('students', students_validator)
    db.command({
        "collMod": "students",
        "validator": students_validator
    })
    students.insert_one(student)

    # Majors Collection
    if 'majors' not in db.list_collection_names():
        db.create_collection('majors', check_exists=True)

    major = {
        'name': 'Biology',
        'department_abbreviation': 'CECS'
    }

    majors = db['majors']
    db.command({
        "collMod": "majors",
        "validator": majors_validator
    })
    majors.insert_one(major)

    departments = db["departments"]
    """Department Uniqueness Constraints"""
    departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviations")
    departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_names')
    departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                             unique=True, name="departments_buildings_and_offices")
    departments.create_index([('name', pymongo.ASCENDING)], unique=True, name="departments_names")

    # main menu running
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
