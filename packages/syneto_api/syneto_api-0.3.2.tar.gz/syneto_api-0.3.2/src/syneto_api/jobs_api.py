import os
from datetime import datetime
from typing import List, Optional

from .api_client import APIClientBase, InvalidInputException


class Jobs(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("PROTECTION_SERVICE", ""), **kwargs)

    def get_jobs(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        types: Optional[List[str]] = None,
        free_text: Optional[str] = None,
        categories: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        created_after: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        hide_acknowledged: Optional[bool] = None,
        hide_nested_jobs: Optional[bool] = None,
    ):
        query_params = {
            "limit": limit,
            "offset": offset,
            "types": types,
            "free_text": free_text,
            "categories": categories,
            "statuses": statuses,
            "created_after": created_after.isoformat() if created_after else None,
            "updated_after": updated_after.isoformat() if updated_after else None,
            "created_before": created_before.isoformat() if created_before else None,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "hide_acknowledged": hide_acknowledged,
            "hide_nested_jobs": hide_nested_jobs,
        }

        query_params = {k: v for k, v in query_params.items() if v is not None}

        query_list = []
        for key, value in query_params.items():
            if isinstance(value, list):
                query_list.extend((key, v) for v in value)
            else:
                query_list.append((key, value))

        return self.get_request("/jobs", query_args=query_list)

    def get_job(self, id: str):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.get_request("/jobs/{id}", id=id)

    def create_job(self, body: dict):
        return self.post_request("/jobs", body=body)

    def patch_job(self, id: str, body: dict):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.patch_request("/jobs/{id}", id=id, body=body)

    def delete_job(self, id: str):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.delete_request("/jobs/{id}", id=id)
