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
from skyfire_sdk.models.eth_network_type import EthNetworkType
from skyfire_sdk.models.wallet_type import WalletType
from typing import Optional, Set
from typing_extensions import Self

class Wallet(BaseModel):
    """
    Wallet
    """ # noqa: E501
    id: StrictStr
    user_id: StrictStr = Field(alias="userId")
    skyfire_user: SkyfireUser = Field(alias="skyfireUser")
    wallet_name: StrictStr = Field(alias="walletName")
    is_default: Optional[StrictBool] = Field(alias="isDefault")
    wallet_type: WalletType = Field(alias="walletType")
    network: EthNetworkType
    wallet_address: StrictStr = Field(alias="walletAddress")
    created_date: datetime = Field(alias="createdDate")
    updated_date: datetime = Field(alias="updatedDate")
    __properties: ClassVar[List[str]] = ["id", "userId", "skyfireUser", "walletName", "isDefault", "walletType", "network", "walletAddress", "createdDate", "updatedDate"]

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
        """Create an instance of Wallet from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of skyfire_user
        if self.skyfire_user:
            _dict['skyfireUser'] = self.skyfire_user.to_dict()
        # set to None if is_default (nullable) is None
        # and model_fields_set contains the field
        if self.is_default is None and "is_default" in self.model_fields_set:
            _dict['isDefault'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Wallet from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "userId": obj.get("userId"),
            "skyfireUser": SkyfireUser.from_dict(obj["skyfireUser"]) if obj.get("skyfireUser") is not None else None,
            "walletName": obj.get("walletName"),
            "isDefault": obj.get("isDefault"),
            "walletType": obj.get("walletType"),
            "network": obj.get("network"),
            "walletAddress": obj.get("walletAddress"),
            "createdDate": obj.get("createdDate"),
            "updatedDate": obj.get("updatedDate")
        })
        return _obj

from skyfire_sdk.models.skyfire_user import SkyfireUser
# TODO: Rewrite to not use raise_errors
Wallet.model_rebuild(raise_errors=False)

