# coding: utf-8

"""
    Notehub API

    The OpenAPI definition for the Notehub.io API. 

    The version of the OpenAPI document: 1.1.0
    Contact: engineering@blues.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class OTAUpdateRequest(BaseModel):
    """
    OTAUpdateRequest
    """ # noqa: E501
    filename: Optional[StrictStr] = Field(default=None, description="The name of the firmware file")
    device_uids: Optional[List[StrictStr]] = Field(default=None, description="The device UIDs to update")
    fleet_uids: Optional[List[StrictStr]] = Field(default=None, description="The fleet UIDs to update")
    device_tags: Optional[List[StrictStr]] = Field(default=None, description="The device tags to update")
    version: Optional[StrictStr] = Field(default=None, description="The version of the firmware")
    md5: Optional[StrictStr] = Field(default=None, description="The MD5 hash of the firmware file", alias="MD5")
    type: Optional[StrictStr] = Field(default=None, description="The type of firmware")
    product: Optional[StrictStr] = Field(default=None, description="The product that the firmware is for")
    target: Optional[StrictStr] = Field(default=None, description="The target device for the firmware")
    unpublished: Optional[StrictBool] = Field(default=None, description="If true, the firmware is unpublished")
    cancel_dfu: Optional[StrictBool] = Field(default=None, description="If true, the DFU is canceled")
    __properties: ClassVar[List[str]] = ["filename", "device_uids", "fleet_uids", "device_tags", "version", "MD5", "type", "product", "target", "unpublished", "cancel_dfu"]

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
        """Create an instance of OTAUpdateRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OTAUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "filename": obj.get("filename"),
            "device_uids": obj.get("device_uids"),
            "fleet_uids": obj.get("fleet_uids"),
            "device_tags": obj.get("device_tags"),
            "version": obj.get("version"),
            "MD5": obj.get("MD5"),
            "type": obj.get("type"),
            "product": obj.get("product"),
            "target": obj.get("target"),
            "unpublished": obj.get("unpublished"),
            "cancel_dfu": obj.get("cancel_dfu")
        })
        return _obj


