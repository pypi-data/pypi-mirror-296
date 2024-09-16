# LeanHTML

`leanhtml` is a Python library designed to significantly reduce HTML file sizes, making them up to 5x smaller. This helps in optimizing the delivery of static or pre-rendered HTML content by reducing server network bandwidth load.

## Installation

You can install the `leanhtml` library using pip:

```bash
pip install leanhtml
```

## Use Case
`leanhtml` is particularly useful for scenarios where you need to minimize the size of pre-rendered or static HTML files. By reducing the size of these files, you can decrease the bandwidth usage on your server and improve loading times for users.

## How It Works
1. `Minification:` The library first minifies the HTML content to remove unnecessary whitespace and reduce file size.
2. `Compression:` It then compresses the minified HTML using gzip to further reduce its size.
3. `Template Usage:` The compressed HTML content is embedded into an HTML template (templates/lean.html). This template includes JavaScript that decompresses the content on the client side, rendering the original HTML.

## Example Use

Here’s how you can use the compress_html function to process an HTML file:

```python
from leanhtml import compress_html

# Compress an HTML file
compressed_html = compress_html('path/to/your/file.html')
```

In this example, `compress_html` reads the HTML file specified by file_path, minifies and compresses it, and returns a string containing the HTML with embedded compressed content.
The resulting string can be used for further processing or written to a HTML file.

## Template Customization
The library uses an HTML template named `lean.html` located in the leanhtml/templates directory. You can customize this template to fit your specific requirements for handling compressed content on the client side.