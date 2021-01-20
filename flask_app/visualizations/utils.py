from dataclasses import dataclass
from glob import glob
from pathlib import Path
import subprocess
from typing import Dict, Tuple, Union


BOKEH_LAUNCH_CMD = 'bokeh serve visualizations/{app} --allow-websocket-origin=127.0.0.1:5000'

BokehServerMapping = Dict[Path, Tuple[Union[subprocess.Popen, None], int]]


def get_server_map() -> BokehServerMapping:
    cfl = Path(__file__).parent.resolve()
    bk_apps = glob(str(cfl / '*.py'))
    bk_apps = [Path(app) for app in bk_apps if 'utils.py' not in app and
                                               '__init__.py' not in app]
    port = 5006
    app_ports = {}
    for app in bk_apps:
        port += 1
        # None will be replaced by the subprocess that ends up running the server
        app_ports[app] = (None, port)
    return app_ports


def launch_bokeh_servers(app_ports: BokehServerMapping) -> BokehServerMapping:
    for app, (_, port) in app_ports.items():
        cmd = BOKEH_LAUNCH_CMD.format(app=app.name).split(' ')
        cmd += ['--port', str(port)]
        p = subprocess.Popen(cmd)
        app_ports[app] = (p, port)
    return app_ports


@dataclass
class BokehServerConfig:
    # TODO
    template: str
    url: str
    name: str = ''
