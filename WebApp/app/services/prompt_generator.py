# Data structure for phases, tasks and prompt templates
project_phases = [
    {'id': 'planning', 'name': 'Planning & Approval'},
    {'id': 'demolition', 'name': 'Demolition'},
    {'id': 'sitePreperation', 'name': 'Site Preparation'},
    {'id': 'foundations', 'name': 'Foundations & Slab'},
    {'id': 'framing', 'name': 'Framing & Structure'},
    {'id': 'lockup', 'name': 'Construction to Lockup'},
    {'id': 'fitout', 'name': 'Interior Fit-out'},
    {'id': 'completion', 'name': 'Completion & Sign-off'},
]

tasks_by_phase = {
    'planning': [
        {'id': 'plans', 'name': 'Reading Plans & Specifications'},
        {'id': 'approvals', 'name': 'Council Approvals & Permits'},
        {'id': 'costing', 'name': 'Budgeting & Cost Estimation'},
        {'id': 'scheduling', 'name': 'Creating a Project Schedule'},
        {'id': 'hiring', 'name': 'Finding Contractors & Quotes'},
        {'id': 'safetyPlan', 'name': 'Site Safety Planning'},
    ],
    'demolition': [
        {'id': 'prepDemo', 'name': 'Preparing for Demolition'},
        {'id': 'utilities', 'name': 'Disconnecting Utilities'},
        {'id': 'asbestos', 'name': 'Asbestos Removal'},
        {'id': 'structure', 'name': 'Structure Demolition'},
        {'id': 'waste', 'name': 'Waste Management & Recycling'},
    ],
    'sitePreperation': [
        {'id': 'clearing', 'name': 'Site Clearing & Leveling'},
        {'id': 'excavation', 'name': 'Excavation Work'},
        {'id': 'services', 'name': 'Service Connections (Water, Sewer, Power)'},
        {'id': 'drainage', 'name': 'Drainage Systems'},
        {'id': 'access', 'name': 'Site Access & Security'},
    ],
    'foundations': [
        {'id': 'footings', 'name': 'Footings Construction'},
        {'id': 'slab', 'name': 'Slab Preparation & Pouring'},
        {'id': 'waterproofing', 'name': 'Foundation Waterproofing'},
        {'id': 'insulation', 'name': 'Underfloor Insulation'},
        {'id': 'inspection', 'name': 'Foundation Inspection'},
    ],
    'framing': [
        {'id': 'wallFraming', 'name': 'Wall Framing'},
        {'id': 'roofFraming', 'name': 'Roof Framing'},
        {'id': 'trusses', 'name': 'Trusses Installation'},
        {'id': 'bracing', 'name': 'Structural Bracing'},
        {'id': 'windows', 'name': 'Rough Window & Door Openings'},
    ],
    'lockup': [
        {'id': 'roofing', 'name': 'Roof Installation'},
        {'id': 'cladding', 'name': 'External Cladding/Brickwork'},
        {'id': 'windowsInstall', 'name': 'Windows & External Doors Installation'},
        {'id': 'flashings', 'name': 'Flashings & Weatherproofing'},
        {'id': 'roughIn', 'name': 'Plumbing & Electrical Rough-in'},
    ],
    'fitout': [
        {'id': 'insulation', 'name': 'Insulation Installation'},
        {'id': 'plasterboard', 'name': 'Plasterboard/Drywall'},
        {'id': 'internalDoors', 'name': 'Internal Doors & Trim'},
        {'id': 'flooring', 'name': 'Flooring Installation'},
        {'id': 'kitchen', 'name': 'Kitchen Installation'},
        {'id': 'bathroom', 'name': 'Bathroom Fit-out'},
        {'id': 'painting', 'name': 'Painting & Finishing'},
        {'id': 'fixtures', 'name': 'Fixtures & Fittings'},
    ],
    'completion': [
        {'id': 'finalElectrical', 'name': 'Final Electrical & Plumbing'},
        {'id': 'cleanup', 'name': 'Final Cleanup'},
        {'id': 'inspection', 'name': 'Final Inspections'},
        {'id': 'certification', 'name': 'Obtaining Occupation Certificate'},
        {'id': 'defects', 'name': 'Defect Identification & Rectification'},
        {'id': 'documentation', 'name': 'Project Documentation & Handover'},
    ],
}

