import traceback

def error(e, logfile, info=None):
    with open(logfile, 'a') as f:
        traceback.print_exc(file=f)
