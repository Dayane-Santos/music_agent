# 🎸 Empório da Música — Assistente Virtual Tom

O **Tom** é o assistente virtual da loja **Empório da Música** (Campo Grande/MS), desenvolvido para realizar atendimentos automatizados de forma rápida, amigável e precisa.

## ✨ Funcionalidades

- **Catálogo de instrumentos:** consulta em tempo real via banco de dados SQL.
- **Status de pedidos:** verificação de andamento e rastreamento por código do pedido.
- **Políticas da loja:** respostas sobre devolução, garantia e direito de arrependimento utilizando **RAG** (*Retrieval-Augmented Generation*).
- **Regras rígidas de escopo:** comercialização exclusiva de instrumentos musicais, com recusa educada de vendas de acessórios e de temas fora do domínio da loja.

---

## 📑 Sumário

1. [Instruções para Rodar o Projeto](#-instruções-para-rodar-o-projeto)
2. [Justificativa das Decisões Técnicas](#️-justificativa-das-decisões-técnicas)
3. [Limitações Conhecidas e Evoluções Futuras](#️-limitações-conhecidas-e-evoluções-futuras)
4. [Uso de Assistentes de Código e Workflow](#-uso-de-assistentes-de-código-e-workflow)
5. [Exemplos de Interação e Demonstração](#-exemplos-de-interação-e-demonstração-do-agente)

---

## 🚀 Instruções para Rodar o Projeto

### 1. Pré-requisitos

- **Python 3.10+** instalado.
- Chave de API do **Google AI Studio** (`GOOGLE_API_KEY`).

### 2. Configuração do Ambiente

**2.1. Clonar o repositório**

```bash
git clone https://github.com/Dayane-Santos/music_agent.git
cd music_agent
```

**2.2. Criar e ativar o ambiente virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

**2.3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**2.4. Configurar as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto contendo a chave de API do provedor selecionado:

```env
GOOGLE_API_KEY=sua_chave_do_google_ai_studio_aqui
```

### 3. Execução da Aplicação

Inicie o servidor local da interface Streamlit:

```bash
streamlit run app.py
```

Em seguida, acesse a interface gráfica no navegador: <http://localhost:8501>

---

## 🏗️ Justificativa das Decisões Técnicas

| Componente | Tecnologia | Justificativa |
|---|---|---|
| **Framework de agentes** | LangChain | Maturidade na orquestração de ferramentas (`create_tool_calling_agent` e `AgentExecutor`), com integração nativa entre chamadas SQL, busca vetorial RAG e gerenciamento do histórico de conversação. |
| **Provedor de LLM** | `gemini-3.8-flash` / `gemini-2.0-flash` via `langchain-google-genai` | Alta velocidade de resposta, suporte robusto a *tool-calling* e capacidade de raciocínio contextual para manter a persona. |
| **Retrieval (RAG)** | Chroma + FastEmbed | Busca vetorial das políticas internas da loja. O modelo de embeddings local, com vetor indexado em memória, garante respostas instantâneas para regras de devolução e garantia e reduz chamadas desnecessárias à API da LLM. |
| **Prompting e persona** | `SYSTEM_PROMPT` em `src/agent.py` | Define o tom de voz amigável e apaixonado por música, a instrução de consultar as ferramentas antes de responder dados de estoque/pedidos e a trava estrita contra venda de acessórios (cordas, cabos, amplificadores) e temas fora do escopo. |
| **Interface e estilização** | Streamlit + CSS externo | Estilos desacoplados em `src/style.css`, mantendo o código Python limpo. Inclui animação de equalizador no carregamento inicial, barra lateral informativa e cartões com atalhos de teste rápido. |
| **Desempenho e cache** | `@st.cache_resource` | Aplicado no carregamento da base de dados e do vetor RAG em `app.py`, evitando que reinicializações da página reconectem o SQLite ou reindexem documentos a cada interação. |

---

## ⚠️ Limitações Conhecidas e Evoluções Futuras

### Limitações Conhecidas

- **Rate limits do plano gratuito (Free Tier):** a cota da API gratuita do Google AI Studio impõe restrições de requisições por minuto (RPM) e por dia (RPD), o que pode causar exceções temporárias de cota (`429 RESOURCE_EXHAUSTED`) ou instabilidade por alta demanda (`503 UNAVAILABLE`).
- **Truncamento do histórico de memória:** para otimizar a velocidade de resposta e conter o consumo de tokens por requisição, o histórico enviado à LLM é limitado às **últimas 4 mensagens** ativas da sessão.

### O que seria feito com mais tempo

- **Fallback multiprovedor:** suporte automático para alternar entre provedores (ex.: Groq, OpenAI ou modelos locais) em caso de oscilações na API principal.
- **Persistência de sessões:** substituição do estado local do Streamlit por um banco de sessões (ex.: Redis ou PostgreSQL) para manter históricos contínuos entre múltiplos acessos.
- **Suíte de testes automatizados:** testes unitários e de integração com `pytest` para validar o roteamento das ferramentas SQL e RAG e as travas de escopo.

---

## 🤖 Uso de Assistentes de Código e Workflow

Durante o desenvolvimento, utilizou-se o **Gemini AI Plus** (integrado a LLMs de apoio ao desenvolvimento) como copiloto de engenharia de software.

| Área | Contribuição |
|---|---|
| **Arquitetura e refatoração** | Separação de responsabilidades (desacoplamento do CSS para `src/style.css`), otimização dos payloads de histórico de chat e organização de diretórios. |
| **Resolução de problemas e debugging** | Diagnóstico ágil de erros de execução (`httpx.ReadTimeout`, limites de taxa `429` e instabilidades `503`), orientando o ajuste de *timeout*, retentativas e `max_iterations` no `AgentExecutor`. |
| **Padronização e documentação** | Apoio na escrita de comentários explicativos em inglês no código, na documentação técnica e nos exemplos de conversa em Markdown. |

---

## 📸 Exemplos de Interação e Demonstração do Agente

O repositório inclui registros completos das conversas e capturas de tela do Tom em funcionamento, cobrindo cenários variados de atendimento:

| Cenário | Descrição |
|---|---|
| 🎸 **Consulta de catálogo (SQL)** | Busca de violões disponíveis até R$ 1.000, com filtro dinâmico de preços. |
| 📦 **Consulta de pedidos (SQL)** | Verificação em tempo real do status e rastreamento de um pedido pelo código. |
| 📜 **Políticas da loja (RAG)** | Esclarecimento de dúvidas sobre regras de devolução e direito de arrependimento. |
| 🚫 **Restrição de escopo** | Recusa amigável de solicitações de acessórios (cordas, amplificadores), mantendo o foco exclusivo em instrumentos musicais. |

Os arquivos de imagens completas da interface estão organizados em:

📁 [`docs/conversation_examples/screenshots`](docs/conversation_examples/)
