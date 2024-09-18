from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import requests

from .client import PyroApiClient
from .core import POST


@dataclass
class PyroUploadCreds:
    access_key_id: str
    secret_access_key: str
    session_token: str


@dataclass
class PyroUploadIntent:
    creds: PyroUploadCreds
    key: str
    bucket: str
    region: str


def _file_stream_generator(file, chunk_size=8192):
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield chunk


class PyroJobFileResource:
    def __init__(self, client: PyroApiClient):
        self._client = client

    def create(self, job_id: str, name: str, size: int):
        data = {"display_name": name, "size_bytes": size}
        url = f"jobs/{job_id}/files"
        raw = self._client.request(POST, url, data)
        _dict = {**raw, "_resource": self}
        return PyroFile.from_dict(_dict)

    def create_upload_intent(self, job_id: str, file_id: str):
        url = f"jobs/{job_id}/files/{file_id}/create_upload_intent"
        raw = self._client.request(POST, url)
        intent = PyroUploadIntent(
            PyroUploadCreds(
                raw["creds"]["accessKeyId"],
                raw["creds"]["secretAccessKey"],
                raw["creds"]["sessionToken"],
            ),
            raw["key"],
            raw["bucket"],
            raw["region"],
        )
        return intent

    def signed_url(self, file_id: str):
        url = f"files/{file_id}/signed_url"
        raw = self._client.request(POST, url)
        return raw["url"]

    def signed_url_for_upload(self, file_id: str):
        url = f"files/{file_id}/signed_url_for_upload"
        raw = self._client.request(POST, url)
        return raw["url"]

    def to_s3(self, signed_url: str, fpath: Path):
        # TODO: handle multipart upload for bigger files
        with open(fpath, "rb") as file:
            # response = requests.put(signed_url, data=_file_stream_generator(file))
            response = requests.put(signed_url, data=file)


@dataclass
class PyroFile:
    id: str
    name: str
    extension: str
    size_bytes: str
    is_active: str
    created_at: str
    status: str
    display_name: str
    s3_uri: Optional[str]
    life_cycle: Optional[str]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroFile":
        return PyroFile(
            d["id"],
            d["name"],
            d["extension"],
            d["size_bytes"],
            d["is_active"],
            d["created_at"],
            d["status"],
            d["display_name"],
            d["s3_uri"],
            d["life_cycle"],
        )
