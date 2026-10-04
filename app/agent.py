import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from app.tools import search_products, get_order_status
from app.rag import search_knowledge_base_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

tools = [search_knowledge_base_tool, search_products, get_order_status]

SYSTEM_PROMPT = """You are SupportPilot, a customer support AI for an online electronics store.

You have access to three tools:
- search_knowledge_base_tool: for policy/FAQ questions (returns, shipping, payment, warranties)
- search_products: for product availability, pricing, recommendations
- get_order_status: for order tracking questions (requires an order ID)

Rules:
1. Always use a tool when the question relates to what that tool covers. Never guess or make up information.
2. You must ONLY help with topics related to this store: orders, products, shipping, returns, 
   payments, and store policies. 
3. If a customer asks about ANYTHING outside this scope — including general knowledge questions, 
   math problems, trivia, coding help, or any topic unrelated to the store — do NOT answer it, 
   even if you know the answer and even if it seems simple or harmless. Instead, politely decline 
   and redirect them back to store topics. Do this every time, not just once.
4. If a customer's request is something you cannot resolve with your tools — such as complaints, 
   compensation requests, wrong/damaged items, or anything requiring human judgment — do NOT attempt 
   to resolve it yourself. Instead, respond with exactly this format:
   "HANDOFF_REQUIRED: I'll forward this conversation to a support representative who can help with this."
5. Be concise, friendly, and professional in all responses.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def ask_agent(message: str) -> dict:
    """
    Runs the customer's message through the agent and returns the response,
    along with a flag indicating whether human handoff is required.
    """
    result = agent.invoke({
        "messages":[
            {"role":"user", "content":message}
        ]
    })
    output = result["messages"][-1].content[0]["text"]

    handoff = output.strip().startswith("HANDOFF_REQUIRED")
    if handoff:
        output = output.replace("HANDOFF_REQUIRED:", "").strip()

    return {"response": output, "handoff": handoff}