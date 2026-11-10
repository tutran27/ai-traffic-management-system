"use client";

import React, { memo } from "react";
import { useTrafficStore } from "@/store/trafficStore";
import type { IntersectionState, VehicleState } from "@/lib/types";
import IntersectionNode from "./IntersectionNode";
import HeatLayer from "./HeatLayer";

// SUMO world → SVG mapping
const X_SLOPE = 1000 / 1400;        // (1250-250) / (1900-500)
const X_INTER = 250 - 500 * X_SLOPE;
const toSvgX = (wx: number) => wx * X_SLOPE + X_INTER;

// A1 wy=1000 → SVG cy=270; A0 wy=500 → SVG cy=455
const Y_SLOPE = (455 - 270) / (500 - 1000);  // -0.37
const Y_INTER = 270 - 1000 * Y_SLOPE;        // 640
const toSvgY = (wy: number) => wy * Y_SLOPE + Y_INTER;

const SUMO_IDS = ["A1", "B1", "C1", "A0", "B0", "C0"] as const;

const NODE_POS: Record<string, { cx: number; cy: number }> = {
  A1: { cx: 250,  cy: 270 },
  B1: { cx: 750,  cy: 270 },
  C1: { cx: 1250, cy: 270 },
  A0: { cx: 250,  cy: 455 },
  B0: { cx: 750,  cy: 455 },
  C0: { cx: 1250, cy: 455 },
};

// Top arterial centre y=270, bottom y=455. Three lanes per direction.
const TOP_E_BOUND_Y = [294, 286, 278];   // lane 0..2
const TOP_W_BOUND_Y = [246, 254, 262];
const BOT_E_BOUND_Y = [479, 471, 463];
const BOT_W_BOUND_Y = [431, 439, 447];

function nBoundX(centreX: number) { return [centreX + 17, centreX + 8]; }
function sBoundX(centreX: number) { return [centreX - 17, centreX - 8]; }

function isEastbound(edge: string): boolean {
  if (/^[A-C][01][A-C][01]$/.test(edge)) return edge[0] < edge[2];
  if (/^[A-C][01]right[01]$/.test(edge)) return true;
  if (/^left[01][A-C][01]$/.test(edge)) return true;
  return false;
}

function isNorthbound(edge: string): boolean {
  if (/^[A-C][01][A-C][01]$/.test(edge)) return edge[1] < edge[3];
  if (/^[A-C][01]top[0-2]$/.test(edge)) return true;
  if (/^bottom[0-2][A-C][01]$/.test(edge)) return true;
  return false;
}

const H_EDGES: Record<string, [number, number, number, number]> = {
  left0A0:   [0.0, 489.6, 0.0, 220.0],
  left1A1:   [0.0, 489.6, 0.0, 220.0],
  A0left0:   [489.6, 0.0, 225.0, 0.0],
  A1left1:   [489.6, 0.0, 225.0, 0.0],
  A0B0:      [510.4, 1189.6, 275.0, 720.0],
  A1B1:      [510.4, 1189.6, 275.0, 720.0],
  B0A0:      [1189.6, 510.4, 725.0, 280.0],
  B1A1:      [1189.6, 510.4, 725.0, 280.0],
  B0C0:      [1210.4, 1889.6, 775.0, 1220.0],
  B1C1:      [1210.4, 1889.6, 775.0, 1220.0],
  C0B0:      [1889.6, 1210.4, 1225.0, 780.0],
  C1B1:      [1889.6, 1210.4, 1225.0, 780.0],
  C0right0:  [1910.4, 2400.0, 1275.0, 1500.0],
  C1right1:  [1910.4, 2400.0, 1275.0, 1500.0],
  right0C0:  [2400.0, 1910.4, 1500.0, 1280.0],
  right1C1:  [2400.0, 1910.4, 1500.0, 1280.0],
};

