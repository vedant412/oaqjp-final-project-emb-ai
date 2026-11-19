"""Serve the Emotion Detector interface and analysis route with Flask."""

from flask import Flask, Response, render_template, request

from EmotionDetection import WatsonServiceError, emotion_detector

app = Flask(__name__)


@app.get("/")
def render_index_page():
    """Render the text entry form."""
    return render_template("index.html")


@app.get("/emotionDetector")
def analyze_emotion():
    """Analyze the textToAnalyze query parameter and display the result."""
    try:
        result = emotion_detector(request.args.get("textToAnalyze"))
    except WatsonServiceError as error:
        app.logger.warning("%s", error)
        return Response(
            "The emotion service is unavailable. Please try again later.",
            status=502,
            mimetype="text/plain",
        )

    if result["dominant_emotion"] is None:
        return Response("Invalid text! Please try again!", mimetype="text/plain")

    return Response(
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}.",
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
