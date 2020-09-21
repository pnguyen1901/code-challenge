# Base Image
FROM python:3.7-slim-buster

EXPOSE 5000

# Keeps python from generating .pyc files in the container
ENV PYTHONONWRITEBYTECODE 1

# Install dependencies, -y to auto install subdependencides without human intervention. 
# Abscence of this can cause the docker process to fail
COPY requirements.txt .
RUN apt-get update
RUN apt-get install -y libpq-dev gcc python3-dev musl-dev
RUN python -m pip install -r requirements.txt

# Set a working directory on the container and copy all project files into app folder.
WORKDIR /app
COPY . /app

# Switching to non-root user and set the appuser the owner of app folder.
RUN useradd appuser && chown -R appuser /app
USER appuser

CMD ["python", "/app/run.py"]