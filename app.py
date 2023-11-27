# Flask application
import io
import json
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template, jsonify, make_response
import pandas as pd

# Create a Flask app instance
app = Flask(__name__)

# Route for rendering the index.html page
@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Route for converting JSON to XML or CSV
@app.route('/convert', methods=['POST'])
def convert():
    """
    Endpoint to handle JSON input and convert it to XML or CSV.
    """
    json_data = request.files.get('json_file') or request.form.get('json_input')
    
    if not json_data:
        return jsonify({'error': 'No JSON input provided'}), 400

    try:
        json_object = json.loads(json_data)
    except json.decoder.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON input'}), 400

    conversion_type = request.form.get('conversion_type')

    if conversion_type == 'xml':
        xml_data = convert_json_to_xml(json_object)
        return jsonify({'output': xml_data})

    elif conversion_type == 'csv':
        csv_data = convert_json_to_csv(json_object)
        return jsonify({'output': csv_data})

    return jsonify({'error': 'Invalid conversion type'}), 400

# Function to convert JSON to XML
def convert_json_to_xml(json_data):
    """
    Convert JSON to XML recursively.
    """
    root = ET.Element("root")
    convert_json_to_xml_recursive(json_data, root)
    xml_data = ET.tostring(root).decode('utf-8')
    return xml_data

# Recursive helper function for converting JSON to XML
def convert_json_to_xml_recursive(json_data, parent):
    """
    Recursive helper function for converting JSON to XML.
    """
    if isinstance(json_data, dict):
        for tag, value in json_data.items():
            element = ET.SubElement(parent, tag)
            convert_json_to_xml_recursive(value, element)
    elif isinstance(json_data, list):
        for item in json_data:
            element = ET.SubElement(parent, "item")
            convert_json_to_xml_recursive(item, element)

# Function to convert JSON to CSV
def convert_json_to_csv(json_data):
    """
    Convert JSON to CSV.
    """
    df = pd.json_normalize(json_data)
    csv_data = df.to_csv(index=False)
    return csv_data

if __name__ == '__main__':
    app.run()(debug=True)