FROM python:3.10.0-alpine
ADD showbaseline.py /
RUN pip install schedule
RUN pip install requests


CMD [ "python", "./showbaseline.py" ]


