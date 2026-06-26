from fastapi.responses import JSONResponse,RedirectResponse

def success_response(message = "Success", data=None):
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )

def error_response(message="Error",data=None):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": message,
            "data": data,
        },
    )

def not_found_response(message="Resource not found", data=None):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": message,
            "data": data,
        },
    )

def unauthorized_response(message="Unauthorized", data=None):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": message,
            "data": data,
        },
    )

def redirect_response(url:str):
    return RedirectResponse(
        url=url, 
        status_code=302
    )