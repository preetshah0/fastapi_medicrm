from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

def success_response(message="Success", data=None):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "success": True,
            "message": message,
            "data": data,
        }),
    )

def error_response(message="Error", data=None):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "success": False,
            "message": message,
            "data": data,
        }
    )


def validation_error_response(message="Validation failed", data=None):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "success": False,
            "message": message,
            "data": data,
        }
    )


def not_found_response(message="Resource not found", data=None):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail = {
            "success": False,
            "message": message,
            "data": data,
        }
    )

def unauthorized_response(message="Unauthorized", data=None):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = {
            "success": False,
            "message": message,
            "data": data,
        }
    )

def redirect_response(url: str):
    return RedirectResponse(
        url=url, 
        status_code=status.HTTP_302_FOUND
    )



def HTTP_403_RESPONSE(message="Forbidden", data=None):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "success": False,
            "message": message,
            "data": data,
        },
    )