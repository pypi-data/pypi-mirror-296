# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetScheduleResult',
    'AwaitableGetScheduleResult',
    'get_schedule',
    'get_schedule_output',
]

@pulumi.output_type
class GetScheduleResult:
    """
    A collection of values returned by getSchedule.
    """
    def __init__(__self__, ending_on=None, id=None, identifier=None, name=None, repeats=None, rules=None, schedule_type=None, starting_from=None, time_zone=None):
        if ending_on and not isinstance(ending_on, str):
            raise TypeError("Expected argument 'ending_on' to be a str")
        pulumi.set(__self__, "ending_on", ending_on)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, float):
            raise TypeError("Expected argument 'identifier' to be a float")
        pulumi.set(__self__, "identifier", identifier)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if repeats and not isinstance(repeats, list):
            raise TypeError("Expected argument 'repeats' to be a list")
        pulumi.set(__self__, "repeats", repeats)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if schedule_type and not isinstance(schedule_type, str):
            raise TypeError("Expected argument 'schedule_type' to be a str")
        pulumi.set(__self__, "schedule_type", schedule_type)
        if starting_from and not isinstance(starting_from, str):
            raise TypeError("Expected argument 'starting_from' to be a str")
        pulumi.set(__self__, "starting_from", starting_from)
        if time_zone and not isinstance(time_zone, str):
            raise TypeError("Expected argument 'time_zone' to be a str")
        pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter(name="endingOn")
    def ending_on(self) -> str:
        """
        Time until which schedule will be active. Need to be in YYYY-MM-DD HH:mm:SS format. Eg 2006-01-02 15:04:05
        """
        return pulumi.get(self, "ending_on")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> float:
        """
        Unique identifier of the schedule
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the schedule
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def repeats(self) -> Sequence['outputs.GetScheduleRepeatResult']:
        """
        For defining periodic schedule. Periodic nature will be applicable from the time of creation of schedule, unless specific 'time_period' is specified
        """
        return pulumi.get(self, "repeats")

    @property
    @pulumi.getter
    def rules(self) -> Sequence[float]:
        """
        ID of AutoStopping rules on which the schedule applies
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="scheduleType")
    def schedule_type(self) -> str:
        """
        Type of the schedule. Valid values are `uptime` and `downtime`
        """
        return pulumi.get(self, "schedule_type")

    @property
    @pulumi.getter(name="startingFrom")
    def starting_from(self) -> str:
        """
        Time from which schedule will be active. Schedule will take immediate effect if starting_from is not specified. Need to be in YYYY-MM-DD HH:mm:SS format. Eg 2006-01-02 15:04:05
        """
        return pulumi.get(self, "starting_from")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> str:
        """
        Time zone in which schedule needs to be executed
        """
        return pulumi.get(self, "time_zone")


class AwaitableGetScheduleResult(GetScheduleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScheduleResult(
            ending_on=self.ending_on,
            id=self.id,
            identifier=self.identifier,
            name=self.name,
            repeats=self.repeats,
            rules=self.rules,
            schedule_type=self.schedule_type,
            starting_from=self.starting_from,
            time_zone=self.time_zone)


def get_schedule(schedule_type: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScheduleResult:
    """
    Data source for retrieving a fixed schedule for Harness AutoStopping rule


    :param str schedule_type: Type of the schedule. Valid values are `uptime` and `downtime`
    """
    __args__ = dict()
    __args__['scheduleType'] = schedule_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:autostopping/getSchedule:getSchedule', __args__, opts=opts, typ=GetScheduleResult).value

    return AwaitableGetScheduleResult(
        ending_on=pulumi.get(__ret__, 'ending_on'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        name=pulumi.get(__ret__, 'name'),
        repeats=pulumi.get(__ret__, 'repeats'),
        rules=pulumi.get(__ret__, 'rules'),
        schedule_type=pulumi.get(__ret__, 'schedule_type'),
        starting_from=pulumi.get(__ret__, 'starting_from'),
        time_zone=pulumi.get(__ret__, 'time_zone'))


@_utilities.lift_output_func(get_schedule)
def get_schedule_output(schedule_type: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScheduleResult]:
    """
    Data source for retrieving a fixed schedule for Harness AutoStopping rule


    :param str schedule_type: Type of the schedule. Valid values are `uptime` and `downtime`
    """
    ...
