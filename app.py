# Import required libraries
from flask import Flask, request, render_template, send_file
import json
import csv
import xml.etree.ElementTree as ET

# Initialize Flask app
app = Flask(__name__)

# Homepage to upload JSON file or provide JSON input
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle JSON input
@app.route('/convert', methods=['POST'])
def convert():
    json_data = request.files['json_file'] if 'json_file' in request.files else request.form.get('json_input')
    conversion_type = request.form.get('conversion_type')

    # Convert JSON to XML
    if conversion_type == 'xml':
        root = ET.Element("root")
        convert_json_to_xml(json.loads(json_data), root)
        xml_data = ET.tostring(root).decode('utf-8')

        return render_template('output.html', output=xml_data)

    # Convert JSON to CSV
    elif conversion_type == 'csv':
        csv_data = convert_json_to_csv(json.loads(json_data))

        return render_template('output.html', output=csv_data)

    return 'Invalid conversion type'

# Convert JSON to XML recursively
def convert_json_to_xml(json_data, parent):
    if isinstance(json_data, dict):
        for tag, value in json_data.items():
            element = ET.SubElement(parent, tag)
            convert_json_to_xml(value, element)
    elif isinstance(json_data, list):
        for item in json_data:
            element = ET.SubElement(parent, 'item')
            convert_json_to_xml(item, element)
    else:
        parent.text = str(json_data)

# Convert JSON to CSV
def convert_json_to_csv(json_data):
    output = ''
    keys = set()

    for item in json_data:
        keys.update(item.keys())

    writer = csv.DictWriter(output, fieldnames=keys)
    writer.writeheader()
    writer.writerows(json_data)

    return output

# Endpoint to download the converted file
@app.route('/download', methods=['POST'])
def download():
    output = request.form.get('output')
    conversion_type = request.form.get('conversion_type')

    if conversion_type == 'xml':
        filename = 'output.xml'
        response = send_file(output, as_attachment=True, attachment_filename=filename, mimetype='application/xml')
    elif conversion_type == 'csv':
        filename = 'output.csv'
        response = send_file(output, as_attachment=True, attachment_filename=filename, mimetype='text/csv')

    return response

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
