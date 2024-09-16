# Automation System

This project is an automation system for e-commerce product management. It includes tools for keyword search, SEO optimization, and product matching with Taobao.

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/automation-system.git
   cd automation-system
   ```
2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:

   ```
   pip install -e .
   ```

## Usage

After installation, you can use the following commands:

- `keyword_search`: Run the keyword search script
- `seo`: Run the SEO optimization script
- `tao`: Run the Taobao matching script
- `percenty`: Run the Percenty script
- `heyseller`: Run the Heyseller script
- `gui`: Launch the GUI application

## Configuration

Before running the scripts, make sure to set up your Google Sheets API credentials and place the JSON key file in the `C:\자동화시스템` directory. Also, create a `spreadsheet_url.txt` file in the same directory with your Google Sheets URL.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
