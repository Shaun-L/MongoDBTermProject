students_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['last_name', 'first_name', 'email'],
        'properties': {
            "_id": {},
            'last_name': {'bsonType': 'string'},
            'first_name': {'bsonType': 'string'},
            'email': {'bsonType': 'string'},
            'enrollments': {
                'bsonType': 'array',
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
                                    'enum': ["A", "B", "C"],
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
                'bsonType': 'array',
                'items': {
                    'bsonType': 'object',
                    'required': ['major_name', 'declaration_date'],
                    'properties': {
                        'major_name': {'bsonType': 'string'},
                        # TODO: add constraint - "declrationDate <= today"
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
        'required': ['department_abbreviation', 'course_number', 'section_number', 'semester', 'section_year', 'building', 'room', 'schedule', 'start_time',
                     'instructor', 'student_references'],
        'properties': {
            "_id": {},
            'department_abbreviation': {
                'bsonType': 'string',
                'description': 'TBD'
            },
            'course_number': {
                'bsonType': 'int',
                'description': 'TBD'
            },
            'section_number': {
                'bsonType': 'int',
                'description': 'must be an integer and is required'
            },
            'semester': {
                'enum': ["Fall", "Spring", "Summer I", "Summer II", "Summer III", "Winter"],
                'description': 'must be a string and is required'
            },
            'section_year': {
                'bsonType': 'int',
                'description': 'must be an integer and is required'
            },
            'building': {
                'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"],
                'description': 'must be a string and is required'
            },
            'room': {
                'bsonType': 'int',
                'minimum': 1,
                'maximum': 999,
                'description': 'must be an integer and is required'
            },
            'schedule': {
                'enum': ["MW", "TuTh", "MWF", "F", "S"],
                'description': 'must be a string and is required'
            },
            'start_time': {
                # TODO: add constraint - "startTime >= 8:00AM and <= 7:30PM"
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
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['department_abbreviation', 'course_number', 'name', 'description', 'units'],
            'properties': {
                "_id": {},
                'department_abbreviation': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'course_number': {
                    'bsonType': 'int',
                    'minimum': 100,
                    'maximum': 699,
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
                    'minimum': 1,
                    'maximum': 5,
                    'description': 'must be an integer and is required'
                }
            }
        }

}

majors_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['name', 'department_abbreviation'],
        'properties': {
            "_id": {},
            'name': {
                'bsonType': 'string',
                'enum': ["Biology", "Computer Science", "Mathematics"],
                'description': 'must be a string and is required'
            },
            'department_abbreviation': {
                'bsonType': 'string',
                'description': 'must be a string and is required, referring to the department offering the major'
            }
        }
    }
}

departments_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'the basic administrative unit within the University organized to carry on and develop'
                           ' the instructional and research activities of its faculty.',
            'required': ['abbreviation', 'name', 'chair_name', 'building', 'room', 'description'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': "string",
                    'description': "The label that identifies a singular department."
                },
                'abbreviation': {
                    'bsonType': "string",
                    "minLength": 1,
                    "maxLength": 6,
                    'description': "A shortened string that identifies a singular department"
                },
                'chair_name': {
                    'bsonType': "string",
                    "minLength": 1,
                    "maxLength": 80,
                    'description': "The person who is in charge of the department"
                },
                'building': {
                    'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"],
                    'description': "The string name of the structure the head office of the department will be"
                },
                'office': {
                    'bsonType': "int",
                    'minimum': 1,
                    'description': "An integer identifying the room the head office of"
                                   " the department will be"
                },
                'description': {
                    'bsonType': "string",
                    "maxLength": 80,
                    'description': "A sentence describing the department"
                },
            }
        }
}
