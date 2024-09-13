from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ReorderRequestItem")


@attr.s(auto_attribs=True)
class ReorderRequestItem:
    """
    Attributes:
        id (str):
        index (int):
    """

    id: str
    index: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        index = self.index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "index": index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        index = d.pop("index")

        reorder_request_item = cls(
            id=id,
            index=index,
        )

        reorder_request_item.additional_properties = d
        return reorder_request_item

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
