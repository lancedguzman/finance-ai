import cv2
import pytesseract
import numpy as np
import re
from PIL import Image
from datetime import datetime
import dateparser

# Point to your tesseract executable if on Windows (Adjust path as needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_receipt_data(image_file):
    """
    Reads an image file, preprocesses it, and extracts Date and Amount 
    based on GCash/BDO patterns.
    """
    # 1. Convert uploaded file to OpenCV format
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 2. Pre-processing (Grayscale + Thresholding)
    # This helps removing the blue background in GCash receipts
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 3. Extract Text
    text = pytesseract.image_to_string(thresh)
    
    # 4. Parsing Logic
    extracted_data = {
        'date': None,
        'amount': None,
        'merchant': None # Optional: Try to find merchant name
    }

    # --- REGEX PATTERNS based on your uploads ---
    
    # Amount Pattern: Looks for P, Php, PHP followed by digits and commas
    # Matches: "PHP 200.00", "P198.00"
    amount_pattern = r'(?:PHP|P|Php)\s?\.?\s*([\d,]+\.\d{2})'
    
    # Date Pattern: Looks for "Nov 13, 2025" or "Oct 22, 2025"
    date_pattern = r'([A-Z][a-z]{2}\s\d{1,2},?\s\d{4})'

    # Find Amount
    amounts = re.findall(amount_pattern, text, re.IGNORECASE)
    if amounts:
        # If multiple amounts found (e.g. Total + Fee), usually the largest or the last one is the total.
        # Clean commas: "1,000.00" -> 1000.00
        clean_amounts = [float(a.replace(',', '')) for a in amounts]
        extracted_data['amount'] = max(clean_amounts)

    # Find Date
    dates = re.search(date_pattern, text)
    if dates:
        date_str = dates.group(1)
        # Parse "Nov 13, 2025" to Python Date Object
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            extracted_data['date'] = parsed_date.strftime('%Y-%m-%d')

    return extracted_data
