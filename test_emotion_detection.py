"""Test emotion formatting, Flask behavior, and the live Watson course examples."""

import os
import unittest
from unittest.mock import patch

from requests import Timeout

from EmotionDetection import WatsonServiceError, emotion_detector
from server import app

COURSE_EXAMPLES = {
    "joy": "I am glad this happened",
    "anger": "I am really mad about this",
    "disgust": "I feel disgusted just hearing about this",
    "sadness": "I am so sad about this",
    "fear": "I am really afraid that this will happen",
}
INVALID_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}
WATSON_POST = "EmotionDetection.emotion_detection.requests.post"


class EmotionDetectorTests(unittest.TestCase):
    """Test the package with controlled Watson HTTP responses."""

    @patch(WATSON_POST)
    def test_five_dominant_emotions_and_output_format(self, post):
        """Return exactly five scores and the correct dominant emotion."""
        post.return_value.status_code = 200
        for dominant, sentence in COURSE_EXAMPLES.items():
            with self.subTest(dominant=dominant):
                scores = dict.fromkeys(COURSE_EXAMPLES, 0.05)
                scores[dominant] = 0.9
                post.return_value.json.return_value = {
                    "emotionPredictions": [{"emotion": scores}]
                }
                self.assertEqual(
                    emotion_detector(sentence), {**scores, "dominant_emotion": dominant}
                )

    @patch(WATSON_POST)
    def test_watson_request_and_http_400(self, post):
        """Use the expected Watson request and return null scores on HTTP 400."""
        post.return_value.status_code = 400
        self.assertEqual(emotion_detector("Test sentence"), INVALID_RESULT)
        post.assert_called_once_with(
            "https://sn-watson-emotion.labs.skills.network/"
            "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict",
            json={"raw_document": {"text": "Test sentence"}},
            headers={"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"},
            timeout=10,
        )
        post.return_value.json.assert_not_called()

    @patch(WATSON_POST)
    def test_blank_input_skips_watson(self, post):
        """Handle missing, empty, and whitespace-only text locally."""
        for text in (None, "", " \n\t"):
            with self.subTest(text=text):
                self.assertEqual(emotion_detector(text), INVALID_RESULT)
        post.assert_not_called()

    @patch(WATSON_POST, side_effect=Timeout)
    def test_network_timeout(self, _post):
        """Report a Watson service error if the request times out."""
        with self.assertRaises(WatsonServiceError):
            emotion_detector("Test sentence")

    @patch(WATSON_POST)
    def test_malformed_prediction(self, post):
        """Report a Watson service error if the response lacks a prediction."""
        post.return_value.status_code = 200
        post.return_value.json.return_value = {"emotionPredictions": []}
        with self.assertRaises(WatsonServiceError):
            emotion_detector("Test sentence")


class FlaskTests(unittest.TestCase):
    """Test the Flask routes with the built-in test client."""

    def setUp(self):
        """Create a Flask client for each test."""
        self.client = app.test_client()

    def test_index(self):
        """The homepage includes the form controls and result element."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="textToAnalyze"', response.data)
        self.assertIn(b'id="system_response"', response.data)

    @patch(WATSON_POST)
    def test_blank_input(self, post):
        """The route shows the course error message without a Watson request."""
        for params in ({}, {"textToAnalyze": ""}, {"textToAnalyze": "  "}):
            with self.subTest(params=params):
                response = self.client.get("/emotionDetector", query_string=params)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")
        post.assert_not_called()

    @patch(WATSON_POST)
    def test_formatted_result(self, post):
        """The Flask route formats a Watson prediction for the browser."""
        post.return_value.status_code = 200
        post.return_value.json.return_value = {
            "emotionPredictions": [
                {"emotion": {"anger": 0.1, "disgust": 0.2, "fear": 0.3, "joy": 0.9, "sadness": 0.4}}
            ]
        }
        response = self.client.get(
            "/emotionDetector", query_string={"textToAnalyze": COURSE_EXAMPLES["joy"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "For the given statement, the system response is "
            "'anger': 0.1, 'disgust': 0.2, 'fear': 0.3, 'joy': 0.9 and 'sadness': 0.4. "
            "The dominant emotion is joy.",
        )

    @patch(WATSON_POST, side_effect=Timeout)
    def test_service_unavailable(self, _post):
        """A service failure produces a response distinct from invalid input."""
        with self.assertLogs(app.logger, level="WARNING"):
            response = self.client.get(
                "/emotionDetector", query_string={"textToAnalyze": "Test sentence"}
            )
        self.assertEqual(response.status_code, 502)
        self.assertIn(b"emotion service is unavailable", response.data)


@unittest.skipUnless(os.getenv("WATSON_LIVE_TESTS") == "1", "set WATSON_LIVE_TESTS=1")
class WatsonLiveTests(unittest.TestCase):
    """Run the five course examples against IBM Watson NLP itself."""

    def test_joy(self):
        """Recognize joy."""
        self.assertEqual(emotion_detector(COURSE_EXAMPLES["joy"])["dominant_emotion"], "joy")

    def test_anger(self):
        """Recognize anger."""
        self.assertEqual(emotion_detector(COURSE_EXAMPLES["anger"])["dominant_emotion"], "anger")

    def test_disgust(self):
        """Recognize disgust."""
        result = emotion_detector(COURSE_EXAMPLES["disgust"])
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        """Recognize sadness."""
        result = emotion_detector(COURSE_EXAMPLES["sadness"])
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        """Recognize fear."""
        self.assertEqual(emotion_detector(COURSE_EXAMPLES["fear"])["dominant_emotion"], "fear")


if __name__ == "__main__":
    unittest.main()
