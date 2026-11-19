"""Public interface for the EmotionDetection package."""

from .emotion_detection import WatsonServiceError, emotion_detector

__all__ = ["WatsonServiceError", "emotion_detector"]
