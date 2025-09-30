"""
CyberMentor AI - Funções utilitárias para interface web
Helpers e configurações compartilhadas entre módulos
"""

import streamlit as st

def setup_page_config():
    """Configura as definições básicas da página Streamlit"""
    if not hasattr(st, '_is_page_config_set'):
        st.set_page_config(
            page_title="CyberMentor AI - Cibersegurança",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st._is_page_config_set = True

def load_custom_css():
    """Carrega CSS personalizado com tema cybersecurity"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Variáveis de cores cyberpunk MELHORADAS */
    :root {
        --cyber-green: #00ff88;
        --cyber-blue: #00aaff;
        --cyber-purple: #aa00ff;
        --cyber-orange: #ff8800;
        --dark-bg: #0a0a0a;
        --darker-bg: #121212;
        --card-bg: #1e1e1e;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
        --text-tertiary: #999999;
    }

    /* Background com efeito Matrix */
    .stApp {
        background: linear-gradient(45deg, #0f0f23, #1a1a2e, #16213e);
        background-size: 400% 400%;
        animation: matrixGlow 10s ease infinite;
    }

    @keyframes matrixGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Header principal com efeito cyberpunk */
    .main-header {
        background: linear-gradient(45deg, var(--dark-bg), var(--darker-bg), var(--card-bg));
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        color: var(--cyber-green);
        font-family: 'Orbitron', monospace;
        border: 2px solid var(--cyber-green);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 65, 0.1), transparent);
        animation: scanLine 3s linear infinite;
    }

    @keyframes scanLine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }

    .main-title {
        font-size: 3em;
        text-shadow: 0 0 20px var(--cyber-green);
        margin-bottom: 10px;
        animation: textGlow 2s ease-in-out infinite alternate;
    }

    @keyframes textGlow {
        from { text-shadow: 0 0 20px var(--cyber-green); }
        to { text-shadow: 0 0 30px var(--cyber-green), 0 0 40px var(--cyber-green); }
    }

    .main-subtitle {
        font-size: 1.2em;
        color: var(--cyber-blue);
        margin: 0;
    }

    /* Cards com animações cyber */
    .cyber-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 1px solid var(--cyber-blue);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .cyber-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 102, 255, 0.4);
        border-color: var(--cyber-green);
    }

    .cyber-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.2), transparent);
        transition: left 0.5s;
    }

    .cyber-card:hover::after {
        left: 100%;
    }

    /* Botões cyber */
    .stButton > button {
        background: linear-gradient(45deg, var(--cyber-blue), var(--cyber-purple));
        color: white;
        border: 2px solid var(--cyber-green);
        border-radius: 25px;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        padding: 15px 30px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, var(--cyber-green), var(--cyber-blue));
        box-shadow: 0 0 25px var(--cyber-green);
        transform: scale(1.05);
    }

    /* Métricas com efeito cyber */
    .metric-container {
        background: rgba(0, 255, 65, 0.1);
        border: 1px solid var(--cyber-green);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 65, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 65, 0.6); }
    }

    /* Sidebar cyber com MELHOR VISIBILIDADE */
    .css-1d391kg, .css-1l02zno, .css-17eq0hr {
        background: linear-gradient(180deg, var(--dark-bg), var(--darker-bg)) !important;
        border-right: 3px solid var(--cyber-green) !important;
    }
    
    .sidebar .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.9) !important;
        border: 2px solid var(--cyber-blue) !important;
        color: var(--text-primary) !important;
    }
    
    .sidebar .element-container {
        background: rgba(0, 255, 136, 0.05) !important;
        border-radius: 8px !important;
        padding: 5px !important;
        margin: 5px 0 !important;
    }
    
    .sidebar .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .sidebar .stTitle {
        color: var(--cyber-green) !important;
        text-shadow: 0 0 10px var(--cyber-green) !important;
    }

    /* Alertas com estilo cyber */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid var(--cyber-orange);
        background: rgba(255, 107, 53, 0.1);
    }

    /* Dataframes com tema cyber */
    .stDataFrame {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        border: 1px solid var(--cyber-blue);
    }

    /* Código com tema matrix */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid var(--cyber-green);
        border-radius: 5px;
    }

    /* Footer cyber */
    .footer {
        background: linear-gradient(145deg, var(--darker-bg), var(--card-bg));
        color: var(--cyber-green);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid var(--cyber-green);
        margin-top: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
    }

    .footer a {
        color: var(--cyber-orange);
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .footer a:hover {
        color: white;
        text-shadow: 0 0 10px var(--cyber-orange);
    }

    /* Animação de loading cyber */
    .cyber-loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 255, 65, 0.3);
        border-radius: 50%;
        border-top-color: var(--cyber-green);
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Efeito de typing */
    .typing-effect {
        overflow: hidden;
        border-right: 2px solid var(--cyber-green);
        white-space: nowrap;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: var(--cyber-green); }
    }

    /* Elementos específicos do Streamlit com MELHOR CONTRASTE */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid var(--cyber-blue) !important;
        border-radius: 10px;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
        background: rgba(0, 0, 0, 0.9) !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: var(--text-primary) !important;
        background: rgba(0, 0, 0, 0.9) !important;
    }
    
    .stSelectbox label {
        color: var(--cyber-green) !important;
        font-weight: bold !important;
    }

    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid var(--cyber-blue) !important;
        border-radius: 10px;
        color: var(--text-primary) !important;
        font-size: 16px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-tertiary) !important;
    }
    
    .stTextInput label {
        color: var(--cyber-green) !important;
        font-weight: bold !important;
    }

    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid var(--cyber-green) !important;
        border-radius: 10px;
        color: var(--text-primary) !important;
        font-family: 'Courier New', monospace;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-tertiary) !important;
    }
    
    .stTextArea label {
        color: var(--cyber-green) !important;
        font-weight: bold !important;
    }

    /* Progresso com tema cyber */
    .stProgress .st-bo {
        background: var(--cyber-green);
        box-shadow: 0 0 10px var(--cyber-green);
    }

    /* Tabs com estilo cyber */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 102, 255, 0.1);
        border: 1px solid var(--cyber-blue);
        color: var(--cyber-blue);
        font-family: 'Orbitron', monospace;
    }

    .stTabs [aria-selected="true"] {
        background: var(--cyber-green);
        color: black;
        box-shadow: 0 0 15px var(--cyber-green);
    }
    
    /* Dropdown options com MELHOR CONTRASTE */
    .stSelectbox ul {
        background: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid var(--cyber-blue) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox li {
        color: var(--text-primary) !important;
        background: rgba(0, 0, 0, 0.9) !important;
        padding: 10px !important;
        border-bottom: 1px solid var(--cyber-blue) !important;
    }
    
    .stSelectbox li:hover {
        background: var(--cyber-blue) !important;
        color: white !important;
        transform: scale(1.02) !important;
    }
    
    /* Número de input melhorado */
    .stNumberInput > div > div > input {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid var(--cyber-orange) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    .stNumberInput label {
        color: var(--cyber-orange) !important;
        font-weight: bold !important;
    }
    
    /* Radio buttons melhorados */
    .stRadio > div {
        background: rgba(0, 255, 136, 0.05) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    .stRadio label {
        color: var(--cyber-green) !important;
        font-weight: bold !important;
    }
    
    .stRadio div[role="radiogroup"] > label {
        color: var(--text-primary) !important;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_status_alert(alert_type, message):
    """Exibe alertas com estilo cybersecurity"""
    if alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)
    elif alert_type == "info":
        st.info(message)

def create_cyber_metric(label, value, delta=None, help_text=None):
    """Cria métricas com estilo cyberpunk"""
    st.markdown(f"""
    <div class="metric-container">
        <div style="color: var(--cyber-green); font-family: 'Orbitron', monospace; font-size: 0.8em;">
            {label}
        </div>
        <div style="color: white; font-size: 2em; font-weight: bold; margin: 10px 0;">
            {value}
        </div>
        {f'<div style="color: var(--cyber-blue); font-size: 0.9em;">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def create_cyber_card(title, content, icon="🔐"):
    """Cria cards com estilo cybersecurity"""
    st.markdown(f"""
    <div class="cyber-card">
        <h3 style="color: var(--cyber-green); font-family: 'Orbitron', monospace;">
            {icon} {title}
        </h3>
        <div style="color: white; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_typing_effect(text):
    """Mostra texto com efeito de digitação"""
    st.markdown(f"""
    <div class="typing-effect" style="color: var(--cyber-green); font-family: 'Orbitron', monospace; font-size: 1.2em;">
        {text}
    </div>
    """, unsafe_allow_html=True)

def cyber_loading_animation():
    """Mostra animação de loading cyberpunk"""
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div class="cyber-loading"></div>
        <p style="color: var(--cyber-green); margin-top: 10px; font-family: 'Orbitron', monospace;">
            Processando dados...
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_hacker_section():
    """Cria seção sobre hacking ético"""
    st.markdown("""
    <div class="cyber-card">
        <h2 style="color: var(--cyber-green); font-family: 'Orbitron', monospace; text-align: center;">
            🕵️‍♂️ Por que Precisamos de Hackers Éticos?
        </h2>
        
        <div style="color: white; line-height: 1.8; font-size: 1.1em;">
            <p><strong style="color: var(--cyber-orange);">Hackers Éticos</strong> são os <strong>guardiões digitais</strong> do nosso mundo conectado. Eles usam as mesmas técnicas dos criminosos, mas para <strong>PROTEGER</strong> ao invés de atacar.</p>
            
            <h3 style="color: var(--cyber-blue);">🛡️ O que fazem?</h3>
            <ul>
                <li><strong>Penetration Testing:</strong> Simulam ataques reais para encontrar vulnerabilidades</li>
                <li><strong>Bug Bounty:</strong> Caçam falhas em sistemas para empresas como Google, Facebook</li>
                <li><strong>Security Research:</strong> Descobrem novas ameaças antes dos criminosos</li>
                <li><strong>Incident Response:</strong> Combatem ataques em tempo real</li>
            </ul>
            
            <h3 style="color: var(--cyber-blue);">💰 Por que é crucial?</h3>
            <ul>
                <li><strong>Prejuízos evitados:</strong> Um hack pode custar até $10 milhões</li>
                <li><strong>Reputação preservada:</strong> Vazamentos destroem confiança do cliente</li>
                <li><strong>Conformidade legal:</strong> LGPD, GDPR exigem proteção de dados</li>
                <li><strong>Continuidade do negócio:</strong> Evita paralisações custosas</li>
            </ul>
            
            <div style="background: rgba(255, 107, 53, 0.1); padding: 20px; border-radius: 10px; border-left: 4px solid var(--cyber-orange); margin: 20px 0;">
                <h4 style="color: var(--cyber-orange);">⚡ Fato Impressionante:</h4>
                <p>Um hacker ético pode ganhar <strong>mais de $500,000/ano</strong> e receber até <strong>$1 milhão</strong> por encontrar uma única vulnerabilidade crítica em grandes empresas!</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_protection_tips():
    """Cria seção com dicas de proteção do computador"""
    st.markdown("""
    <div class="cyber-card">
        <h2 style="color: var(--cyber-green); font-family: 'Orbitron', monospace; text-align: center;">
            🛡️ Como Proteger Seu Computador: Guia Definitivo
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="background: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 10px; border: 1px solid var(--cyber-green);">
                <h3 style="color: var(--cyber-green);">🔐 Proteção Básica</h3>
                <ul style="color: white;">
                    <li><strong>Antivírus atualizado:</strong> Windows Defender + Malwarebytes</li>
                    <li><strong>Firewall ativo:</strong> Bloqueia conexões suspeitas</li>
                    <li><strong>Updates automáticos:</strong> Sistema e programas sempre atualizados</li>
                    <li><strong>Senhas fortes:</strong> 12+ caracteres, únicos por site</li>
                    <li><strong>2FA obrigatório:</strong> Autenticação em duas etapas</li>
                </ul>
            </div>
            
            <div style="background: rgba(0, 102, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid var(--cyber-blue);">
                <h3 style="color: var(--cyber-blue);">🌐 Navegação Segura</h3>
                <ul style="color: white;">
                    <li><strong>HTTPS obrigatório:</strong> Só acesse sites com cadeado</li>
                    <li><strong>Downloads confiáveis:</strong> Apenas sites oficiais</li>
                    <li><strong>Email suspeito:</strong> NUNCA clique em links duvidosos</li>
                    <li><strong>WiFi público:</strong> Use VPN sempre</li>
                    <li><strong>Extensões seguras:</strong> uBlock Origin, HTTPS Everywhere</li>
                </ul>
            </div>
            
            <div style="background: rgba(102, 0, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid var(--cyber-purple);">
                <h3 style="color: var(--cyber-purple);">💾 Backup e Recovery</h3>
                <ul style="color: white;">
                    <li><strong>Regra 3-2-1:</strong> 3 cópias, 2 mídias, 1 offsite</li>
                    <li><strong>Backup automático:</strong> Google Drive, OneDrive</li>
                    <li><strong>Teste de restore:</strong> Verifique se funciona</li>
                    <li><strong>Criptografia:</strong> Dados sensíveis criptografados</li>
                    <li><strong>Versioning:</strong> Múltiplas versões dos arquivos</li>
                </ul>
            </div>
            
            <div style="background: rgba(255, 107, 53, 0.1); padding: 20px; border-radius: 10px; border: 1px solid var(--cyber-orange);">
                <h3 style="color: var(--cyber-orange);">🚨 Detecção de Ameaças</h3>
                <ul style="color: white;">
                    <li><strong>Monitor de rede:</strong> Glasswire, Wireshark</li>
                    <li><strong>Behavioral analysis:</strong> Processos suspeitos</li>
                    <li><strong>Log monitoring:</strong> Event Viewer no Windows</li>
                    <li><strong>Performance alerts:</strong> CPU/RAM anômalos</li>
                    <li><strong>Scan regular:</strong> Verificação semanal completa</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(45deg, rgba(255, 0, 0, 0.1), rgba(255, 107, 53, 0.1)); padding: 20px; border-radius: 10px; border: 2px solid red; margin: 20px 0;">
            <h3 style="color: red; text-align: center;">🚨 SINAIS DE COMPROMISSO</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <h4 style="color: var(--cyber-orange);">⚠️ Sintomas Críticos:</h4>
                    <ul style="color: white;">
                        <li>Lentidão súbita inexplicável</li>
                        <li>Programas abrindo sozinhos</li>
                        <li>Arquivos modificados/deletados</li>
                        <li>Tráfego de rede anômalo</li>
                        <li>Senhas não funcionando</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: var(--cyber-orange);">🔥 Ação Imediata:</h4>
                    <ul style="color: white;">
                        <li>Desconectar da internet</li>
                        <li>Scan completo antivírus</li>
                        <li>Verificar contas online</li>
                        <li>Trocar senhas importantes</li>
                        <li>Contatar suporte técnico</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)