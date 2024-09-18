from dataclasses import dataclass
from typing import Optional

from .core import POST, require_resource
from .client import PyroApiClient


class PyroProjectResource:
    def __init__(self, client: PyroApiClient):
        self.client = client
        self._endpoint = "projects"

    def create(self, name: Optional[str] = None):
        data = {"name": name}
        raw = self.client.request("POST", self._endpoint, data)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def get(self, id: str):
        url = f"{self._endpoint}/{id}"
        raw = self.client.request("GET", url)
        return PyroProject.from_dict(raw)

    def filter(self, params: dict):
        raw = self.client.request("GET", self._endpoint, params)
        # TODO: parse list

    def add_job(self, id: str, job_id: str):
        url = f"{self._endpoint}/{id}/add_job"
        self.client.request(POST, url, {"job_id": job_id})


@dataclass
class PyroProject:
    id: str
    name: str
    created_at: str
    is_active: str
    _resource: Optional[PyroProjectResource]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroProject":
        return PyroProject(
            d["id"],
            d["name"],
            d["created_at"],
            d["is_active"],
            d["_resource"],
        )

    @require_resource
    def add_job(self, job_id: str):
        assert self._resource is not None
        return self._resource.add_job(self.id, job_id)
