# Week 7: Web services. REST, Building API

## Backend
### 1. Backend overview
In software development, frontend refers to the presentation layer that users interact with, while backend involves the data management and processing behind the scenes, and full-stack development refers to mastering both. In the client–server model, the client is usually considered the frontend, handling user-facing tasks, and the server is the backend, managing data and logic. Some presentation tasks may also be performed by the server.

![alt text](schema.png)


### 2. Setup
To install FastAPI module we need to install it first: 
```bash
pip install fastapi uvicorn python-multipart
```


### 3. Writing "Hello world"
```example_1.py```
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/")
def hello_world_json():
    return {"Hello": "World"}

@app.get("/text")
def hello_world_text():
    return "Hello world"

@app.get("/html", response_class=HTMLResponse)
def hello_world_text():
    return """<h1> Hello world </h1>"""

if __name__ == "__main__": 
  uvicorn.run(app, host="0.0.0.0", port=8000)
```

To access web page you can visit: 
```127.0.0.1:8000```, ```localhost:8000```, or ```0.0.0.0:8000```


### 4. Documentation & Route tags
#### 4.1 Documentation
FastAPI has self documentation feature. For each application you write, there is an option to visit ```host:port/docs``` to see each route that your application currently has. 
![alt text](self_doc.png)

#### 4.2 Route tags
If you found FastAPI self documentation is not complete enough you can also group all your routes to groups via assigning tag(s) to them, write description and summary to them. 
```example_1.py```
```python
@app.get("/text", 
         tags=["hello group"], 
         description="Returns a simple text response", 
         summary="Returns Hello World as text")    
def hello_world_text():
    return "Hello world"
```

![alt text](self_doc_ext.png)


### 5. Parametrised requests.

Input data that can be passed in the route can be (in general) splitted on 3 main parts: path parameters, query parameters, and body. This section will show you how we can use all of them to build an API. Complete code for this section can be found in ```example_2.py```

#### 5.1 Path parameters
The simplest way to make such request is to 
1. Specify the path in your route - just name it in "{}" (like a python f-string)
2. Add input parameter to a function that process a request 
```python
@app.get("/any_parameter/{parameter}", tags=['path parameters'])
def with_any_paramteres(parameter):
  return {"parameter": parameter, 'type': type(parameter).__name__} 
```

Input parameters can also be typed, for this you need to specify type in the function header ```parameter: type```. 
```python
@app.get("/typed_parameter/{parameter}", tags=['path parameters'])
def with_int_paramteres(parameter: int):
  return {"parameter": parameter, 'type': type(parameter).__name__} 
```
In case your parameter do not pass type-check you will have 422 status code (Unprocessable entity).

Request with path parameter would look like: ```http://server/parameter/123```where ```123``` is our parameter. 

#### 5.2 Query parameters
Query parameters also passed via url itself, but has different syntax: 
```http://server?parameter1=123&parameter2=456```, where we pass 2 parameters, 1st is called ```parameter1``` with value of ```123``` and 2nd is called ```parameter2``` with value ```456```. 

Example that would accept 1 parameter called ```parameter``` that would accepts any values: 
```python
@app.get("any_query_parameter", tags=['query parameters'])
def with_any_query_parameters(parameter):
  return {"parameter": parameter, 'type': type(parameter).__name__}
```

<br>

And an example of same route, which would only accept integer parameters. The only difference - type is added in the header of a function.
```python
@app.get("/typed_query_parameter", tags=['query parameters'])
def with_typed_query_parameters(parameter: int):
  return {"parameter": parameter, 'type': type(parameter).__name__}
```

#### 5.3 Body 
When the number of parameters is large and putting them url making no sense, we can choose passing them in the body of the request as an option. 
A good practice for body parameters would be validating their types and values, for it pydantic is usually used among with FastAPI.

