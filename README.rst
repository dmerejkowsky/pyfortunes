setup the server:
-----------------

* fortunes-data.git: bare repo where you push, install the hook in
  hooks/post-update

* fortunes-data: mirror of the bar repo, updated by the hook

* pyfortunes: source code of the server

* Create a config file looking like

  .. code:: ini


    [server]
    # used by pyf-get
    url = http://sd-20870.dedibox.fr/pyfortunes
    # debug = true # uncomment during development
    port = 5000
    pickle_path = /path/to/pickle


    [text_db]
    # ued by pyf-dtc and pyf-parse
    base_dir = /path/to/fortunes-data

* Configure nginx and uwsgi (there are 2 system services to create and
  enable, some changes to be made in nginx's config and a special
  file to create for uwsgi)
