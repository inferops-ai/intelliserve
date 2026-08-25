FROM python:3.14

WORKDIR inference_engine

COPY ./requirements.txt /inference_engine/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /inference_engine/requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY . /inference_engine

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]