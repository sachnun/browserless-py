# python lite
FROM python:3.9.17-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# set install requirements
COPY requirements.txt ./

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
