import gradio as gr
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend API URL
API_BASE_URL = "http://localhost:8000"

def process_pdf_and_generate_documents(pdf_file):
    """Process PDF and generate all documents"""
    try:
        if pdf_file is None:
            return "Please upload a PDF file", "", "", "", "Error: No file uploaded"
        
        # Send PDF to backend
        with open(pdf_file.name, 'rb') as f:
            files = {'file': (pdf_file.name, f, 'application/pdf')}
            response = requests.post(f"{API_BASE_URL}/generate-documents", files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract different formats
            markdown_report = result.get('markdown_report', '')
            json_export = result.get('json_export', '')
            ado_import = result.get('ado_import', '')
            
            # Store documents for ADO push
            global generated_documents
            generated_documents = result.get('documents', {})
            
            return (
                "✅ Documents generated successfully!",
                markdown_report,
                json_export,
                ado_import,
                "Ready to push to Azure DevOps"
            )
        else:
            error_msg = response.json().get('detail', 'Unknown error')
            return f"❌ Error: {error_msg}", "", "", "", "Error occurred"
            
    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", "", "Error occurred"

def push_to_azure_devops():
    """Push generated documents to Azure DevOps"""
    try:
        global generated_documents
        if not generated_documents:
            return "❌ No documents to push. Please generate documents first."
        
        response = requests.post(
            f"{API_BASE_URL}/push-to-ado",
            json=generated_documents,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            results = result.get('results', {})
            
            summary = "✅ Successfully pushed to Azure DevOps:\n\n"
            
            # Epics
            epics = results.get('epics', [])
            if epics:
                summary += "**Epics Created:**\n"
                for epic in epics:
                    summary += f"- {epic['title']} (ID: {epic['id']})\n"
                summary += "\n"
            
            # Stories
            stories = results.get('stories', [])
            if stories:
                summary += "**Stories Created:**\n"
                for story in stories:
                    summary += f"- {story['title']} (ID: {story['id']})\n"
                summary += "\n"
            
            # Errors
            errors = results.get('errors', [])
            if errors:
                summary += "**Errors:**\n"
                for error in errors:
                    summary += f"- {error}\n"
            
            return summary
        else:
            error_msg = response.json().get('detail', 'Unknown error')
            return f"❌ Error pushing to ADO: {error_msg}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

def download_file(content, filename):
    """Create downloadable file"""
    if not content:
        return None
    
    temp_file = f"/tmp/{filename}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    return temp_file

# Global variable to store generated documents
generated_documents = {}

# Create Gradio interface
with gr.Blocks(title="GenAI Document Generator", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🤖 GenAI Document Generator
    
    Upload a PDF with business requirements and generate:
    - ADO Epics, Stories, and Use Cases
    - Technical Design Document
    - Data Model
    - Push directly to Azure DevOps
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📄 Upload Business Requirements")
            pdf_input = gr.File(
                label="Upload PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            
            generate_btn = gr.Button(
                "🚀 Generate Documents",
                variant="primary",
                size="lg"
            )
            
            status_output = gr.Textbox(
                label="Status",
                interactive=False,
                lines=2
            )
        
        with gr.Column(scale=2):
            gr.Markdown("## 📋 Generated Documents")
            
            with gr.Tabs():
                with gr.TabItem("📊 Markdown Report"):
                    markdown_output = gr.Textbox(
                        label="Comprehensive Report",
                        lines=20,
                        max_lines=30,
                        interactive=False
                    )
                    markdown_download = gr.File(
                        label="Download Markdown Report",
                        interactive=False
                    )
                
                with gr.TabItem("📄 JSON Export"):
                    json_output = gr.Textbox(
                        label="JSON Format",
                        lines=20,
                        max_lines=30,
                        interactive=False
                    )
                    json_download = gr.File(
                        label="Download JSON Export",
                        interactive=False
                    )
                
                with gr.TabItem("🔄 ADO Import"):
                    ado_output = gr.Textbox(
                        label="Azure DevOps Import Format",
                        lines=20,
                        max_lines=30,
                        interactive=False
                    )
                    ado_download = gr.File(
                        label="Download ADO Import",
                        interactive=False
                    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 🚀 Azure DevOps Integration")
            ado_status = gr.Textbox(
                label="ADO Push Status",
                interactive=False,
                lines=3
            )
            
            push_ado_btn = gr.Button(
                "📤 Push to Azure DevOps",
                variant="secondary",
                size="lg"
            )
    
    # Event handlers
    generate_btn.click(
        fn=process_pdf_and_generate_documents,
        inputs=[pdf_input],
        outputs=[status_output, markdown_output, json_output, ado_output, ado_status]
    )
    
    push_ado_btn.click(
        fn=push_to_azure_devops,
        outputs=[ado_status]
    )
    
    # Download handlers
    markdown_output.change(
        fn=lambda content: download_file(content, "project_documentation.md") if content else None,
        inputs=[markdown_output],
        outputs=[markdown_download]
    )
    
    json_output.change(
        fn=lambda content: download_file(content, "project_export.json") if content else None,
        inputs=[json_output],
        outputs=[json_download]
    )
    
    ado_output.change(
        fn=lambda content: download_file(content, "ado_import.json") if content else None,
        inputs=[ado_output],
        outputs=[ado_download]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )