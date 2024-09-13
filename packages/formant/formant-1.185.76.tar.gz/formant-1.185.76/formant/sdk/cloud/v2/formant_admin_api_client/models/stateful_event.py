import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.stateful_event_severity import StatefulEventSeverity
from ..models.stateful_event_stream_type import StatefulEventStreamType
from ..models.stateful_event_type import StatefulEventType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stateful_event_metadata import StatefulEventMetadata
    from ..models.stateful_event_tags import StatefulEventTags


T = TypeVar("T", bound="StatefulEvent")


@attr.s(auto_attribs=True)
class StatefulEvent:
    """
    Attributes:
        time (datetime.datetime): Start time of the data range relevant to this event.
        type (Union[Unset, StatefulEventType]):
        severity (Union[Unset, StatefulEventSeverity]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, StatefulEventTags]):
        organization_id (Union[Unset, str]): ID of the organization in which to create this new event.
        end_time (Union[Unset, None, datetime.datetime]): End time of the data range relevant to this event.
        parent_id (Union[Unset, str]): If this custom event is related to another event, you can add the ID of that
            parent event here.
        metadata (Union[Unset, StatefulEventMetadata]): User-customizable metadata associated with this event in key-
            value pair format.
        message (Union[Unset, str]): Message of this event. Must match the `message` field in the Formant UI when
            configuring a custom event.
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]): ID of the device relevant to this event.
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, StatefulEventStreamType]):
        event_trigger_id (Union[Unset, None, str]):
        notification_enabled (Union[Unset, bool]): Set this to `true` to enable notifications for this event.
    """

    time: datetime.datetime
    type: Union[Unset, StatefulEventType] = UNSET
    severity: Union[Unset, StatefulEventSeverity] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "StatefulEventTags"] = UNSET
    organization_id: Union[Unset, str] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    parent_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "StatefulEventMetadata"] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, StatefulEventStreamType] = UNSET
    event_trigger_id: Union[Unset, None, str] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time = self.time.isoformat()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        organization_id = self.organization_id
        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        parent_id = self.parent_id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        message = self.message
        viewed = self.viewed
        device_id = self.device_id
        stream_name = self.stream_name
        stream_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.stream_type, Unset):
            stream_type = self.stream_type.value if self.stream_type else None

        event_trigger_id = self.event_trigger_id
        notification_enabled = self.notification_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "time": time,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if severity is not UNSET:
            field_dict["severity"] = severity
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if message is not UNSET:
            field_dict["message"] = message
        if viewed is not UNSET:
            field_dict["viewed"] = viewed
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if stream_name is not UNSET:
            field_dict["streamName"] = stream_name
        if stream_type is not UNSET:
            field_dict["streamType"] = stream_type
        if event_trigger_id is not UNSET:
            field_dict["eventTriggerId"] = event_trigger_id
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stateful_event_metadata import StatefulEventMetadata
        from ..models.stateful_event_tags import StatefulEventTags

        d = src_dict.copy()
        time = isoparse(d.pop("time"))

        _type = d.pop("type", UNSET)
        type: Union[Unset, StatefulEventType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = StatefulEventType(_type)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, StatefulEventSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = StatefulEventSeverity(_severity)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, StatefulEventTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = StatefulEventTags.from_dict(_tags)

        organization_id = d.pop("organizationId", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        parent_id = d.pop("parentId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, StatefulEventMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = StatefulEventMetadata.from_dict(_metadata)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, StatefulEventStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = StatefulEventStreamType(_stream_type)

        event_trigger_id = d.pop("eventTriggerId", UNSET)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        stateful_event = cls(
            time=time,
            type=type,
            severity=severity,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
            organization_id=organization_id,
            end_time=end_time,
            parent_id=parent_id,
            metadata=metadata,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            event_trigger_id=event_trigger_id,
            notification_enabled=notification_enabled,
        )

        stateful_event.additional_properties = d
        return stateful_event

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
