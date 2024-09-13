import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.triggered_event_severity import TriggeredEventSeverity
from ..models.triggered_event_stream_type import TriggeredEventStreamType
from ..models.triggered_event_type import TriggeredEventType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.triggered_event_metadata import TriggeredEventMetadata
    from ..models.triggered_event_tags import TriggeredEventTags


T = TypeVar("T", bound="TriggeredEvent")


@attr.s(auto_attribs=True)
class TriggeredEvent:
    """
    Attributes:
        severity (TriggeredEventSeverity):
        interval (int):
        time (datetime.datetime): Start time of the data range relevant to this event.
        event_trigger_id (Union[Unset, None, str]):
        interval_start (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, TriggeredEventTags]):
        type (Union[Unset, TriggeredEventType]):
        organization_id (Union[Unset, str]): ID of the organization in which to create this new event.
        end_time (Union[Unset, None, datetime.datetime]): End time of the data range relevant to this event.
        parent_id (Union[Unset, str]): If this custom event is related to another event, you can add the ID of that
            parent event here.
        metadata (Union[Unset, TriggeredEventMetadata]): User-customizable metadata associated with this event in key-
            value pair format.
        message (Union[Unset, str]): Message of this event. Must match the `message` field in the Formant UI when
            configuring a custom event.
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]): ID of the device relevant to this event.
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, TriggeredEventStreamType]):
        notification_enabled (Union[Unset, bool]): Set this to `true` to enable notifications for this event.
    """

    severity: TriggeredEventSeverity
    interval: int
    time: datetime.datetime
    event_trigger_id: Union[Unset, None, str] = UNSET
    interval_start: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "TriggeredEventTags"] = UNSET
    type: Union[Unset, TriggeredEventType] = UNSET
    organization_id: Union[Unset, str] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    parent_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "TriggeredEventMetadata"] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, TriggeredEventStreamType] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        severity = self.severity.value

        interval = self.interval
        time = self.time.isoformat()

        event_trigger_id = self.event_trigger_id
        interval_start: Union[Unset, str] = UNSET
        if not isinstance(self.interval_start, Unset):
            interval_start = self.interval_start.isoformat()

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

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

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

        notification_enabled = self.notification_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "severity": severity,
                "interval": interval,
                "time": time,
            }
        )
        if event_trigger_id is not UNSET:
            field_dict["eventTriggerId"] = event_trigger_id
        if interval_start is not UNSET:
            field_dict["intervalStart"] = interval_start
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type is not UNSET:
            field_dict["type"] = type
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
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.triggered_event_metadata import TriggeredEventMetadata
        from ..models.triggered_event_tags import TriggeredEventTags

        d = src_dict.copy()
        severity = TriggeredEventSeverity(d.pop("severity"))

        interval = d.pop("interval")

        time = isoparse(d.pop("time"))

        event_trigger_id = d.pop("eventTriggerId", UNSET)

        _interval_start = d.pop("intervalStart", UNSET)
        interval_start: Union[Unset, datetime.datetime]
        if isinstance(_interval_start, Unset):
            interval_start = UNSET
        else:
            interval_start = isoparse(_interval_start)

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
        tags: Union[Unset, TriggeredEventTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = TriggeredEventTags.from_dict(_tags)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TriggeredEventType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TriggeredEventType(_type)

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
        metadata: Union[Unset, TriggeredEventMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = TriggeredEventMetadata.from_dict(_metadata)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, TriggeredEventStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = TriggeredEventStreamType(_stream_type)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        triggered_event = cls(
            severity=severity,
            interval=interval,
            time=time,
            event_trigger_id=event_trigger_id,
            interval_start=interval_start,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
            type=type,
            organization_id=organization_id,
            end_time=end_time,
            parent_id=parent_id,
            metadata=metadata,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            notification_enabled=notification_enabled,
        )

        triggered_event.additional_properties = d
        return triggered_event

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
