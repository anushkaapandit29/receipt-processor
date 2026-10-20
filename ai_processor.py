import json
from google import genai
from google.genai import types
from PIL import Image

def extract_receipt_details(image_path, api_key):
    """Uses Google Gemini API to extract structured data from receipt images."""
    client = genai.Client(api_key=api_key)
    img = Image.open(image_path)

    prompt = """
    Analyze this receipt or invoice image carefully and extract the following details in raw JSON format:
    {
        "vendor": "Store/Company Name",
        "date": "YYYY-MM-DD",
        "total_amount": 0.00,
        "tax": 0.00,
        "items": "Item 1, Item 2, Item 3"
    }

    Rules:
    1. If date or tax is not visible, set them to "N/A" or 0.00.
    2. Ensure total_amount and tax are numeric float values (e.g. 150.50).
    3. Return ONLY valid JSON, without markdown formatting or extra text.
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[img, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None
