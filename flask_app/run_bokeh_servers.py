import time

from visualizations.utils import (BokehServerMapping,
                                  get_server_map,
                                  launch_bokeh_servers)


if __name__ == '__main__':
    try:
        servers = get_server_map()
        servers = launch_bokeh_servers(servers)
        subps = [p for (p, _) in servers.values()]
        while True:
            print('Bokeh servers running')
            time.sleep(60)
    finally:
        for ps in subps:
            ps.kill()
            print(f'Killed {ps}')
        print('All subprocesses killed')
