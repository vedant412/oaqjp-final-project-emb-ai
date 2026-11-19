"""Analyze English text with the IBM Watson NLP EmotionPredict API."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


class WatsonServiceError(RuntimeError):
    """The Watson service could not return usable emotion scores."""


def emotion_detector(text_to_analyze: str | None) -> dict[str, float | str | None]:
    """Return the five emotion scores and the name of the highest-scoring emotion."""
    if text_to_analyze is None or not text_to_analyze.strip():
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(
            WATSON_URL, json=payload, headers=WATSON_HEADERS, timeout=10
        )
        if response.status_code == 400:
            return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
        response.raise_for_status()

        prediction = response.json()["emotionPredictions"][0]["emotion"]
        scores = {emotion: float(prediction[emotion]) for emotion in EMOTIONS}
    except requests.RequestException as error:
        raise WatsonServiceError("Watson NLP could not complete the request.") from error
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise WatsonServiceError("Watson NLP returned invalid emotion data.") from error

    return {**scores, "dominant_emotion": max(scores, key=scores.__getitem__)}
