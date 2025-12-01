import os
from typing import TypedDict, List
from dotenv import load_dotenv

# 导入 LangChain 相关库
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
from langgraph.graph import StateGraph, END

# 加载 .env 文件中的环境变量
load_dotenv()

# ==================== 1. 定义状态 (State) ====================
class AgentState(TypedDict):
    task: str                # 用户任务
    plan: List[str]          # 搜索计划
    content: List[str]       # 搜索到的原始内容
    final_report: str        # 最终报告

# ==================== 2. 封装 Agent 类 ====================
class ResearchAgent:
    def __init__(self):
        # 检查 Key 是否存在
        if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
            raise ValueError("API Keys not found in .env file!")

        # 初始化模型 (Llama 3.3 or 3.1)
        self.model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # 编译图
        self.app = self._build_graph()

    def _build_graph(self):
        """内部方法：构建 LangGraph 工作流"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("planner", self.plan_node)
        workflow.add_node("researcher", self.research_node)
        workflow.add_node("writer", self.write_node)
        
        # 定义连线
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "writer")
        workflow.add_edge("writer", END)
        
        return workflow.compile()

    # ---------- 节点逻辑 ----------
    
    def plan_node(self, state: AgentState):
        """规划节点：生成搜索词"""
        print(f"--- Step 1: Planning for {state['task']} ---")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个资深搜索专家。"),
            ("user", "任务: {task}\n\n请生成 3 个最高效的英文搜索引擎关键词。仅返回关键词，用逗号分隔，不要有其他文字。")
        ])
        chain = prompt | self.model
        response = chain.invoke({"task": state["task"]})
        queries = [q.strip() for q in response.content.split(",")]
        return {"plan": queries}

    def research_node(self, state: AgentState):
        """搜索节点：执行搜索并提取摘要"""
        print(f"--- Step 2: Researching ---")
        queries = state["plan"]
        collected_content = []
        
        for query in queries:
            try:
                # include_answer=True 让 Tavily 尝试直接给答案，速度更快
                result = self.tavily.search(query=query, max_results=2, include_answer=True)
                for r in result['results']:
                    # 记录来源 URL 和内容
                    content = f"[Source: {r['url']}]\nTitle: {r['title']}\nContent: {r['content'][:800]}..." 
                    collected_content.append(content)
            except Exception as e:
                print(f"Search Error: {e}")
        
        return {"content": collected_content}

    def write_node(self, state: AgentState):
        """写作节点：生成报告"""
        print(f"--- Step 3: Writing Report ---")
        content = "\n\n".join(state["content"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的技术分析师。请用中文撰写一份详细的分析报告。"),
            ("user", "任务: {task}\n\n参考资料:\n{content}\n\n要求：\n1. 结构清晰，使用 Markdown 格式。\n2. 必须在文中适当位置标注来源（如 [Source: http://...]）。\n3. 如果资料不足，请诚实说明。")
        ])
        chain = prompt | self.model
        response = chain.invoke({"task": state["task"], "content": content})
        return {"final_report": response.content}

    def run(self, task: str):
        """外部调用入口"""
        return self.app.invoke({"task": task})