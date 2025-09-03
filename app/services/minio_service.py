from app.repositories.minio_repository import MinioRepository

class MinioService:
    def __init__(self, bucket_name: str):
        self.repo = MinioRepository(bucket_name)

    async def upload_file(self, filename: str, file: bytes, bucket_name: str = None, directory: str = None):
        if directory:
            if not directory.strip()[-1] == "/":
                directory += "/"

            filename = f"{directory}{filename}"

        await self.repo.upload_file(key=filename, data=file, bucket_name=bucket_name)

    async def get_all_files(self, directory: str = None, bucket_name: str = None) -> dict[str, str]:
        return await self.repo.list_files(directory=directory, bucket_name=bucket_name)

    async def get_file_content(self, filename: str, bucket_name: str = None, directory: str = None) -> bytes:
        if directory:
            if not directory.strip()[-1] == "/":
                directory += "/"
            filename = f"{directory}{filename}"
        data = await self.repo.download_file(filename, bucket_name=bucket_name)
        return data

    async def remove_file(self, filename: str, bucket_name: str = None, directory: str = None):
        if directory:
            if not directory.strip()[-1] == "/":
                directory += "/"
            filename = f"{directory}{filename}"

        await self.repo.delete_file(key=filename, bucket_name=bucket_name)

