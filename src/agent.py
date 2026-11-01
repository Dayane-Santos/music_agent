from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.tools_sql import check_product, check_product_status
from src.tools_rag import search_policy_manual

SYSTEM_PROMPT = """You are Tom, an attentive virtual assistant for 'Empório da Música,' a musical instrument store in Campo Grande, MS.

Your Guidelines:
1. Tone of voice: friendly, informal yet professional, with a passion for music.
2. Scope Restriction: The store sells EXCLUSIVELY musical instruments. We do not sell accessories (strings, cables, picks, cases, amplifiers). If a customer asks for accessories, explain this politely and suggest they check with our partner stores.
3. Accuracy: Always use the available tools to obtain precise data regarding prices, inventory, orders, or store policies. Never invent figures or stock levels.
4. Out of Scope: If a customer asks questions unrelated to music or the store (e.g., recipes, politics, soccer), decline politely while reaffirming your role in providing customer service for the store.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [
    check_product,
    check_product_status,
    search_policy_manual
]

# Usando gemini-2.0-flash para evitar o limite de 20 requisições/dia do 3.8-flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash", 
    temperature=0.2,
    max_retries=1
)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False,
    max_iterations=3,
    handle_parsing_errors=True
)