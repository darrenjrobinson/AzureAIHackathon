# Microsoft Azure AI Developer Hackathon 2025

## Owner Builder AI Assistant

Owner builders navigating building standards, getting quotes &amp; managing the sheer complexity can feel overwhelming. The Owner Builder AI Assistant assists with the power of Azure AI.

Built for the [Microsoft Azure AI Developer Hackathon - March 2025](https://azureaidev.devpost.com/) by [Darren J Robinson](https://blog.darrenjrobinson.com)

[Devpost Hackathon Link](https://devpost.com/software/owner-builder-ai-assistant)


## Prerequsite Azure Services

- Azure AI Services - For intelligent document analysis
- Azure AI Search - For intelligent document search
- Azure OpenAI - For generating responses and analysis
- Azure Computer Vision - For analyzing construction drawings
- Flask - Python web framework

![Solution and Architecture Overview](./Owner%20Builder%20AI%20Assistant%20Arch.png)


## Create Azure Resources

### Setup and Configuration

1. Clone this repository to your local machine:

```
git clone https://github.com/[your-username]/AzureAIHackathon.git cd AzureAIHackathon/WebApp
```

### Resource Group, Azure AI Search, Storage Account

Create a Resource Group https://portal.azure.com/#@increment.inc/resource/subscriptions/d7811fe3-0750-41c6-8aaa-ff63b48aef6d/resourceGroups/AIHack/overview 

	a. Create an Azure AI Search instance
		i. Enabled System Assigned Managed Identity
	b. Create a Storage Account
		i. Enable hierarchical storage 
		ii. Create a container (Blob Storage)
			1) Manage ACL and grant the Search Instance Read & Execute
			2) Create a Folder named 'guidelines'
            3) Upload construction reference documents to the folder
		iii. Add Storage Blob Data Reader permission to the Azure AI Search Service Managed Identity	
	c. Back to Azure AI Search
		i. Add a Data Source - Azure Data Lage Storage Gen2
			1) Storage account container created above
			2) Folder => guidelines
			3) Authenticate => System-assigned managed identity
		ii. Add the Search Index Data Reader and Search Service Contributor roles to the Azure Open AI System-assigned managed identity


### Azure Open AI

	d. Create an Azure Open AI instance
		i. Got to AI Foundry => Deployments
			1) Deploy the gpt-4o-mini model

## Azure AI Services

	e. Create Azure AI Services 
		i. Deploy Azure AI Services
        ii. Enable System-assigned managed identity

## Configure Azure AI Search

Configuring Azure AI Search requires creating configurations for a datasource skillset an indexer and an index. 

The following templates give the structure and configuration.

Create a datasource connection 
[Example](./Azure%20AI%20Search/owner-builder-datasource.json)

Create Index 
[Example](./Azure%20AI%20Search/owner-builder-index.json)

Create a Skillset
[Example](./Azure%20AI%20Search/owner-builder-skillset.json)

Create an Indexer
[Example](./Azure%20AI%20Search/owner-builder-indexer.json)

## Python Web App Setup

1. Create and activate a virtual environment:

```
python -m venv venv
```

On Windows
```
venv\Scripts\activate
```

On macOS/Linux
```
source venv/bin/activate
```

### Install dependencies

2. Install dependencies

```
pip install -r requirements.txt
```

3. Create a `.env` file in the WebApp directory with your Azure service credentials.

[Copy, update and rename this example](./WebApp/example%20env.txt)

```
# Flask configuration
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=yourkey

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://<yourendpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=yourkey
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-10-21

# Azure Cognitive Services
AZURE_VISION_ENDPOINT=https://<yourendpoint>.cognitiveservices.azure.com/
AZURE_VISION_KEY=yourkey

# Azure AI Search
AZURE_SEARCH_SERVICE_ENDPOINT=https://<yourendpoint>.search.windows.net
AZURE_SEARCH_INDEX_NAME=owner-builder-index
AZURE_SEARCH_API_KEY=yourkey 

```

## Running the WebApp

### Development mode
```
python run.py
```

### Production mode with gunicorn (Linux/macOS)
```
gunicorn -w 4 run:app
```
Access the application in your browser at `http://localhost:5000`