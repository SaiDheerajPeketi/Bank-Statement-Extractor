# Bank Statement Extractor

A Python-based tool that extracts and processes bank statements from PDF files into structured Excel format. This project supports multiple bank statement formats and provides both a Jupyter notebook interface and a Streamlit web application for ease of use.

## Features

- **PDF bank statement data extraction** using Camelot
- **Support for multiple bank statement formats**
- **Automatic table detection** and processing
- **Excel output** with formatted columns
- **Password-protected PDF support**
- **Web interface** using Streamlit
- **Opening and closing balance detection**
- **Custom date validation and formatting**

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SaiDheerajPeketi/Bank-Statement-Extractor
    cd Bank-Statement-Extractor
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

   Note: This project requires Python 3.6 or higher.

## Dependencies

- **pdf2image** - For PDF to image conversion
- **pytesseract** - For OCR capabilities
- **pillow** - For image processing
- **pandas** - For data manipulation
- **camelot-py** - For PDF table extraction
- **opencv-contrib-python** - For image processing
- **openpyxl** - For Excel file handling
- **streamlit** - For web interface
- **PyPDF2** - For PDF manipulation

## Usage

### Using the Streamlit Web Interface

1. Start the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to the provided local URL.
3. Upload your PDF bank statement.
4. Select your bank from the dropdown menu.
5. Enter the PDF password if applicable.
6. Click **Process** to extract the data.
7. The processed data will be displayed and can be downloaded as an Excel file.

### Using the Jupyter Notebook

1. Open `main.ipynb` in Jupyter Notebook or JupyterLab.
2. Update the variables in the second cell:
    ```python
    pdf_file_name = 'your_statement.pdf'
    excel_file_name = 'output.xlsx'
    bank_name = 'Bank1'  # or 'Bank2'
    ```
3. Run the cells to process your PDF and generate Excel output.

## Supported Banks

The processor currently supports two bank statement formats:

### Bank 1
- Uses stream-based table extraction.
- Supports specific user name validation.
- Handles multi-line transactions.
- Processes 6 or 7 column formats.

### Bank 2
- Uses lattice-based table extraction.
- Includes opening and closing balance extraction.
- Supports standard transaction formats.
- Handles multiple pages.

## File Structure

```
Bank-Statement-Extractor/
├── app.py                 # Streamlit web application
├── main.ipynb             # Jupyter notebook implementation
├── preprocessor.py        # Core processing functions
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Processing Logic

The processor performs the following steps:
1. Reads the PDF file using Camelot.
2. Detects and extracts tables.
3. Validates date formats.
4. Processes multi-line transactions.
5. Extracts opening and closing balances.
6. Converts numerical values.
7. Formats the output in Excel.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided as-is without any warranty. Please verify the extracted data matches your bank statements before using it for any purpose.

## Support

For issues and feature requests, please create an issue in the GitHub repository.

