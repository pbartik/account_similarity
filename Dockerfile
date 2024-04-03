
FROM python:3.9 AS builder

WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

# quick way to make utils.py available for import in the main module
ENV PYTHONPATH "${PYTHONPATH}:/code/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]