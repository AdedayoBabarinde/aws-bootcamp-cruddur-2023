# Week 2 — Distributed Tracing


## Required Homework

## HoneyComb

- Add HoneyComb opentelemetry libraries in `requirements.txt` and used pip to install them.

```txt
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```
- I Imported these libraries in `app.py`
```python
# HoneyComb ---------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
```
- Create and initialize a tracer and Flask instrumentation to send data to Honeycomb.
- Add 2 lines of code that will output logs to STDOUT of flask container.(for debugging).
```python
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)
```
- Set HoneyComb API env var in gitpod for docker compose backend that will make honeycomb know where to send the data. 
```yml
      OTEL_SERVICE_NAME: 'backend-flask'
      OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
      OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
```
- Created a tracer in `home_activities.py`
```py
from opentelemetry import trace
tracer = trace.get_tracer("home.Activities") # this will show up in attribute of field library
```

- **Created a custom span in home activities** to display it in honeycomb.
- **Created a custom attribute inside the span**
```py
with tracer.start_as_current_span("home-activites-mock-data"):
    span = trace.get_current_span() 
    now = datetime.now(timezone.utc).astimezone()
    span.set_attribute("app.now", now.isoformat()) 
```
- Custom fields are prefix with app so we could find them easily like `"app.now"`

**Run queries to explore traces within Honeycomb.io**

![image](https://user-images.githubusercontent.com/50416701/224509032-9dbd81f9-4303-49fa-861b-82ed894c51a0.png)


**Features of the our custom span**

![image](https://user-images.githubusercontent.com/50416701/224508987-35f8e28c-fc3b-4f62-ae3d-729392aba5a5.png)


**Important Notes from Live Stream**:
- Why opentelemetry exist?<br>
All observabilty platforms has standard for sending data. then opentelemetry made a standard and all
platforms used it now even AWS x-rays use it now.

- when setting any env like honecompo api key and then using docker compose up from
  VScode UI, it won't pick up the env because it is set in other terminal.<br>
*SOLVING THE ISSUE:*
- either put the env in gp env and close the workspace and open a new one.
- or use docker compose from the same termianl.

## AWS X-RAY

### Instrument AWS X-Ray into Back-End Flask Application
- Add to the `requirements.txt` and install it using `pip install -r requirements.txt`.

```py
aws-xray-sdk
```

- Add to `app.py` the import and configureation of x-rays.

```py
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# above lines should be above app Flask.
app = Flask(__name__)
# next line should be after app Flask.
XRayMiddleware(app, xray_recorder)
```
- Run this command to create a log group inside AWS X-Ray (CloudWatch Logs).
```sh
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
```
- Added `aws/json/xray-sampling-rule.json`.

```json
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "backend-flask",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```
- Run this command to create a sampling rule that we created above.
```sh
aws xray create-sampling-rule --cli-input-json file://aws/json/xray-sampling-rule.json
```

### Configure and provision X-Ray daemon within docker-compose and send data back to X-Ray API

- **Two ways for Installing X-Ray**:
  - The two lines above [this link](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-2/journal/week2.md#add-deamon-service-to-docker-compose) will install X-Ray manually (not preferred).
  - The better way is using docker-compose (preferred).
```yml
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "eu-south-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```
- Add these two env vars to my backend-flask in `docker-compose-gitpod.yml` file
```yml
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```

### Observe X-Ray traces within the AWS Console
**proof of work**

![image](https://user-images.githubusercontent.com/50416701/224508270-90bcd719-b74e-4459-84ca-bdc262cac362.png)



> See My Implementation here [commit details](https://github.com/AdedayoBabarinde/aws-bootcamp-cruddur-2023/commits/main)




## AWS CloudWatch Logs

### Install WatchTower and Import It in the Code
- Add to the `requirements.txt`
```sh
watchtower
```

- Imported libraries into `app.py`

```
import watchtower
import logging
from time import strftime
```
### Write a Custom Logger to Send Application Log Data to CloudWatch Log Group.
- Init CloudWatch Logs
```py
# Configure Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# setup log group inside CloudWatch 
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
# logs
LOGGER.info("test log from app.py")
```
- This will log ERRORS to CloudWatch
```py
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```
- Set the env var in backend-flask for `docker-compose-gitpod.yml`

```yml
      AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```
- Finally, add a custom logging in `home_activities.py`, and edit a logger variable as follow
```py
# home_activities.py  
  def run(logger):
    logger.info("HomeActivities")

# app.py
@app.route("/api/activities/home", methods=['GET'])
def data_home():
  data = HomeActivities.run(logger=LOGGER)
  return data, 200
```

**Proof of work**

![image](https://user-images.githubusercontent.com/50416701/224509461-a59611ff-9e79-4a7b-87fc-6f6edf6d6881.png)







## Rollbar

### Integrate Rollbar for Error Logging

- I exported my credentials of rollbar and put them inside gitpod envs.

### Trigger an error and observe it

- Removed the return of the function from home_activities.py file. Observation is as shown below
![image](https://user-images.githubusercontent.com/50416701/224507960-f09de091-3de3-4fe7-a6f0-30a351cbef26.png)


![image](https://user-images.githubusercontent.com/50416701/224507936-bfc43eaf-b8d5-4540-96c3-c4d79502ffa5.png)
