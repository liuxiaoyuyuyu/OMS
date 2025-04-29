# Flask App
This is a flask app that follows the JSON:API specification. `app.py` uses plain Flask, while `app_flask_restful.py` uses Flask-RESTful.

For now, the goal is to duplicate what the current server (written in JavaScript) does:
```
https://cmsoms.cern.ch/agg/api/v1/fills/
```

## Set up the virtual enviroment
```
cd OMS/myproject
python3 -m venv venv
source venv/bin/activate
pip install flask flask-restful pandas
```

## How to run the code 
```
python3 app_flask_restful.py
```
In a browser, go to http://127.0.0.1:5000/api/v1/fills/

### Examples 
• Filter fills with fill_number > 10000:
```
http://localhost:5000/api/v1/fills/?filter[fill_number][GT]=10000
```
• Filter where duration <= 5000:
```
http://localhost:5000/api/v1/fills/?filter[duration][LTE]=5000
```
• Sort by peak lumi (ascending):
```
http://localhost:5000/api/v1/fills/?sort=peak_lumi
```
• Sort by duration (descending):
```
http://localhost:5000/api/v1/fills/?sort=-duration
```

