"use client";

import React, { memo, useState } from "react";

import type { IntersectionState } from "@/lib/types";
import { useTrafficStore } from "@/store/trafficStore";

interface Props {
  intersection: IntersectionState;
  cx: number;
  cy: number;
}

function phaseToLabel(
  phaseIndex: number,
  intersectionId: string,
): { dir: string; sub: "G" | "y" | "r" } {
  const sub = phaseIndex % 3;
  const subKey = sub === 0 ? "G" : sub === 1 ? "y" : "r";

  // Highway meters (E1/E2/W1/W2) use a 2-phase cycle: 0 green / 1 red.
  if (intersectionId.startsWith("E") || intersectionId.startsWith("W")) {
    const dir = phaseIndex === 0 ? "Svc" : "Wait";
    return { dir, sub: phaseIndex === 0 ? "G" : "r" };
  }

  // Dual-phase arterial: Opposite directions paired together (N-S and E-W)
  const group = Math.floor(phaseIndex / 3) % 4;
  const isNS  = group === 0 || group === 2;
  const dir   = isNS ? "N-S" : "E-W";
  return { dir, sub: subKey };
}

function phaseColor(sub: "G" | "y" | "r") {
  if (sub === "G") return "#22c55e";
  if (sub === "y") return "#eab308";
  return "#ef4444";
}

function getApproachColors(
  phaseIndex: number,
  intersectionId: string,
): { N: string; E: string; S: string; W: string } {
  const isMeter = intersectionId.startsWith("E") || intersectionId.startsWith("W");
  if (isMeter) {
    const c = phaseIndex === 0 ? "#22c55e" : "#ef4444";
    return { N: "#ef4444", S: "#ef4444", E: c, W: c };
  }
  const group = Math.floor(phaseIndex / 3) % 4;
  const sub = phaseIndex % 3;
  const activeColor = sub === 0 ? "#22c55e" : sub === 1 ? "#eab308" : "#ef4444";
  const red = "#ef4444";

  // Opposite directions always have the exact same color and countdown time
  const isNS = group === 0 || group === 2;

  return {
    N: isNS ? activeColor : red,
    S: isNS ? activeColor : red,
    E: !isNS ? activeColor : red,
    W: !isNS ? activeColor : red,
  };
}

function IntersectionNode({ intersection, cx, cy }: Props) {
  const selectedId        = useTrafficStore((s) => s.selectedIntersection);
  const selectIntersection = useTrafficStore((s) => s.selectIntersection);
  const isSelected        = selectedId === intersection.id;
  const [hover, setHover] = useState(false);

  const { dir, sub } = phaseToLabel(intersection.phase_index, intersection.id);
  const remaining    = Math.max(0, Math.round(intersection.phase_remaining_s));
  const fill         = isSelected ? "#3b82f6" : phaseColor(sub);
  const glow         = isSelected ? "#3b82f6" : phaseColor(sub);
  const r            = isSelected ? 17 : 15;
  const isArterial   = !intersection.id.startsWith("E") && !intersection.id.startsWith("W");
  const approachColors = getApproachColors(intersection.phase_index, intersection.id);

  // Equidistant traffic lights and stop lines (27px from node center)
  const LIGHT_DIST = 27;
  const LIGHT_BAR_HALF = 16;

  function handleClick(e: React.MouseEvent) {
    e.stopPropagation();
    selectIntersection(isSelected ? null : intersection.id);
  }

  return (
    <g
      transform={`translate(${cx},${cy})`}
      onClick={handleClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{ cursor: "pointer" }}
    >
      {/* Glow ring */}
      <circle r={r + 8} fill={glow} fillOpacity={isSelected ? 0.18 : 0.12} />
      {/* Selected pulse ring */}
      {isSelected && (
        <circle r={r + 14} fill="none" stroke="#93c5fd" strokeWidth={1.5} strokeOpacity={0.5} />
      )}
      {/* Main circle */}
      <circle
        r={r}
        fill={fill}
        fillOpacity={0.92}
        stroke={isSelected ? "#93c5fd" : "none"}
        strokeWidth={isSelected ? 2 : 0}
      />
      {/* 4-Way Directional Traffic Lights & Stop Lines - Perfectly Equidistant from Center */}
      {isArterial && (
        <g pointerEvents="none">
          {/* North approach (cars coming from top) */}
          <line
            x1={-LIGHT_BAR_HALF}
            y1={-LIGHT_DIST}
            x2={LIGHT_BAR_HALF}
            y2={-LIGHT_DIST}
            stroke={approachColors.N}
            strokeWidth={2.8}
            strokeLinecap="round"
            opacity={0.95}
          />
          <circle cx={0} cy={-LIGHT_DIST} r={3.2} fill={approachColors.N} stroke="#0b111e" strokeWidth={0.8} />

          {/* South approach (cars coming from bottom) */}
          <line
            x1={-LIGHT_BAR_HALF}
            y1={LIGHT_DIST}
            x2={LIGHT_BAR_HALF}
            y2={LIGHT_DIST}
            stroke={approachColors.S}
            strokeWidth={2.8}
            strokeLinecap="round"
            opacity={0.95}
          />
          <circle cx={0} cy={LIGHT_DIST} r={3.2} fill={approachColors.S} stroke="#0b111e" strokeWidth={0.8} />

          {/* West approach (cars coming from left) */}
          <line
            x1={-LIGHT_DIST}
            y1={-LIGHT_BAR_HALF}
            x2={-LIGHT_DIST}
            y2={LIGHT_BAR_HALF}
            stroke={approachColors.W}
            strokeWidth={2.8}
            strokeLinecap="round"
            opacity={0.95}
          />
          <circle cx={-LIGHT_DIST} cy={0} r={3.2} fill={approachColors.W} stroke="#0b111e" strokeWidth={0.8} />

          {/* East approach (cars coming from right) */}
          <line
            x1={LIGHT_DIST}
            y1={-LIGHT_BAR_HALF}
            x2={LIGHT_DIST}
            y2={LIGHT_BAR_HALF}
            stroke={approachColors.E}
            strokeWidth={2.8}
            strokeLinecap="round"
            opacity={0.95}
          />
          <circle cx={LIGHT_DIST} cy={0} r={3.2} fill={approachColors.E} stroke="#0b111e" strokeWidth={0.8} />
        </g>
      )}

      {/* Intersection ID */}
      <text
        y={-3.5}
        textAnchor="middle"
        fill="#ffffff"
        fontSize={8.5}
        fontFamily="ui-monospace, monospace"
        fontWeight="bold"
        style={{
          pointerEvents: "none",
          userSelect: "none",
          filter: "drop-shadow(0 1px 2px rgba(0,0,0,0.85))",
        }}
      >
        {intersection.id}
      </text>

      {/* Countdown timer badge - high contrast dark pill for maximum legibility */}
      <rect
        x={-12}
        y={0.5}
        width={24}
        height={12}
        rx={3.5}
        fill="#080e1a"
        fillOpacity={0.82}
        stroke="rgba(255,255,255,0.18)"
        strokeWidth={0.5}
        style={{ pointerEvents: "none" }}
      />
      <text
        y={9.5}
        textAnchor="middle"
        fill="#ffffff"
        fontSize={10}
        fontFamily="ui-monospace, monospace"
        fontWeight="bold"
        style={{ pointerEvents: "none", userSelect: "none" }}
      >
        {remaining}s
      </text>

      {/* Hover tooltip — anchored just above the puck. Suppressed when
          the intersection is the selected one (the right panel covers it). */}
      {hover && !isSelected && (
        <Tooltip intersection={intersection} radius={r} />
      )}
    </g>
  );
}

