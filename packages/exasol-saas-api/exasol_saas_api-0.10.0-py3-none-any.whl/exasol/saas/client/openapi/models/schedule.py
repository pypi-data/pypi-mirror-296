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
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.schedule_action_type_0 import ScheduleActionType0
from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.cluster_action_scale import ClusterActionScale
  from ..models.cluster_action_start_stop import ClusterActionStartStop





T = TypeVar("T", bound="Schedule")


@_attrs_define
class Schedule:
    """ 
        Attributes:
            action (ScheduleActionType0):
            cron_rule (str): cron rule in format: <minute> <hour> <day> <month> <weekday>
            payload (Union['ClusterActionScale', 'ClusterActionStartStop']):
            id (Union[Unset, str]):
            cluster_name (Union[Unset, str]):
     """

    action: ScheduleActionType0
    cron_rule: str
    payload: Union['ClusterActionScale', 'ClusterActionStartStop']
    id: Union[Unset, str] = UNSET
    cluster_name: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.cluster_action_scale import ClusterActionScale
        from ..models.cluster_action_start_stop import ClusterActionStartStop
        action: str
        if isinstance(self.action, ScheduleActionType0):
            action = self.action.value


        cron_rule = self.cron_rule

        payload: Dict[str, Any]
        if isinstance(self.payload, ClusterActionScale):
            payload = self.payload.to_dict()
        else:
            payload = self.payload.to_dict()


        id = self.id

        cluster_name = self.cluster_name


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "action": action,
            "cronRule": cron_rule,
            "payload": payload,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if cluster_name is not UNSET:
            field_dict["clusterName"] = cluster_name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cluster_action_scale import ClusterActionScale
        from ..models.cluster_action_start_stop import ClusterActionStartStop
        d = src_dict.copy()
        def _parse_action(data: object) -> ScheduleActionType0:
            if not isinstance(data, str):
                raise TypeError()
            action_type_0 = ScheduleActionType0(data)



            return action_type_0

        action = _parse_action(d.pop("action"))


        cron_rule = d.pop("cronRule")

        def _parse_payload(data: object) -> Union['ClusterActionScale', 'ClusterActionStartStop']:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payload_type_0 = ClusterActionScale.from_dict(data)



                return payload_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            payload_type_1 = ClusterActionStartStop.from_dict(data)



            return payload_type_1

        payload = _parse_payload(d.pop("payload"))


        id = d.pop("id", UNSET)

        cluster_name = d.pop("clusterName", UNSET)

        schedule = cls(
            action=action,
            cron_rule=cron_rule,
            payload=payload,
            id=id,
            cluster_name=cluster_name,
        )

        return schedule

