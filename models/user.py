from models import user_dbs
from pymongo import errors

user_collection = user_dbs['user']


def get_user_details(username, role):
    try:
        user_data = user_collection.find_one(
            {"_id": username, "role": role}
        )

        return user_data
    except Exception as e:
        print(f"Error/get_user_details: {e}")
        return False


def register(data):
    try:
        user_collection.insert_one(data)

        err = ""
    except errors.DuplicateKeyError:
        err = "User already exists"
    except Exception as e:
        print(f"Error/register: {e}")
        err = "Something went wrong"
    
    return err


def find_donars(blood, state, district):
    try:
        donars = user_collection.find(
            {"blood": blood, "state": state, "district": district, "role": "donar"}
        )

        return donars
    except Exception as e:
        print(f"Error/find_donars: {e}")
        return False


def find_hospitals(state, district):
    try:
        hospitals = user_collection.find(
            {"role": "hospital", "state": state, "district": district}
        )

        return hospitals
    except Exception as e:
        print(f"Error/find_hospitals: {e}")
        return False
