import pkg_resources
from htmlmin import minify
import gzip
import base64
from flask import Flask, render_template_string

app = Flask(__name__)

def get_template(template_name):
    """Load a template from the package."""
    resource_path = pkg_resources.resource_filename(__name__, f'templates/{template_name}')
    with open(resource_path, 'r', encoding='utf-8') as template_file:
        return template_file.read()

def compress_html(file_path):
    """Process an HTML file: minify, gzip, and base64 encode it."""
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Minify the HTML content
    minified_html = minify(html_content, remove_empty_space=True)
    
    # Compress the minified HTML content using gzip
    compressed_content = gzip.compress(minified_html.encode())

    # Convert compressed content to base64 encoding
    compressed_content_base64 = base64.b64encode(compressed_content).decode()

    # Render the lean.html template with embedded compressed content
    template_content = get_template('lean.html')
    with app.app_context():
        with app.test_request_context():
            lean_html = render_template_string(template_content, compressed_content=compressed_content_base64)

    return lean_html
