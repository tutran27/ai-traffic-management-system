"""Unit tests for the ActuatedController leftover-queue policy."""

from __future__ import annotations

import pytest

from adaptive_policy.actuated import ActuatedController, default_arterial_plan
from shared.types import (
    ActuatedPolicyParams,
    IntersectionState,
    QueueLengths,
    SignalCommand,
)


def _make_state(tl_id: str, phase: int, q_n: int = 0, q_e: int = 0, q_s: int = 0, q_w: int = 0) -> IntersectionState:
    return IntersectionState(
        id=tl_id,
        signal_state="GG",
        phase_index=phase,
        phase_remaining_s=10.0,
        queue_lengths=QueueLengths(N=q_n, E=q_e, S=q_s, W=q_w),
        vehicle_count=q_n + q_e + q_s + q_w,
        avg_wait_s=0.0,
    )


def test_actuated_initial_targets():
    params = ActuatedPolicyParams(
        base_green_n=20.0,
        base_green_s=20.0,
        base_green_e=30.0,
        base_green_w=30.0,
    )
    ctl = ActuatedController(params=params)
    targets = ctl.get_targets("A0")

    assert targets["N"]["base"] == 20.0
    assert targets["N"]["target"] == 20.0
    assert targets["N"]["delta"] == 0.0

    assert targets["E"]["base"] == 30.0
    assert targets["E"]["target"] == 30.0
    assert targets["E"]["delta"] == 0.0


def test_actuated_commands_on_green_entry():
    ctl = ActuatedController()
    
    # Phase 0 is green N (in default arterial plan)
    st1 = _make_state("A0", phase=0)
    decision = ctl.decide([st1], sim_time=0.0)

    assert len(decision.commands) == 1
    cmd = decision.commands[0]
    assert cmd.intersection_id == "A0"
    assert cmd.duration_s == 15.0  # default base_green_n


def test_actuated_leftover_smoothing_and_redistribution():
    params = ActuatedPolicyParams(
        base_green_n=15.0,
        base_green_e=35.0,
        base_green_s=15.0,
        base_green_w=35.0,
        max_redist_s=10.0,
        smooth_alpha=1.0,  # no smoothing lag for test determinism
    )
    ctl = ActuatedController(params=params)

    # 4-phase arterial cycle:
    # Green N (0) -> Yellow N (1)
    # Green E (3) -> Yellow E (4)
    # Green S (6) -> Yellow S (7)
    # Green W (9) -> Yellow W (10)

    # Cycle 1: Heavy queue on N (10 veh leftover at yellow), 0 on others
    ctl.decide([_make_state("A0", phase=0)], sim_time=0.0)
    ctl.decide([_make_state("A0", phase=1, q_n=10)], sim_time=15.0)

    ctl.decide([_make_state("A0", phase=3)], sim_time=18.0)
    ctl.decide([_make_state("A0", phase=4, q_e=0)], sim_time=53.0)

    ctl.decide([_make_state("A0", phase=6)], sim_time=56.0)
    ctl.decide([_make_state("A0", phase=7, q_s=0)], sim_time=71.0)

    ctl.decide([_make_state("A0", phase=9)], sim_time=74.0)
    # Yellow W completes full cycle
    ctl.decide([_make_state("A0", phase=10, q_w=0)], sim_time=109.0)

    # N should gain green time redistributed from satisfied directions
    targets = ctl.get_targets("A0")
    assert targets["N"]["target"] > 15.0
    assert targets["N"]["delta"] > 0.0

    # Satisfied directions (E, S, W) should have contributed green time
    assert targets["E"]["target"] < 35.0
