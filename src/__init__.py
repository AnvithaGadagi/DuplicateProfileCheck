from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from mongoengine import OperationError,ValidationError
from flask import Blueprint, request, jsonify
import datetime
from fuzzywuzzy import fuzz
import json

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine()
db.init_app(app)


from src.models import Profile


@app.route("/")
def index():
    return "Hello World"


def add_profile(profile_data):
    profile = Profile(
        first_name=profile_data["first_name"],
        last_name=profile_data["last_name"],
        date_of_birth=datetime.datetime.strptime(profile_data["date_of_birth"], '%Y-%M-%d')
        if "date_of_birth" in profile_data
        else None,
        class_year=profile_data["class_year"]
        if "class_year" in profile_data
        else None,
        email=profile_data["email"]
    )
    profile.save()
    return profile


def check_field(profile1, profile2, fields, values, total_score):
    matching_attributes = []
    for value in values:
        is_matching = -1
        if value in fields and profile1[value] and profile2[value]:
            if profile1[value] == profile2[value]:
                total_score += 1
                is_matching = 1
            else:
                total_score -= 1
                is_matching = 0
        matching_attributes.append(is_matching)
    return total_score,matching_attributes


def check_ratio(profile1, profile2, fields, values, ratio, total_score):
    matching_attributes = []
    for value in values:
        is_matching = -1
        if value in fields:
            if fuzz.ratio(profile1[value], profile2[value]) > ratio:
                total_score += 1
                is_matching = 1
            else:
                is_matching = 0
        matching_attributes.append(is_matching)
    return total_score, matching_attributes


@app.route("/duplicate_check", methods=["GET"])
def find_duplicates():
    try:
        body = request.json
        profile1_data = body["profile1"]
        profile2_data = body["profile2"]
        fields = body["fields"]
        profile1 = add_profile(profile1_data)
        profile2 = add_profile(profile2_data)

        total_score = 0
        matching_attributes = []
        non_matching_attributes = []
        ignored_attributes = []

        if "first_name" in fields and "last_name" in fields and "email" in fields:
            name_email1 = profile1.first_name + profile1.last_name + profile1.email
            name_email2 = profile2.first_name + profile2.last_name + profile2.email
            if fuzz.ratio(name_email1,name_email2) > 80:
                total_score += 1
                matching_attributes.extend(["first_name","last_name","email"])
            else:
                non_matching_attributes.extend(["first_name","last_name","email"])
        elif "first_name" in fields and "last_name" in fields:
            ignored_attributes.append("email")
            name_email1 = profile1.first_name + profile1.last_name
            name_email2 = profile2.first_name + profile2.last_name
            if fuzz.ratio(name_email1, name_email2) > 80:
                total_score += 1
                matching_attributes.extend(["first_name", "last_name"])
            else:
                non_matching_attributes.extend(["first_name", "last_name"])
        elif "first_name" in fields and "email" in fields:
            ignored_attributes.append("last_name")
            name_email1 = profile1.first_name + profile1.email
            name_email2 = profile2.first_name + profile2.email
            if fuzz.ratio(name_email1, name_email2) > 80:
                total_score += 1
                matching_attributes.extend(["first_name", "email"])
            else:
                non_matching_attributes.extend(["first_name", "email"])
        elif "last_name" in fields and "email" in fields:
            ignored_attributes.append("first_name")
            name_email1 = profile1.last_name + profile1.email
            name_email2 = profile2.last_name + profile2.email
            if fuzz.ratio(name_email1, name_email2) > 80:
                total_score += 1
                matching_attributes.extend(["last_name", "email"])
            else:
                non_matching_attributes.extend(["last_name", "email"])
        else:
            value_check_list = ["first_name", "last_name", "email"]
            total_score, is_matching_list = check_ratio(profile1, profile2, fields, value_check_list, 80, total_score)
            for value, is_matching in zip(value_check_list, is_matching_list):
                if is_matching == -1:
                    ignored_attributes.append(value)
                elif is_matching == 1:
                    matching_attributes.append(value)
                else:
                    non_matching_attributes.append(value)

        value_check_list = ["class_year", "date_of_birth"]
        total_score, is_matching_list = check_field(profile1, profile2, fields, value_check_list, total_score)
        for value, is_matching in zip(value_check_list, is_matching_list):
            if is_matching == -1:
                ignored_attributes.append(value)
            elif is_matching == 1:
                matching_attributes.append(value)
            else:
                non_matching_attributes.append(value)

        if total_score > 1:
            return jsonify({"duplicate_profile": True, "total_match_score": total_score, "matching_attributes": matching_attributes, "non_matching_attributes": non_matching_attributes, "ignored_attributes": ignored_attributes}), 200
        else:
            return jsonify({"duplicate_profile": False, "total_match_score": total_score, "matching_attributes": matching_attributes, "non_matching_attributes": non_matching_attributes, "ignored_attributes": ignored_attributes}), 200
    except (OperationError, ValidationError) as ex:
        return jsonify({"error_msg": str(ex)}), 400
    except Exception as ex:
        return jsonify({"error_msg": ex}), 500