```
$ cat requirements.txt
PyVimeo==1.1.0
Flask==2.0.2
$ pip install -r requirements.txt
...
$ python metadata.py -h
usage: metadata.py [-h] --token TOKEN --client-id CLIENT_ID --secret SECRET [--format {csv,json}] [--csv-delimiter CSV_DELIMITER]
                   [--recursive]
                   FOLDER_ID

options:
  -h, --help            show this help message and exit

Vimeo:
  --token TOKEN, -t TOKEN
                        Vimeo token
  --client-id CLIENT_ID, -c CLIENT_ID
                        Vimeo Client ID
  --secret SECRET, -s SECRET
                        Vimeo secret
  --format {csv,json}, -f {csv,json}
                        Default: csv
  --csv-delimiter CSV_DELIMITER
                        Default: `;`
  --recursive, -R       Recurse into subfolders
  FOLDER_ID             Folder ID to get videos from
```

***

Há dois scripts que podem ser usados para executar o programa.

* [`run`](./run) executa `metadata.py`;
* [`run-flask`](./run-flask) executa `app.py`.

**Nota:** Para executar os scripts, é necessário definir os parâmetros ou
variáveis `TOKEN`, `CLIENT_ID` e `SECRET` presentes no script que será
utilizado.

Caso você decida subir o servidor flask, pode acessar a rota principal em
http://localhost:5000/fetch/FID substituindo `FID` pelo ID da pasta do Vimeo de
onde os dados devem ser extraídos.
