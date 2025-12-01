import streamlit as st
import time
from agent_engine import ResearchAgent

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="DeepSearch Pro", 
    page_icon="🔍",
    layout="wide"
)

# 自定义 CSS 让界面更漂亮 (暗黑模式适配)
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

# ==================== 侧边栏 ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
    st.title("DeepSearch Pro")
    st.caption("🚀 Powered by Llama 3 & LangGraph")
    st.markdown("---")
    st.markdown("### 关于项目")
    st.info(
        "这是一个基于 **Agentic AI** 架构的自主调研助手。\n\n"
        "它不像 ChatGPT 那样只凭记忆回答，而是会**自主联网**、"
        "**阅读网页**、**去伪存真**，最后生成带引用的专业报告。"
    )

# ==================== 主界面 ====================
st.header("🔍 深度调研助手 (AI Agent)")
st.markdown("输入你想研究的话题，AI 将为你自动执行：`规划` -> `联网搜索` -> `阅读整合` -> `生成报告`")

# 用户输入
task_input = st.text_input("请输入研究话题：", placeholder="例如：分析 2024 年生成式 AI 在医疗领域的应用趋势")

# 执行按钮
if st.button("🚀 开始深度调研", use_container_width=True):
    if not task_input:
        st.warning("请输入话题后再开始！")
    else:
        try:
            # 实例化 Agent
            agent = ResearchAgent()
            
            # 创建进度容器
            status_container = st.status("🕵️ Agent 正在工作中...", expanded=True)
            
            # --- 步骤 1: 规划 ---
            status_container.write("🧠 正在拆解任务，生成搜索策略...")
            # 这里调用 agent 的内部逻辑并没有暴露每一步的回调，为了演示效果，我们模拟一下进度条
            # (在进阶版中，我们会用 callback 实时更新，但现在先跑通 MVP)
            time.sleep(1) 
            
            # --- 真正运行 Agent ---
            # 注意：因为 agent.run 是同步的，这里会卡住直到完成。
            # 为了更好的体验，后续我们可以拆解 run 方法，但现在先看结果。
            result = agent.run(task_input)
            
            # --- 步骤展示 (从结果反推，或者优化 Agent 类暴露中间步骤) ---
            # 这里我们假设已经拿到结果，为了展示给用户看，我们打印出它的 Plan
            plan = result.get("plan", [])
            status_container.write(f"✅ 已生成搜索关键词: {', '.join(plan)}")
            
            status_container.write("🌐 正在并发搜索 6 个网页源...")
            content_count = len(result.get("content", []))
            status_container.write(f"✅ 已阅读并提取 {content_count} 份核心资料")
            
            status_container.write("✍️ 正在整合信息并撰写报告...")
            status_container.update(label="✅ 调研完成！", state="complete", expanded=False)
            
            # --- 结果展示区 ---
            st.divider()
            st.subheader("📝 调研报告")
            
            report = result["final_report"]
            st.markdown(report)
            
            # --- 导出按钮 ---
            st.download_button(
                label="📥 下载报告 (Markdown)",
                data=report,
                file_name=f"report_{task_input[:10]}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"运行出错: {e}")
            st.error("请检查 .env 文件中的 API Key 是否正确配置。")