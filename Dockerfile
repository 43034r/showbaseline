FROM python:3
ADD showbaseline.py /
RUN pip install schedule
RUN pip install requests


CMD [ "python", "./showbaseline.py" ]


