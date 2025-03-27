from flask import Blueprint, render_template, request, jsonify
from app.services.prompt_generator import get_phases, get_tasks_for_phase, generate_prompts

prompt_generator_bp = Blueprint('prompt_generator', __name__)

@prompt_generator_bp.route('/')
def index():
    """Render the prompt generator interface"""
    phases = get_phases()
    return render_template('prompt_generator.html', phases=phases)

@prompt_generator_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get tasks for a specific phase"""
    phase_id = request.args.get('phase_id')
    if not phase_id:
        return jsonify({"error": "Phase ID is required"}), 400
    
    # Add debugging
    print(f"Getting tasks for phase: {phase_id}")
    
    tasks = get_tasks_for_phase(phase_id)
    
    # Add debugging
    print(f"Found {len(tasks)} tasks")
    
    return jsonify({"tasks": tasks})

@prompt_generator_bp.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate prompts"""
    try:
        data = request.get_json()
        
        # Debug the incoming request
        print("Received prompt generation request:", data)
        
        phase_id = data.get('phase_id')
        task_ids = data.get('task_ids', [])
        work_method = data.get('work_method', 'diy')
        
        if not phase_id or not task_ids:
            return jsonify({"error": "Phase ID and at least one task are required"}), 400
        
        prompts = generate_prompts(phase_id, task_ids, work_method)
        
        # Debug the generated prompts
        print(f"Generated prompts of length: {len(prompts)}")
        
        return jsonify({"prompts": prompts})
    
    except Exception as e:
        # Log the full exception
        import traceback
        print("Error generating prompts:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500 