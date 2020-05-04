bind = "0.0.0.0:4000"
workers = 4
timeout = 30
proc_name = "AMI-Uploader"

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