const V_EDGES: Record<string, [number, number, number, number]> = {
  top0A1:    [1500.0, 1013.6, 0.0, 222.0],
  top1B1:    [1500.0, 1013.6, 0.0, 222.0],
  top2C1:    [1500.0, 1013.6, 0.0, 222.0],
  A1top0:    [1013.6, 1500.0, 230.0, 0.0],
  B1top1:    [1013.6, 1500.0, 230.0, 0.0],
  C1top2:    [1013.6, 1500.0, 230.0, 0.0],
  A1A0:      [986.4, 513.6, 310.0, 407.0],
  B1B0:      [986.4, 513.6, 310.0, 407.0],
  C1C0:      [986.4, 513.6, 310.0, 407.0],
  A0A1:      [513.6, 986.4, 415.0, 318.0],
  B0B1:      [513.6, 986.4, 415.0, 318.0],
  C0C1:      [513.6, 986.4, 415.0, 318.0],
  bottom0A0: [0.0, 486.4, 600.0, 503.0],
  bottom1B0: [0.0, 486.4, 600.0, 503.0],
  bottom2C0: [0.0, 486.4, 600.0, 503.0],
  A0bottom0: [486.4, 0.0, 495.0, 600.0],
  B0bottom1: [486.4, 0.0, 495.0, 600.0],
  C0bottom2: [486.4, 0.0, 495.0, 600.0],
};

function vehicleToSvg(v: VehicleState): { x: number; y: number } {
  const i = v.lane_id.lastIndexOf("_");
  const edge = i >= 0 ? v.lane_id.slice(0, i) : v.lane_id;
  const lane = i >= 0 ? parseInt(v.lane_id.slice(i + 1), 10) : 0;

  if (edge.startsWith(":")) {
    const jId = edge.slice(1, 3);
    const colX = jId[0] === "A" ? 250 : jId[0] === "B" ? 750 : 1250;
    const rowY = jId[1] === "1" ? 270 : 455;
    const wCx = jId[0] === "A" ? 500.0 : jId[0] === "B" ? 1200.0 : 1900.0;
    const wCy = jId[1] === "1" ? 1000.0 : 500.0;

    const px = Math.max(0, Math.min(1, (v.x - (wCx - 10.4)) / 20.8));
    const py = Math.max(0, Math.min(1, (v.y - (wCy - 13.6)) / 27.2));
    const sx = (colX - 25) + px * 50;
    const sy = (rowY + 40) - py * 80;
    return { x: sx, y: sy };
  }

  if (edge in H_EDGES) {
    const [wStart, wEnd, sStart, sEnd] = H_EDGES[edge];
    const prog = Math.max(0, Math.min(1, (v.x - wStart) / (wEnd - wStart)));
    const sx = sStart + prog * (sEnd - sStart);

    const isTop = v.y > 750;
    const eb = isEastbound(edge);
    const rows = isTop
      ? (eb ? TOP_E_BOUND_Y : TOP_W_BOUND_Y)
      : (eb ? BOT_E_BOUND_Y : BOT_W_BOUND_Y);
    return { x: sx, y: rows[Math.min(lane, rows.length - 1)] };
  }

  if (edge in V_EDGES) {
    const [wStart, wEnd, sStart, sEnd] = V_EDGES[edge];
    const prog = Math.max(0, Math.min(1, (v.y - wStart) / (wEnd - wStart)));
    const sy = sStart + prog * (sEnd - sStart);

    const col = v.x < 850 ? 250 : v.x < 1550 ? 750 : 1250;
    const nb = isNorthbound(edge);
    const cols = nb ? nBoundX(col) : sBoundX(col);
    return { x: cols[Math.min(lane, cols.length - 1)], y: sy };
  }

  return { x: toSvgX(v.x), y: toSvgY(v.y) };
}

function makePlaceholder(id: string): IntersectionState {
  return {
    id,
    signal_state: "rrrrrrrr",
    phase_index: 0,
    phase_remaining_s: 0,
    queue_lengths: { N: 0, S: 0, E: 0, W: 0 },
    vehicle_count: 0,
    avg_wait_s: 0,
  };
}

