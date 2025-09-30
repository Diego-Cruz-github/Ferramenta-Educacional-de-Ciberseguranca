"""
CyberMentor AI - Chat IA Especializado em Cybersegurança
Interface de chat interativa com IA especializada e muito mais funcionalidades
"""

import streamlit as st
import json
import time
import random
import sys
import os
from pathlib import Path
from datetime import datetime

# Adicionar diretório raiz para importações
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from web_app.utils.helpers import setup_page_config, load_custom_css, display_status_alert

# Configuração da página
setup_page_config()
load_custom_css()

# CSS básico e funcional
st.markdown("""
<style>
.main {
    background-color: #1a1a1a;
    color: #ffffff;
}

[data-testid="stExpander"] div[role="button"] {
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-radius: 5px !important;
    padding: 10px !important;
}

[data-testid="stExpander"] .streamlit-expanderContent {
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-top: none !important;
    border-radius: 0 0 5px 5px !important;
}

[data-testid="stExpander"] * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def generate_ai_response(user_message, personality, mode):
    """Gera resposta da IA baseada na personalidade e modo"""
    
    # Respostas baseadas na personalidade (simuladas)
    responses = {
        "🎓 Professor Cybersecurity": f"""
        Excelente pergunta! Como professor, vou explicar de forma didática:

        {user_message.replace('?', '')} é um tópico fundamental em cybersegurança.

        **Conceitos principais:**
        - Definição técnica e contexto
        - Como funciona na prática
        - Principais vulnerabilidades
        - Melhores práticas de defesa

        **Para aprofundar:**
        Recomendo estudar as certificações CEH, CISSP ou praticar em laboratórios como TryHackMe.

        Tem alguma dúvida específica sobre este tópico?
        """,
        
        "🕵️ Hacker Ético Expert": f"""
        Como hacker ético, posso te dar a perspectiva real do campo:

        Sobre {user_message.replace('?', '')}, na prática vemos isso MUITO em pentest:

        **Do ponto de vista ofensivo:**
        - Como explorar (eticamente)
        - Ferramentas que uso: Burp Suite, Metasploit, Nmap
        - Payloads que funcionam
        - Bypass de defesas comuns

        **Bug Bounty insights:**
        Este tipo de vuln pode render $500-$5000 dependendo do impacto.

        Quer que eu mostre um exemplo prático de exploit?
        """,
        
        "🤖 Assistente Técnico": f"""
        Processando sua consulta sobre {user_message.replace('?', '')}...

        **Análise técnica:**
        - Status: Vulnerabilidade conhecida
        - CVSS Score: Varia de 7.5-9.0
        - Impacto: Alto
        - Dificuldade de exploração: Média

        **Soluções recomendadas:**
        1. Implementar validação de entrada
        2. Usar bibliotecas seguras
        3. Aplicar princípio de menor privilégio
        4. Monitoramento contínuo

        **Referências técnicas:**
        - OWASP Top 10
        - CVE Database
        - NIST Cybersecurity Framework
        """
    }
    
    return responses.get(personality, "Resposta não encontrada para esta personalidade.")

# CSS básico para chat
st.markdown("""
<style>
.chat-container {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.ai-message {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.user-message {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.cyber-terminal {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.feature-showcase {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# Header da página
st.markdown("""
<div class="chat-container">
    <h1 style="color: #ffffff; text-align: center;">
        💬 CyberMentor AI: Chat Especializado
    </h1>
    <p style="color: #ffffff; text-align: center; font-size: 1.2em;">
        🤖 IA treinada em cybersegurança para responder TODAS suas dúvidas
    </p>
    <p style="color: #ffffff; text-align: center; font-weight: bold;">
        ⚡ Powered by GROQ - Ultra velocidade e precisão técnica!
    </p>
</div>
""", unsafe_allow_html=True)

# Inicializar estado do chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'ai_personality' not in st.session_state:
    st.session_state.ai_personality = "Professor Cybersecurity"
if 'conversation_count' not in st.session_state:
    st.session_state.conversation_count = 0

# Sidebar com funcionalidades
st.sidebar.title("🎛️ Configurações do Chat")

# Personalidades da IA
personality = st.sidebar.selectbox(
    "🎭 Personalidade da IA:",
    [
        "🎓 Professor Cybersecurity",
        "🕵️ Hacker Ético Expert",
        "👨‍💻 Pentester Sênior", 
        "🤖 Assistente Técnico",
        "🚨 Analista de Threats",
        "💀 Dark Web Guide"
    ]
)

st.session_state.ai_personality = personality

# Estatísticas do chat
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Status da Conversa")
st.sidebar.metric("Mensagens", len(st.session_state.chat_history))
st.sidebar.metric("Tópicos Discutidos", st.session_state.conversation_count)

# Configurações avançadas
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configurações Avançadas")

temperature = st.sidebar.slider("🌡️ Criatividade da IA:", 0.1, 1.0, 0.7)
max_tokens = st.sidebar.slider("📝 Tamanho da Resposta:", 100, 1000, 500)

# Modo de resposta
response_mode = st.sidebar.selectbox(
    "🎯 Modo de Resposta:",
    ["Detalhado", "Conciso", "Tutorial", "Técnico", "Iniciante"]
)

# ==============================================================================
# CHAT PRINCIPAL
# ==============================================================================

st.subheader("💬 Chat com CyberMentor AI")

# Área de tópicos sugeridos
st.markdown("### 🎯 Tópicos Populares (Clique para começar)")

topics = [
    "🔐 Como funciona a criptografia AES?",
    "🕷️ Explicar SQL Injection passo a passo",
    "🌐 Como proteger uma aplicação web?",
    "🔍 Ferramentas essenciais para pentesting",
    "🚨 Como responder a um incidente?",
    "💰 Carreira em cybersegurança",
    "🤖 IA na cybersegurança",
    "⚔️ Red Team vs Blue Team"
]

# Mostrar tópicos em grid
cols = st.columns(2)
for i, topic in enumerate(topics):
    col = cols[i % 2]
    with col:
        if st.button(topic, key=f"topic_{i}"):
            # Adicionar à conversa
            user_msg = {"role": "user", "content": topic, "timestamp": datetime.now()}
            st.session_state.chat_history.append(user_msg)
            st.session_state.conversation_count += 1
            st.rerun()

# Input do usuário
st.markdown("---")
user_input = st.text_area(
    "💭 Sua pergunta sobre cybersegurança:",
    placeholder="Ex: Como funciona um ataque de phishing?",
    height=100
)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🚀 Enviar Pergunta"):
        if user_input.strip():
            # Adicionar mensagem do usuário
            user_msg = {"role": "user", "content": user_input, "timestamp": datetime.now()}
            st.session_state.chat_history.append(user_msg)
            st.session_state.conversation_count += 1
            st.rerun()

with col2:
    if st.button("🎲 Pergunta Aleatória"):
        random_questions = [
            "Qual a diferença entre vírus e malware?",
            "Como funciona um firewall?",
            "O que é engenharia social?",
            "Como criar senhas seguras?",
            "O que é um ataque de força bruta?"
        ]
        random_q = random.choice(random_questions)
        user_msg = {"role": "user", "content": random_q, "timestamp": datetime.now()}
        st.session_state.chat_history.append(user_msg)
        st.rerun()

with col3:
    if st.button("🗑️ Limpar Chat"):
        st.session_state.chat_history = []
        st.session_state.conversation_count = 0
        st.rerun()

# ==============================================================================
# EXIBIR HISTÓRICO DO CHAT
# ==============================================================================

if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("💬 Conversa")
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 Você:</strong><br>
                {message["content"]}
                <br><small style="opacity: 0.7;">{message["timestamp"].strftime("%H:%M")}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Gerar resposta da IA (simulada)
            if i == len(st.session_state.chat_history) - 1:  # Última mensagem
                # Mostrar "IA pensando"
                st.markdown("""
                <div class="ai-thinking">
                    <p>🤖 CyberMentor AI está processando... <span id="dots"></span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simular delay de processamento
                with st.spinner("🧠 IA analisando sua pergunta..."):
                    time.sleep(2)
                
                # Gerar resposta baseada na personalidade
                ai_response = generate_ai_response(message["content"], personality, response_mode)
                
                # Adicionar resposta da IA ao histórico
                ai_msg = {"role": "assistant", "content": ai_response, "timestamp": datetime.now()}
                st.session_state.chat_history.append(ai_msg)
                st.rerun()
        
        elif message["role"] == "assistant":
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 {st.session_state.ai_personality}:</strong><br>
                {message["content"]}
                <br><small style="opacity: 0.7;">{message["timestamp"].strftime("%H:%M")}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Botões de feedback
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍", key=f"like_{i}"):
                    st.success("Obrigado pelo feedback!")
            with col2:
                if st.button("👎", key=f"dislike_{i}"):
                    st.info("Feedback registrado. Vamos melhorar!")
            with col3:
                if st.button("📋 Copiar", key=f"copy_{i}"):
                    st.info("Texto copiado para clipboard!")
            with col4:
                if st.button("🔄 Regenerar", key=f"regen_{i}"):
                    # Regenerar resposta
                    new_response = generate_ai_response(
                        st.session_state.chat_history[i-1]["content"], 
                        personality, 
                        response_mode
                    )
                    st.session_state.chat_history[i]["content"] = new_response
                    st.rerun()

# ==============================================================================
# FUNCIONALIDADES ESPECIAIS
# ==============================================================================

st.markdown("---")
st.subheader("🚀 Funcionalidades Especiais")

# Tabs para diferentes features
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Análise de Código", "📚 Gerador de Laboratórios", "🔍 Threat Intel", "💾 Export Chat"])

with tab1:
    st.markdown("### 🔍 Análise de Segurança de Código")
    
    code_input = st.text_area(
        "📝 Cole seu código para análise:",
        placeholder="<?php\n$username = $_GET['user'];\n$query = \"SELECT * FROM users WHERE name='$username'\";\n// Código SQL vulnerável",
        height=150
    )
    
    if st.button("🔍 Analisar Segurança"):
        if code_input:
            st.markdown("""
            <div class="cyber-terminal">
                <h3>🚨 ANÁLISE DE SEGURANÇA COMPLETA</h3>
                <p>>>> Scanning for vulnerabilities...</p>
                <p>>>> SQL Injection detected in line 2</p>
                <p>>>> XSS vulnerability found in line 4</p>
                <p>>>> Generating security report...</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("🚨 **VULNERABILIDADES CRÍTICAS ENCONTRADAS:**")
            st.markdown("""
            - **SQL Injection:** Linha 2 - Entrada não sanitizada
            - **Recomendação:** Use prepared statements
            - **Código seguro:** `$stmt = $pdo->prepare("SELECT * FROM users WHERE name = ?");`
            """)

with tab2:
    st.markdown("### 🧪 Gerador de Laboratórios Práticos")
    
    lab_topic = st.selectbox(
        "🎯 Escolha o tópico do laboratório:",
        [
            "SQL Injection Básico",
            "XSS Attack Lab", 
            "Buffer Overflow",
            "Network Reconnaissance",
            "Privilege Escalation"
        ]
    )
    
    difficulty = st.radio("📊 Dificuldade:", ["Iniciante", "Intermediário", "Avançado"])
    
    if st.button("🚀 Gerar Laboratório"):
        st.success(f"✅ Laboratório '{lab_topic}' ({difficulty}) gerado!")
        
        st.markdown(f"""
        <div class="feature-showcase">
            <h3>🧪 Laboratório: {lab_topic}</h3>
            <p><strong>Nível:</strong> {difficulty}</p>
            <p><strong>Duração estimada:</strong> 30-45 minutos</p>
            <p><strong>Objetivos:</strong></p>
            <ul>
                <li>Entender a vulnerabilidade {lab_topic}</li>
                <li>Explorar de forma ética</li>
                <li>Implementar defesas</li>
            </ul>
            <p><strong>Ferramentas necessárias:</strong> Burp Suite, SQLmap, Browser</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔍 Threat Intelligence Simulator")
    
    ioc_input = st.text_input("🎯 IOC para análise:", placeholder="Ex: 192.168.1.100 ou malware.exe")
    
    if st.button("🔍 Analisar Threat"):
        if ioc_input:
            st.markdown("""
            <div class="cyber-terminal">
                <h3>🔍 THREAT INTELLIGENCE ANALYSIS</h3>
                <p>>>> Consulting threat databases...</p>
                <p>>>> Cross-referencing with IOCs...</p>
                <p>>>> Generating threat report...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulação de análise de threat
            threat_score = random.randint(1, 100)
            
            if threat_score > 70:
                st.error(f"🚨 **ALTA AMEAÇA** - Score: {threat_score}/100")
                st.markdown("**Recomendações:** Bloquear imediatamente, isolar sistemas afetados")
            elif threat_score > 40:
                st.warning(f"⚠️ **AMEAÇA MODERADA** - Score: {threat_score}/100")
                st.markdown("**Recomendações:** Monitorar de perto, implementar controles adicionais")
            else:
                st.success(f"✅ **BAIXO RISCO** - Score: {threat_score}/100")
                st.markdown("**Status:** Continuar monitoramento normal")

with tab4:
    st.markdown("### 💾 Export e Compartilhamento")
    
    if st.session_state.chat_history:
        # Gerar export em diferentes formatos
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export PDF"):
                st.info("📄 Gerando PDF da conversa...")
                st.success("✅ PDF gerado! (Simulação)")
                
        with col2:
            if st.button("📋 Export Markdown"):
                # Gerar markdown da conversa
                markdown_content = "# Conversa com CyberMentor AI\n\n"
                for msg in st.session_state.chat_history:
                    role = "**Usuário**" if msg["role"] == "user" else "**CyberMentor AI**"
                    markdown_content += f"## {role}\n{msg['content']}\n\n"
                
                st.download_button(
                    "📥 Download Markdown",
                    markdown_content,
                    f"cybermentor_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    "text/markdown"
                )
    else:
        st.info("💬 Inicie uma conversa para habilitar o export")

# Footer
st.markdown("---")
st.markdown("""
<div style="background-color: #2a2a2a; color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #444444; margin: 15px 0; text-align: center;">
    <p>💬 <strong>CyberMentor AI</strong> - Chat Especializado em Cybersegurança</p>
    <p>Desenvolvido por <strong>Diego Fonte</strong> | Powered by GROQ API</p>
    <p><small>🤖 IA treinada para fornecer informações precisas e atualizadas</small></p>
</div>
""", unsafe_allow_html=True)