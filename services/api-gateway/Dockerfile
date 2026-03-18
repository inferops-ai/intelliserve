FROM python:3.14

WORKDIR api_gateway

COPY ./requirements.txt /api_gateway/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api_gateway/requirements.txt 

COPY . /api_gateway

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]