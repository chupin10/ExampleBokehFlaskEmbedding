import subprocess

from bokeh.embed import server_document

from flask import Flask, render_template

from visualizations.utils import BokehServerMapping, get_server_map


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Example of embedding Bokeh visualizations with active Bokeh servers in a Flask app'

    vizes: BokehServerMapping = get_server_map()
    viznames_to_server = {str(k.name.strip('.py')): k for (k, v) in vizes.items()}
    subprocess.Popen(['python3', 'run_bokeh_servers.py'])

    @app.route('/visualizations/<viz>')
    def visualizations(viz: str):
        app_path = viznames_to_server.get(viz, None)
        if app_path is None:
            return f'No visual found by name: {viz}'
        port = vizes[app_path][1]
        script = server_document(f'http://127.0.0.1:{port}/{viz}')  # bokeh import
        return render_template('bokeh.html', bokS=script)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