First what we need to define is pydantic Schema: 
```python
class Item(BaseModel):
  # Simple string field that accept any string and cannot be empty
  name: str
  
  # Integer field that must be greater than 0 and less than or equal to 1000
  price: float = Field(gt=0, le=1000)
  
  # Optional string field that can be None or a string with a maximum 
  # length of 3 characters, and defaults to None if not provided
  description: str | None = Field(default=None, max_length=100)
```
In schema we need to define name of the parameters, their types, and optionally some other bounds on values, like in price field (we require price to be in greater than 0, but less than 1000) and description (max length of it should be no more than 100 symbols, if it is not passed None will be set). 

Second step would be to define the route itself: 
```python
@app.post("/body_parameters", tags=['body parameters'])
def with_body_parameters(item: Item):
    return {
      "item": item, 
      'type': type(item).__name__, 
    }
```

### 6. File upload
For our project we will implement feature of predicting values for the whole csv file that would be given to backend. For this we need to be ready to process a file: 
```python
from fastapi import UploadFile, HTTPException
import pandas as pd

@app.post("/file_upload", tags=['file uploads'])
def upload_file(file: UploadFile):
  if not file.filename.endswith('.csv'):
    raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
  
  df = pd.read_csv(file.file, encoding='utf-8')
  
  return {
    "filename": file.filename,
    "content_type": file.content_type,
    "columns": list(df.columns),
    "row_count": len(df),
  }
```
In this example we accept only csv files, read them with pandas and return information about ciolumns & number of rows in the file. 

### 7. Load ML model
The complete example is available in the ```backend.py```. 
Routes defined: 
+ healthcheck
+ predict single sample (with pydantic validation), returns ```{"prediction": "yes"/"no"}```
+ predict batch: takes a *.csv file and returns ```{
  "filename": "bank-sample.csv",
  "predictions": [
    "no",
    "no",
    "no",
    "no",
    "no",
    "no", ...
  ]
}```

## Frontend
### 1. Requests/curl recap 
#### 1.1 Setup
```bash
pip install requests streamlit
```

#### 1.2 Curl
As we already seen in the FastAPI self-documentation there are examples of how we can do request from terminal via curl:
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/health' \
  -H 'accept: application/json'
```

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 0,
  "job": "string",
  "marital": "string",
  "education": "string",
  "default": "string",
  "balance": 0,
  "housing": "string",
  "loan": "string",
  "contact": "string",
  "day": 0,
  "month": "string",
  "duration": 0,
  "campaign": 0,
  "pdays": 0,
  "previous": 0,
  "poutcome": "string"
}'
```

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/predict_batch' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@bank-sample.csv;type=text/csv'
```

For our purposes it would be enougn to know these flags: 
+ ```-X METHOD``` - specifies the method of request to be sent (GET, POST, DELETE, PUT...)
+ ```-H header``` - specifies headers of request `accept: application/json` - would specify the way we pass data to the server
+ `-d 'data'` - would attach data as a bytes to the request 
+ `-F file=@filepath` - is needed to attach a file to the request  

#### 1.3 Requests
Requests python library allows you to make similar things but with more convenience, also it would help us to make communication between frontend & backend. 

Simple request without parameters
```python
import requests

response = requests.get("http://0.0.0.0:8000/health")

print(response.status_code) # 200 - success
print(response.url) # http://0.0.0.0:8000/health
print(response.json()) # {"status": "healthy"}
```

Request with query parameters
```python
response = requests.get("http://0.0.0.0:8000/health", params={'a': 1, 'b': '2'})

print(response.url) # 'http://0.0.0.0:8000/health?a=1&b=2'
```

Request with body: 
```python
body = {
  "age": 0,
  "job": "string",
  "marital": "string",
  "education": "string",
  "default": "string",
  "balance": 0,
  "housing": "string",
  "loan": "string",
  "contact": "string",
  "day": 0,
  "month": "string",
  "duration": 0,
  "campaign": 0,
  "pdays": 0,
  "previous": 0,
  "poutcome": "string"
}

