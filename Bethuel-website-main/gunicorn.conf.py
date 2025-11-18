# gunicorn.conf.py
# For more details on Gunicorn settings, see:
# https://docs.gunicorn.org/en/stable/settings.html

import multiprocessing

# -- Server Socket --

# The address and port to bind to.
# This must match the upstream configuration in Nginx (e.g., web:8000).
bind = "0.0.0.0:8000"

# -- Worker Processes --

# Use the 'gthread' worker class for threaded workers.
worker_class = "gthread"

# The number of worker processes.
# A common formula is (2 * number_of_cpu_cores) + 1.
workers = (multiprocessing.cpu_count() * 2) + 1

# The number of threads per worker.
# Increases concurrency for I/O-bound applications.
threads = 4

# -- Timeouts --

# Workers silent for more than this many seconds are killed and restarted.
timeout = 120

# -- Logging --

# Log to stdout and stderr, which is the standard for containerized applications.
accesslog = "-"
errorlog = "-"
loglevel = "info"