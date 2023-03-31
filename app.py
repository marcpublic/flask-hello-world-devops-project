#!/bin/env python3

import flask
from elasticapm.contrib.flask import ElasticAPM
import logging
from elasticapm.handlers.logging import LoggingHandler

TPL = flask.render_template # Pour éviter de toujours taper flask.render_template...

app = flask.Flask(__name__, template_folder='.')
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'flask-service',
  'SECRET_TOKEN': 'LG5PoPO8Mw9fJ9Dq1d',
  'SERVER_URL': 'https://822e8d5da0df47de93ba7d00e69b6c38.apm.eu-west-1.aws.cloud.es.io:443',
  'ENVIRONMENT': 'my-deployment',
}

apm = ElasticAPM(app, loging=True)

@app.route('/')
def info():
    data = """\
    Bonjour Thales!!!
    """
    return TPL("default.html", title='Home', data=data)
  
@app.route('/test')
def test():
#    data = """\
#    Test passed
#    """
    app.logger.error( 'erreur personnelle :-)', exc_info=True)
    flask.abort(500)
#    return TPL("default.html", title='Test', data=data)
  
@app.route('/paramurl/<int:number>')
def paramurl(number):
    data = """\
    Vous avez mis  {} dans l'URL.
    """.format(number)
    return TPL("default.html", title='ParamUrl', data=data)

@app.route('/paramget')
def paramget():
    login = flask.request.args['login']
    data = """\
    Le login entré est {}.
    """.format(login)
    return TPL("default.html", title='Paramget', data=data)

@app.route('/formulaire')
def formulaire():
    data = """\
    <form action="validate" method="post">
    <input type="text" name="login"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title='Formulaire', data=data)

# Récupération des données d'un formulaire, en POST uniquement
# Si les données sont postées en json et non en
# application/x-www-form-urlencoded ou multipart/form-data
# utiliser flask.request.get_json()  au lieu
# de flask.request.form
@app.route('/validate', methods=["POST"])
def validate():
    login = flask.request.form['login']
    data = """\
    Le login entré est {}.
    """.format(login)
    return TPL("default.html", title='Validate', data=data)


# Renvoie du json
@app.route('/data_json')
def data_json():
    liste = [1, 2, 3, "toto"]
    dico = {"val1": liste, "val2": "Salut"}
    return flask.jsonify(dico) # Renvoie la chaîne json en gérant correctement l'entête HTTP

# Code de retour :
# https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP
@app.route('/forbidden')
def forbidden():
    app.logger.error( 'Désolé, c\'est interdit :-)', exc_info=True)
    flask.abort(403)

@app.route('/internal')
def internal():
    app.logger.error( 'Trop fatigué pour répondre :-)', exc_info=True)
    flask.abort(500)

@app.route('/redirect_me')
def redirect_me():
    return flask.redirect(flask.url_for('info'))

print("PATH =====>", app.instance_path)
if __name__ == '__main__':
    app.config['DEBUG'] = False
    handler = LoggingHandler(client=apm.client)
    handler.setLevel(logging.WARN)
    app.logger.addHandler(handler)
    app.secret_key = 'chooseaverysecretkeyhere'
    app.run(host='0.0.0.0', port=5000)
#    app.run(host='0.0.0.0', port=80)
