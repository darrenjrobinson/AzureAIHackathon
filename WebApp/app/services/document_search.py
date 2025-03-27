import os
import requests
from openai import AzureOpenAI

def search_documents(query, top=3, document_filter='All Documents'):
    """
    Search for documents in Azure AI Search
    
    Args:
        query (str): Search query
        top (int): Number of results to return
        document_filter (str): Type of document to filter by
        
    Returns:
        list: Search results
    """
    url = f"{os.environ.get('AZURE_SEARCH_SERVICE_ENDPOINT')}/indexes/{os.environ.get('AZURE_SEARCH_INDEX_NAME')}/docs/search?api-version=2023-11-01"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": os.environ.get("AZURE_SEARCH_API_KEY")
    }
    
    # Base payload
    payload = {
        "search": query,
        "queryType": "simple",
        "searchFields": "content, keyphrases, organizations, persons, locations",
        "select": "content, metadata_storage_name",
        "top": top
    }
    
    # Add filter if a specific document type is selected
    if document_filter != 'All Documents':
        # Using search.ismatchscoring for filtering documents
        if document_filter == 'White Card Manual':
            payload["filter"] = "search.ismatchscoring(metadata_storage_name, 'white_card', 'simple') or search.ismatchscoring(metadata_storage_name, 'Whitecard', 'simple')"
        elif document_filter == 'Owner Builder Guidelines':
            payload["filter"] = "search.ismatchscoring(metadata_storage_name, 'obcnsw', 'simple')"
        elif document_filter == 'Building Specifications':
            payload["filter"] = "search.ismatchscoring(metadata_storage_name, 'Building', 'simple') or search.ismatchscoring(metadata_storage_name, 'Specifications', 'simple')"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        results = response.json()
        return {
            "success": True,
            "results": results.get("value", [])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

def generate_response(system_instruction, user_query, context_text):
    """
    Generate response using Azure OpenAI
    
    Args:
        system_instruction (str): System instruction for the AI
        user_query (str): User's query
        context_text (str): Context information from documents
        
    Returns:
        str: Generated response
    """
    try:
        # Initialize OpenAI client with explicit API version
        client = AzureOpenAI(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",  # Explicitly set API version
            timeout=30.0  # Set timeout to 30 seconds
        )
        
        # Prepare messages with truncated context if too long
        max_context_length = 6000  # Adjust based on token limits
        if len(context_text) > max_context_length:
            context_text = context_text[:max_context_length] + "..."
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Here is my question: {user_query}\n\nHere is relevant information from construction documents: {context_text}"}
        ]
        
        # Get deployment name from environment or use default
        deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        
        # Make the API call with explicit parameters
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
            timeout=30.0,  # Set timeout to 30 seconds
            stream=False   # Ensure we're not using streaming
        )
        
        # Check if we got a valid response
        if not response or not response.choices or not response.choices[0].message:
            raise Exception("No valid response received from OpenAI")
        
        return {
            "success": True,
            "response": response.choices[0].message.content
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in generate_response: {str(e)}\n{error_details}")
        return {
            "success": False,
            "error": f"Error generating response: {str(e)}",
            "response": ""
        } 