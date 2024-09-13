from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Quaternion")


@attr.s(auto_attribs=True)
class Quaternion:
    """
    Attributes:
        x (float):
        y (float):
        z (float):
        w (float):
    """

    x: float
    y: float
    z: float
    w: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        x = self.x
        y = self.y
        z = self.z
        w = self.w

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "x": x,
                "y": y,
                "z": z,
                "w": w,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        x = d.pop("x")

        y = d.pop("y")

        z = d.pop("z")

        w = d.pop("w")

        quaternion = cls(
            x=x,
            y=y,
            z=z,
            w=w,
        )

        quaternion.additional_properties = d
        return quaternion

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
