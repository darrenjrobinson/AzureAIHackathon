import os
import io
import base64
import requests
import tempfile
from PIL import Image
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from pdf2image import convert_from_bytes, convert_from_path
import logging
import traceback
import time
import re
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def analyze_construction_drawing(file_data, file_type):
    """
    Analyze a construction drawing using Azure Computer Vision 4.0
    """
    try:
        logger.info(f"Starting analysis of {file_type} file")
        
        vision_base_url = os.environ.get('AZURE_VISION_ENDPOINT', '').rstrip('/')
        
        # Updated to correct 4.0 API endpoint format with computervision path
        analyze_url = f"{vision_base_url}/computervision/imageanalysis:analyze"
        
        vision_headers = {
            "Ocp-Apim-Subscription-Key": os.environ.get("AZURE_VISION_KEY"),
            "Content-Type": "application/octet-stream"
        }

        # Updated parameters to use only supported features
        vision_params = {
            "api-version": "2023-04-01-preview",
            "features": "objects,read,tags",
            "language": "en"
        }

        if file_type == 'pdf':
            logger.info("Processing PDF file")
            try:
                images = convert_from_bytes(file_data, dpi=150)
                logger.info(f"Successfully converted PDF to {len(images)} images")
                
                all_results = []
                for i, image in enumerate(images):
                    logger.info(f"Processing page {i+1}")
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='JPEG', quality=85)
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    page_results = analyze_single_drawing(
                        img_byte_arr, 
                        analyze_url,
                        vision_headers, 
                        vision_params
                    )
                    all_results.append({
                        'page': i + 1,
                        'analysis': page_results
                    })
                
                return {
                    'success': True,
                    'type': 'pdf',
                    'pageCount': len(images),
                    'pages': all_results
                }
                
            except Exception as pdf_error:
                logger.error(f"PDF processing error: {str(pdf_error)}")
                raise Exception(f"PDF processing failed: {str(pdf_error)}")
        else:
            logger.info(f"Processing single {file_type} image")
            results = analyze_single_drawing(
                file_data, 
                analyze_url,
                vision_headers, 
                vision_params
            )
            return {
                'success': True,
                'type': 'image',
                'analysis': results
            }
    except Exception as e:
        logger.error(f"Drawing analysis failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def analyze_single_drawing(image_data: bytes, analyze_url: str, headers: Dict, params: Dict) -> Dict:
    """
    Analyze a single drawing image using Azure Vision API 4.0.
    
    Args:
        image_data: The image data in bytes
        analyze_url: The Azure Vision API endpoint URL
        headers: Request headers including API key
        params: Request parameters including API version and features
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Process image size before analysis
        image_data = process_image_size(image_data)
        
        # Log request details for debugging
        logger.debug(f"Making request to: {analyze_url}")
        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request params: {params}")
        logger.debug(f"Request data size: {len(image_data)} bytes")
        
        # Send request to Azure Vision API 4.0
        response = requests.post(
            analyze_url,
            headers=headers,
            params=params,
            data=image_data
        )
        
        # Log response details for debugging
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        if response.status_code != 200:
            logger.debug(f"Response content: {response.text}")
        
        response.raise_for_status()
        results = response.json()
        
        # Extract construction-specific information with default values
        formatted_results = {
            'caption': {
                'text': 'No caption available',
                'confidence': 0
            },
            'construction_elements': extract_construction_elements(results),
            'measurements': extract_measurements(results),
            'technical_details': extract_technical_details(results),
            'spatial_analysis': analyze_spatial_relationships(results),
            'annotations': extract_annotations(results),
            'metadata': results.get('metadata', {}),
            'description': {
                'text': results.get('readResult', {}).get('content', ''),
                'confidence': 0
            },
            'tags': [{'name': tag.get('name', ''), 'confidence': tag.get('confidence', 0)} 
                   for tag in results.get('tagsResult', {}).get('values', [])],
            'objects': [{'name': obj.get('name', ''), 'confidence': obj.get('confidence', 0)} 
                      for obj in results.get('objectsResult', {}).get('values', [])]
        }
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error in analyze_single_drawing: {str(e)}")
        logger.error(traceback.format_exc())
        raise Exception(f"Image analysis failed: {str(e)}")

def process_image_size(image_data: bytes, max_dimension: int = 2048) -> bytes:
    """
    Process image size to ensure it's within Azure Vision API limits.
    Resizes the image if it exceeds the maximum dimension while maintaining aspect ratio.
    
    Args:
        image_data: The image data in bytes
        max_dimension: Maximum allowed dimension (width or height)
        
    Returns:
        Processed image data in bytes
    """
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Get current dimensions
        width, height = image.size
        
        # Check if resizing is needed
        if width > max_dimension or height > max_dimension:
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(max_dimension / width, max_dimension / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or 'JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return img_byte_arr
            
        return image_data
        
    except Exception as e:
        logger.error(f"Error processing image size: {str(e)}")
        return image_data

def extract_annotations(results):
    """Extract all annotations from the API response"""
    annotations = {
        'labels': [],
        'objects': [],
        'text': [],
        'lines': []
    }
    
    # Extract labels
    for label in results.get('tagsResult', {}).get('values', []):
        annotations['labels'].append({
            'name': label['name'],
            'confidence': label['confidence']
        })
    
    # Extract objects
    for obj in results.get('objectsResult', {}).get('values', []):
        annotations['objects'].append({
            'name': obj['name'],
            'confidence': obj['confidence'],
            'bounds': obj.get('boundingBox', {})
        })
    
    # Extract text
    for text in results.get('readResult', {}).get('blocks', []):
        for line in text.get('lines', []):
            annotations['text'].append({
                'text': line.get('text', ''),
                'confidence': line.get('confidence', 0),
                'bounds': line.get('boundingBox', {})
            })
    
    return annotations

def extract_construction_elements(results):
    """Extract construction-specific elements using object detection"""
    elements = []
    
    # Process objects
    for obj in results.get('objectsResult', {}).get('values', []):
        if is_construction_element(obj['name']):
            elements.append({
                'type': 'object',
                'name': obj['name'],
                'confidence': obj['confidence'],
                'bounds': obj.get('boundingBox', {}),
                'category': categorize_element(obj['name'])
            })
    
    return elements

def extract_technical_details(results):
    """Extract technical information from text"""
    details = {
        'text_annotations': [],
        'detected_lines': [],
        'symbols': []
    }
    
    # Process text (OCR results)
    for text in results.get('readResult', {}).get('blocks', []):
        for line in text.get('lines', []):
            content = line.get('text', '')
            if is_technical_content(content):
                details['text_annotations'].append({
                    'text': content,
                    'confidence': line.get('confidence', 0),
                    'bounds': line.get('boundingBox', {}),
                    'type': classify_technical_text(content)
                })
    
    return details

def analyze_spatial_relationships(results):
    """Analyze spatial relationships between detected elements"""
    relationships = []
    
    # Use polygon detection for room layouts
    polygons = results.get('polygonsResult', {}).get('values', [])
    
    # Analyze polygon relationships
    for poly in polygons:
        relationships.append({
            'type': 'space',
            'area': calculate_area(poly['boundingBox']),
            'adjacent_elements': find_adjacent_elements(poly, results),
            'bounds': poly['boundingBox']
        })
    
    return relationships

def extract_measurements(results):
    """Extract measurements and dimensions"""
    measurements = []
    
    # Process text for measurement patterns
    for text in results.get('textResult', {}).get('blocks', []):
        for line in text.get('lines', []):
            content = line.get('text', '')
            extracted = extract_measurement_values(content)
            if extracted:
                measurements.append({
                    'value': extracted['value'],
                    'unit': extracted['unit'],
                    'confidence': line.get('confidence', 0),
                    'location': line.get('boundingBox'),
                    'type': 'dimension'
                })
    
    return measurements

# Helper functions
def is_construction_element(name):
    """Check if detected object is a construction element"""
    construction_terms = {
        'wall', 'door', 'window', 'beam', 'column', 'stairs',
        'floor', 'ceiling', 'roof', 'pipe', 'duct', 'outlet'
    }
    return name.lower() in construction_terms

def categorize_element(name):
    """Categorize construction elements"""
    categories = {
        'structural': {'wall', 'beam', 'column', 'foundation'},
        'architectural': {'door', 'window', 'stairs'},
        'mechanical': {'duct', 'pipe', 'outlet'},
        'finish': {'floor', 'ceiling', 'roof'}
    }
    
    name = name.lower()
    for category, elements in categories.items():
        if name in elements:
            return category
    return 'other'

def extract_measurement_values(text):
    """Extract measurement values and units"""
    # Common measurement patterns in construction drawings
    patterns = {
        'imperial': r'(\d+(?:-\d+)?(?:\s*\d+/\d+)?)\s*((?:ft|\'|inch|\"|\'))',
        'metric': r'(\d+(?:\.\d+)?)\s*(mm|cm|m)',
        'angle': r'(\d+(?:\.\d+)?)\s*(deg|°)',
        'area': r'(\d+(?:\.\d+)?)\s*(sq\.?\s*(?:ft|m))',
    }
    
    for measure_type, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return {
                'value': match.group(1),
                'unit': match.group(2),
                'type': measure_type
            }
    return None

def generate_audio_description(text, output_path):
    """
    Convert text description to audio using Azure Speech Services
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the audio file
    
    Returns:
        bool: Success status
    """
    try:
        # Configure Azure Speech Services
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get("AZURE_VISION_KEY"), 
            region="eastus"
        )
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
        
        # Output audio file
        audio_output = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_output
        )
        
        # Synthesize speech
        result = speech_synthesizer.speak_text_async(text).get()
        
        return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted
    
    except Exception:
        return False 