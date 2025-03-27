import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.prompt_generator import prompt_generator_bp
    from app.routes.drawing_analyzer import drawing_analyzer_bp
    from app.routes.document_search import document_search_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(prompt_generator_bp, url_prefix='/prompts')
    app.register_blueprint(drawing_analyzer_bp, url_prefix='/drawings')
    app.register_blueprint(document_search_bp, url_prefix='/document_search')
    
    return app 