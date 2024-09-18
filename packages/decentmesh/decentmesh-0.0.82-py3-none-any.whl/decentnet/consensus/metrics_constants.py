import os

METRICS_SERVER_HOST = os.environ.get('METRICS_SERVER_HOST', 'localhost')
METRICS_SERVER_PORT = int(os.environ.get('METRICS_SERVER_PORT', 8008))
