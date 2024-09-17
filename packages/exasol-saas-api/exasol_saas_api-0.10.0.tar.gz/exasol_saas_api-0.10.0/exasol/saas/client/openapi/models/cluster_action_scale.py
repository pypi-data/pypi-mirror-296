from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="ClusterActionScale")


@_attrs_define
class ClusterActionScale:
    """ 
        Attributes:
            cluster_id (str):
            size (str):
     """

    cluster_id: str
    size: str


    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id

        size = self.size


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "clusterId": cluster_id,
            "size": size,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("clusterId")

        size = d.pop("size")

        cluster_action_scale = cls(
            cluster_id=cluster_id,
            size=size,
        )

        return cluster_action_scale

