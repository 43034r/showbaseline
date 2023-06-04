FROM python:3.10.0-alpine
ADD src/showbaseline.py /
RUN pip install schedule
RUN pip install requests


CMD [ "python", "./showbaseline.py" ]


