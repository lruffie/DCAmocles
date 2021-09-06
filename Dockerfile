FROM python:3.9

WORKDIR /src
COPY . .

RUN pip install -r requirements.txt


CMD [ "python", "src/main_job.py" ]
