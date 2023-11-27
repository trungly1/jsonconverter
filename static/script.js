// Add event listener to file input
const fileInput = document.getElementById('json_file');
fileInput.addEventListener('change', handleFileUpload);

// Toggle visibility of file input and text area based on user selection
const conversionType = document.getElementById('conversion_type');
conversionType.addEventListener('change', toggleInputFields);

function handleFileUpload() {
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const jsonInput = document.getElementById('json_input');
        jsonInput.value = e.target.result;
    };

    reader.readAsText(file);
}

function toggleInputFields() {
    const selectedOption = conversionType.value;
    const jsonFileInput = document.getElementById('json_file');
    const jsonInput = document.getElementById('json_input');

    if (selectedOption === 'xml') {
        jsonFileInput.style.display = 'block';
        jsonInput.style.display = 'none';
    } else if (selectedOption === 'csv') {
        jsonFileInput.style.display = 'none';
        jsonInput.style.display = 'block';
    }
}