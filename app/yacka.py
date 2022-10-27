from flask import request, session  # , request
# from flask_script import Manager # no longer supported after flask 2.0 upgrade
# following line added after Flask 2.0 transition
import click

from flask_migrate import Migrate

from sqlalchemy.orm import close_all_sessions
import logging
from main import create_app, db
from main.config import environments, config_name
from api import blueprint
from tests import test as yacka_test

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

app = create_app(config_name)
app.register_blueprint(blueprint)
app.app_context().push()
migrate = Migrate(compare_type = True)
migrate.init_app(app, db)


def close_all_db_sessions() :
    close_all_sessions()


@app.before_request
def before_request():
    session.permanent = True
    session.modified = True


# Les requêtes de type PATCH sont "preflighted", càd précédées d'une requête préliminaire
# de type OPTIONS, à laquelle il faut répondre par une validation de l'origine émettrice
# (ici le même serveur avec le port 3000, mais on pourrait inclure dans la liste l'adresse
# spécifique d'un autre serveur.)
@app.after_request
def after_request_func(response):
    if request.method == 'OPTIONS':
        # response = make_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods', 'PATCH, POST, PUT, GET, OPTIONS, DELETE')

    # The following is to enforce security rule on the client side
    # To prevent man-in-the-middle attacks
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # To prevent content type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # To avoid clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # To avoid cross site scripting attacks
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    # Fix CORS issue. When Access-Control-Allow-Credentials = true, Access-Control-Allow-Origin cannot be "*"
    response.headers.add('Access-Control-Allow-Origin', environments[config_name]["web_manager_url"], )
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.cli.command('test')
@click.argument('test_type')
@click.option('--arg', default = None)
@click.option('--arg2', default = None)
@click.option('--arg3', default = None)
@click.option('--arg4', default = None)
@click.option('--arg5', default = None)
def test(test_type, arg, arg2, arg3, arg4, arg5):
    """ Runs a sequence of tests mentionned by test_type.

    Usage : flask test [ list_all_users | list_users_with_multiple_shared_trips [--arg=<status>] | \
    list_users_with_one_shared_trip [--arg=<status>] | show_shared_trip_consistency |\
    list_concurrent_shared_trips | delete_pending_shared_trips | overall_shared_trip_history | \
    shared_trip_history --arg=<sht_id> | trips_with_shared_trips | show_shared_trip_statuses | \
    terminate_a_shared_trip --arg=<shared_trip_id> ]
    """

    return yacka_test(test_type, arg, arg2, arg3, arg4, arg5)
