import json
from typing import Optional, Type, TypedDict, TypeVar

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from .models import Pagination
from .utils import filter_dict_values

_FieldT = TypeVar('_FieldT')
_FilterFieldDictT = TypedDict('_FilterFieldDictT', {
    'default': Optional[_FieldT],
    'example': Optional[_FieldT],
    'description': Optional[str]
})
_IntFieldDictT = TypedDict('_IntFieldDictT', {
    'default': Optional[int],
    'example': Optional[int],
    'description': Optional[str]
})


def get_pagination_dependency(offset_kwargs: Optional[_IntFieldDictT] = None,
                              limit_kwargs: Optional[_IntFieldDictT] = None,
                              filter_kwargs: Optional[_FilterFieldDictT] = None):
    offset_kwargs = {
        'default': 0,
        'ge': 0,
        **(offset_kwargs or {})
    }

    limit_kwargs = {
        'default': 250,
        'ge': 1,
        **(limit_kwargs or {})
    }

    filter_kwargs = {
        'default': None,
        'description': 'Represents values passed to the query as kwargs',
        **(filter_kwargs or {})
    }

    class PageRequestSchema:
        def __init__(self,
                     offset: int = Query(**offset_kwargs),
                     limit: Optional[int] = Query(**limit_kwargs),
                     filter: Optional[str] = Query(**filter_kwargs)):
            self.offset = offset
            self.limit = limit
            # ignore filter, it will be handled by 'pg.Pagination'

        def dict(self):
            return {
                'offset': self.offset,
                'limit': self.limit,
            }

    async def _parse_pagination_request(request: Request,
                                        page_request: PageRequestSchema = Depends()) -> Pagination:
        base_url = str(request.url).split('?')[0]
        extra_params = {k: v
                        for k, v in request.query_params.items()
                        if k not in ('offset', 'limit')}
        for k, v in extra_params.items():
            try:
                extra_params[k] = json.loads(v)
            except json.JSONDecodeError:
                pass  # do nothing

        return Pagination(
            # filter `None` values
            base_url=base_url,
            request=filter_dict_values({
                **extra_params,
                **page_request.dict(),
            })
        )

    return _parse_pagination_request


def generate_response_schema(of_type: Type):
    class PageResponseSchema(BaseModel):
        results: list[of_type]
        count: int
        next: str
        previous: str
    return PageResponseSchema
