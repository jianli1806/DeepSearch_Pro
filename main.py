import streamlit as st
import time
from agent_engine import ResearchAgent

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="DeepSearch Pro", 
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for better UI (Dark mode compatible)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .report-box {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Sidebar ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
    st.title("DeepSearch Pro")
    st.caption("🚀 Powered by Llama 3 & LangGraph")
    st.markdown("---")
    st.markdown("### About Project")
    st.info(
        "This is an **Agentic AI** autonomous research assistant.\n\n"
        "Unlike standard Chatbots that rely solely on memory, this agent can "
        "**autonomously browse the web**, **read pages**, **verify facts**, "
        "and generate professional reports with citations."
    )

# ==================== Main Interface ====================
st.header("🔍 DeepSearch Pro (AI Agent)")
st.markdown("Enter a topic, and the AI will execute: `Plan` -> `Web Search` -> `Read & Synthesize` -> `Generate Report`")

# User Input
task_input = st.text_input("Enter research topic:", placeholder="e.g., Analysis of Generative AI trends in Healthcare 2024")

# Execution Button
if st.button("🚀 Start Deep Research", use_container_width=True):
    if not task_input:
        st.warning("Please enter a topic first!")
    else:
        try:
            # Instantiate Agent
            agent = ResearchAgent()
            
            # Create status container
            status_container = st.status("🕵️ Agent is working...", expanded=True)
            
            # --- Step 1: Planning ---
            status_container.write("🧠 Decomposing task & generating search strategy...")
            # Simulate progress for better UX
            time.sleep(1) 
            
            # --- Run the Agent ---
            # Note: agent.run is synchronous
            result = agent.run(task_input)
            
            # --- Display Steps (Post-execution visualization) ---
            plan = result.get("plan", [])
            status_container.write(f"✅ Generated search keywords: {', '.join(plan)}")
            
            status_container.write("🌐 Searching 6 concurrent web sources...")
            content_count = len(result.get("content", []))
            status_container.write(f"✅ Read and extracted {content_count} core documents")
            
            status_container.write("✍️ Synthesizing information and writing report...")
            status_container.update(label="✅ Research Complete!", state="complete", expanded=False)
            
            # --- Result Display Area ---
            st.divider()
            st.subheader("📝 Research Report")
            
            report = result["final_report"]
            st.markdown(report)
            
            # --- Export Button ---
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=report,
                file_name=f"report_{task_input[:10].replace(' ', '_')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Runtime Error: {e}")
            st.error("Please check if API Keys are correctly configured in the .env file.")
