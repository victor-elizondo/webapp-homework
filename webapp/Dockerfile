FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8501
COPY ./webapp.py /code/webapp.py
ENTRYPOINT ["streamlit", "run"]
CMD ["webapp.py"]