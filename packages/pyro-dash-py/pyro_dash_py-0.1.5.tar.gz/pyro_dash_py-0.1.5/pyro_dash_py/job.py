from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

from .job_file import PyroFile, PyroJobFileResource

from .core import (
    GET,
    POST,
    PUT,
    IncompatibleJobTypeError,
    PyroJobTypes,
    require_resource,
)
from .client import PyroApiClient


class PyroJobResource:
    """
    Represents Jobs such as WildEST, FSim, Fuelscape, Liability Risk Pipeline, etc.
    """

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
        # NOTE: the GET /jobs endpoint accepts filters that are
        # either in the query string OR in the body
        # we specify our filters in the json body because it's more
        # "compatible" with objects (i.e. less buggy)
        resp = self._client.request(GET, self._endpoint, data=None, json={**kwargs})

        jobs = []
        for raw_job in resp["data"]:
            job = PyroJob.from_dict({**raw_job, "_resource": self})
            jobs.append(job)

        return PyroJobList(
            resp["page"],
            resp["limit"],
            resp["totalPages"],
            resp["totalRecords"],
            jobs,
        )

    def update(self, id: str, **kwargs) -> "PyroJob":
        # NOTE: updates any property of a job
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        resp = self._client.request(PUT, url, data=None, json={**kwargs})
        _dict = {**resp, "_resource": self}
        return PyroJob.from_dict(_dict)

    def set_config(self, id: str, config: dict) -> "PyroJob":
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        resp = self._client.request(PUT, url, data=None, json={"config": config})
        _dict = {**resp, "_resource": self}
        return PyroJob.from_dict(_dict)

    def duplicate(self, id: str) -> "PyroJob":
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
        files.update(id, file.id, status="ready")

    def preview(self, id: str):
        raise NotImplementedError()

    def start(self, id: str):
        raise NotImplementedError()

    def delete(self, id: str):
        raise NotImplementedError()

    def cancel(self, id: str):
        raise NotImplementedError()

    def list_inputs(self, id: str):
        raise NotImplementedError()

    def list_outputs(self, id: str):
        raise NotImplementedError()

    def list_files(self, id: str) -> List[PyroFile]:
        url = f"{self._endpoint}/{id}/files"
        resp = self._client.request(GET, url)

        file_resource = PyroJobFileResource(self._client)

        files: List[PyroFile] = []
        for raw_file in resp:
            files.append(PyroFile.from_dict({**raw_file, "_resource": file_resource}))

        return files

    def get_file(self, id: str, file_id: str):
        raise NotImplementedError()

    def duration(self, id: str):
        raise NotImplementedError()

    def cost(self, id: str):
        raise NotImplementedError()

    def get_logs(self, id: str):
        raise NotImplementedError()

    def get_status(self, id: str):
        raise NotImplementedError()


@dataclass
class PyroJobComputeConfig:
    cluster: Optional[str] = None
    node_group: Optional[str] = None
    max_uptime: Optional[str] = None


@dataclass
class PyroJob:
    """
    Represents a single PyroJob.

    """

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
        """
        Create a PyroJob from a python dict.
        """
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
        """
        Duplicate this job. Returns a new instance of `PyroJob`.

        Example:

        ```python
        my_job = pyro.jobs.create("fsim")
        new_job = my_job.duplicate()
        ```
        """
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
        if self.type != "wildest":
            raise IncompatibleJobTypeError(
                "weather scenarios are only valid for WildEST"
            )

        old_config = {} if self.config is None else self.config
        cfg = {
            **old_config,
            "wind_speeds": [speed],
            "wind_directions": [direction],
            "moisture_contents": [mc],
        }
        self._resource.set_config(self.id, cfg)

    @require_resource
    def list_files(self):
        assert self._resource is not None
        return self._resource.list_files(self.id)


@dataclass
class PyroJobList:
    page: int
    limit: int
    total_pages: int
    total_records: int
    data: List[PyroJob]
