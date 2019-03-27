FROM python:3
RUN apt-get update
RUN apt-get install zip
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./market.py" ]
---


