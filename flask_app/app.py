import subprocess

from bokeh.embed import server_document

from flask import Flask, render_template

from visualizations.utils import BokehServerMapping, get_server_map


APP_ROUTE_TEMPLATE =\
"""@app.route(f'/visualizations/{viz}')
def {viz}():
    script = server_document(f'http://127.0.0.1:{port}/{viz}')
    return render_template('bokeh.html', bokS=script)"""


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Example of embedding Bokeh visualizations with active Bokeh servers in a Flask app'

    vizes: BokehServerMapping = get_server_map()
    subprocess.Popen(['python3', 'run_bokeh_servers.py'])

    @app.route('/visualizations')
    def visualizations():
        return '\n'.join([viz for (_, viz) in vizes.values()])

    for port, (_, viz) in vizes.items():
        exec(APP_ROUTE_TEMPLATE.format(viz=viz.name.strip('.py'), port=port))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
