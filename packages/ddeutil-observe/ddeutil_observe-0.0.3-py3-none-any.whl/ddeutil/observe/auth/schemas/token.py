# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Union

from pydantic import UUID4, BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")


class TokenRefresh(Token):
    refresh_token: str


class TokenRefreshCreate(TokenRefresh):
    user_id: UUID4
    is_active: bool = Field(default=True)


class TokenRefreshForm(BaseModel):
    refresh_token: str


class TokenDataSchema(BaseModel):
    username: Union[str, None] = None
    scopes: list[str] = []
