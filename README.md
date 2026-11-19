# Final project

Emotion Detector is a Python and Flask application for IBM’s Developing AI Applications
with Python and Flask course. It sends English text to the IBM Skills Network Watson NLP
EmotionPredict API, returns scores for anger, disgust, fear, joy and sadness, and reports
the emotion with the highest score. The Flask interface exposes the course route
`GET /emotionDetector?textToAnalyze=...`.

The project uses the route and frontend conventions of the
[IBM Skills Network starter repository](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai).

## Run the application

Use Python 3.10 or newer. Extract the ZIP into your project directory. Run these
commands from the directory containing `server.py`. In the Skills Network lab, use
`python3` if the terminal uses that command.

```sh
python -m pip install -r requirements.txt
python server.py
```

Open [the local app](http://127.0.0.1:5000/) or, in the IBM lab, select
**Skills Network Toolbox → Launch Application** and enter port **5000**.
For predictions, run the app where the course Watson endpoint is reachable. See the
[Skills Network Cloud IDE guide](https://github.com/ibm-skills-network/labs-knowledgebase/blob/main/docs/Lab%20Tools/_CloudIDECommon.mdx).

The package returns a dictionary with the keys `anger`, `disgust`, `fear`, `joy`,
`sadness` and `dominant_emotion`. Blank input and HTTP 400 from Watson both yield
`None` for all six keys. Flask displays **Invalid text! Please try again!** for those
inputs. If Watson cannot serve the request, Flask shows a service-unavailable message.
The invalid-input message uses a successful HTTP response for compatibility with the
course starter’s browser script.

## Run the checks

The first command checks the package and Flask routes with simulated Watson responses.
The second runs the static analysis required by the rubric. The third checks all
Python files. The Pylint configuration permits the exact package name `EmotionDetection`
required by the course.

```sh
python -m unittest -v test_emotion_detection.EmotionDetectorTests test_emotion_detection.FlaskTests
python -m pylint server.py
python -m pylint server.py EmotionDetection test_emotion_detection.py
```

In the IBM lab, run the five live tests for the required emotion examples. The
following command sets the test flag for one invocation in the lab's Bash terminal.

```sh
WATSON_LIVE_TESTS=1 python -m unittest -v test_emotion_detection.WatsonLiveTests
```

On Windows PowerShell, use these commands if Watson is reachable there.

```powershell
$env:WATSON_LIVE_TESTS = '1'
python -m unittest -v test_emotion_detection.WatsonLiveTests
Remove-Item Env:WATSON_LIVE_TESTS
```

## Collect the submission evidence

Fork the IBM starter to your own public GitHub repository and clone your fork. Place
the extracted project files at the root of that clone, keep its Git history, and commit
and push the project files. Open `README.md` and
`EmotionDetection/__init__.py` on GitHub and copy each file’s page URL for the rubric.

Run these commands in the IBM lab and save the command and actual output from each.

**Task 2 · Import and run the application module**

```sh
python3
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I love this new technology.")
```

**Task 3 · Show the formatted result**

```sh
python3
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I am so happy I am doing this")
```

**Task 4 · Import directly from the package and call it**

```sh
python3
>>> from EmotionDetection import emotion_detector
>>> emotion_detector("I hate working long hours")
```

For Task 5, save the live test command and its complete output. For Task 8, save the
`python -m pylint server.py` command and its actual score.

For Task 6, open the running app, enter **I think I am having fun**, click
**Analyze emotions**, and capture the browser showing the entered text and the
successful Watson result. Save the image as `6b_deployment_test.png`.

For Task 7, clear the field, click **Analyze emotions**, and capture the browser
showing the blank field and **Invalid text! Please try again!**. Save the image as
`7c_error_handling_interface.png`.
