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

T = TypeVar("T", bound="ClusterActionStartStop")


@_attrs_define
class ClusterActionStartStop:
    """ 
        Attributes:
            cluster_id (str):
     """

    cluster_id: str


    def to_dict(self) -> Dict[str, Any]:
        cluster_id = self.cluster_id


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "clusterId": cluster_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_id = d.pop("clusterId")

        cluster_action_start_stop = cls(
            cluster_id=cluster_id,
        )

        return cluster_action_start_stop

