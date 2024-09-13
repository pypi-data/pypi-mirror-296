# coding: utf-8

"""
    Skyfire API

    The Skyfire API is designed to allow agents to interact with the Skyfire platform to enable autonomous payments.

    The version of the OpenAPI document: 1.0.0
    Contact: support@skyfire.xyz
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from skyfire_sdk.models.user_type import UserType
from typing import Optional, Set
from typing_extensions import Self

class SkyfireUser(BaseModel):
    """
    SkyfireUser
    """ # noqa: E501
    id: StrictStr
    username: StrictStr
    email: StrictStr
    is_admin: StrictBool = Field(alias="isAdmin")
    is_enterprise_admin: StrictBool = Field(alias="isEnterpriseAdmin")
    is_active: StrictBool = Field(alias="isActive")
    is_onboarded: StrictBool = Field(alias="isOnboarded")
    user_type: Optional[UserType] = Field(default=None, alias="userType")
    created_date: datetime = Field(alias="createdDate")
    updated_date: datetime = Field(alias="updatedDate")
    wallets: List[Wallet]
    parent_skyfire_user: Optional[SkyfireUser] = Field(default=None, alias="parentSkyfireUser")
    created_users: List[SkyfireUser] = Field(alias="createdUsers")
    stytch_user_id: Optional[StrictStr] = Field(default=None, alias="stytchUserId")
    __properties: ClassVar[List[str]] = ["id", "username", "email", "isAdmin", "isEnterpriseAdmin", "isActive", "isOnboarded", "userType", "createdDate", "updatedDate", "wallets", "parentSkyfireUser", "createdUsers", "stytchUserId"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of SkyfireUser from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in wallets (list)
        _items = []
        if self.wallets:
            for _item in self.wallets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['wallets'] = _items
        # override the default output from pydantic by calling `to_dict()` of parent_skyfire_user
        if self.parent_skyfire_user:
            _dict['parentSkyfireUser'] = self.parent_skyfire_user.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in created_users (list)
        _items = []
        if self.created_users:
            for _item in self.created_users:
                if _item:
                    _items.append(_item.to_dict())
            _dict['createdUsers'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SkyfireUser from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "username": obj.get("username"),
            "email": obj.get("email"),
            "isAdmin": obj.get("isAdmin"),
            "isEnterpriseAdmin": obj.get("isEnterpriseAdmin"),
            "isActive": obj.get("isActive"),
            "isOnboarded": obj.get("isOnboarded"),
            "userType": obj.get("userType"),
            "createdDate": obj.get("createdDate"),
            "updatedDate": obj.get("updatedDate"),
            "wallets": [Wallet.from_dict(_item) for _item in obj["wallets"]] if obj.get("wallets") is not None else None,
            "parentSkyfireUser": SkyfireUser.from_dict(obj["parentSkyfireUser"]) if obj.get("parentSkyfireUser") is not None else None,
            "createdUsers": [SkyfireUser.from_dict(_item) for _item in obj["createdUsers"]] if obj.get("createdUsers") is not None else None,
            "stytchUserId": obj.get("stytchUserId")
        })
        return _obj

from skyfire_sdk.models.wallet import Wallet
# TODO: Rewrite to not use raise_errors
SkyfireUser.model_rebuild(raise_errors=False)

