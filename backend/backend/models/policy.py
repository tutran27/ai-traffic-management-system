"""Pydantic schemas for policy variants and parameter suggestions."""

from __future__ import annotations

from pydantic import BaseModel


class PolicyVariant(BaseModel):
    name: str
    params: dict
    family: str = "arterial"  # "arterial" | "highway"
    description: str = ""


class SuggestRequest(BaseModel):
    draft: dict
    family: str = "arterial"
    goal: str = "balanced"


class Suggestion(BaseModel):
    field: str
    value: float
    reason: str


class SuggestResponse(BaseModel):
    suggestions: list[Suggestion]
    sample_size: int
    note: str = ""
