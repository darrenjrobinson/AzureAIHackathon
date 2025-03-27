import os
import uuid
import tempfile
from flask import Blueprint, render_template, request, jsonify, send_file
from app.services.drawing_analyzer import analyze_construction_drawing, generate_audio_description

drawing_analyzer_bp = Blueprint('drawing_analyzer', __name__)

# Ensure temporary directories exist
os.makedirs('temp_audio', exist_ok=True)
os.makedirs('temp_drawings', exist_ok=True)

@drawing_analyzer_bp.route('/')
def index():
    """Render the drawing analyzer interface"""
    return render_template('drawing_analyzer.html')

@drawing_analyzer_bp.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze construction drawings"""
    if 'drawing' not in request.files:
        return jsonify({"error": "No drawing file uploaded"}), 400
    
    file = request.files['drawing']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Get file extension
        ext = os.path.splitext(file.filename)[1].lower()
        
        # Read file data
        file_data = file.read()
        
        # Determine file type based on extension
        if ext == '.pdf':
            file_type = 'pdf'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            file_type = 'image'
        else:
            return jsonify({"error": "Unsupported file format. Please upload a PDF or image file (JPG, PNG, GIF)."}), 400
        
        # Analyze the drawing
        results = analyze_construction_drawing(file_data, file_type)
        
        if not results.get('success', False):
            return jsonify({"error": results.get('error', 'Analysis failed')}), 500
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@drawing_analyzer_bp.route('/generate-audio', methods=['POST'])
def generate_audio():
    """API endpoint to generate audio description"""
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate unique filename
        filename = f"audio_{uuid.uuid4()}.wav"
        output_path = os.path.join('temp_audio', filename)
        
        # Generate audio
        success = generate_audio_description(text, output_path)
        
        if not success:
            return jsonify({"error": "Failed to generate audio"}), 500
        
        return jsonify({"success": True, "filename": filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@drawing_analyzer_bp.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """Serve generated audio files"""
    try:
        filepath = os.path.join('temp_audio', filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 404 