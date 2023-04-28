# showbaseline
This is small script \ container \ POD will get BaseLine from Dynatrace and show it dashboard level

![Default looks](https://github.com/43034r/showbaseline/raw/main/default.JPG)

This python script use predict=true More - https://www.dynatrace.com/news/blog/how-to-ask-your-monitoring-system-about-the-future/

Also it can be used to add baselines to dashboard level.

=== Start with as docker container:
docker run -e YOUR_DT_API_TOKEN=dt0c01.x.x -e YOUR_DT_API_URL=https://dynatrace-api-url/api/v1 -e YOUR_SVC_LIST=SERVICE-F531D98ABDEE9F9D,SERVICE-D2E55F5D48FF41A1