"""Flask app to display data, plots and descriptions as a website."""

from flask import Flask, request, abort, render_template, send_from_directory
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

MAPPING_HTML_JSON = {
    'zipf': 'all_words',
    'global-stats': 'all_years-clean',
    'yearly-stats': 'nouns_years-clean',
    'followed-words': 'followed_words'
}

@app.errorhandler(404)
def page_not_found(e):
    """Not found page"""

    return render_template('404.html'), 404

@app.route('/')
def home():
    """Home route"""

    return render_template('home.html')

@app.route('/<string:name>')
def data(name):
    """Data routes with name parameter"""

    if name.lower() in MAPPING_HTML_JSON:
        template = f"{name}.html"
        json = f'{MAPPING_HTML_JSON[name]}.json'
        return html_or_json(template, json)
    else:
        abort(404)

def html_or_json(template, json):
    """Helper function to return HTML or JSON based on the format parameter."""

    format_arg = request.args.get('format', default='html', type=str)
    if format_arg == 'json':
        return send_from_directory('data', json)

    return render_template(template)

# In production, mount the Flask app under a subpath for reverse proxying via nginx.
# This ensures all routes are served under /post-scriptum instead of /.
production = DispatcherMiddleware(None, {
    '/post-scriptum': app
})

# Run the Flask app directly for local development.
# This bypasses DispatcherMiddleware and serves the app on port 3000.
# Use only for debugging; production uses gunicorn with DispatcherMiddleware.
if __name__ == '__main__':
    app.run(port=3000, debug=True)
