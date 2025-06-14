import os
import json
from flask import Flask, request, jsonify 
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Setup
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Konfigurasi Gemini API
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # Menggunakan model 'gemini-1.5-pro-latest' yang stabil dan kuat
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def create_prompt():
    """
    Prompt yang disederhanakan: Fokus hanya pada analisis warna dan palet, 
    tanpa produk, untuk mempercepat respons AI secara signifikan.
    """
    return """
    You are an expert AI fashion stylist specializing in the 12-season color analysis system.
    Your task is to analyze the user's photo and determine which of the 12 seasons they belong to. 
    
    You MUST choose ONLY ONE season from the following list:
    - Light Spring, Warm Spring, Clear Spring
    - Light Summer, Cool Summer, Soft Summer
    - Deep Autumn, Warm Autumn, Soft Autumn
    - Deep Winter, Cool Winter, Clear Winter

    After choosing a season, provide a single, complete, and valid JSON object as your response. 
    Do not include any text outside this single JSON object.

    The JSON object must have the following structure:
    {
      "colorAnalysis": {
        "season": "The chosen season from the list above",
        "description": "Your detailed reasoning based on undertone, value, and chroma."
      },
      "recommendedColors": {
        "description": "A brief explanation of why these colors work for the chosen season.",
        "palette": [
            {"name": "Color Name 1", "hex": "#RRGGBB"},
            {"name": "Color Name 2", "hex": "#RRGGBB"},
            {"name": "Color Name 3", "hex": "#RRGGBB"},
            {"name": "Color Name 4", "hex": "#RRGGBB"},
            {"name": "Color Name 5", "hex": "#RRGGBB"},
            {"name": "Color Name 6", "hex": "#RRGGBB"},
            {"name": "Color Name 7", "hex": "#RRGGBB"},
            {"name": "Color Name 8", "hex": "#RRGGBB"},
            {"name": "Color Name 9", "hex": "#RRGGBB"},
            {"name": "Color Name 10", "hex": "#RRGGBB"},
            {"name": "Color Name 11", "hex": "#RRGGBB"},
            {"name": "Color Name 12", "hex": "#RRGGBB"}
        ]
      },
      "avoidColors": {
        "description": "A brief explanation of why these colors should be avoided.",
        "palette": [
            {"name": "Avoid Color 1", "hex": "#RRGGBB"},
            {"name": "Avoid Color 2", "hex": "#RRGGBB"},
            {"name": "Avoid Color 3", "hex": "#RRGGBB"},
            {"name": "Avoid Color 4", "hex": "#RRGGBB"},
            {"name": "Avoid Color 5", "hex": "#RRGGBB"},
            {"name": "Avoid Color 6", "hex": "#RRGGBB"},
            {"name": "Avoid Color 7", "hex": "#RRGGBB"},
            {"name": "Avoid Color 8", "hex": "#RRGGBB"},
            {"name": "Avoid Color 9", "hex": "#RRGGBB"},
            {"name": "Avoid Color 10", "hex": "#RRGGBB"},
            {"name": "Avoid Color 11", "hex": "#RRGGBB"},
            {"name": "Avoid Color 12", "hex": "#RRGGBB"},
        ]
      }
    }
    """

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if not model:
        return jsonify({"error": "Gemini API is not configured"}), 500
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    
    try:
        img = Image.open(image_file.stream)
    except Exception as e:
        return jsonify({"error": f"Invalid image file: {e}"}), 400
        
    prompt = create_prompt()

    try:
        # Panggilan non-streaming. Akan menunggu hingga semua respons selesai.
        response = model.generate_content([prompt, img])
        
        # Membersihkan dan mem-parsing respons JSON tunggal
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        result_data = json.loads(cleaned_text)
        
        return jsonify(result_data)

    except Exception as e:
        # Menangani error seperti timeout atau parsing yang gagal
        print(f"Error during AI call or JSON parsing: {e}")
        return jsonify({"error": f"An error occurred with the AI analysis: {e}"}), 500

if __name__ == '__main__':
    # Railway akan menyediakan variabel PORT. Jika tidak ada (saat di lokal), gunakan 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
