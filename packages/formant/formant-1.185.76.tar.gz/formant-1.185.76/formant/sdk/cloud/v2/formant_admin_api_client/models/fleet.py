import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.device_scope import DeviceScope
    from ..models.fleet_tags import FleetTags


T = TypeVar("T", bound="Fleet")


@attr.s(auto_attribs=True)
class Fleet:
    """
    Attributes:
        name (str):
        organization_id (Union[Unset, str]):
        scope (Union[Unset, DeviceScope]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, FleetTags]):
    """

    name: str
    organization_id: Union[Unset, str] = UNSET
    scope: Union[Unset, "DeviceScope"] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "FleetTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        organization_id = self.organization_id
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if scope is not UNSET:
            field_dict["scope"] = scope
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_scope import DeviceScope
        from ..models.fleet_tags import FleetTags

        d = src_dict.copy()
        name = d.pop("name")

        organization_id = d.pop("organizationId", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: Union[Unset, DeviceScope]
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = DeviceScope.from_dict(_scope)

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
        tags: Union[Unset, FleetTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = FleetTags.from_dict(_tags)

        fleet = cls(
            name=name,
            organization_id=organization_id,
            scope=scope,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
        )

        fleet.additional_properties = d
        return fleet

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
