import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Page Setup
st.set_page_config(
    page_title="Empório da Música | Tom Assistant",
    page_icon="🎸",
    layout="wide"
)

# Helper function to load external CSS file
def load_css(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom styles from external stylesheet in src directory
load_css("src/style.css")

# Sidebar Information Panel
with st.sidebar:
    st.image("https://img.icons8.com/color/96/guitar.png", width=70)
    st.title("Empório da Música")
    st.caption("Campo Grande / MS")
    
    st.markdown("---")
    st.markdown("### 🏪 Informações da Loja")
    st.markdown("**📍 Endereço:** Rua das Acácias, 450 - Centro")
    st.markdown("**🕒 Horário:** Seg-Sexta 08h-18h | Sáb 08h-12h")
    st.markdown("**🛡️ Garantia:** Conforme política interna")
    
    st.markdown("---")
    st.markdown("### 🤖 Status do Agente")
    st.success("Tom AI System: Online")
    st.info("Modelo: Gemini + RAG")

# Main Header Banner
st.markdown("""
<div class="main-header">
    <h1>🎸 Assistente Virtual Tom</h1>
    <p>Atendimento especializado da Empório da Música — Instrumentos, Pedidos e Políticas</p>
</div>
""", unsafe_allow_html=True)

# Cache Resource Loading with Animated Soundwave Spinner
@st.cache_resource(show_spinner=False)
def load_agent_system():
    from src.database import get_db_connection
    from src.tools_sql import set_connection
    from src.tools_rag import init_rag
    from src.agent import agent_executor
    
    conn = get_db_connection()
    set_connection(conn)
    init_rag()
    return agent_executor

# Initial Boot Loader Display
if "agent_loaded" not in st.session_state:
    loader_placeholder = st.empty()
    with loader_placeholder.container():
        st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <div class="equalizer-container">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            <p style="color: #a5b4fc; font-weight: 500;">Inicializando Tom Assistant e indexando base de dados...</p>
        </div>
        """, unsafe_allow_html=True)
        agent_executor = load_agent_system()
        st.session_state["agent_loaded"] = True
    loader_placeholder.empty()
else:
    agent_executor = load_agent_system()

# Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Prompt Cards for Fast Testing
st.markdown("##### 💡 Sugestões de teste rápido:")
col1, col2, col3, col4 = st.columns(4)
prompt_to_submit = None

if col1.button("🎸 Violões até R$1000"):
    prompt_to_submit = "Quais opções de violões disponíveis vocês têm custando até R$ 1000?"
if col2.button("📦 Status do Pedido #1"):
    prompt_to_submit = "Qual é o status do meu pedido de número 1?"
if col3.button("📜 Política de Devolução"):
    prompt_to_submit = "Me arrependi da minha compra feita no site há 3 dias, posso devolver?"
if col4.button("🚫 Pergunta de Acessórios"):
    prompt_to_submit = "Vocês vendem encordoamento para violão ou amplificador?"

# Chat Input field
user_input = st.chat_input("Digite sua dúvida para o Tom...")

if prompt_to_submit or user_input:
    active_prompt = prompt_to_submit if prompt_to_submit else user_input
    st.session_state.messages.append({"role": "user", "content": active_prompt})

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process Assistant Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Tom está consultando a base da loja..."):
            recent_messages = st.session_state.messages[:-1][-4:]
            formatted_history = [
                (msg["role"], msg["content"]) for msg in recent_messages
            ]
            
            try:
                raw_response = agent_executor.invoke({
                    "input": st.session_state.messages[-1]["content"],
                    "chat_history": formatted_history
                })
                
                output = raw_response.get("output", "")
                
                if isinstance(output, list):
                    text_parts = [
                        item.get("text", "") if isinstance(item, dict) else str(item)
                        for item in output
                    ]
                    final_text = "\n".join(text_parts)
                elif isinstance(output, dict):
                    final_text = output.get("text", str(output))
                else:
                    final_text = str(output)
                    
            except Exception as e:
                final_text = f"⚠️ Erro de execução: {str(e)}"

            st.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
            st.rerun()

# âncora no final da página
st.markdown("<div id='bottom-anchor'></div>", unsafe_allow_html=True)

# Injeção de script nativa para scroll automático até a âncora
st.markdown(
    """
    <script>
        var element = window.parent.document.getElementById("bottom-anchor");
        if (element) {
            element.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
        }
    </script>
    """,
    unsafe_allow_html=True
)