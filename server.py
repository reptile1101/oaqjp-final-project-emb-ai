from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    # Get the text from the query string
    text_to_analyze = request.args.get('textToAnalyze')
    
    if not text_to_analyze:
        return "Error: No text provided for analysis.", 400

    # Call your emotion detection function
    response = emotion_detector(text_to_analyze)

    # If API fails or returns None
    if response is None:
        return "Error: Unable to process the request at the moment.", 500

    # Format output string
    output_text = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

    return output_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)