# DIY Prompts
diy_prompt_templates = {
    'planning': {
        'plans': "As an owner builder, I need help understanding how to read and interpret my building plans and specifications. What are the key things I should look for in the drawings, and how do I ensure I'm correctly understanding the construction requirements?",
        'approvals': "I'm preparing my council approval application as an owner builder. What documents do I need to submit, what's the typical process, and what common issues should I watch out for?",
        'costing': "I need to create a detailed budget for my owner builder project. How do I estimate costs accurately for materials, labor, and unexpected expenses? Are there standard percentages I should allocate for different aspects of the build?",
        'scheduling': "How do I create a realistic timeline for my owner builder project? What's the typical sequence of construction tasks, and how do I account for dependencies between different trades?",
        'hiring': "I need to find reliable contractors for my owner builder project. What questions should I ask, what should be in the contract, and how do I verify their credentials and insurance?",
        'safetyPlan': "As an owner builder, what safety requirements am I legally responsible for? How do I create a site safety plan and what documentation do I need to maintain throughout the project?",
    },
    'demolition': {
        'prepDemo': "I'm about to start demolition work myself on my owner builder project. What preparations should I make, what permits do I need, and what safety precautions should I take? What tools and equipment will I need?",
        'utilities': "I need to disconnect utilities before demolition. What's the process for electricity, gas, water, and sewage disconnection, and who needs to be notified? Which parts can I do myself and which require licensed professionals?",
        'asbestos': "I suspect there might be asbestos in the building I'm demolishing as an owner builder. What are the legal requirements for testing and removal, and can I do any of this work myself? What safety gear would I need?",
        'structure': "I'll be doing some structural demolition myself. What's the correct sequence, what tools will I need, and how do I ensure the remaining structure stays safe and stable throughout the process?",
        'waste': "I'll be managing the waste removal from my demolition myself. How should I sort different materials, what can be recycled, and what are the disposal requirements for different types of construction waste?",
    },
    'sitePreperation': {
        'clearing': "I'm planning to clear and level my site myself. What equipment will I need to hire or buy, what's the process, and what environmental considerations should I be aware of?",
        'excavation': "I need to do excavation work myself for my foundations. What safety precautions should I take, how do I determine the correct depth, what equipment will I need, and how do I operate it safely?",
        'services': "I want to arrange for service connections (water, sewer, power) to my site. What parts of this can I do myself versus requiring professionals? What's the process, who do I contact, and what are the typical costs?",
        'drainage': "I'm installing drainage systems myself. How do I plan the system, what materials do I need, what tools are required, and how do I ensure water flows away from the building?",
        'access': "I need to set up site access and security. What are the best types of temporary fencing, gates, and security measures I can install myself to prevent theft and vandalism during construction?",
    },
    'foundations': {
        'footings': "I'm planning to construct footings myself. What's the process, what tools and materials will I need, how do soil types affect my design, and what are the critical steps to ensure they pass inspection?",
        'slab': "I want to prepare and pour my concrete slab myself. What steps are involved, what reinforcement do I need, what tools will I need, and what weather conditions should I avoid?",
        'waterproofing': "I need to waterproof my foundation myself. What materials should I use, what's the application process, what tools will I need, and what are the critical areas that need special attention?",
        'insulation': "I'm installing underfloor insulation myself. What are the best materials to use, what tools will I need, what's the installation method, and what R-values should I aim for?",
        'inspection': "I have a foundation inspection coming up. What will the inspector be looking for, what documentation should I have ready, and what are common issues that cause inspection failures?",
    },
    'framing': {
        'wallFraming': "I'll be doing my own wall framing. What tools and materials do I need, what's the step-by-step process, how do I ensure walls are square and plumb, and what are common mistakes to avoid?",
        'roofFraming': "I'm planning to do my own roof framing. What are the different methods I could use, what tools will I need, how do I calculate loads, and what safety precautions should I take while working at height?",
        'trusses': "I'm planning to install roof trusses myself. What equipment will I need, what's the safe installation method, how many people will be required, and what preparation do I need before delivery?",
        'bracing': "I need to add structural bracing to my framing. What types of bracing are needed, where should they be placed, what materials and fasteners should I use, and how do I comply with building codes?",
        'windows': "I'm framing rough openings for windows and doors. What are the step-by-step instructions, how much allowance should I add to the actual window dimensions, and what headers do I need to install?",
    },
    'lockup': {
        'roofing': "I'm planning to install my roof myself. What materials should I consider, what tools will I need, what's the installation process, and what safety precautions should I take for working at height?",
        'cladding': "I want to install external cladding myself. What types would be easiest for a DIY owner builder, what tools will I need, what's the installation process, and what weatherproofing details are critical?",
        'windowsInstall': "I'll be installing windows and external doors myself. What's the step-by-step procedure, what tools will I need, how do I ensure they're weathertight, and what flashing details are crucial?",
        'flashings': "I need to install flashings myself. What types of flashings do I need for different areas, what materials should I use, what tools will I need, and what are the correct installation methods?",
        'roughIn': "I'm considering doing some of the plumbing and electrical rough-in myself. What parts can I legally do, what requires licensed professionals, and how do I prepare for inspections?",
    },
    'fitout': {
        'insulation': "I'm planning to install insulation myself. What materials should I use for walls and ceiling, what tools will I need, what safety gear is required, and what's the correct installation method?",
        'plasterboard': "I'll be installing plasterboard/drywall myself. What tools and materials will I need, what's the step-by-step process, and how do I achieve a professional finish with the jointing and sanding?",
        'internalDoors': "I want to install internal doors and trim myself. What tools will I need, what's the step-by-step process, and how do I ensure doors hang straight and operate smoothly?",
        'flooring': "I'm planning to install flooring myself. What types would be most suitable for a DIY installation, what tools and materials will I need, and what's the installation process for each type?",
        'kitchen': "I want to install my kitchen myself. What's the correct sequence, what tools will I need, what measurements are critical, and how do I connect plumbing and electrical components?",
        'bathroom': "I'm doing my own bathroom fit-out. What waterproofing methods and materials should I use, what's the correct sequence of installation, and what are common DIY mistakes to avoid?",
        'painting': "I'll be doing my own painting. What tools and materials do I need, how do I properly prepare surfaces, what types of paint should I use in different areas, and how do I achieve a professional finish?",
        'fixtures': "I'm planning to install fixtures and fittings myself. What tools will I need, what's the process for different types of fixtures, and how do I ensure electrical fixtures are safely installed?",
    },
    'completion': {
        'finalElectrical': "I'm nearing completion of my owner builder project. What aspects of final electrical and plumbing connections can I do myself, and which require licensed professionals? What testing is required?",
        'cleanup': "I'll be doing the final site cleanup myself. What's involved, how do I dispose of different types of construction waste, and what level of cleaning is expected before handover or occupation?",
        'inspection': "I have final inspections coming up. What will the inspector be looking for, what documentation should I have ready, and how do I prepare to ensure I pass the first time?",
        'certification': "I need to obtain my occupation certificate. What documentation do I need to prepare myself, what forms must I submit, and what are common issues that delay the certification process?",
        'defects': "I want to identify and fix any defects myself before final inspection. What should I look for, what are common defects in new builds, and what's the best way to document and fix issues?",
        'documentation': "I need to compile project documentation for handover/my records. What should be included, how should it be organized, and what warranties, manuals, and maintenance schedules are important?",
    },
}

