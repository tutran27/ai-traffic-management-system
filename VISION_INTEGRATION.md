# Computer Vision Integration — YOLOv11m Perception Pipeline

This module integrates a custom **YOLOv11m** vehicle-detection and tracking pipeline for real-time traffic monitoring and adaptive control:
- Vehicle detection and classification across 7 classes (`car`, `bus`, `truck`, `motorcycle`, and emergency vehicles: `ambulance`, `police_car`, `fire_truck`)
- Real-time vehicle speed estimation via camera homography
- Lane-level queue length measurement and stationary vehicle identification
- Emergency vehicle detection for automatic signal preemption and green-wave clearance
- Red-light stop-line violation monitoring

---

## 1. Prerequisites & Models

- Python 3.9+ with `torch`, `torchvision`, `ultralytics`, and `opencv-python`
- NVIDIA GPU recommended for real-time inference (CPU fallback supported)
- Fine-tuned model weights bundled at `packages/cv-pipeline/models/best.pt` (~39 MB)

## 2. Installation

Install required computer vision packages in your environment:

```bash
pip install -e packages/cv-pipeline
pip install ultralytics torch opencv-python
```

## 3. Pipeline Architecture

1. **Detection & Classification:**
   `YoloV11Detector` wraps YOLOv11m to detect traffic actors and emergency vehicles.
2. **Multi-Object Tracking:**
   ByteTrack tracks vehicle trajectories frame-to-frame, assigning unique track IDs.
3. **Speed & Homography:**
   `ApproachAnalyzer` projects 2D image coordinates onto the real-world road plane via homography matrix `H` to estimate real-world vehicle speed (m/s and km/h).
4. **Queue & Violation Analytics:**
   Lanes and stop-line regions are evaluated per frame. Vehicles below the stationary threshold are counted into queue lengths; vehicles crossing stop lines on red trigger violation logs.
5. **Adaptive Signal Feedback:**
   Estimated approach queues and detected emergency vehicles feed directly into the adaptive policy engine (`adaptive-policy`) for real-time signal timing adjustments.