response = requests.post("http://0.0.0.0:8000/predict", json=body)
print(response.status_code) # 200
print(response.json()) # {'prediction': 'no'}
print(response.request.body) # b'{"age": 0, ... "poutcome": "string"}'
```

Request with file attached
```python
file = open('bank-sample.csv')
response = request.post("http://0.0.0.0:8000/predict_batch", file={'file': file})

print(response.status_code) # 200
print(reponse.json()) 
# {'filename': 'bank-sample.csv', 'predictions': ['no', 'no', ..., 'no']
```



### 2. Streamlit
Streamlit is an open-source Python library designed for quickly creating and sharing interactive web applications for data science and machine learning. It helps to build interactive dashboards and web apps with minimal code.

To create webpage you need to put streamlit widgets: 
```python
import streamlit as st

# put title on the page
st.title("Application Example")

# creates field for text input
string = st.text_input("String input")

# will go to "if" statement only if button clicked
if st.button("Submit"):
    st.write(f"You wrote: {string}")

# number input as a slider, min, max, and start values specified 
number = st.slider("Select number", 0, 100, 25)
# puts an immutable string to the page
st.write(f"Selected number: {number}")

import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 15, 25, 30]
})

# shows dataframe
st.dataframe(data)

# input field for numbers 
number_input = st.number_input("Enter number", min_value=0, max_value=120, value=30)
# input field for strings
text_input = st.text_input("Enter string", "default value")
st.write(f"Number: {number_input}, Text: {text_input}")
```

## Project tasks:
#### Backend
Write backend file(s) for your project. It should support the following requests: 
1. ```/health```
Healthcheck
<br>

2. ```/predict```
Predicting for a single sample, you need to accept arguments as json in input and return predicted price as a float. 
Example of the response: 
```{"prediction": 1234.56}```
<br>

3. ```/predict_batch```
Takes csv file **in the exactly same format as dataset given to you but without target column** ([example](https://drive.google.com/file/d/1Gr3204qQ9PYKYFl5WCxD3WImiCBOqkKc/view)), 

| year | make      | model           | trim   | body         | transmission | vin              | state | condition | odometer | color | interior | seller                          | saledate                                      |
|------|-----------|-----------------|--------|--------------|--------------|------------------|-------|-----------|----------|-------|----------|---------------------------------|-----------------------------------------------|
| 2014 | Kia       | Optima          | LX     | Sedan        | automatic    | 5xxgm4a71eg328703| tx    | 49        | 11485    | gray  | gray     | kia motors america  inc        | Wed Feb 04 2015 02:30:00 GMT-0800 (PST)       |
| 2014 | Kia       | Optima          | LX     | Sedan        | automatic    | 5xxgm4a71eg318141| tx    | 26        | 14265    | white | beige    | kia motors america  inc        | Wed Feb 04 2015 02:30:00 GMT-0800 (PST)       |
| 2006 | Chrysler  | Town and Country| Limited| Minivan      | automatic    | 2a8gp64l96r821834| az    | 19        | 92649    | gold  | tan      | onesource/southwest remarketing| Thu Jan 22 2015 03:00:00 GMT-0800 (PST)       |
| 2006 | Chevrolet | Silverado 1500  | LS     | Extended Cab |              | 1gcek19bx6z269153| tx    | 22        | 166999   | white | gray     | texas direct auto              | Wed Feb 25 2015 02:20:00 GMT-0800 (PST)       |



and returns data in the following format
```{"predictions": [15700, 15900,  4700]}```
Length of the output list is equal to the size of the input .csv file. 
<br>

4. If you need some other routes feel free to create them. (e.g. you can create route/page for showing information about your model type, metrics, plots..)

#### Frontend
Develop a frontend application for your model. The following functions needs to be implemented: 
1. Predicting for a single sample that can be entered via input widgets 
2. Uploading a *.csv file (as described above), showing first 3-5 rows of it, and predicting a target values of it. 

After the prediction there should be an opportunity to download same csv file, but with one new ```sellingprice``` column.  