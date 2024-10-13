from typing import List

from pydantic import BaseModel, RootModel, Field


class PartizanPerson(BaseModel):
    surname: str | None = Field(default="Не указано.")
    name: str | None = Field(default="Не указано.")
    middlename: str | None = Field(default="Не указано.")
    date_of_birth: str | None = Field(default="Не указано.")
    place_of_birth: str | None = Field(default="Не указано.")
    call_place: str | None = Field(default="Не указано.")
    last_call_place: str | None = Field(default="Не указано.")
    rank: str | None = Field(default="Не указано.")
    reason_of_leave: str | None = Field(default="Не указано.")
    date_of_leave: str | None = Field(default="Не указано.")
    place_of_leave: str | None = Field(default="Не указано.")
    issue: str | None = Field(default="Не указано.")


class Partizan(BaseModel):
    id: str
    full_name: str
    date_of_birth: str | None
    date_of_die: str | None


class AllPartizans(RootModel):
    root: List[Partizan]
