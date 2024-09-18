from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from .job_file import PyroJobFileResource

from .core import GET, POST, PUT, PyroJobTypes, require_resource
from .client import PyroApiClient


class PyroJobResource:
    def __init__(self, client: PyroApiClient):
        self._client = client
        self._endpoint = "jobs"

    @classmethod
    def from_client(cls, client: PyroApiClient) -> "PyroJobResource":
        return PyroJobResource(client)

    def create(self, job_type: str):
        raw = self._client.request(POST, self._endpoint, {"type": job_type})
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def get(self, id: str):
        url = f"{self._endpoint}/{id}"
        raw = self._client.request(GET, url)
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def filter(self, **kwargs):
        pass

    def update(self, id: str, **kwargs):
        # NOTE: updates any property of a job
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        job = self._client.request(PUT, url, data=None, json={**kwargs})
        print("updated job: ", job)
        # FIXME: return new job?
        # FIXME: finish

    def set_config(self, id: str, config: dict):
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        job = self._client.request(PUT, url, data=None, json={"config": config})
        print("set_config, updated job:", job)
        # FIXME: return new job?

    def delete(self, id: str):
        pass

    def duplicate(self, id: str):
        url = f"{self._endpoint}/{id}/duplicate"
        raw = self._client.request(POST, url)
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def add_file(self, id: str, fpath: str):
        path = Path(fpath)
        files = PyroJobFileResource(self._client)
        file = files.create(id, path.name, path.stat().st_size)
        intent = files.create_upload_intent(id, file.id)
        signed_url = files.signed_url_for_upload(file.id)
        files.to_s3(signed_url, path)


@dataclass
class PyroJobComputeConfig:
    cluster: Optional[str] = None
    node_group: Optional[str] = None
    max_uptime: Optional[str] = None


@dataclass
class PyroJob:
    id: str
    _resource: Optional[PyroJobResource] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[PyroJobTypes] = None
    compute_config: Optional[dict] = None
    config: Optional[dict] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None

    @classmethod
    def default(cls, **kwargs) -> "PyroJob":
        return PyroJob(**kwargs)

    @classmethod
    def from_dict(cls, _dict: dict) -> "PyroJob":
        return PyroJob(
            _dict["id"],
            _dict["_resource"],
            _dict["name"],
            _dict["description"],
            _dict["type"],
            _dict["compute_config"],
            _dict["config"],
            _dict["status"],
            _dict["is_active"],
            _dict["created_at"],
        )

    def set_resource(self, resource: PyroJobResource):
        self._resource = resource

    @require_resource
    def update(self, **kwargs):
        assert self._resource is not None
        self._resource.update(self.id, **kwargs)

    @require_resource
    def duplicate(self):
        assert self._resource is not None
        return self._resource.duplicate(self.id)

    @require_resource
    def delete(self):
        assert self._resource is not None
        return self._resource.delete(self.id)

    @require_resource
    def add_file(self, fpath: str):
        assert self._resource is not None
        return self._resource.add_file(self.id, fpath)

    @require_resource
    def set_name(self, name: str):
        assert self._resource is not None
        return self._resource.update(self.id, name=name)

    @require_resource
    def use_weather_scenario(self, speed: int, direction: int, mc: int):
        assert self._resource is not None
        # FIXME: only valid for wildest type jobs
        old_config = {} if self.config is None else self.config
        cfg = {
            **old_config,
            "wind_speeds": [speed],
            "wind_directions": [direction],
            "moisture_contents": [mc],
        }
        self._resource.set_config(self.id, cfg)
