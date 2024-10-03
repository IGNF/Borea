# Docker image
FROM ubuntu:jammy-20240427

# installation lib
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip libgdal-dev=3.4.1+dfsg-1build4 && apt-get clean

# Copy and install requirements
COPY . .
RUN pip install --no-cache-dir -r borea_dependency/requirements.txt && pip install --no-cache-dir GDAL==3.4.1

# WORKDIR
WORKDIR /borea_tools

# Action
ENTRYPOINT ["python3"]
CMD ["docker_help.py"]
