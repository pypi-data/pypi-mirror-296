import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.query_aggregate import QueryAggregate
from ..models.query_types_item import QueryTypesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Query")


@attr.s(auto_attribs=True)
class Query:
    """
    Attributes:
        start (datetime.datetime):
        end (datetime.datetime):
        aggregate (Union[Unset, QueryAggregate]):
        latest_only (Union[Unset, bool]):
        next_ (Union[Unset, Any]):
        limit (Union[Unset, int]):
        drop_experimental_query_data (Union[Unset, bool]):
        device_ids (Union[Unset, List[str]]):
        names (Union[Unset, List[str]]):
        types (Union[Unset, List[QueryTypesItem]]):
        tags (Union[Unset, Any]):
        not_tags (Union[Unset, Any]):
        not_names (Union[Unset, List[str]]):
        agent_ids (Union[Unset, List[str]]):
    """

    start: datetime.datetime
    end: datetime.datetime
    aggregate: Union[Unset, QueryAggregate] = UNSET
    latest_only: Union[Unset, bool] = UNSET
    next_: Union[Unset, Any] = UNSET
    limit: Union[Unset, int] = UNSET
    drop_experimental_query_data: Union[Unset, bool] = UNSET
    device_ids: Union[Unset, List[str]] = UNSET
    names: Union[Unset, List[str]] = UNSET
    types: Union[Unset, List[QueryTypesItem]] = UNSET
    tags: Union[Unset, Any] = UNSET
    not_tags: Union[Unset, Any] = UNSET
    not_names: Union[Unset, List[str]] = UNSET
    agent_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start = self.start.isoformat()

        end = self.end.isoformat()

        aggregate: Union[Unset, str] = UNSET
        if not isinstance(self.aggregate, Unset):
            aggregate = self.aggregate.value

        latest_only = self.latest_only
        next_ = self.next_
        limit = self.limit
        drop_experimental_query_data = self.drop_experimental_query_data
        device_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_ids, Unset):
            device_ids = self.device_ids

        names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names

        types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = []
            for types_item_data in self.types:
                types_item = types_item_data.value

                types.append(types_item)

        tags = self.tags
        not_tags = self.not_tags
        not_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.not_names, Unset):
            not_names = self.not_names

        agent_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.agent_ids, Unset):
            agent_ids = self.agent_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
            }
        )
        if aggregate is not UNSET:
            field_dict["aggregate"] = aggregate
        if latest_only is not UNSET:
            field_dict["latestOnly"] = latest_only
        if next_ is not UNSET:
            field_dict["next"] = next_
        if limit is not UNSET:
            field_dict["limit"] = limit
        if drop_experimental_query_data is not UNSET:
            field_dict["dropExperimentalQueryData"] = drop_experimental_query_data
        if device_ids is not UNSET:
            field_dict["deviceIds"] = device_ids
        if names is not UNSET:
            field_dict["names"] = names
        if types is not UNSET:
            field_dict["types"] = types
        if tags is not UNSET:
            field_dict["tags"] = tags
        if not_tags is not UNSET:
            field_dict["notTags"] = not_tags
        if not_names is not UNSET:
            field_dict["notNames"] = not_names
        if agent_ids is not UNSET:
            field_dict["agentIds"] = agent_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        _aggregate = d.pop("aggregate", UNSET)
        aggregate: Union[Unset, QueryAggregate]
        if isinstance(_aggregate, Unset):
            aggregate = UNSET
        else:
            aggregate = QueryAggregate(_aggregate)

        latest_only = d.pop("latestOnly", UNSET)

        next_ = d.pop("next", UNSET)

        limit = d.pop("limit", UNSET)

        drop_experimental_query_data = d.pop("dropExperimentalQueryData", UNSET)

        device_ids = cast(List[str], d.pop("deviceIds", UNSET))

        names = cast(List[str], d.pop("names", UNSET))

        types = []
        _types = d.pop("types", UNSET)
        for types_item_data in _types or []:
            types_item = QueryTypesItem(types_item_data)

            types.append(types_item)

        tags = d.pop("tags", UNSET)

        not_tags = d.pop("notTags", UNSET)

        not_names = cast(List[str], d.pop("notNames", UNSET))

        agent_ids = cast(List[str], d.pop("agentIds", UNSET))

        query = cls(
            start=start,
            end=end,
            aggregate=aggregate,
            latest_only=latest_only,
            next_=next_,
            limit=limit,
            drop_experimental_query_data=drop_experimental_query_data,
            device_ids=device_ids,
            names=names,
            types=types,
            tags=tags,
            not_tags=not_tags,
            not_names=not_names,
            agent_ids=agent_ids,
        )

        query.additional_properties = d
        return query

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
