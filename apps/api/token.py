from config.settings import SECRET_KEY
from datetime import datetime, timedelta
import jwt

def generate_token_from_user(user):
    user["expires"] = str(datetime.now() + timedelta(minutes=5))
    token = jwt.encode(user, SECRET_KEY, "HS256")
    return token

def validate_token(token):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expires = datetime.strptime(user["expires"], '%Y-%m-%d %H:%M:%S.%f')
        difference = datetime.now() - expires
        if difference > timedelta(minutes=5):
            return {
                "status": False,
                "message": "Expired token"
            }
        else:
            data = {
                "status": True,
                "message": "Your email has been verified",
                "user": user,
            }
            return data
    except:
        data = {
            "status": False,
            "message": "Invalid Token"
        }
        return data
