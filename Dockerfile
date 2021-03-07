FROM python:3.9.2-alpine3.13
LABEL maintainer="Pavel Derendyaev <dddpaul@gmail.com>"
WORKDIR /app
COPY mailblaster.py /app
ENTRYPOINT [ "python", "/app/mailblaster.py" ]
