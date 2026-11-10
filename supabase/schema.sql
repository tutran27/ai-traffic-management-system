-- =====================================================================
-- Unified Schema for AI Smart Traffic Management System (Supabase)
-- =====================================================================

-- 1. Reference data for the 3x2 arterial grid (6 intersections: A0, A1, B0, B1, C0, C1)
CREATE TABLE IF NOT EXISTS intersections (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    grid_row INTEGER NOT NULL,
    grid_col INTEGER NOT NULL,
    x_coord FLOAT NOT NULL,
    y_coord FLOAT NOT NULL,
    num_phases INTEGER NOT NULL DEFAULT 4,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Simulation sessions / experiment runs
CREATE TABLE IF NOT EXISTS simulation_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    policy_type TEXT NOT NULL,
    config JSONB NOT NULL,
    status TEXT DEFAULT 'running',
    total_ticks INTEGER,
    notes TEXT
);

-- 3. Signal state per intersection per tick
CREATE TABLE IF NOT EXISTS signal_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    tick INTEGER NOT NULL,
    sim_time FLOAT NOT NULL,
    intersection_id TEXT REFERENCES intersections(id),
    phase_index INTEGER NOT NULL,
    state_string TEXT NOT NULL,
    phase_duration_s FLOAT,
    is_preempted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_signal_logs_run_tick ON signal_logs(run_id, tick);
CREATE INDEX IF NOT EXISTS idx_signal_logs_intersection ON signal_logs(intersection_id, run_id);

-- 4. Vehicle snapshots (sampled periodically)
CREATE TABLE IF NOT EXISTS vehicle_snapshots (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    tick INTEGER NOT NULL,
    vehicle_id TEXT NOT NULL,
    vehicle_type TEXT NOT NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    speed FLOAT NOT NULL,
    lane_id TEXT,
    accumulated_wait_s FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vehicle_snapshots_run_tick ON vehicle_snapshots(run_id, tick);

-- 5. End-of-cycle intersection metrics
CREATE TABLE IF NOT EXISTS intersection_metrics (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    tick INTEGER NOT NULL,
    sim_time FLOAT NOT NULL,
    intersection_id TEXT REFERENCES intersections(id),
    queue_length_n INTEGER,
    queue_length_s INTEGER,
    queue_length_e INTEGER,
    queue_length_w INTEGER,
    total_vehicles INTEGER,
    avg_wait_s FLOAT,
    phase_index INTEGER,
    phase_remaining_s FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_intersection_metrics_run ON intersection_metrics(run_id, tick);
CREATE INDEX IF NOT EXISTS idx_intersection_metrics_inter ON intersection_metrics(intersection_id, run_id);

-- 6. System-wide global metrics
CREATE TABLE IF NOT EXISTS global_metrics (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    tick INTEGER NOT NULL,
    sim_time FLOAT NOT NULL,
    total_vehicles INTEGER,
    total_completed INTEGER,
    completed_trips INTEGER,
    avg_delay_s FLOAT,
    avg_trip_time_s FLOAT,
    avg_control_delay_s FLOAT,
    control_delay_samples INTEGER,
    throughput_veh_per_min FLOAT,
    total_halting INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_global_metrics_run ON global_metrics(run_id, tick);

-- 7. Emergency vehicle events
CREATE TABLE IF NOT EXISTS emergency_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    vehicle_id TEXT NOT NULL,
    injected_at_tick INTEGER NOT NULL,
    route TEXT NOT NULL,
    preempted_intersections TEXT[],
    total_preemption_time_s FLOAT,
    response_time_s FLOAT,
    compensation_applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Comparison experiments
CREATE TABLE IF NOT EXISTS experiments (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          TEXT,
    seed          INTEGER NOT NULL,
    status        TEXT NOT NULL DEFAULT 'running',  -- running | completed | cancelled | failed
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_experiments_created ON experiments(created_at DESC);

CREATE TABLE IF NOT EXISTS experiment_runs (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id            UUID REFERENCES experiments(id) ON DELETE CASCADE,
    run_index                INTEGER NOT NULL,
    run_id                   UUID REFERENCES simulation_runs(id),
    config                   JSONB NOT NULL,
    status                   TEXT NOT NULL DEFAULT 'pending',  -- pending | running | completed | failed | cancelled
    error                    TEXT,
    clearance_s              FLOAT,
    avg_trip_time_s          FLOAT,
    completed_trips          INTEGER,
    avg_control_delay_s      FLOAT,
    throughput_veh_per_min   FLOAT,
    UNIQUE(experiment_id, run_index)
);

CREATE INDEX IF NOT EXISTS idx_experiment_runs_exp ON experiment_runs(experiment_id);

-- 9. Computer vision detection logs
CREATE TABLE IF NOT EXISTS cv_detections (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
    tick INTEGER NOT NULL,
    intersection_id TEXT REFERENCES intersections(id),
    detections JSONB NOT NULL,
    inference_time_ms FLOAT,
    frame_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Saved policy variants (arterial & highway)
CREATE TABLE IF NOT EXISTS policy_variants (
    name        TEXT PRIMARY KEY,
    params      JSONB NOT NULL,
    family      TEXT NOT NULL DEFAULT 'arterial',  -- 'arterial' | 'highway'
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Initial seed data for the 3x2 arterial intersections
INSERT INTO intersections (id, label, grid_row, grid_col, x_coord, y_coord, num_phases) VALUES
    ('A0', 'Intersection A0', 1, 0,   0.0,   0.0, 4),
    ('A1', 'Intersection A1', 0, 0,   0.0, 500.0, 4),
    ('B0', 'Intersection B0', 1, 1, 700.0,   0.0, 4),
    ('B1', 'Intersection B1', 0, 1, 700.0, 500.0, 4),
    ('C0', 'Intersection C0', 1, 2, 1400.0,  0.0, 4),
    ('C1', 'Intersection C1', 0, 2, 1400.0, 500.0, 4)
ON CONFLICT (id) DO NOTHING;
