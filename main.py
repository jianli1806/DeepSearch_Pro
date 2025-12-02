import streamlit as st
from agent_engine import ResearchAgent

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="DeepSearch Pro", 
    page_icon="🔍",
    layout="wide"
)

# ==================== CSS Fixes (关键修复) ====================
# 1. fix-scroll: 强制主区域高度，防止错位
# 2. padding-bottom: 预留底部空间，防止生成时内容被遮挡
st.markdown("""
<style>
    .main {
        padding-bottom: 100px; 
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .report-box {
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 修复 Streamlit Cloud 上的滚动抖动 */
    [data-testid="stAppViewContainer"] {
        overflow-y: scroll; 
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
        "Unlike standard Chatbots, this agent **plans**, **searches**, "
        "**reads**, and **synthesizes** information from the live web."
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
        # 使用空容器占位，保证布局稳定
        status_placeholder = st.empty()
        report_placeholder = st.container()

        try:
            # Instantiate Agent
            agent = ResearchAgent()
            
            # --- 阶段 1: 进度展示 (Status) ---
            with status_placeholder.status("🕵️ Agent is working...", expanded=True) as status:
                
                status.write("🧠 Decomposing task & generating search strategy...")
                # 移除 time.sleep，减少渲染卡顿
                
                # --- Run the Agent (同步执行) ---
                result = agent.run(task_input)
                
                # 更新进度信息
                plan = result.get("plan", [])
                status.write(f"✅ Generated keywords: {', '.join(plan)}")
                
                content_count = len(result.get("content", []))
                status.write(f"✅ Extracted {content_count} web documents")
                
                status.write("✍️ Synthesizing final report...")
                status.update(label="✅ Research Complete!", state="complete", expanded=False)
            
            # --- 阶段 2: 报告展示 (Report) ---
            # 在独立的 Container 中渲染，防止和 Status 发生 CSS 冲突
            with report_placeholder:
                st.divider()
                st.subheader("📝 Research Report")
                
                report = result["final_report"]
                
                # 使用自定义 CSS 框包裹报告，看起来更稳定
                st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True) # 增加一点空隙
                
                # Export Button
                st.download_button(
                    label="📥 Download Report (Markdown)",
                    data=report,
                    file_name=f"report_{task_input[:10].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
        except Exception as e:
            st.error(f"Runtime Error: {e}")
            st.info("Please check if API Keys are correctly configured in Streamlit Secrets.")
