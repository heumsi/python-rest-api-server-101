from typing import List

from humps import camelize
from pydantic import BaseModel
from fastapi import Request

def to_camel(string):
    return camelize(string)


class SchemaModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Link(SchemaModel):
    rel: str
    href: str


class Pagination(SchemaModel):
    offset: int
    limit: int
    total: int


def get_links_for_pagination(offset: int, limit: int, total: int, request: Request) -> List[Link]:
    next_offset = offset + limit
    prev_offset = offset - limit
    request_url_without_query_params = str(request.url.remove_query_params(keys=["limit", "offset"]))
    links = [
        Link(
            rel="self",
            href=str(request.url)
        )
    ]
    if next_offset < total:
        links.append(
            Link(
                rel="next",
                href=f"{request_url_without_query_params}?offset={next_offset}&limit={limit}"
            )
        )
    if offset > 0:
        links.append(
            Link(
                rel="prev",
                href=f"{request_url_without_query_params}?offset={prev_offset}&limit={limit}"
            )
        )
    return links