// Static background memoized: blocks, buildings, roads, markings rendered once
const StaticGridBackground = memo(function StaticGridBackground() {
  return (
    <>
      {/* City blocks */}
      <rect x={0}    y={0}   width={225} height={230} fill="#0d1421" />
      <rect x={275}  y={0}   width={450} height={230} fill="#0d1421" />
      <rect x={775}  y={0}   width={450} height={230} fill="#0d1421" />
      <rect x={1275} y={0}   width={225} height={230} fill="#0d1421" />
      <rect x={0}    y={495} width={225} height={105} fill="#0d1421" />
      <rect x={275}  y={495} width={450} height={105} fill="#0d1421" />
      <rect x={775}  y={495} width={450} height={105} fill="#0d1421" />
      <rect x={1275} y={495} width={225} height={105} fill="#0d1421" />
      <rect x={0}    y={310} width={225} height={105} fill="#0d1421" />
      <rect x={275}  y={310} width={450} height={105} fill="#0d1421" />
      <rect x={775}  y={310} width={450} height={105} fill="#0d1421" />
      <rect x={1275} y={310} width={225} height={105} fill="#0d1421" />

      {/* Building footprints */}
      {[
        [25,20,70,40],[110,30,55,28],[20,75,80,30],[105,80,70,32],[25,125,80,40],[120,125,55,30],[25,175,90,40],
        [290,20,90,35],[395,25,75,30],[490,30,65,35],[580,20,80,40],[660,25,55,30],
        [290,75,75,40],[380,80,90,32],[485,85,75,40],[580,75,85,35],[675,80,40,30],
        [290,135,85,45],[390,140,75,35],[480,135,90,40],[585,140,75,35],[680,140,35,40],
        [790,20,75,40],[880,25,65,30],[955,30,90,32],[1060,20,75,38],[1145,25,70,32],
        [790,80,70,35],[875,80,90,30],[975,85,70,32],[1060,80,80,40],[1150,85,60,30],
        [790,140,90,42],[890,135,75,38],[975,140,85,35],[1070,140,70,36],[1150,140,65,40],
        [1290,20,75,40],[1375,25,65,30],[1450,30,40,32],[1290,75,80,32],[1380,80,60,35],
        [1290,130,90,40],[1390,135,70,35],
      ].map(([x, y, w, h], i) => (
        <rect key={i} x={x} y={y} width={w} height={h} fill="#0f1a2e" rx={2} />
      ))}

      {/* Roads */}
      <rect x={0} y={230} width={1500} height={80} fill="#111d2e" />
      <rect x={0} y={415} width={1500} height={80} fill="#111d2e" />
      <rect x={225}  y={0} width={50} height={600} fill="#111d2e" />
      <rect x={725}  y={0} width={50} height={600} fill="#111d2e" />
      <rect x={1225} y={0} width={50} height={600} fill="#111d2e" />

      {/* Arterial lane markings */}
      {[247, 258, 282, 293].map((y) => (
        <g key={`tdash-${y}`}>
          <line x1={0}    y1={y} x2={225}  y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={275}  y1={y} x2={725}  y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={775}  y1={y} x2={1225} y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={1275} y1={y} x2={1500} y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
        </g>
      ))}
      {[268.5, 271.5].map((y) => (
        <g key={`tmed-${y}`}>
          <line x1={0}    y1={y} x2={225}  y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={275}  y1={y} x2={725}  y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={775}  y1={y} x2={1225} y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={1275} y1={y} x2={1500} y2={y} stroke="#3a5a82" strokeWidth={1.0} />
        </g>
      ))}
      {[432, 443, 467, 478].map((y) => (
        <g key={`bdash-${y}`}>
          <line x1={0}    y1={y} x2={225}  y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={275}  y1={y} x2={725}  y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={775}  y1={y} x2={1225} y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={1275} y1={y} x2={1500} y2={y} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
        </g>
      ))}
      {[453.5, 456.5].map((y) => (
        <g key={`bmed-${y}`}>
          <line x1={0}    y1={y} x2={225}  y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={275}  y1={y} x2={725}  y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={775}  y1={y} x2={1225} y2={y} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={1275} y1={y} x2={1500} y2={y} stroke="#3a5a82" strokeWidth={1.0} />
        </g>
      ))}

      {/* Cross street lane markings */}
      {[
        [237, 250, 263, 0, 230], [237, 250, 263, 310, 415], [237, 250, 263, 495, 600],
        [737, 750, 763, 0, 230], [737, 750, 763, 310, 415], [737, 750, 763, 495, 600],
        [1237, 1250, 1263, 0, 230], [1237, 1250, 1263, 310, 415], [1237, 1250, 1263, 495, 600],
      ].map(([xL, xC, xR, y1, y2], i) => (
        <g key={`vert-${i}`}>
          <line x1={xL} y1={y1} x2={xL} y2={y2} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={xR} y1={y1} x2={xR} y2={y2} stroke="#1e3048" strokeWidth={1.2} strokeDasharray="18 12" />
          <line x1={xC - 1.5} y1={y1} x2={xC - 1.5} y2={y2} stroke="#3a5a82" strokeWidth={1.0} />
          <line x1={xC + 1.5} y1={y1} x2={xC + 1.5} y2={y2} stroke="#3a5a82" strokeWidth={1.0} />
        </g>
      ))}
    </>
  );
});

