from app.core.minio import get_s3_client
from botocore.exceptions import ClientError

class MinioRepository:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    async def upload_file(self, key: str, data: bytes, bucket_name: str = None):
        if bucket_name:
            self.bucket_name = bucket_name
        async with get_s3_client() as s3:
            await s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    async def list_files(self, bucket_name: str = None, directory: str = None) -> dict[str, str]:
        if bucket_name:
            self.bucket_name = bucket_name

        prefix = f"{directory.rstrip('/')}/" if directory else ""


        async with get_s3_client() as s3:
            response = await s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                Delimiter="/",
            )

            result: dict[str, str] = {}

            # --- папки ---
            for common_prefix in response.get("CommonPrefixes", []):
                folder_name = common_prefix["Prefix"].split("/")[-2] + "/"
                result[folder_name] = "dir"

            # --- файлы ---
            for obj in response.get("Contents", []):
                # убираем путь к директории, оставляем только имя
                filename = obj["Key"].split("/")[-1]
                if filename:  # исключаем "пустые" ключи (папки)
                    result[filename] = "file"

            return result

    async def download_file(self, key: str, bucket_name: str = None) -> bytes:
        if bucket_name:
            self.bucket_name = bucket_name
        async with get_s3_client() as s3:
            obj = await s3.get_object(Bucket=self.bucket_name, Key=key)
            content = await obj["Body"].read()
            return content


    async def delete_file(self, key: str, bucket_name: str = None):
        if bucket_name:
            self.bucket_name = bucket_name
        async with get_s3_client() as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=key)

    async def move_file(self, src_key: str, dest_key: str, bucket_name: str = None):
        if bucket_name:
            self.bucket_name = bucket_name
        async with get_s3_client() as s3:
            # Проверяем существование исходного файла
            try:
                await s3.head_object(Bucket=self.bucket_name, Key=src_key)
            except ClientError:
                raise ValueError(f"Source file '{src_key}' does not exist")

            # Копируем файл
            try:
                await s3.copy_object(
                    Bucket=self.bucket_name,
                    CopySource={'Bucket': self.bucket_name, 'Key': src_key},
                    Key=dest_key
                )
            except ClientError as e:
                raise RuntimeError(f"Failed to copy file: {e}")

            # Удаляем исходный файл только если копирование прошло успешно
            try:
                await s3.delete_object(Bucket=self.bucket_name, Key=src_key)
            except ClientError as e:
                raise RuntimeError(f"File copied but failed to delete original: {e}")