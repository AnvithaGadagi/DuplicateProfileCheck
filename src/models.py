from src import db

class Profile(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    date_of_birth = db.DateField(required=False)
    class_year = db.IntField(required=False)
    email = db.EmailField(required=True)