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
from notehub_py.models.firmware_status import FirmwareStatus
from typing import Optional, Set
from typing_extensions import Self

class OTAStatus(BaseModel):
    """
    OTAStatus
    """ # noqa: E501
    device_uid: Optional[StrictStr] = Field(default=None, description="The device UID")
    tags: Optional[StrictStr] = Field(default=None, description="The tags associated with the device")
    notecard_current_firmware: Optional[FirmwareStatus] = None
    notecard_dfu_began_at: Optional[StrictStr] = Field(default=None, description="The time the Notecard DFU began")
    notecard_dfu_status: Optional[StrictStr] = Field(default=None, description="The status of the Notecard DFU")
    notecard_requested_firmware: Optional[FirmwareStatus] = None
    notecard_requested_at: Optional[StrictStr] = Field(default=None, description="The time the Notecard firmware was requested")
    notecard_requested_scope: Optional[StrictStr] = Field(default=None, description="The scope of the Notecard firmware request")
    notecard_requested_show_details: Optional[StrictBool] = Field(default=None, description="Whether to show details of the Notecard firmware request")
    notecard_requested_status: Optional[StrictStr] = Field(default=None, description="The status of the Notecard firmware request")
    host_current_firmware: Optional[FirmwareStatus] = None
    host_dfu_began_at: Optional[StrictStr] = Field(default=None, description="The time the host DFU began")
    host_dfu_status: Optional[StrictStr] = Field(default=None, description="The status of the host DFU")
    host_requested_firmware: Optional[FirmwareStatus] = None
    host_requested_at: Optional[StrictStr] = Field(default=None, description="The time the host firmware was requested")
    host_requested_scope: Optional[StrictStr] = Field(default=None, description="The scope of the host firmware request")
    host_requested_show_details: Optional[StrictBool] = Field(default=None, description="Whether to show details of the host firmware request")
    host_requested_status: Optional[StrictStr] = Field(default=None, description="The status of the host firmware request")
    __properties: ClassVar[List[str]] = ["device_uid", "tags", "notecard_current_firmware", "notecard_dfu_began_at", "notecard_dfu_status", "notecard_requested_firmware", "notecard_requested_at", "notecard_requested_scope", "notecard_requested_show_details", "notecard_requested_status", "host_current_firmware", "host_dfu_began_at", "host_dfu_status", "host_requested_firmware", "host_requested_at", "host_requested_scope", "host_requested_show_details", "host_requested_status"]

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
        """Create an instance of OTAStatus from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of notecard_current_firmware
        if self.notecard_current_firmware:
            _dict['notecard_current_firmware'] = self.notecard_current_firmware.to_dict()
        # override the default output from pydantic by calling `to_dict()` of notecard_requested_firmware
        if self.notecard_requested_firmware:
            _dict['notecard_requested_firmware'] = self.notecard_requested_firmware.to_dict()
        # override the default output from pydantic by calling `to_dict()` of host_current_firmware
        if self.host_current_firmware:
            _dict['host_current_firmware'] = self.host_current_firmware.to_dict()
        # override the default output from pydantic by calling `to_dict()` of host_requested_firmware
        if self.host_requested_firmware:
            _dict['host_requested_firmware'] = self.host_requested_firmware.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OTAStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "device_uid": obj.get("device_uid"),
            "tags": obj.get("tags"),
            "notecard_current_firmware": FirmwareStatus.from_dict(obj["notecard_current_firmware"]) if obj.get("notecard_current_firmware") is not None else None,
            "notecard_dfu_began_at": obj.get("notecard_dfu_began_at"),
            "notecard_dfu_status": obj.get("notecard_dfu_status"),
            "notecard_requested_firmware": FirmwareStatus.from_dict(obj["notecard_requested_firmware"]) if obj.get("notecard_requested_firmware") is not None else None,
            "notecard_requested_at": obj.get("notecard_requested_at"),
            "notecard_requested_scope": obj.get("notecard_requested_scope"),
            "notecard_requested_show_details": obj.get("notecard_requested_show_details"),
            "notecard_requested_status": obj.get("notecard_requested_status"),
            "host_current_firmware": FirmwareStatus.from_dict(obj["host_current_firmware"]) if obj.get("host_current_firmware") is not None else None,
            "host_dfu_began_at": obj.get("host_dfu_began_at"),
            "host_dfu_status": obj.get("host_dfu_status"),
            "host_requested_firmware": FirmwareStatus.from_dict(obj["host_requested_firmware"]) if obj.get("host_requested_firmware") is not None else None,
            "host_requested_at": obj.get("host_requested_at"),
            "host_requested_scope": obj.get("host_requested_scope"),
            "host_requested_show_details": obj.get("host_requested_show_details"),
            "host_requested_status": obj.get("host_requested_status")
        })
        return _obj


