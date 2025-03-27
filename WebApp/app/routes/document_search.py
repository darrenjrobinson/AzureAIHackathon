import os
from flask import Blueprint, render_template, request, jsonify
from app.services.document_search import search_documents, generate_response

document_search_bp = Blueprint('document_search', __name__)

# Default system instruction
DEFAULT_SYSTEM_INSTRUCTION = """
You are a knowledgeable assistant for Owner Builders who are managing construction projects. 
Your goal is to provide accurate, helpful information based on construction manuals, 
building specifications, and safety guides. When responding:

1. Draw on the information from the construction documents to ensure accuracy
2. Provide practical advice that follows Australian building standards
3. Include specific references to relevant sections of building codes where applicable
4. Identify and state if the task can only be completed by a skilled an licensed tradesperson
5. List an specific items from the developement application approval conditions that need to be met
6. Ensure that inspections are performed by council or a private certifier at each phase of the build
7. Format your responses clearly with headings, bullet points, and sections as needed
8. If you're uncertain about any information, acknowledge the limitations of your knowledge
9. When providing templates or examples, make them comprehensive and ready to use

Focus on being helpful to an Owner Builder who is managing their construction project themselves.

When it is specified that the work will be done myself for any construction task, generate a comprehensive safety protocol by:

1. Identifying the specific hazards associated with the selected task
2. Listing required personal protective equipment (PPE)
3. Outlining safety precautions before, during, and after the work
4. Providing emergency response guidance for potential accidents
5. Including relevant regulatory compliance information

Format the safety protocol as a practical, actionable checklist that can be printed or saved.
"""

@document_search_bp.route('/')
def index():
    """Render the document search interface"""
    return render_template('document_search.html', default_instruction=DEFAULT_SYSTEM_INSTRUCTION)

@document_search_bp.route('/search', methods=['POST'])
def search():
    """API endpoint to search documents"""
    try:
        data = request.get_json()
        query = data.get('query')
        result_count = data.get('result_count', 3)
        document_filter = data.get('document_filter', 'All Documents')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        search_results = search_documents(query, result_count, document_filter)
        
        if not search_results.get('success', False):
            return jsonify({"error": search_results.get('error', 'Search failed')}), 500
        
        return jsonify({"results": search_results.get('results', [])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@document_search_bp.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate responses"""
    try:
        data = request.get_json()
        query = data.get('query')
        system_instruction = data.get('system_instruction', DEFAULT_SYSTEM_INSTRUCTION)
        selected_docs = data.get('selected_docs', [])
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not selected_docs:
            return jsonify({"error": "At least one document must be selected"}), 400
        
        # Prepare context from selected documents
        context_text = ""
        for doc in selected_docs:
            doc_name = doc.get("metadata_storage_name", "Unknown")
            content = doc.get("content", "")
            # Limit content length to avoid token limits
            if len(content) > 2000:
                content = content[:2000] + "..."
            
            context_text += f"--- Document: {doc_name} ---\n{content}\n\n"
        
        # Generate response
        response_data = generate_response(system_instruction, query, context_text)
        
        if not response_data.get('success', False):
            return jsonify({"error": response_data.get('error', 'Response generation failed')}), 500
        
        return jsonify({"response": response_data.get('response', '')})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 