// Vehicle dots with CSS transition for 60 FPS buttery smooth motion
const VehicleDots = memo(function VehicleDots({ vehicles }: { vehicles: VehicleState[] }) {
  if (vehicles.length > 1500) return null;
  return (
    <>
      {vehicles.map((v) => {
        const { x, y } = vehicleToSvg(v);
        const isEmg = String(v.type) === "emergency";
        return (
          <circle
            key={v.id}
            cx={x}
            cy={y}
            r={isEmg ? 3.5 : 2.5}
            fill={isEmg ? "#ef4444" : "#3b82f6"}
            fillOpacity={0.85}
            style={{ transition: "cx 95ms linear, cy 95ms linear" }}
          />
        );
      })}
    </>
  );
});

interface Props {
  showHeat?: boolean;
}

export default function SumoGrid({ showHeat = true }: Props) {
  const intersections   = useTrafficStore((s) => s.intersections);
  const vehicles        = useTrafficStore((s) => s.vehicles);
  const activeEvRoutes  = useTrafficStore((s) => s.activeEvRoutes);

  const byId = new Map(intersections.map((i) => [i.id, i]));
  SUMO_IDS.forEach((id) => { if (!byId.has(id)) byId.set(id, makePlaceholder(id)); });

  return (
    <>
      {/* 1. Static map background (rendered only once) */}
      <StaticGridBackground />

      {/* 2. Heatmap layer */}
      {showHeat && <HeatLayer />}

      {/* 3. Emergency vehicle route lines */}
      {activeEvRoutes.map((route, ri) =>
        route.slice(0, -1).map((fromId, si) => {
          const toId = route[si + 1];
          const from = NODE_POS[fromId];
          const to   = NODE_POS[toId];
          if (!from || !to) return null;
          return (
            <line
              key={`ev-route-${ri}-${si}`}
              x1={from.cx} y1={from.cy}
              x2={to.cx}   y2={to.cy}
              stroke="#ef4444"
              strokeWidth={3}
              strokeDasharray="8 4"
              opacity={0.85}
            />
          );
        })
      )}

      {/* 4. Smooth moving vehicle dots */}
      <VehicleDots vehicles={vehicles} />

      {/* 5. Intersection nodes */}
      {SUMO_IDS.map((id) => {
        const pos = NODE_POS[id];
        const it  = byId.get(id)!;
        return <IntersectionNode key={id} intersection={it} cx={pos.cx} cy={pos.cy} />;
      })}
    </>
  );
}
