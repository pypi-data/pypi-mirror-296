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

from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class DeviceUsage(BaseModel):
    """
    DeviceUsage
    """ # noqa: E501
    since: Optional[Union[StrictFloat, StrictInt]] = None
    duration: Optional[Union[StrictFloat, StrictInt]] = None
    bytes_rcvd: Optional[Union[StrictFloat, StrictInt]] = None
    bytes_sent: Optional[Union[StrictFloat, StrictInt]] = None
    bytes_rcvd_secondary: Optional[Union[StrictFloat, StrictInt]] = None
    bytes_sent_secondary: Optional[Union[StrictFloat, StrictInt]] = None
    sessions_tcp: Optional[Union[StrictFloat, StrictInt]] = None
    sessions_tls: Optional[Union[StrictFloat, StrictInt]] = None
    notes_rcvd: Optional[Union[StrictFloat, StrictInt]] = None
    note_sent: Optional[Union[StrictFloat, StrictInt]] = None
    __properties: ClassVar[List[str]] = ["since", "duration", "bytes_rcvd", "bytes_sent", "bytes_rcvd_secondary", "bytes_sent_secondary", "sessions_tcp", "sessions_tls", "notes_rcvd", "note_sent"]

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
        """Create an instance of DeviceUsage from a JSON string"""
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
        """Create an instance of DeviceUsage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "since": obj.get("since"),
            "duration": obj.get("duration"),
            "bytes_rcvd": obj.get("bytes_rcvd"),
            "bytes_sent": obj.get("bytes_sent"),
            "bytes_rcvd_secondary": obj.get("bytes_rcvd_secondary"),
            "bytes_sent_secondary": obj.get("bytes_sent_secondary"),
            "sessions_tcp": obj.get("sessions_tcp"),
            "sessions_tls": obj.get("sessions_tls"),
            "notes_rcvd": obj.get("notes_rcvd"),
            "note_sent": obj.get("note_sent")
        })
        return _obj


