FROM python:slim-bullseye

COPY . /app/vimeo-metadata
WORKDIR /app/vimeo-metadata

# O Gunicorn não está no requirements pois não
# é necessário para dev. Fica apenas aqui para
# usar no container.
# Esta foi a versão instalada para testar localmente.
RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --keep-alive 300 --config gunicorn.conf.py -w 4 -b 0.0.0.0:5000 app:app
