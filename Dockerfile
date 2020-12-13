FROM python:3.9.1-alpine3.12
LABEL maintainer="Pavel Derendyaev <dddpaul@gmail.com>"
WORKDIR /app
COPY mailblaster.py /app
CMD [ "python", "/app/mailblaster.py" ]
