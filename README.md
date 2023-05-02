# showbaseline
This is small script \ container \ POD will get BaseLine from Dynatrace and show it dashboard level

![Default looks](https://github.com/43034r/showbaseline/raw/main/default.JPG)
![Count looks](https://github.com/43034r/showbaseline/raw/main/count.JPG)

This python script use predict=true More - https://www.dynatrace.com/news/blog/how-to-ask-your-monitoring-system-about-the-future/

Also it can be used to add baselines to dashboard level.

=== Start with as docker container:
docker run -e YOUR_DT_API_TOKEN=dt0c01.x.x -e YOUR_DT_API_URL=https://dynatrace-api-url/api/v1 -e YOUR_SVC_LIST=SERVICE-F531D98ABDEE9F9D,SERVICE-D2E55F5D48FF41A1

flags:
YOUR_DT_API_TOKEN - your token with [ ]

YOUR_DT_API_URL - your api url contains /api/v1

YOUR_SVC_LIST - svc list - like SERVICE-F531D98ABDEE9F9D,SERVICE-D2E55F5D48FF41A1

YOUR_LOG_LEVEL  0 - debug 1 info 2 errors

YOUR_UPDATE_INTERVAL = 5 # in minutes - recommended 5 minutes.

YOUR_A_SEND_MINMAX = 1 # send min\max or only median - 0 - no, 1 - yes

YOUR_A_SEND_COUNT = 1 # send baseline - count of requests or not - 0 - no , 1 - yes
