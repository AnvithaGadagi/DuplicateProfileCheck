# Duplicate Profile Check


## Prerequisites
- Python
- MongoDB
- pip

## Install the packages with
1. Run `pip install -r requirements.txt` to install depedencies
2. Create Database `profiledb` with profile collection in Mongodb
3. Set environment variables `FLASK_APP=main.py` and `FLASK_ENV=development`

## Starting the Server
Run `flask run` from terminal, Server will be running http://127.0.0.1:5000

## Api
`http://127.0.0.1:5000/duplicate_check` with body as the below mentioned data

## Input Samples:
Sample Input 1:

{
"profile1":{ "id": 1, "email": "knowkanhai@gmail.com", "first_name": "Kanhai", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"profile2":{ "id": 2, "email": "knowkanhai@gmail.com", "first_name": "Kanhai1", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"fields":["email","first_name", "last_name", "class_year", "date_of_birth"]
}

Output:

{
    "duplicate_profile": true,
    "ignored_attributes": [],
    "matching_attributes": [
        "first_name",
        "last_name",
        "email",
        "class_year",
        "date_of_birth"
    ],
    "non_matching_attributes": [],
    "total_match_score": 3
}



Sample Input 2:

{
"profile1":{ "id": 1, "email": "knowkanhai@gmail.com", "first_name": "Kanhai", "last_name": "Shah"},
"profile2":{ "id": 2, "email": "knowkanhai@gmail.com", "first_name": "Kanhai1", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"fields":["email","first_name", "last_name", "class_year", "date_of_birth"]
}

Output:

{
    "duplicate_profile": false,
    "ignored_attributes": [
        "class_year",
        "date_of_birth"
    ],
    "matching_attributes": [
        "first_name",
        "last_name",
        "email"
    ],
    "non_matching_attributes": [],
    "total_match_score": 1
}



Sample Input 3:

{
"profile1":{ "id": 1, "email": "knowkanhai@gmail.com", "first_name": "Kanhai", "last_name": "Shah"},
"profile2":{ "id": 2, "email": "knowkanhai+donotcompare@gmail.com", "first_name": "Kanhai1", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"fields":["first_name", "last_name"]
}

Output:

{
    "duplicate_profile": false,
    "ignored_attributes": [
        "email",
        "class_year",
        "date_of_birth"
    ],
    "matching_attributes": [
        "first_name",
        "last_name"
    ],
    "non_matching_attributes": [],
    "total_match_score": 1
}



Sample Input 4:

{
"profile1":{ "id": 1, "email": "knowkanhai@gmail.com", "first_name": "Kanhai", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"profile2":{ "id": 2, "email": "knowkanhai+donotcompare@gmail.com", "first_name": "Kanhai1", "last_name": "Shah","class_year": 2012, "date_of_birth": "1990-10-11" },
"fields":["first_name", "last_name","class_year","date_of_birth"]
}

Output:

{
    "duplicate_profile": true,
    "ignored_attributes": [
        "email"
    ],
    "matching_attributes": [
        "first_name",
        "last_name",
        "class_year",
        "date_of_birth"
    ],
    "non_matching_attributes": [],
    "total_match_score": 3
}

