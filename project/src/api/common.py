from humps import camelize
from pydantic import BaseModel


def to_camel(string):
    return camelize(string)


class SchemaModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Link(SchemaModel):
    rel: str
    href: str
