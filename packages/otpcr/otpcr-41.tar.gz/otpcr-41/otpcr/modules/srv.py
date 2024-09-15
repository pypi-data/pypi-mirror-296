# This file is placed in the Public Domain.


"create service file"


import getpass


from ..main import Config, Commands


def srv(event):
    "create service file (pipx)."
    if event.args:
        name = event.args[0]
    else:
        name  = getpass.getuser()
    progname = Config.name
    txt = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""
    event.reply(txt % (progname.upper(), name, name, name, progname))


Commands.add(srv)
