# showbaseline
This is small script \ container \ POD will get BaseLine from Dynatrace and show it on dashboard level

Important! For work wait an hour after custom metric creation 

plans:


(-) reduce network overhead (1 request instead five small)

(-) add metric for failure rate

default it is look likes:
![Default looks](https://github.com/43034r/showbaseline/raw/main/img/default.JPG)
How it is look likes on dashboard:
![Count looks](https://github.com/43034r/showbaseline/raw/main/img/response.JPG)
How look likes prediction of load (count) of the service
![Count looks](https://github.com/43034r/showbaseline/raw/main/img/count.JPG)
![Count looks](https://github.com/43034r/showbaseline/raw/main/img/count2.JPG)
Prediction - example usecase
![Count looks](https://github.com/43034r/showbaseline/raw/main/img/example.JPG)

This python script use predict=true More - https://www.dynatrace.com/news/blog/how-to-ask-your-monitoring-system-about-the-future/

Also it can be used to add baselines to dashboard level.

=== Start with as docker container:
docker run -e DT_API_TOKEN=dt0c01.x.x -e DT_API_URL=https://dynatrace-api-url/api/v1 -e SVC_LIST=SERVICE-F531D98ABDEE9F9D,SERVICE-D2E55F5D48FF41A1

flags:

DT_API_TOKEN - your token with [ ]

DT_API_URL - your api url contains /api/v1

SVC_LIST - svc list - like SERVICE-F531D98ABDEE9F9D,SERVICE-D2E55F5D48FF41A1

LOG_LEVEL  0 - debug 1 info 2 errors

UPDATE_INTERVAL = 5 # in minutes - recommended 5 minutes.

A_SEND_MINMAX = 1 # send min\max or only median - 0 - no, 1 - yes

A_SEND_COUNT = 1 # send baseline - count of requests or not - 0 - no , 1 - yes


=== ShowBaseLine.json substitute service ID (SERVICE-F531D98ABDEE9F9D) your service ID.

#Example - yaml - if you want to start container in k8s

```
apiVersion: v1
kind: Secret
metadata:
  name: tokensecret
  namespace: dev
type: Opaque
stringData:
  token: "dt0c01.xxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: showbaseline
  name: showbaseline
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: showbaseline
  strategy: {}
  template:
    metadata:
      labels:
        app: showbaseline
    spec:
      containers:
      - image: docker.io/43034r/showbaseline:latest
        env:
        - name: SVC_LIST
          value: "SERVICE-F531D98ABDEE9F9D"
        - name: DT_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: tokensecret
              key: token
          value: ""
        - name: DT_API_URL
          value: "https://someapiurl/api/v1"
        - name: A_SEND_MINMAX
          value: "1"
        - name: A_SEND_COUNT
          value: "1"
        - name: LOG_LEVEL
          value: "0"
        name: showbaseline
```

![Default looks](https://github.com/43034r/showbaseline/raw/main/img/ex1.JPG)