# Contractor Prompts
contractor_prompt_templates = {
    'planning': {
        'plans': "I'm an owner builder seeking help to understand what aspects of my plans I should be discussing with potential contractors. What key elements of the plans should I focus on when getting quotes, and what details should contractors be aware of before providing estimates?",
        'approvals': "I'm an owner builder seeking a contractor to help with my council approval application. What services should I ask for, what information should I provide them, and how should I evaluate their expertise in this area?",
        'costing': "I'm looking to hire someone to help create a detailed budget for my owner builder project. What services should they provide, what information should they include in the budget, and how can I verify their estimates are reasonable?",
        'scheduling': "I want to hire someone to create a construction schedule for my owner builder project. What should I expect them to deliver, what information should I provide them, and how should I evaluate the quality of their work?",
        'hiring': "I need to develop a system for finding and evaluating contractors for my owner builder project. What should my selection criteria include, what documentation should I request, and what should be in a solid contract to protect me?",
        'safetyPlan': "I want to hire someone to create and implement a site safety plan for my owner builder project. What services should they provide, what qualifications should they have, and what documentation should I expect them to maintain?",
    },
    'demolition': {
        'prepDemo': "I'm seeking quotes for demolition work on my owner builder project. What information should I include in my request for quotes, what specific services should I ask for, and how can I evaluate the quality and completeness of the quotes I receive?",
        'utilities': "I need to hire professionals to disconnect utilities before demolition. What services should I request quotes for, what information do I need to provide them, and what qualifications should they have?",
        'asbestos': "I suspect asbestos in my building and need to hire professionals for testing and removal. What services should I request quotes for, what qualifications should they have, and what documentation should I expect them to provide?",
        'structure': "I'm seeking quotes for structural demolition. What information should I include in my request, what services should I specifically ask for, and how can I evaluate if a contractor is qualified for this type of work?",
        'waste': "I need to hire contractors for waste management during my demolition. What services should I request quotes for, how should waste be sorted and disposed of, and what should I look for in their waste management plan?",
    },
    'sitePreperation': {
        'clearing': "I'm seeking quotes for site clearing and leveling. What services should be included, what information should I provide in my request, and how can I evaluate if a contractor has the right equipment and expertise for my site?",
        'excavation': "I need quotes for excavation work for my foundations. What information should I provide to contractors, what services should I specifically request, and how can I verify they'll dig to the correct depth?",
        'services': "I need to arrange for service connections (water, sewer, power) to my site. What contractors do I need to hire, what information should I provide in my request for quotes, and what should be included in their service?",
        'drainage': "I'm seeking quotes for drainage system installation. What information should I include in my request, what specific services should contractors provide, and how can I evaluate the quality of their proposed solutions?",
        'access': "I need quotes for site access and security solutions. What should be included in a comprehensive site security package, what information should I provide contractors, and how should I evaluate their proposals?",
    },
    'foundations': {
        'footings': "I'm seeking quotes for footing construction. What information should I include in my request, what specific services should contractors provide, and how can I ensure they'll construct footings that meet engineering requirements?",
        'slab': "I need quotes for concrete slab preparation and pouring. What information should I provide contractors, what should be included in their service, and how can I verify they'll deliver a quality result?",
        'waterproofing': "I'm looking for quotes for foundation waterproofing. What information should I include in my request, what materials and methods should contractors propose, and what guarantees should I ask for?",
        'insulation': "I need quotes for underfloor insulation. What information should I provide to contractors, what options should they present to me, and how can I evaluate the quality and energy efficiency of their proposals?",
        'inspection': "I want to hire someone to help prepare for foundation inspections. What services should they provide, what qualifications should they have, and how can they help ensure I pass inspection the first time?",
    },
    'framing': {
        'wallFraming': "I'm seeking quotes for wall framing. What information should I include in my request, what specific services should contractors provide, and how can I verify they'll deliver quality, square, and plumb walls?",
        'roofFraming': "I need quotes for roof framing. What information should I provide to contractors, what should be included in their service, and how can I evaluate if they have the expertise for my roof design?",
        'trusses': "I'm looking for quotes for truss supply and installation. What information should I include in my request, what services should be included, and what questions should I ask to ensure they're qualified?",
        'bracing': "I need quotes for structural bracing. What information should I provide contractors, what should be included in their service, and how can I verify they'll install bracing that meets building code requirements?",
        'windows': "I'm seeking quotes for framing rough openings for windows and doors. What information should I include in my request, what specific services should contractors provide, and how can I ensure accurate openings?",
    },
    'lockup': {
        'roofing': "I'm seeking quotes for roof installation. What information should I include in my request, what materials and options should I consider, and how can I evaluate contractors' expertise and guarantees?",
        'cladding': "I need quotes for external cladding/brickwork. What information should I provide contractors, what options should they present, and how can I evaluate the quality of their materials and installation methods?",
        'windowsInstall': "I'm looking for quotes for window and external door installation. What information should I include in my request, what services should be included, and what questions should I ask about weatherproofing?",
        'flashings': "I need quotes for flashing and weatherproofing. What information should I provide contractors, what should be included in their service, and how can I verify they'll install proper water management details?",
        'roughIn': "I'm seeking quotes for plumbing and electrical rough-in. What information should I include in my request, what services should be included, and how can I verify they're properly licensed and will comply with codes?",
    },
    'fitout': {
        'insulation': "I'm seeking quotes for insulation installation. What information should I include in my request, what materials and R-values should I specify, and how can I verify contractors will install it correctly?",
        'plasterboard': "I need quotes for plasterboard/drywall installation. What information should I provide contractors, what level of finish should I specify, and how can I evaluate the quality of their work?",
        'internalDoors': "I'm looking for quotes for internal door and trim installation. What information should I include in my request, what services should contractors provide, and how can I ensure quality installation?",
        'flooring': "I need quotes for flooring installation. What information should I provide contractors, what options should they present for different areas, and what questions should I ask about preparation and installation?",
        'kitchen': "I'm seeking quotes for kitchen installation. What information should I include in my request, what services should be included, and how can I verify contractors have the skills for cabinetry, plumbing, and electrical work?",
        'bathroom': "I need quotes for bathroom fit-out. What information should I provide contractors, what services should be included, and how can I verify they'll provide proper waterproofing and quality installation?",
        'painting': "I'm looking for quotes for interior painting. What information should I include in my request, what preparation and finish should I specify, and how can I evaluate the quality of contractors' previous work?",
        'fixtures': "I need quotes for installing fixtures and fittings. What information should I provide contractors, what services should be included, and how can I verify they're qualified for both general and electrical installations?",
    },
    'completion': {
        'finalElectrical': "I'm seeking quotes for final electrical and plumbing connections. What information should I include in my request, what services and certifications should be included, and how can I verify they're properly licensed?",
        'cleanup': "I need quotes for final site cleanup. What information should I provide contractors, what services should be included, and what level of cleaning should I specify for handover or occupation?",
        'inspection': "I'm looking for someone to help prepare for final inspections. What services should they provide, what qualifications should they have, and how can they help ensure I pass all inspections the first time?",
        'certification': "I need help obtaining my occupation certificate. What services should contractors provide, what documentation should they help prepare, and what qualifications should they have for this task?",
        'defects': "I want to hire someone to identify and document defects before final inspection. What services should they provide, what qualifications should they have, and what documentation should they deliver?",
        'documentation': "I need help compiling project documentation for handover. What services should contractors provide, what documents should be included, and how should everything be organized for future reference?",
    },
}

def get_phases():
    """Return all available project phases"""
    return project_phases

def get_tasks_for_phase(phase_id):
    """Return tasks for a specific phase"""
    if phase_id in tasks_by_phase:
        return tasks_by_phase[phase_id]
    return []

def generate_prompts(phase_id, task_ids, work_method):
    """Generate prompts based on selected phase, tasks and work method"""
    if not phase_id or not task_ids:
        return ""
    
    # Add debugging
    print(f"Generating prompts for phase: {phase_id}, tasks: {task_ids}, method: {work_method}")
    
    prompts = []
    for task_id in task_ids:
        if work_method == 'diy':
            prompt_template = diy_prompt_templates.get(phase_id, {}).get(task_id)
        else:  # contractor
            prompt_template = contractor_prompt_templates.get(phase_id, {}).get(task_id)
        
        if prompt_template:
            # Get the task name
            task_name = next((task['name'] for task in tasks_by_phase[phase_id] 
                            if task['id'] == task_id), task_id)
            prompts.append(f"### {task_name}\n\n{prompt_template}\n")
    
    # Add debugging
    print(f"Generated {len(prompts)} prompts")
    
    return "\n".join(prompts)