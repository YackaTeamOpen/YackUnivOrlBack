# Entrypoint for gevent
from gevent import monkey
monkey.patch_all()

import logging
from main.config import environments, config_name
from yacka import app, close_all_db_sessions
from gevent.pywsgi import WSGIServer
from gevent import signal


# logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

http_server = WSGIServer(
    ('0.0.0.0', int(environments[config_name]["server_port"])), app)


def stop_server(sig, stackFrame):
    log.info('Closing all db sessions...')
    # Not sure it is useful, but we had some mysql session locks when not using WSGI, so...
    close_all_db_sessions()
    log.info('Stopping server...')
    # According to what i saw in docs, the following stops accepting connections
    # and waits for the current requests handlers to exit (within the timeout delay,
    # after which they are killed). - Olivier
    # 1 is the default timeout anyway, but can be changed...
    http_server.stop(timeout=1)


# Only use pywsgi if we are running in alpha/prod
# commenté car produit un warning disant qu'app.run est ignoré lorsque lancé par flask
# if config_name == "local" or config_name == "alpha":
#     app.run(host=environments[config_name]["host"], port=int(
#         environments[config_name]["server_port"]), debug=environments[config_name]["debug"])
# else:
signal.signal(signal.SIGTERM, stop_server)
log.info('Starting server...')
http_server.serve_forever()
