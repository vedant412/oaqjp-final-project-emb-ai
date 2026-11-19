"""Capture the exact rubric examples and unit tests from the final project directory."""

import builtins
from code import InteractiveConsole
import json
import os
from pathlib import Path
import sys
from tempfile import mkdtemp
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import unittest

FIELDS = {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}
EXAMPLES = (
    ("2b_application_creation", "EmotionDetection.emotion_detection",
     "I love this new technology.", "joy"),
    ("3b_formatted_output_test", "EmotionDetection.emotion_detection",
     "I am so happy I am doing this", "joy"),
    ("4b_packaging_test", "EmotionDetection", "I hate working long hours", "anger"),
)


def run_example(module_name, sentence, expected):
    """Run real interactive Python calls and validate all six result fields."""
    console = InteractiveConsole()
    if hasattr(builtins, "_"):
        del builtins._
    print("$ python3")
    print(f"Python {sys.version.split()[0]} (InteractiveConsole)")
    lines = [
        f"from {module_name} import emotion_detector",
        f"emotion_detector({json.dumps(sentence)})",
    ]
    for line in lines:
        print(f">>> {line}")
        console.push(line)
    result = getattr(builtins, "_", None)
    return (
        isinstance(result, dict)
        and result.keys() == FIELDS
        and all(isinstance(result[emotion], (int, float)) for emotion in FIELDS - {"dominant_emotion"})
        and result["dominant_emotion"] == expected
    )


def run_unit_tests():
    """Run the five emotion tests against the chosen prediction service."""
    os.environ["WATSON_LIVE_TESTS"] = "1"
    print("$ WATSON_LIVE_TESTS=1 python3 -m unittest -v test_emotion_detection.WatsonLiveTests")
    tests = unittest.defaultTestLoader.loadTestsFromName(
        "test_emotion_detection.WatsonLiveTests"
    )
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(tests)
    return result.wasSuccessful() and result.testsRun == 5 and not result.skipped


def main():
    """Run each check and save pass and failure transcripts under distinct filenames."""
    if not Path("EmotionDetection/emotion_detection.py").is_file():
        raise SystemExit("Run the script from inside the cloned project directory.")
    sys.path.insert(0, str(Path.cwd()))
    destination = Path(mkdtemp(prefix="evidence-", dir="."))
    print(f"Saving evidence to {destination.resolve()}", flush=True)
    all_passed = True
    for filename, module_name, sentence, expected in EXAMPLES:
        captured = StringIO()
        with redirect_stdout(captured), redirect_stderr(captured):
            passed = run_example(module_name, sentence, expected)
        all_passed &= passed
        suffix = ".txt" if passed else ".failed.txt"
        (destination / (filename + suffix)).write_text(captured.getvalue(), encoding="utf-8")
        print(f"{filename}{suffix}", flush=True)
    captured = StringIO()
    with redirect_stdout(captured), redirect_stderr(captured):
        passed = run_unit_tests()
    all_passed &= passed
    unit_file = "5b_unit_testing_result.txt" if passed else "5b_unit_testing_result.failed.txt"
    (destination / unit_file).write_text(captured.getvalue(), encoding="utf-8")
    print(unit_file)
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