function Tooltip({
  intersection,
  radius,
}: {
  intersection: IntersectionState;
  radius: number;
}) {
  const q = intersection.queue_lengths;
  const wait = Math.round(intersection.avg_wait_s);
  const { dir, sub } = phaseToLabel(intersection.phase_index, intersection.id);
  const remaining = Math.max(0, Math.round(intersection.phase_remaining_s));

  // Fixed-size tooltip so we don't need to measure. 90 × 72 px above the puck.
  const W = 96, H = 72;
  const offset = radius + 10;   // gap between puck and tooltip
  const x = -W / 2;
  const y = -(offset + H);

  // Bar widths normalized — 24 vehicles ≈ full width.
  const bar = (n: number) => Math.max(2, Math.min(38, (n / 24) * 38));

  return (
    <g pointerEvents="none">
      {/* Pointer triangle */}
      <polygon
        points={`-5,${-offset} 5,${-offset} 0,${-offset + 6}`}
        fill="#0d1421"
        stroke="#374151"
        strokeWidth={0.6}
      />
      {/* Body */}
      <rect
        x={x} y={y}
        width={W} height={H}
        rx={3}
        fill="#0d1421"
        stroke="#374151"
        strokeWidth={0.8}
      />
      {/* Header row: id + phase */}
      <text
        x={x + 5} y={y + 11}
        fill="#d1d5db" fontSize={9} fontFamily="monospace" fontWeight="bold"
      >
        {intersection.id}
      </text>
      <text
        x={x + W - 5} y={y + 11}
        textAnchor="end"
        fill={phaseColor(sub)}
        fontSize={8} fontFamily="monospace"
      >
        {dir}·{remaining}s
      </text>
      {/* Avg wait */}
      <text x={x + 5} y={y + 22} fill="#9ca3af" fontSize={7} fontFamily="monospace">
        wait {wait}s
      </text>
      {/* Queue mini-bars */}
      {(["N","E","S","W"] as const).map((d, i) => {
        const rowY = y + 32 + i * 9;
        const w = bar(q[d]);
        return (
          <g key={d}>
            <text
              x={x + 5} y={rowY + 6}
              fill="#6b7280" fontSize={7} fontFamily="monospace"
            >
              {d}
            </text>
            <rect
              x={x + 16} y={rowY + 1}
              width={38} height={6}
              fill="#1f2937"
            />
            <rect
              x={x + 16} y={rowY + 1}
              width={w} height={6}
              fill={q[d] >= 20 ? "#ef4444" : q[d] >= 10 ? "#f97316" : q[d] >= 4 ? "#fbbf24" : "#22c55e"}
            />
            <text
              x={x + W - 5} y={rowY + 6}
              textAnchor="end"
              fill="#9ca3af" fontSize={7} fontFamily="monospace"
            >
              {q[d]}
            </text>
          </g>
        );
      })}
    </g>
  );
}

export default memo(IntersectionNode);
