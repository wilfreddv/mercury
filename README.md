# mercury

## Small webserver in Python


### How to
`mercury` is currently only available for every system with a `/etc` folder.
You can use `mercury` by cloning this repository and installing the modules in `requirements.txt`.

#### conf file options
"HOST" : string - host (e.g. 'localhost')
"PORT" : integer - port number
"HOME_DIR" : string - path to the base directory of your site (static only)
"LOAD" : string - 'wsgi' (Flask) or 'static' (plain HTML)
"APP" : string - path to the `app.py` file (wsgi only)
