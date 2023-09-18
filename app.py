import os
import flask
import vimeo
import requests
import metadata
import formatters

from flask import request
from threading import Thread


ENVVAR_PREFIX = 'VIMEO'


app = flask.Flask(__name__)

try:
    vimeo_client = vimeo.VimeoClient(
        os.environ[f'{ENVVAR_PREFIX}_TOKEN'],
        os.environ[f'{ENVVAR_PREFIX}_CLIENT_ID'],
        os.environ[f'{ENVVAR_PREFIX}_SECRET'])

except KeyError as ke:
    import sys
    print(
        f"\033[1;31mA envvar \033[37;41m{ke.args[0]}\033[0;1;31m parece não estar setada.",
        "Eu preciso dela pra funcionar.\033[0m",
        file=sys.stderr)
    raise


@app.route("/")
def home():
    return "vimeo-metadata lives!"


@app.route("/fetch/<usuario>/<folder_id>")
def fetch(usuario, folder_id):

    thread = Thread(target=fetch_file, kwargs={'id': request.args.get('id', folder_id), 'user': request.args.get('user', usuario)})
    thread.start()

    return (f'''A aplicação está sendo executada, dentro de alguns momentos receberá o arquivo pelo rocketchat, {usuario}. 
O tempo de execução varia de acordo com o tamanho da pasta.''')

def fetch_file(id, user):
    with app.app_context():
        response = metadata.fetch_metadata(
            vimeo_client, id,
            formatters.CSVFormatter(metadata.HEADERS, delimiter=';'),
            True)

        headers = {}
        json_data = {
            'channel': f'@{user}',
            'username': '4SecBot',
            'avatar': 'https://blog.domain.com.br/wp-content/uploads/2022/10/4secbot.png',
            'text': f'```{response}```'
                    }
        
        requests.post('https://chat.domain.com.br/hooks/132/123', headers=headers, json=json_data)


if __name__ == '__main__':
    app.run(debug=True)
