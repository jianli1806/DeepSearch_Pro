import os
from typing import TypedDict, List
from dotenv import load_dotenv

# Import LangChain related libraries
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
from langgraph.graph import StateGraph, END

# Load environment variables from .env file
load_dotenv()

# ==================== 1. Define State ====================
class AgentState(TypedDict):
    task: str                # User task
    plan: List[str]          # Search plan (keywords)
    content: List[str]       # Collected raw content
    final_report: str        # Final generated report

# ==================== 2. Encapsulate Agent Class ====================
class ResearchAgent:
    def __init__(self):
        # Check if API Keys exist
        if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
            raise ValueError("API Keys not found in .env file!")

        # Initialize model (Llama 3.3 or 3.1)
        # Temperature is set to 0 for deterministic outputs
        self.model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # Compile the graph
        self.app = self._build_graph()

    def _build_graph(self):
        """Internal method: Build LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner", self.plan_node)
        workflow.add_node("researcher", self.research_node)
        workflow.add_node("writer", self.write_node)
        
        # Define edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "writer")
        workflow.add_edge("writer", END)
        
        return workflow.compile()

    # ---------- Node Logic ----------
    
    def plan_node(self, state: AgentState):
        """Planning Node: Generate search queries"""
        print(f"--- Step 1: Planning for {state['task']} ---")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert search planner."),
            ("user", "Task: {task}\n\nPlease generate 3 highly effective English search engine keywords. Return ONLY the keywords, separated by commas, with no other text.")
        ])
        chain = prompt | self.model
        response = chain.invoke({"task": state["task"]})
        queries = [q.strip() for q in response.content.split(",")]
        return {"plan": queries}

    def research_node(self, state: AgentState):
        """Search Node: Execute search and extract summaries"""
        print(f"--- Step 2: Researching ---")
        queries = state["plan"]
        collected_content = []
        
        for query in queries:
            try:
                # include_answer=True asks Tavily to attempt a direct answer, which is faster
                result = self.tavily.search(query=query, max_results=2, include_answer=True)
                for r in result['results']:
                    # Record source URL and content
                    content = f"[Source: {r['url']}]\nTitle: {r['title']}\nContent: {r['content'][:800]}..." 
                    collected_content.append(content)
            except Exception as e:
                print(f"Search Error: {e}")
        
        return {"content": collected_content}

    def write_node(self, state: AgentState):
        """Writing Node: Generate report"""
        print(f"--- Step 3: Writing Report ---")
        content = "\n\n".join(state["content"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a professional technical analyst. Please write a detailed analysis report in English."),
            ("user", "Task: {task}\n\nReference Materials:\n{content}\n\nRequirements:\n1. Clear structure using Markdown format.\n2. Must cite sources in the text (e.g., [Source: http://...]).\n3. If information is insufficient, state it honestly.")
        ])
        chain = prompt | self.model
        response = chain.invoke({"task": state["task"], "content": content})
        return {"final_report": response.content}

    def run(self, task: str):
        """External entry point"""
        return self.app.invoke({"task": task})
