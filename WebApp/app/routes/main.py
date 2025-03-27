from flask import Blueprint, render_template, jsonify, request, session
from app.services.drawing_analyzer import analyze_construction_drawing
import logging
import traceback
from openai import AzureOpenAI
import os
import time

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/drawings/analyze', methods=['POST'])
def analyze_drawing():
    """Handle drawing analysis request"""
    try:
        logger.info("Received drawing analysis request")
        logger.debug(f"Files in request: {request.files}")
        logger.debug(f"Form data: {request.form}")
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
            
        file = request.files['file']
        logger.info(f"Received file: {file.filename}")
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
            
        # Get file type from filename
        file_type = file.filename.rsplit('.', 1)[1].lower()
        logger.info(f"File type: {file_type}")
        
        # Read file data
        file_data = file.read()
        logger.info(f"File size: {len(file_data)} bytes")
        
        # Analyze drawing
        result = analyze_construction_drawing(file_data, file_type)
        
        if result.get('success'):
            logger.info("Analysis completed successfully")
        else:
            logger.error(f"Analysis failed: {result.get('error')}")
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_drawing: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/analyze-page-detail', methods=['POST'])
def analyze_page_detail():
    """Handle detailed page analysis request using OpenAI"""
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received in request")
            return jsonify({'success': False, 'error': 'No data provided'})
            
        page_number = data.get('page_number')
        description = data.get('description', '').strip()
        tags = data.get('tags', '').strip()
        
        logger.debug(f"Analyzing page {page_number}")
        logger.debug(f"Description: {description}")
        logger.debug(f"Tags: {tags}")
        
        # Create a prompt for OpenAI
        prompt = f"""Analyze the following construction drawing page details:

Page Number: {page_number}
Description: {description}
Detected Elements: {tags}

Please provide a detailed analysis including:
1. Key Construction Elements:
   - Identify and explain the significance of major structural components
   - Note any specific materials or dimensions mentioned
   - Highlight critical design features

2. Technical Specifications:
   - List any measurements, dimensions, or specifications
   - Note material requirements and standards
   - Identify any technical annotations or symbols

3. Construction Considerations:
   - Provide recommendations for implementation
   - Note any special installation requirements
   - Highlight potential construction challenges

4. Compliance and Safety:
   - Identify relevant building code considerations
   - Note any safety requirements or precautions
   - Highlight compliance-related specifications
"""
        
        # Initialize OpenAI client
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        # Get analysis from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a construction and architectural expert analyzing drawing details. Provide clear, structured analysis focusing on practical implementation details and technical specifications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        logger.debug(f"Generated analysis: {analysis[:200]}...")  # Log first 200 chars
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_page_detail: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/search')
def document_search():
    return render_template('document_search.html') 