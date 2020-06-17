FROM python:3.6.8-jessie

COPY . /uploader

WORKDIR /uploader

ENV TZ Asia/Taipei

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn==19.9.0

RUN useradd -ms /bin/bash uploader
RUN chown -R uploader:uploader /uploader
USER uploader

EXPOSE 4000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]