# Submission evidence

The [blank-input screenshot](7c_error_handling_interface.png) shows the Flask app
displaying the rubric's error message. The [deployment screenshot](local-model-demo/6b_deployment_test.png)
shows the same Flask interface predicting joy with a labeled local DistilRoBERTa model.
The [local unit tests](5b_unit_testing_result.txt) use simulated Watson HTTP responses.
[Static analysis](8b_static_code_analysis.txt) scored 10.00/10 for server.py.

Run the following from the repository root inside the IBM Skills Network lab.

```sh
python3 -m pip install -r requirements.txt
python3 submission/run_rubric_checks.py
python3 server.py
```

The script saves actual Watson terminal results for Questions 3, 5, and 7, plus
the live emotion tests for Question 9. Start a browser preview on port 5000.
Enter **I think I am having fun** and capture the successful Watson result as
**6b_deployment_test.png** for Question 11.
