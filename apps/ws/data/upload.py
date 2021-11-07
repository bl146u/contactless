import os

from uuid import uuid4
from typing import List
from pathlib import Path
from pydantic import conint, BaseModel
from tempfile import NamedTemporaryFile


class FileData(BaseModel):
    id: str
    path: Path
    user: str
    name: str
    total: conint(ge=0) = 0
    size: conint(ge=0) = 0

    def write(self, data: str):
        with open(self.path, "ba") as path_ref:
            path_ref.write(data)
        self.size = os.path.getsize(self.path)


class UploadPool(BaseModel):
    items: List[BaseModel] = []

    def create(self, user: str, name: str, total: int) -> FileData:
        files = list(
            filter(lambda item: item.name == name and item.user == user, self.items)
        )
        if len(files):
            return files[0]
        file = FileData(
            id=str(uuid4()),
            path=Path(NamedTemporaryFile(mode="x", delete=False).name),
            user=user,
            name=name,
            total=total,
        )
        self.items.append(file)
        return file

    def write(self, uuid: str, data: str) -> FileData:
        files = list(filter(lambda item: item.id == uuid, self.items))
        if not len(files):
            return
        file: FileData = files[0]
        file.write(data)
        return file

    def delete(self, file: FileData):
        self.items = list(filter(lambda item: item.id != file.id, self.items))
        del file
