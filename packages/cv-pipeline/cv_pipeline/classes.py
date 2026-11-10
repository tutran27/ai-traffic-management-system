"""Mapping from our custom 7-class model to vehicle taxonomy and detection structures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Detection:
    """Single object detection result."""

    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]  # (x1, y1, x2, y2)


# Class names as emitted by the custom model (see models/best.pt training set).
MODEL_CLASS_NAMES = (
    "car", "ambulance", "bus", "truck", "police_car", "fire_truck", "bike",
)

# The three classes our model can distinguish that map to an emergency vehicle.
EMERGENCY_CLASSES = frozenset({"ambulance", "police_car", "fire_truck"})

# Model class name -> VehicleType value.
CLASS_TO_VEHICLE_TYPE = {
    "car": "car",
    "bus": "bus",
    "truck": "truck",
    "bike": "motorcycle",
    "ambulance": "emergency",
    "police_car": "emergency",
    "fire_truck": "emergency",
}


def vehicle_type_for(class_name: str) -> str:
    """Map a model class name to a VehicleType value (default 'car')."""
    return CLASS_TO_VEHICLE_TYPE.get(class_name, "car")


def is_emergency(class_name: str) -> bool:
    """True if the class is an emergency vehicle (ambulance/police/fire)."""
    return class_name in EMERGENCY_CLASSES
