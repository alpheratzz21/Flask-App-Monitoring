# using light python base image 
FROM python:3.10-slim

# set working directory in container
WORKDIR /app

# copy requirements for efficient cache
COPY requirements.txt .

# install dependency 
RUN pip install --no-cache-dir -r requirements.txt

# copy all the source code to container
COPY . .

# expose apps port
EXPOSE 5000

# command for running the apps
CMD ["python", "app/app.py"]
