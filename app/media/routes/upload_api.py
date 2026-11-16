from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from app.Enum.UploadCategory import UploadCategory
from app.db.schemas import APIResponse
from app.db.schemas.upload import FileUploadResponse
from app.model.User import User
from app.services.upload_service import save_upload_file
from app.utils.auth_utils import get_any_authenticated_user
from app.utils.ApiResponse import success_response, error_response

router = APIRouter(prefix="/media", tags=["media-upload"])


@router.post("/upload", response_model=APIResponse[FileUploadResponse])
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    category: UploadCategory = Form(default=UploadCategory.PROFILES),
    current_user: User = Depends(get_any_authenticated_user),
):

    base_url = str(request.base_url)
    success, result = await save_upload_file(file=file, category=category.value, base_url=base_url)

    if not success:
        error_response(result)

    return success_response("File uploaded successfully", result)

