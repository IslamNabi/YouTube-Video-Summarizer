import gradio as gr
from modules.my_transcript import get_video_id, get_transcript
from modules.summarizer import generate_summary, MODELS

def summarize_video(video_url: str, model_name: str) -> str:
    """Handle the video summarization pipeline"""
    try:
        # Validate input
        if not video_url.strip():
            return "Please enter a YouTube URL"
        
        # Extract video ID
        video_id = get_video_id(video_url)
        if not video_id:
            return "Invalid YouTube URL"
        
        # Get transcript
        transcript = get_transcript(video_url)

        
        # Generate summary
        model = MODELS.get(model_name, "gpt-4o-mini")
        summary = generate_summary(transcript, model)
        
        return summary
    
    except Exception as e:
        return f"Error: {str(e)}"

def create_interface():
    """Create and configure Gradio interface"""
    with gr.Blocks(title="YouTube Summarizer") as app:
        gr.Markdown("# 🎬 YouTube Video Summarizer")
        
        with gr.Row():
            url_input = gr.Textbox(
                label="YouTube Video URL",
                placeholder="https://www.youtube.com/watch?v=...",
                interactive=True
            )
            model_dropdown = gr.Dropdown(
                label="AI Model",
                choices=list(MODELS.keys()),
                value="GPT-4-turbo"
            )
        
        submit_btn = gr.Button("Summarize", variant="primary")
        
        output = gr.Textbox(
            label="Summary",
            interactive=False,
            lines=10,
            placeholder="Your video summary will appear here..."
        )
        
        gr.Examples(
            examples=[
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
                ["https://www.youtube.com/watch?v=JGwWNGJdvx8"]
            ],
            inputs=url_input
        )
        
        submit_btn.click(
            fn=summarize_video,
            inputs=[url_input, model_dropdown],
            outputs=output
        )
    
    return app