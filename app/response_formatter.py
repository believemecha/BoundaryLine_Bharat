# app/response_formatter.py

def render_success(data=None, message="Success", status_code=200):
    return {
        "status_code": status_code,
        "success": True,
        "message": message,
        "data": data,
    }

def render_error(message="Error occurred", status_code=400, details=None):
    return {
        "status_code": status_code,
        "success": False,
        "message": message,
        "details": details,
    }
