"""
Hugging Face Spaces deployment for Irish Tax Simpler

This file integrates all components directly (no separate API server needed)

Usage in Hugging Face:
- This file will be automatically detected and launched
- API calls are made directly to Python functions (no HTTP)
"""

import os
import time
import gradio as gr
from app.retriever import retrieve
from app.rerank import rerank
from app.generate import generate_answer


def get_answer_with_citations(
    question: str,
    top_k: int = 20,
    top_n: int = 6,
    score_threshold: float = 0.35,
    enable_refinement: bool = True
) -> tuple[str, str, str]:
    """
    Process a question and return answer with citations.
    
    Returns:
        tuple: (answer, diagnostics, citations)
    """
    if not question or not question.strip():
        return "Please enter a question.", "", ""
    
    try:
        start_time = time.time()
        
        # Step 1: Refine the question (handle spelling mistakes) - FAST MODE
        # Skip LLM refinement for speed, just use the original question
        refinement = {"refined": question, "method": "fast"}
        refined_question = question
        refine_time = time.time() - start_time
        
        # Step 2: Retrieve relevant documents
        retrieve_start = time.time()
        retrieved = retrieve(
            refined_question,
            top_k=top_k,
            score_threshold=score_threshold
        )
        retrieve_time = time.time() - retrieve_start
        
        if not retrieved:
            return (
                "No relevant documents found for your question. Try rephrasing or adjusting the score threshold.",
                "Retrieved: 0 documents",
                ""
            )
        
        # Step 3: Rerank documents
        rerank_start = time.time()
        ranked = rerank(refined_question, retrieved, top_n=top_n)
        rerank_time = time.time() - rerank_start
        
        # Step 4: Generate answer
        generate_start = time.time()
        result = generate_answer(question, ranked)
        generate_time = time.time() - generate_start
        
        answer = result.get("answer", "No answer generated.")
        
        total_time = time.time() - start_time
        
        # Format diagnostics with timing
        diagnostics = f"""**Diagnostics:**
- Retrieved: {len(retrieved)} documents ({retrieve_time:.2f}s)
- Reranked: {len(ranked)} documents ({rerank_time:.2f}s)
- Generated: ({generate_time:.2f}s)
- **Total Time: {total_time:.2f}s**"""
        
        # Format citations
        citations_data = result.get("citations", [])
        if citations_data:
            citations_text = "## 📚 Citations\n\n"
            for cit in citations_data:
                filename = cit.get('source_filename', 'Unknown')
                page = cit.get('page', 'N/A')
                score = cit.get('rerank_score', 0)
                
                citations_text += (
                    f"**{cit.get('ref', 'N/A')}** - {filename} "
                    f"(Page {page}, Score: {score:.3f})\n\n"
                )
        else:
            citations_text = "No citations available."
        
        return answer, diagnostics, citations_text
    
    except Exception as e:
        error_msg = f"**Error:** {str(e)}\n\nPlease check your configuration and try again."
        return error_msg, "", ""


# Create Gradio interface
with gr.Blocks(
    title="Irish Tax Simpler",
    theme=gr.themes.Soft()
) as demo:
    
    gr.Markdown("# 🇮🇪 Irish Tax Simpler")
    
    with gr.Row():
        with gr.Column(scale=2):
            question_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is PAYE? How does PRSI work? What are USC charges?",
                lines=3
            )
            
            # Set default values for sliders (hidden from UI) - OPTIMIZED FOR SPEED
            top_k_slider = gr.Slider(value=10, visible=False)  # Reduced from 20
            top_n_slider = gr.Slider(value=3, visible=False)   # Reduced from 6
            threshold_slider = gr.Slider(value=0.35, visible=False)
            refinement_toggle = gr.Checkbox(value=True, visible=False)
            
            ask_button = gr.Button("Get Answer", variant="primary", size="lg")
        
        with gr.Column(scale=3):
            answer_output = gr.Markdown(
                label="Answer",
                value="Ask a question to get started..."
            )
            
            diagnostics_output = gr.Markdown(
                label="Diagnostics"
            )
            
            citations_output = gr.Markdown(
                label="Citations",
                value=""
            )
    
    
    # Event handler
    ask_button.click(
        fn=get_answer_with_citations,
        inputs=[
            question_input,
            top_k_slider,
            top_n_slider,
            threshold_slider,
            refinement_toggle
        ],
        outputs=[answer_output, diagnostics_output, citations_output]
    )


# For Hugging Face Spaces
if __name__ == "__main__":
    demo.launch()
