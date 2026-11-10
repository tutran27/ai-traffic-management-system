"""Unit tests for emergency vehicle preemption and starvation compensation."""

from __future__ import annotations

import pytest

from adaptive_policy.preemption import PreemptionManager
from shared.types import (
    EmergencyVehicleInfo,
    IntersectionState,
    QueueLengths,
    SignalCommand,
)


def _make_state(tl_id: str) -> IntersectionState:
    return IntersectionState(
        id=tl_id,
        signal_state="GG",
        phase_index=0,
        phase_remaining_s=10.0,
        queue_lengths=QueueLengths(),
        vehicle_count=0,
        avg_wait_s=0.0,
    )


def test_preemption_triggers_green_command():
    pm = PreemptionManager()
    pm.reset()

    intersections = [_make_state("A0"), _make_state("B0")]
    # Vehicle on edge "A0B0" moves East approaching B0
    ev = EmergencyVehicleInfo(
        id="ambulance_1",
        x=100.0,
        y=0.0,
        current_edge="A0B0",
    )

    cmds = pm.check_preemption(intersections, [ev])
    assert len(cmds) == 1
    assert cmds[0].intersection_id == "B0"
    # Direction E has phase index 3
    assert cmds[0].phase_index == 3
    assert pm.is_preempted("B0")


def test_preemption_accrues_and_pays_compensation():
    pm = PreemptionManager()
    pm.reset()

    intersections = [_make_state("B0")]
    ev = EmergencyVehicleInfo(id="ev_1", x=100.0, y=0.0, current_edge="A0B0")

    # Start preemption
    pm.check_preemption(intersections, [ev])
    assert pm.is_preempted("B0")

    # EV clears intersection -> preemption ends
    pm.check_preemption(intersections, [])
    assert not pm.is_preempted("B0")

    # Starved directions (N, S) should receive compensation commands
    comp_cmds = pm.get_compensation_commands(intersections)
    assert len(comp_cmds) == 1
    assert comp_cmds[0].intersection_id == "B0"
    assert comp_cmds[0].duration_s > 0.0
