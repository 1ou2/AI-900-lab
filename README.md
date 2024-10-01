# Setup
```
python3 -m venv .venv
source ./venv/bin/activate
pip install -r requirements
```

# Description
Use the diabete infer model from the AI-900 ms course.
- predict_diabetes : infer from command line
- diabete.html : form used to send query -> a post request with json parameters is sent
- proxy_diabetes.py : local proxy server for bypassing cors
- diabete1.json : sample json data

The model outputs a probability

# RUN
## With html form
To avoid CORS problem for javascript requets, you need to launch the proxy
```python3 proxy_diabetes.py```
Then access the diabetes.html file and submit.

## from command line
Use ```python3 predict_diabetes.py```
Key and endpoint are stored in .env


