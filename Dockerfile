FROM python:3.10.0-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
ADD src/showbaseline.py /
RUN pip install schedule
RUN pip install requests


CMD [ "python", "./showbaseline.py" ]


