import certifi as certifi
import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
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


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [shaunlim] -->')
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

    # db.create_collection("students")
    collection = db['students']
    student_majors = {
        'name': 'CS',
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
    }

    student = {
        'first_name': "Jane",
        'last_name': "Smith",
        'email': "email@mail.com",
        'enrollments': enrollment,
        'student_majors': student_majors
    }

    students_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['last_name', 'first_name', 'email'],
            'properties': {
                'last_name': {'bsonType': 'string'},
                'first_name': {'bsonType': 'string'},
                'email': {'bsonType': 'string'},
                'enrollments': {
                    'bsonType': 'object',
                    'items': {
                        'bsonType': 'object',
                        'required': ['type', 'section_details'],
                        'properties': {
                            'type': {'enum': ['letter_grade', 'pass_fail']},
                            'section_details': {
                                'bsonType': 'object',
                                'items': [
                                    {'bsonType': 'string'},  # Assuming all elements in section_details are strings
                                    {'bsonType': 'int'},
                                    {'bsonType': 'int'},
                                    {'bsonType': 'string'},
                                    {'bsonType': 'int'}
                                ],
                            },
                            'letter_grade': {
                                'bsonType': 'object',
                                'description': 'must be an object if bsonType is letter_grade',
                                # Specify properties of letter_grade if needed
                                "properties": {
                                    "min_satisfactory": {
                                        "bsonType": "string",
                                        "description": "must be a string and is required if bsonType is letter_grade"
                                    }
                                }
                            },
                            'pass_fail': {
                                'bsonType': 'object',
                                'description': 'must be an object if bsonType is pass_fail',
                                # Specify properties of pass_fail if needed
                                "properties": {
                                    "application_date": {
                                        "bsonType": "string",
                                        "description": "must be a string and is required if bsonType is pass_fail"
                                    }
                                }
                            }
                        }
                    }
                },
                'student_majors': {
                    'bsonType': 'object',
                    'items': {
                        'bsonType': 'array',
                        'required': ['major_name', 'declaration_date'],
                        'properties': {
                            'major_name': {'bsonType': 'string'},
                            'declaration_date': {'bsonType': 'string'}  # Assuming declaration_date is a string
                        }
                    }
                }
            }
        }
    }

    # db.create_collection('students', students_validator)
    sections_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['section_number', 'semester', 'section_year', 'building', 'room', 'schedule', 'start_time',
                         'instructor', 'student_ids'],
            'properties': {
                'section_number': {
                    'bsonType': 'int',
                    'description': 'must be an integer and is required'
                },
                'semester': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'section_year': {
                    'bsonType': 'int',
                    'description': 'must be an integer and is required'
                },
                'building': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'room': {
                    'bsonType': 'int',
                    'description': 'must be an integer and is required'
                },
                'schedule': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'start_time': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'instructor': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'student_references': {
                    'bsonType': 'array',
                    'items': {
                        'bsonType': 'int',
                        'description': 'must be integers representing student IDs'
                    }
                }
            }
        }
    }

    courses_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['department_abbreviation', 'course_number', 'name', 'description', 'units'],
                'properties': {
                    'department_abbreviation': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'must be an integer and is required'
                    },
                    'name': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'units': {
                        'bsonType': 'int',
                        'description': 'must be an integer and is required'
                    }
                }
            }
        }
    }

    majors_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['name', 'department_abbreviation', 'requirements'],
                'properties': {
                    'name': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'department_abbreviation': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required, referring to the department offering the major'
                    },
                    'requirements': {
                        'bsonType': 'array',
                        'items': {
                            'bsonType': 'string',
                            'description': 'must be strings representing course numbers or other requirement identifiers'
                        }
                    }
                }
            }
        }
    }

    departments_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['abbreviation', 'name', 'chair_name', 'building', 'room', 'description'],
                'properties': {
                    'abbreviation': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'name': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'building': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'room': {
                        'bsonType': 'int',
                        'description': 'must be an integer and is required'
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    }
                }
            }
        }
    }
    db.command({
        "collMod": "students",
        "validator": students_validator
    })
    collection.insert_one(student)
