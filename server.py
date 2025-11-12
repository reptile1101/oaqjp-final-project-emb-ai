"""
server.py

Flask server to provide an endpoint for emotion detection on user input.
"""

from typing import Any, Dict, Optional
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Constants
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
TEXT_PARAM = "textToAnalyze"

# Initialize Flask app
app: Flask = Flask(__name__)


@app.route("/")
def home() -> str:
    """
    Render the home page.
    
    Returns:
        str: HTML content of index page.
    """
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route() -> str:
    """
    Handle GET request to detect emotions from input text.

    Query Parameters:
        textToAnalyze (str): The text provided by the user.

    Returns:
        str: Formatted emotion analysis or error message.
    """
    text_to_analyze: Optional[str] = request.args.get(TEXT_PARAM)

    if not text_to_analyze:
        return "Error: No text provided for analysis.", 400

    try:
        response: Optional[Dict[str, Any]] = emotion_detector(text_to_analyze)
    except Exception:  # noqa: B110
        return "Error: Unable to process the request at the moment.", 500

    if response is None:
        return "Error: Unable to process the request at the moment.", 500

    if response.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    output_text: str = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']}, "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

    return output_text


if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
