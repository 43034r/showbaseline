FROM python:3.10.0-alpine
RUN useradd -ms /bin/bash appuser
USER appuser
ADD src/showbaseline.py /
RUN pip install schedule
RUN pip install requests


CMD [ "python", "./showbaseline.py" ]


