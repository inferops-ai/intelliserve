FROM python:3.14

WORKDIR intent_classifier

COPY ./requirements-inference.txt /intent_classifier/requirements-inference.txt

RUN pip install --no-cache-dir --upgrade -r /intent_classifier/requirements-inference.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY . /intent_classifier

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]