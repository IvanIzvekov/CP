from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends, Body, Form
from app.services.minio_service import MinioService
from app.schemas.minio_schema import Directories
from app.core.database import get_session
from app.dependencies.auth_depend import check_auth_dep
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi.responses import StreamingResponse
import io
from urllib.parse import quote


bucket_name = "photo-ls"
service = MinioService(bucket_name)

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/{bucket_name}/upload")
async def upload_file(bucket_name: str,
                      file: UploadFile = FastAPIFile(...),
                      current_user = Depends(check_auth_dep),
                      directory: Optional[str] = Form(None)):
    try:
        content = await file.read()

        await service.upload_file(filename=file.filename, file=content, bucket_name=bucket_name, directory=directory)
        return {"filename": file.filename, "status": "uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{bucket_name}/files/list")
async def list_files(bucket_name: str,
                     current_user = Depends(check_auth_dep),
                    directory: Optional[str] = Form(None)):
    try:
        files = await service.get_all_files(directory=directory, bucket_name=bucket_name)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{bucket_name}/get-file/{filename}")
async def get_file(bucket_name: str,
                   filename: str,
                current_user = Depends(check_auth_dep),
                directory: Optional[str] = Form(None)):
    try:
        content = await service.get_file_content(filename=filename, bucket_name=bucket_name, directory=directory)
        safe_filename = quote(filename)
        return StreamingResponse(io.BytesIO(content),
                                 media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={safe_filename}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{bucket_name}/delete-file/{filename}")
async def delete_file(bucket_name: str,
                      filename: str,
                      current_user = Depends(check_auth_dep),
                      directory: Optional[str] = Form(None)):
    try:
        await service.remove_file(filename, bucket_name=bucket_name, directory=directory)
        return {"filename": filename, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{bucket_name}/move-file/{filename}")
async def move_file(bucket_name: str,
                    filename: str,
                    current_user = Depends(check_auth_dep),
                    directory_from: Optional[str] = Form(None),
                    directory_to: Optional[str] = Form(None)):
    try:
        content = await service.get_file_content(filename=filename, bucket_name=bucket_name, directory=directory_from)

        await service.upload_file(filename, bucket_name=bucket_name, directory=directory_to, file=content)

        new_content = await service.get_file_content(filename=filename, bucket_name=bucket_name, directory=directory_to)
        if new_content != content:
            raise HTTPException(status_code=500, detail="File verification failed after upload")

        await service.remove_file(filename, bucket_name=bucket_name, directory=directory_from)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": filename, "status": "moved"}
