
# 0002 Logging

At the moment, I'm doing everything that I can to log all of Threepanel's output
with syslog, sending everything to a Papertrail server.

[Taking some pain out of Python Logging](https://hynek.me/articles/taking-some-pain-out-of-python-logging/).

It's easy enough to configure PostgreSQL, Redis, Nginx, and uWSGI to send all of their
output to a syslog server. The only hold-out is Celery. I haven't quite figured out
Celery yet.
