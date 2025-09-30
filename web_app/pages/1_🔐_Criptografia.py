"""
CyberMentor AI - Módulo de Criptografia
Laboratório interativo e gamificado para aprendizado de conceitos criptográficos
"""

import streamlit as st
import hashlib
import secrets
import string
import bcrypt
from cryptography.fernet import Fernet
import base64
import random
import time
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

# CSS SÓ PARA DEIXAR LETRAS VISÍVEIS
st.markdown("""
<style>
/* CSS básico apenas para texto visível */
.main {
    background-color: #1a1a1a;
    color: #ffffff;
}

.game-card {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.crypto-header {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    text-align: center;
    margin: 15px 0;
}

.mini-game {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.hash-result {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.crime-story {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.interactive-demo {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.footer {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
    text-align: center;
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

/* FORÇA TEXTO BRANCO EM TUDO */
.main * {
    color: #ffffff !important;
}

/* Corrigir HTML inline visível */
.crime-story * {
    color: #ffffff !important;
}

.crime-story h3, .crime-story h4 {
    color: #00ff88 !important;
}

.crime-story strong {
    color: #00ff88 !important;
}

/* Todos os elementos inline HTML */
div[style*="background"] * {
    color: #ffffff !important;
}

/* FORÇA HTML a renderizar corretamente */
[data-testid="stMarkdown"] {
    color: #ffffff !important;
}

[data-testid="stMarkdown"] * {
    color: #ffffff !important;
}

/* Força renderização correta em markdown */
[data-testid="stMarkdown"] h3, [data-testid="stMarkdown"] h4 {
    color: #00ff88 !important;
}

[data-testid="stMarkdown"] strong {
    color: #00ff88 !important;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="crypto-header">
    <h1>🔐 Laboratório Interativo de Criptografia</h1>
    <p><strong>Desvendando os Segredos da Criptografia através de Jogos e Demonstrações Práticas</strong></p>
    <p>🎯 Aprenda brincando | 🧩 Resolva desafios | 🔍 Descubra casos reais</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com navegação
st.sidebar.title("🎮 Menu de Atividades")
atividade = st.sidebar.selectbox(
    "👉 **Clique em uma opção abaixo para começar:**",
    [
        "🏠 Introdução à Criptografia",
        "🎯 Jogo: Hash Detective",
        "🔑 Laboratório de Senhas",
        "🎮 Criptografia Simétrica",
        "🕵️ Casos Criminais Famosos",
        "📺 Mr. Robot: Realidade vs Ficção",
        "🔴 Matrix: Realidade vs Ficção",
        "📺 Black Mirror: Tecnologia vs Humanidade",
        "🔬 Computação Quântica: O Futuro da Criptografia",
        "💰 Big Tech: Investimentos Bilionários",
        "₿ Criptomoedas: Revolução Financeira Digital",
        "🎬 O Jogo da Imitação: Criptografia na Guerra",
        "⚔️ Cybersegurança nas Guerras Modernas",
        "🕵️‍♂️ Hackers Éticos: Guardiões Digitais",
        "🛡️ Protegendo Seu Computador",
        "🎮 Easter Egg: Hack the Planet",
        "💰 Guerra Cibernética Corporativa",
        "🛡️ Ofensiva vs Preventiva",
        "🏆 Desafio Final"
    ]
)

# Inicializar estados da sessão
if 'pontos_crypto' not in st.session_state:
    st.session_state.pontos_crypto = 0
if 'nivel_usuario' not in st.session_state:
    st.session_state.nivel_usuario = "Iniciante"
if 'missoes_completas' not in st.session_state:
    st.session_state.missoes_completas = []

# Sistema de pontuação
with st.sidebar:
    st.markdown("---")
    st.subheader("🏆 Seu Progresso")
    st.metric("Pontos", st.session_state.pontos_crypto)
    st.metric("Nível", st.session_state.nivel_usuario)
    
    # Barra de progresso
    progresso = len(st.session_state.missoes_completas) / 9
    st.progress(progresso)
    st.write(f"Missões: {len(st.session_state.missoes_completas)}/9")
    
    # Botão de reset
    if st.button("🔄 Resetar Progresso", key="reset_progress"):
        st.session_state.pontos_crypto = 0
        st.session_state.nivel_usuario = "Iniciante"
        st.session_state.missoes_completas = []
        st.success("✅ Progresso resetado!")
        st.rerun()

# ==============================================================================
# INTRODUÇÃO À CRIPTOGRAFIA
# ==============================================================================
if atividade == "🏠 Introdução à Criptografia":
    st.markdown("""
    <div style="background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; border-left: 4px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">🎓 Bem-vindo ao Mundo da Criptografia!</h2>
        <p style="color: #ffffff; font-size: 1.2em; line-height: 1.6;"><strong style="color: #00ff41;">Criptografia</strong> é a arte e ciência de proteger informações através de códigos e algoritmos matemáticos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="mini-game">
            <h4>🔐 O que é?</h4>
            <p><strong>Criptografia</strong> vem do grego:</p>
            <ul>
                <li><strong>Crypto</strong> = Esconder</li>
                <li><strong>Grafia</strong> = Escrita</li>
            </ul>
            <p>Ou seja: <em>"escrita escondida"</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="mini-game">
            <h4>🎯 Para que serve?</h4>
            <ul>
                <li>🔒 Proteger senhas</li>
                <li>💳 Segurança bancária</li>
                <li>📱 Apps como WhatsApp</li>
                <li>🌐 Sites HTTPS</li>
                <li>💰 Criptomoedas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="mini-game">
            <h4>🧩 Tipos principais</h4>
            <ul>
                <li><strong>Hash</strong>: "Impressão digital"</li>
                <li><strong>Simétrica</strong>: 1 chave</li>
                <li><strong>Assimétrica</strong>: 2 chaves</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # História fascinante da criptografia
    st.markdown("""
    <div class="crime-story">
        <h3>📜 Você Sabia? A História da Criptografia</h3>
        <p><strong>Júlio César (50 a.C.)</strong> já usava cifras para mandar mensagens secretas! 
        Ele deslocava cada letra 3 posições: A→D, B→E, C→F...</p>
        <p><strong>1976:</strong> Diffie-Hellman revolucionou tudo com chaves públicas!</p>
        <p><strong>Hoje:</strong> Seu WhatsApp usa AES-256 - a mesma criptografia usada pela CIA! 🕵️</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demonstração interativa super envolvente
    st.markdown("""
    <div class="interactive-demo">
        <h3>🎮 Mini-Demo: Sua Primeira Criptografia!</h3>
        <p>Vamos criar uma "impressão digital" (hash) do seu nome como os hackers fazem:</p>
        <div class="typing-effect">Processando algoritmos criptográficos...</div>
    </div>
    """, unsafe_allow_html=True)
    
    nome_usuario = st.text_input("Digite seu nome:", placeholder="Ex: João Silva")
    
    if nome_usuario:
        hash_md5 = hashlib.md5(nome_usuario.encode()).hexdigest()
        hash_sha256 = hashlib.sha256(nome_usuario.encode()).hexdigest()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="hash-result">
                <h4>🔍 Hash MD5</h4>
                <code>{hash_md5}</code>
                <p><small>32 caracteres hexadecimais</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="hash-result">
                <h4>🛡️ Hash SHA-256</h4>
                <code>{hash_sha256[:32]}...</code>
                <p><small>64 caracteres hexadecimais</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.success("🎉 Parabéns! Você acabou de criar seus primeiros hashes criptográficos!")
        
        if "intro_completa" not in st.session_state.missoes_completas:
            st.session_state.missoes_completas.append("intro_completa")
            st.session_state.pontos_crypto += 10
            st.balloons()

# ==============================================================================
# JOGO: HASH DETECTIVE
# ==============================================================================
elif atividade == "🎯 Jogo: Hash Detective":
    st.markdown("""
    <div class="game-card">
        <h2>🕵️ Hash Detective - Encontre a Mensagem Original!</h2>
        <p>Você é um detetive digital e precisa descobrir qual mensagem gerou este hash...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Curiosidade histórica
    st.markdown("""
    <div class="crime-story">
        <h3>🎯 Curiosidade: O Jogo dos Hackers Reais</h3>
        <p><strong>Kevin Mitnick</strong>, o hacker mais famoso do mundo, foi preso em 1995 após anos sendo procurado pelo FBI. 
        Ele usava técnicas de engenharia social e quebra de hashes para invadir sistemas!</p>
        <p><strong>Anonymous</strong> usa exatamente essa técnica para quebrar senhas em suas operações! 💀</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gerar desafio com sistema de dicas avançado
    if 'hash_atual' not in st.session_state:
        mensagens_com_dicas = [
            ("senha", {
                "inicial": "🔑 Relacionado à proteção de contas",
                "media": "🔒 Você digita isso para entrar no computador",
                "final": "🎯 É o que você usa para fazer login (em português)",
                "explicacao": "A palavra mais básica da segurança digital!"
            }),
            ("hacker", {
                "inicial": "👨‍💻 Profissional de segurança digital",
                "media": "🔍 Especialista que encontra falhas em sistemas", 
                "final": "💻 Palavra em inglês para 'invasor' ou 'especialista'",
                "explicacao": "Pode ser do bem (white hat) ou do mal (black hat)!"
            }),
            ("bitcoin", {
                "inicial": "💰 Moeda digital famosa no mundo todo",
                "media": "₿ Criptomoeda criada por Satoshi Nakamoto",
                "final": "🪙 'Bit' + nome de uma moeda física antiga",
                "explicacao": "A primeira e mais famosa criptomoeda!"
            }),
            ("virus", {
                "inicial": "🦠 Algo que infecta e se espalha",
                "media": "💻 Programa malicioso que danifica computadores",
                "final": "🔬 Mesma palavra da biologia, mas digital",
                "explicacao": "O pesadelo de qualquer usuário de computador!"
            }),
            ("firewall", {
                "inicial": "🔥 Proteção contra ataques digitais",
                "media": "🛡️ Barreira entre sua rede e a internet",
                "final": "🔥 'Fire' + 'wall' (parede de fogo)",
                "explicacao": "Seu guarda-costas digital contra invasões!"
            })
        ]
        escolha = random.choice(mensagens_com_dicas)
        st.session_state.palavra_secreta = escolha[0]
        st.session_state.dicas_hash = escolha[1]
        st.session_state.hash_atual = hashlib.sha256(escolha[0].encode()).hexdigest()
        st.session_state.tentativas_hash = 0
        st.session_state.jogo_resolvido = False
    
    if not st.session_state.jogo_resolvido:
        # Determinar qual dica mostrar baseado nas tentativas
        if st.session_state.tentativas_hash == 0:
            dica_atual = st.session_state.dicas_hash["inicial"]
        elif st.session_state.tentativas_hash <= 2:
            dica_atual = st.session_state.dicas_hash["inicial"]
        elif st.session_state.tentativas_hash <= 4:
            dica_atual = st.session_state.dicas_hash["media"]
        else:
            dica_atual = st.session_state.dicas_hash["final"]
        
        st.markdown(f"""
        <div class="mini-game">
            <h3>🎯 Desafio Hash Detective</h3>
            <p><strong>Hash Misterioso (SHA-256):</strong></p>
            <code style="background: #333; color: #00ff41; padding: 10px; border-radius: 5px; display: block; word-break: break-all;">{st.session_state.hash_atual}</code>
            <p><strong>Dica Atual:</strong> <span style="color: #00ff41;">{dica_atual}</span></p>
            <p><strong>Tentativas:</strong> {st.session_state.tentativas_hash}</p>
        </div>
        """, unsafe_allow_html=True)
        
        tentativa = st.text_input("🔍 Digite sua tentativa (em minúsculas):", key="hash_detective_input")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 Verificar Resposta", type="primary"):
                if tentativa:
                    st.session_state.tentativas_hash += 1
                    hash_tentativa = hashlib.sha256(tentativa.lower().encode()).hexdigest()
                    
                    if hash_tentativa == st.session_state.hash_atual:
                        st.success(f"🎉 **PARABÉNS!** Você descobriu! A palavra era: **{st.session_state.palavra_secreta}**")
                        st.info(f"💡 **Explicação:** {st.session_state.dicas_hash['explicacao']}")
                        
                        pontos_ganhos = max(30 - (st.session_state.tentativas_hash * 3), 10)
                        st.session_state.pontos_crypto += pontos_ganhos
                        st.success(f"🏆 Você ganhou {pontos_ganhos} pontos!")
                        
                        if "hash_detective" not in st.session_state.missoes_completas:
                            st.session_state.missoes_completas.append("hash_detective")
                        
                        st.session_state.jogo_resolvido = True
                        st.balloons()
                    else:
                        st.error("❌ Não foi desta vez! Tente novamente.")
                        st.info(f"💡 Seu hash: `{hash_tentativa[:20]}...`")
        
        with col2:
            if st.button("🔄 Novo Desafio"):
                # Reset para novo jogo
                del st.session_state.hash_atual
                st.rerun()
    else:
        st.success("🎉 **Jogo concluído!** Você é um verdadeiro Hash Detective!")
        if st.button("🎮 Jogar Novamente", type="primary"):
            # Reset completo
            for key in ['hash_atual', 'palavra_secreta', 'dica_secreta', 'tentativas_hash', 'jogo_resolvido']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Explicação educativa
    with st.expander("📚 Como funciona este jogo?"):
        st.markdown("""
        ### 🧠 Conceitos Aprendidos:
        
        **1. Hash é Unidirecional:** É fácil gerar o hash, mas difícil descobrir a mensagem original
        
        **2. Força Bruta:** Estamos tentando várias palavras até encontrar a correta
        
        **3. Segurança por Complexidade:** Senhas complexas geram hashes mais seguros
        
        **4. Verificação de Integridade:** Hashes são usados para verificar se dados não foram alterados
        
        ### 🛡️ Na Vida Real:
        
        • **Senhas:** Sites armazenam hashes, não senhas em texto
        
        • **Downloads:** Verificar se arquivo não foi corrompido
        
        • **Blockchain:** Bitcoin usa SHA-256 para minerar blocos
        """)

# ==============================================================================
# LABORATÓRIO DE SENHAS
# ==============================================================================
elif atividade == "🔑 Laboratório de Senhas":
    st.markdown("""
    <div class="game-card">
        <h2>🔑 Laboratório de Senhas Seguras</h2>
        <p>Descubra como criar e analisar senhas que resistem a ataques!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Teste sua Senha", "🎮 Gerador Inteligente", "💀 Hall da Fama dos Vazamentos"])
    
    with tab1:
        st.markdown("""
        <div style="background: rgba(0,0,0,0.8); padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h3 style="color: #00ff41;">🔍 Analisador de Força de Senhas</h3>
            <p style="color: #ffffff; font-size: 1.1em;">Digite uma senha e veja o quão segura ela é:</p>
        </div>
        """, unsafe_allow_html=True)
        
        senha_teste = st.text_input("Digite uma senha para testar:", type="password", key="senha_analise")
        
        if senha_teste:
            # Análise de força
            pontos = 0
            criterios = []
            
            if len(senha_teste) >= 8:
                pontos += 20
                criterios.append("✅ Tem pelo menos 8 caracteres")
            else:
                criterios.append("❌ Muito curta (menos de 8 caracteres)")
            
            if any(c.islower() for c in senha_teste):
                pontos += 10
                criterios.append("✅ Contém letras minúsculas")
            else:
                criterios.append("❌ Sem letras minúsculas")
            
            if any(c.isupper() for c in senha_teste):
                pontos += 10
                criterios.append("✅ Contém letras maiúsculas")
            else:
                criterios.append("❌ Sem letras maiúsculas")
            
            if any(c.isdigit() for c in senha_teste):
                pontos += 15
                criterios.append("✅ Contém números")
            else:
                criterios.append("❌ Sem números")
            
            if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in senha_teste):
                pontos += 20
                criterios.append("✅ Contém símbolos especiais")
            else:
                criterios.append("❌ Sem símbolos especiais")
            
            if len(senha_teste) >= 12:
                pontos += 15
                criterios.append("✅ Senha longa (12+ caracteres)")
            
            # Verificar padrões comuns
            padroes_ruins = ["123456", "password", "qwerty", "abc", "111", "000"]
            if any(padrao in senha_teste.lower() for padrao in padroes_ruins):
                pontos -= 30
                criterios.append("❌ Contém padrões comuns (123, abc, etc.)")
            
            # Classificação
            if pontos >= 70:
                cor = "🟢"
                classificacao = "MUITO FORTE"
                tempo_quebra = "Centenas de anos"
            elif pontos >= 50:
                cor = "🟡"
                classificacao = "MODERADA"
                tempo_quebra = "Alguns meses"
            elif pontos >= 30:
                cor = "🟠"
                classificacao = "FRACA"
                tempo_quebra = "Algumas semanas"
            else:
                cor = "🔴"
                classificacao = "MUITO FRACA"
                tempo_quebra = "Minutos ou horas"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="hash-result">
                    <h4>{cor} Força da Senha</h4>
                    <h3>{classificacao}</h3>
                    <p><strong>Pontuação:</strong> {pontos}/90</p>
                    <p><strong>Tempo para quebrar:</strong> {tempo_quebra}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: rgba(0,0,0,0.8); padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                    <h4 style="color: #667eea;">📋 Critérios Analisados</h4>
                </div>
                """, unsafe_allow_html=True)
                for criterio in criterios:
                    st.markdown(f"""
                    <p style="color: #ffffff; background: rgba(0,0,0,0.6); padding: 8px; border-radius: 5px; margin: 5px 0;">
                        {criterio}
                    </p>
                    """, unsafe_allow_html=True)
            
            # Hash da senha
            hash_senha = hashlib.sha256(senha_teste.encode()).hexdigest()
            st.markdown(f"""
            <div class="interactive-demo">
                <h4>🔐 Hash SHA-256 da sua senha:</h4>
                <code>{hash_senha}</code>
                <p><small>É assim que sua senha seria armazenada com segurança!</small></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### 🎮 Gerador de Senhas Inteligente
        Crie senhas personalizadas e seguras:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tamanho = st.slider("Tamanho da senha:", 8, 32, 16)
            incluir_maiuscula = st.checkbox("Incluir maiúsculas (A-Z)", True)
            incluir_minuscula = st.checkbox("Incluir minúsculas (a-z)", True)
            incluir_numeros = st.checkbox("Incluir números (0-9)", True)
            incluir_simbolos = st.checkbox("Incluir símbolos (!@#$%)", True)
        
        if st.button("🎲 Gerar Senha"):
            caracteres = ""
            if incluir_minuscula:
                caracteres += string.ascii_lowercase
            if incluir_maiuscula:
                caracteres += string.ascii_uppercase
            if incluir_numeros:
                caracteres += string.digits
            if incluir_simbolos:
                caracteres += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            if caracteres:
                senha_gerada = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
                
                with col2:
                    st.markdown(f"""
                    <div class="hash-result">
                        <h4>🔑 Sua Nova Senha</h4>
                        <h3><code>{senha_gerada}</code></h3>
                        <p><small>Anote em um local seguro!</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Análise automática da senha gerada
                st.success("✅ Senha gerada com sucesso! Ela é criptograficamente segura.")
    
    with tab3:
        st.markdown("""
        <div class="crime-story">
            <h3>💀 Os Maiores Vazamentos de Senhas da História</h3>
            <p>Aprenda com os erros do passado!</p>
        </div>
        """, unsafe_allow_html=True)
        
        vazamentos = [
            {
                "nome": "Yahoo (2013-2014)",
                "usuarios": "3 bilhões de contas",
                "problema": "Senhas em MD5 sem salt",
                "licao": "MD5 é quebrado facilmente por hackers"
            },
            {
                "nome": "LinkedIn (2012)",
                "usuarios": "165 milhões de contas",
                "problema": "SHA-1 sem salt",
                "licao": "Sempre use salt em hashes de senhas"
            },
            {
                "nome": "Adobe (2013)",
                "usuarios": "153 milhões de contas",
                "problema": "3DES com mesma chave",
                "licao": "Criptografia mal implementada é inútil"
            }
        ]
        
        for vazamento in vazamentos:
            st.markdown(f"""
            <div class="mini-game">
                <h4>🚨 {vazamento['nome']}</h4>
                <p><strong>Impacto:</strong> {vazamento['usuarios']}</p>
                <p><strong>Problema:</strong> {vazamento['problema']}</p>
                <p><strong>Lição:</strong> {vazamento['licao']}</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# CRIPTOGRAFIA SIMÉTRICA
# ==============================================================================
elif atividade == "🎮 Criptografia Simétrica":
    st.markdown("""
    <div class="game-card">
        <h2>🎮 Laboratório de Criptografia Simétrica</h2>
        <p>Aprenda a criptografar e descriptografar mensagens secretas!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; border-left: 4px solid #ff6b35; margin: 20px 0;">
        <h3 style="color: #ff6b35;">🤔 O que é Criptografia Simétrica?</h3>
        <p style="color: #ffffff; font-size: 1.1em; line-height: 1.6;">
            <strong style="color: #ff6b35;">Simétrica</strong> significa que usamos a <strong style="color: #00ff41;">mesma chave</strong> para criptografar e descriptografar.
        </p>
        <p style="color: #ffffff; font-size: 1.1em; line-height: 1.6;">
            É como ter uma caixa com cadeado - você precisa da mesma chave para fechar e abrir! 🔐
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔒 Criptografar Mensagem", "🔓 Descriptografar Mensagem"])
    
    with tab1:
        st.markdown("### 🔒 Transforme sua mensagem em código secreto")
        
        mensagem = st.text_area("Digite sua mensagem secreta:", 
                               placeholder="Ex: Encontro às 15h no local combinado")
        
        if mensagem:
            # Gerar chave
            if 'chave_simetrica' not in st.session_state:
                st.session_state.chave_simetrica = Fernet.generate_key()
            
            cipher = Fernet(st.session_state.chave_simetrica)
            mensagem_criptografada = cipher.encrypt(mensagem.encode())
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="hash-result">
                    <h4>🔑 Sua Chave Secreta</h4>
                    <code>{st.session_state.chave_simetrica.decode()}</code>
                    <p><small>Guarde esta chave com cuidado!</small></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="hash-result">
                    <h4>🔒 Mensagem Criptografada</h4>
                    <code>{mensagem_criptografada.decode()}</code>
                    <p><small>Agora está segura!</small></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.info("💡 **Como funciona:** O algoritmo AES-256 misturou sua mensagem de forma que só quem tem a chave consegue ler!")
    
    with tab2:
        st.markdown("### 🔓 Decodifique uma mensagem criptografada")
        
        chave_input = st.text_input("Cole a chave aqui:", 
                                   placeholder="Ex: gAAAAABh...")
        mensagem_criptografada_input = st.text_area("Cole a mensagem criptografada aqui:",
                                                   placeholder="Ex: gAAAAABh...")
        
        if st.button("🔓 Descriptografar", type="primary"):
            if not chave_input or not mensagem_criptografada_input:
                st.warning("⚠️ Por favor, preencha tanto a chave quanto a mensagem criptografada!")
            else:
                try:
                    # Validar se a chave está no formato correto
                    chave_bytes = chave_input.encode()
                    cipher = Fernet(chave_bytes)
                    
                    # Validar se a mensagem está no formato correto
                    mensagem_bytes = mensagem_criptografada_input.encode()
                    mensagem_original = cipher.decrypt(mensagem_bytes)
                    
                    st.success("🎉 **Descriptografia realizada com sucesso!**")
                    st.markdown(f"""
                    <div class="interactive-demo">
                        <h4>📖 Mensagem Original Revelada:</h4>
                        <h3 style="color: #00ff41; font-size: 1.5em; padding: 15px; background: rgba(0,255,65,0.1); border-radius: 10px;">"{mensagem_original.decode()}"</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if "crypto_simetrica" not in st.session_state.missoes_completas:
                        st.session_state.missoes_completas.append("crypto_simetrica")
                        st.session_state.pontos_crypto += 30
                        st.success("🏆 Você ganhou 30 pontos por dominar a criptografia simétrica!")
                    
                except Exception as e:
                    st.error("❌ **Erro na descriptografia!**")
                    st.info("""
                    **Verifique se:**
                    - A chave está exatamente como foi gerada (copie e cole)
                    - A mensagem criptografada está completa
                    - Não há espaços extras no início ou fim
                    """)
                    st.code(f"Erro técnico: {str(e)}")
        
        # Adicionar exemplo prático
        if st.button("💡 Ver Exemplo Prático"):
            st.markdown("""
            <div style="background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; border-left: 4px solid #00ff41; margin: 20px 0;">
                <h3 style="color: #00ff41;">🎯 Exemplo para Teste:</h3>
                <p style="color: #ffffff; font-size: 1.1em;">Use estes dados para testar a descriptografia:</p>
            </div>
            """, unsafe_allow_html=True)
            
            exemplo_key = Fernet.generate_key()
            exemplo_cipher = Fernet(exemplo_key)
            exemplo_msg = "Esta é uma mensagem secreta para teste!"
            exemplo_encrypted = exemplo_cipher.encrypt(exemplo_msg.encode())
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔑 Chave de exemplo:**")
                st.code(exemplo_key.decode())
            with col2:
                st.markdown("**🔒 Mensagem de exemplo:**")
                st.code(exemplo_encrypted.decode())

# ==============================================================================
# CASOS CRIMINAIS FAMOSOS
# ==============================================================================
elif atividade == "🕵️ Casos Criminais Famosos":
    st.markdown("""
    <div class="crime-story">
        <h2>🕵️ Crimes Digitais que Mudaram a História</h2>
        <p>Aprenda com casos reais como a criptografia salvou ou condenou pessoas!</p>
    </div>
    """, unsafe_allow_html=True)
    
    caso = st.selectbox("Escolha um caso:", [
        "🏴‍☠️ O Enigma Nazista",
        "🔍 Silk Road - O eBay das Drogas", 
        "💰 Mt. Gox - Bitcoin Perdido",
        "🕵️ Edward Snowden - NSA Files"
    ])
    
    if caso == "🏴‍☠️ O Enigma Nazista":
        st.markdown("""
        ### 🏴‍☠️ Máquina Enigma - A Criptografia que Quase Venceu a Guerra
        
        #### 📖 A História
        Durante a Segunda Guerra Mundial, os nazistas usavam a máquina **Enigma** para criptografar todas as comunicações militares. Era considerada inquebrável!
        
        #### 🧩 Como Funcionava
        - 3 rotores mecânicos que giravam a cada letra
        - Plugboard que trocava pares de letras  
        - 159 trilhões de combinações possíveis!
        
        #### 🔍 Como Foi Quebrada
        Alan Turing e sua equipe em Bletchley Park construíram o **Colossus**, um dos primeiros computadores, para quebrar o Enigma.
        
        #### 💡 Impacto
        Estima-se que quebrar o Enigma **reduziu a guerra em 2 anos** e salvou milhões de vidas!
        """)
        
        # Simulação avançada do Enigma
        with st.expander("🎮 Simule a Máquina Enigma"):
            st.markdown("""
            <div style="background: rgba(0,0,0,0.8); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h3 style="color: #ff6b35;">⚙️ Configuração da Máquina Enigma</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rotor1 = st.selectbox("🎛️ Rotor I:", ["I", "II", "III", "IV", "V"], index=0, key="rotor1")
                posicao1 = st.slider("Posição Rotor I:", 0, 25, 0, key="pos1")
            
            with col2:
                rotor2 = st.selectbox("🎛️ Rotor II:", ["I", "II", "III", "IV", "V"], index=1, key="rotor2")
                posicao2 = st.slider("Posição Rotor II:", 0, 25, 0, key="pos2")
            
            with col3:
                rotor3 = st.selectbox("🎛️ Rotor III:", ["I", "II", "III", "IV", "V"], index=2, key="rotor3")
                posicao3 = st.slider("Posição Rotor III:", 0, 25, 0, key="pos3")
            
            st.markdown("---")
            
            mensagem_enigma = st.text_input("📝 Digite sua mensagem secreta:", placeholder="HELLO WORLD")
            
            if mensagem_enigma:
                # Simulação mais realista com rotores diferentes
                rotores = {
                    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE", 
                    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
                    "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
                    "V": "VZBRGITYUPSDNHLXAWMJQOFECK"
                }
                
                resultado = ""
                pos_temp = [posicao1, posicao2, posicao3]
                rotores_escolhidos = [rotores[rotor1], rotores[rotor2], rotores[rotor3]]
                
                for char in mensagem_enigma.upper():
                    if char.isalpha():
                        # Simular movimento dos rotores
                        pos_temp[0] = (pos_temp[0] + 1) % 26
                        if pos_temp[0] % 26 == 0:
                            pos_temp[1] = (pos_temp[1] + 1) % 26
                        if pos_temp[1] % 26 == 0:
                            pos_temp[2] = (pos_temp[2] + 1) % 26
                        
                        # Aplicar rotores
                        char_num = ord(char) - ord('A')
                        
                        # Passar pelos 3 rotores
                        for i in range(3):
                            char_num = (char_num + pos_temp[i]) % 26
                            char_num = ord(rotores_escolhidos[i][char_num]) - ord('A')
                        
                        # Refletor (simplificado)
                        char_num = (25 - char_num) % 26
                        
                        # Voltar pelos rotores (invertido)
                        for i in range(2, -1, -1):
                            char_num = rotores_escolhidos[i].index(chr(char_num + ord('A')))
                            char_num = (char_num - pos_temp[i]) % 26
                        
                        resultado += chr(char_num + ord('A'))
                    else:
                        resultado += char
                
                # Exibir resultado
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 4px solid #00ff41;">
                        <h4 style="color: #00ff41;">📝 Mensagem Original:</h4>
                        <code style="color: #ffffff; font-size: 16px;">{mensagem_enigma.upper()}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 4px solid #ff6b35;">
                        <h4 style="color: #ff6b35;">🔐 Código Enigma:</h4>
                        <code style="color: #ffffff; font-size: 16px;">{resultado}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info("⚡ **Curiosidade:** Na Enigma real, os rotores giravam fisicamente e criavam trilhões de combinações diferentes!")
                
                # Adicionar botão para configuração aleatória
                if st.button("🎲 Configuração Aleatória", key="random_enigma"):
                    st.rerun()
    
    elif caso == "🔍 Silk Road - O eBay das Drogas":
        st.markdown("""
        <div class="crime-story">
            <h3>🔍 Silk Road - Como Bitcoin e Tor Criaram o "eBay das Drogas"</h3>
            
            <h4>📖 A História</h4>
            <p>Ross Ulbricht criou o <strong>Silk Road</strong> em 2011, um marketplace na dark web 
            para venda de drogas usando Bitcoin e rede Tor.</p>
            
            <h4>🔐 Tecnologias Usadas</h4>
            <ul>
                <li><strong>Tor Network:</strong> Anonimato na navegação</li>
                <li><strong>Bitcoin:</strong> Pagamentos "anônimos"</li>
                <li><strong>PGP:</strong> Criptografia de mensagens</li>
                <li><strong>Tumbler:</strong> "Lavagem" de bitcoins</li>
            </ul>
            
            <h4>🕵️ Como Foi Descoberto</h4>
            <p>O FBI rastreou Ulbricht através de:</p>
            <ul>
                <li>Análise da blockchain do Bitcoin</li>
                <li>Correlação de horários de atividade</li>
                <li>Erros operacionais (IP vazado)</li>
                <li>Engenharia social</li>
            </ul>
            
            <h4>⚖️ Consequências</h4>
            <p>Ross Ulbricht foi condenado à <strong>prisão perpétua</strong> em 2015.</p>
            
            <h4>🎓 Lições</h4>
            <ul>
                <li>Bitcoin NÃO é completamente anônimo</li>
                <li>Anonimato perfeito é quase impossível</li>
                <li>Um erro pequeno pode comprometer toda a operação</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif caso == "💰 Mt. Gox - Bitcoin Perdido":
        st.markdown("""
        <div class="crime-story">
            <h3>💰 Mt. Gox - O Dia em que 850.000 Bitcoins Desapareceram</h3>
            
            <h4>📖 A História</h4>
            <p>Mt. Gox era a maior exchange de Bitcoin do mundo, controlando <strong>70% do tráfego</strong> 
            de Bitcoin em 2013. Em 2014, anunciou que havia perdido 850.000 bitcoins!</p>
            
            <h4>💸 O Roubo</h4>
            <ul>
                <li><strong>Valor:</strong> ~$450 milhões na época (hoje seria +$30 bilhões!)</li>
                <li><strong>Método:</strong> Hackers exploraram falhas no sistema por anos</li>
                <li><strong>Descoberta:</strong> Só perceberam quando já era tarde demais</li>
            </ul>
            
            <h4>🔍 Problemas de Segurança</h4>
            <ul>
                <li>Chaves privadas armazenadas online (hot wallet)</li>
                <li>Sistema de segurança inadequado</li>
                <li>Auditoria inexistente</li>
                <li>Gestão financeira ruim</li>
            </ul>
            
            <h4>🎓 Lições para Criptografia</h4>
            <ul>
                <li><strong>Cold Storage:</strong> Mantenha chaves offline</li>
                <li><strong>Multi-sig:</strong> Use múltiplas assinaturas</li>
                <li><strong>Auditoria:</strong> Verifique regularmente</li>
                <li><strong>"Not your keys, not your coins"</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif caso == "🕵️ Edward Snowden - NSA Files":
        st.markdown("""
        <div class="crime-story">
            <h3>🕵️ Edward Snowden - O Maior Vazamento de Documentos Classificados</h3>
            
            <h4>📖 A História</h4>
            <p>Em 2013, Edward Snowden, ex-funcionário da NSA, vazou milhares de documentos 
            revelando programas de vigilância global dos EUA.</p>
            
            <h4>🔐 Como Ele Fez</h4>
            <ul>
                <li><strong>Tor Browser:</strong> Comunicação anônima com jornalistas</li>
                <li><strong>Linux TAILS:</strong> Sistema operacional que não deixa rastros</li>
                <li><strong>PGP:</strong> Criptografia de emails</li>
                <li><strong>Signal/Wickr:</strong> Mensagens criptografadas</li>
            </ul>
            
            <h4>📊 O que Foi Revelado</h4>
            <ul>
                <li><strong>PRISM:</strong> Acesso direto a dados do Google, Facebook, etc.</li>
                <li><strong>XKeyscore:</strong> Busca em tempo real de atividades na internet</li>
                <li><strong>Backdoors:</strong> NSA inseriu portas traseiras em produtos</li>
                <li><strong>Quebra de criptografia:</strong> Ataques a algoritmos "seguros"</li>
            </ul>
            
            <h4>🌍 Impacto Global</h4>
            <ul>
                <li>Maior adoção de HTTPS</li>
                <li>Crescimento de apps de criptografia</li>
                <li>Leis de proteção de dados (GDPR)</li>
                <li>Desconfiança em produtos americanos</li>
            </ul>
            
            <h4>🎓 Lições</h4>
            <ul>
                <li>Criptografia forte é essencial para privacidade</li>
                <li>Governos podem tentar quebrar criptografia</li>
                <li>Open source é mais confiável</li>
                <li>Metadados também são importantes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MR. ROBOT: REALIDADE VS FICÇÃO
# ==============================================================================
elif atividade == "📺 Mr. Robot: Realidade vs Ficção":
    st.markdown("""
    ## 📺 Mr. Robot: O que é Real vs Ficção
    Análise técnica da série que revolucionou como vemos a cibersegurança na TV!
    """)
    
    st.markdown("""
    ### 🎬 Por que Mr. Robot é Diferente?
    Diferente de filmes como "Hackers" (1995), Mr. Robot usa **técnicas REAIS** de hacking consultadas por hackers profissionais!
    """)
    
    cena = st.selectbox("Escolha uma cena para analisar:", [
        "💀 Hack da E-Corp (1ª Temporada)",
        "🏛️ Hack do FBI (2ª Temporada)", 
        "🌐 Stage 3 - Bangladesh Bank (3ª Temporada)",
        "🏢 Deus Ex Machina - Whiterose (4ª Temporada)"
    ])
    
    if cena == "💀 Hack da E-Corp (1ª Temporada)":
        st.markdown("""
        ### 💀 O Hack que Deletou Todas as Dívidas do Mundo
        
        #### 📺 Na Série
        Elliot usa **rootkits**, **engenharia social** e **malware** para deletar todos os registros de dívidas da E-Corp, causando caos financeiro global.
        
        #### 🤔 É Possível na Vida Real?
        **✅ PARCIALMENTE REAL**
        
        #### 🛠️ Técnicas Usadas (Reais):
        - **Social Engineering:** ✅ Funciona - 90% dos ataques começam assim
        - **Rootkits:** ✅ Existem - Stuxnet usou isso para atacar o Irã
        - **Raspberry Pi:** ✅ Real - Hackers usam para infiltração física
        - **CD de Boot Malicioso:** ✅ Técnica conhecida desde os anos 2000
        
        #### ❌ Problemas da Série:
        - **Backups:** Empresas têm cópias em vários locais
        - **Blockchain:** Registros distribuídos são impossíveis de deletar totalmente
        - **Bancos Centrais:** Têm seus próprios sistemas independentes
        - **Papel:** Muitos contratos ainda existem fisicamente
        
        #### 🎯 Caso Real Similar:
        **Sony Pictures (2014):** Hackers norte-coreanos deletaram TUDO dos servidores da Sony, incluindo filmes não lançados, emails executivos, dados de funcionários. Prejuízo: +$100 milhões.
        """)
        
        # Mini-game interativo
        with st.expander("🎮 Teste: Você conseguiria hackear a E-Corp?"):
            st.markdown("**Cenário:** Você precisa entrar no prédio da E-Corp. Qual sua estratégia?")
            
            estrategia = st.radio("Escolha sua abordagem:", [
                "🚪 Tentar forçar a porta (força bruta)",
                "👔 Se disfarçar de funcionário (engenharia social)",  
                "💻 Hackear o sistema remotamente",
                "📱 Ligar se passando por suporte técnico"
            ])
            
            if st.button("🎯 Executar Plano"):
                if estrategia == "👔 Se disfarçar de funcionário (engenharia social)":
                    st.success("🎉 SUCESSO! 90% dos hackers reais usam engenharia social. Você pensou como Elliot!")
                    if "mr_robot_ecorp" not in st.session_state.missoes_completas:
                        st.session_state.missoes_completas.append("mr_robot_ecorp")
                        st.session_state.pontos_crypto += 25
                elif estrategia == "📱 Ligar se passando por suporte técnico":
                    st.success("🎉 EXCELENTE! Kevin Mitnick ficou famoso por essa técnica!")
                else:
                    st.error("❌ Detectado! Segurança chamada. Tente engenharia social na próxima!")
    
    elif cena == "🏛️ Hack do FBI (2ª Temporada)":
        st.markdown("""
        ### 🏛️ Invadindo o FBI - A Prisão Digital
        
        #### 📺 Na Série
        Elliot, preso, precisa hackear o FBI de dentro da cadeia usando um **smartphone contrabandeado** e conexões WiFi.
        
        #### ✅ Técnicas 100% Reais:
        - **Femtocells:** ✅ Equipamentos que interceptam celulares
        - **WiFi Pineapple:** ✅ Dispositivo real usado por pentesters
        - **IMSI Catchers:** ✅ FBI usa isso para rastrear criminosos
        - **Tor Browser:** ✅ Desenvolvido pela própria NSA (ironia!)
        
        #### 🔍 Caso Real: Edward Snowden
        Snowden trabalhou **DENTRO** da NSA e conseguiu copiar milhares de documentos classificados usando técnicas similares às da série!
        
        #### 💡 Curiosidade
        O consultor técnico de Mr. Robot é **Marc Rogers**, hacker ético que já trabalhou para empresas como Cloudflare e DefCon. Por isso as técnicas são tão realistas!
        """)
    
    elif cena == "🌐 Stage 3 - Bangladesh Bank (3ª Temporada)":
        st.markdown("""
        ### 🌐 O Roubo de $1 Bilhão do Bangladesh Bank
        
        #### 📺 Na Série
        Dark Army hackeia o sistema bancário internacional SWIFT para roubar bilhões.
        
        #### 😱 ISSO ACONTECEU DE VERDADE!
        **Fevereiro de 2016:** Hackers norte-coreanos roubaram $81 milhões do Bangladesh Bank usando exatamente as técnicas mostradas na série!
        
        #### 🛠️ Como Foi Feito (Real):
        - **Spear Phishing:** Emails falsos para funcionários do banco
        - **SWIFT Hack:** Acesso ao sistema de transferências internacionais
        - **Money Laundering:** Lavagem via cassinos filipinos
        - **Typo que Salvou Bilhões:** Erro de digitação alertou o sistema!
        
        #### 🎯 Técnicas Usadas (Lazarus Group - Coreia do Norte):
        - **Custom Malware:** Vírus feito especificamente para SWIFT
        - **Living off the Land:** Usar ferramentas já instaladas no sistema
        - **False Flags:** Deixar pistas falsas apontando para outros países
        
        #### 💰 Prejuízos Globais:
        - **Sony Pictures:** $100 milhões
        - **WannaCry:** $4 bilhões globais
        - **Bangladesh Bank:** $81 milhões roubados
        - **Total estimado:** +$10 bilhões desde 2014
        """)
    
    elif cena == "🏢 Deus Ex Machina - Whiterose (4ª Temporada)":
        st.markdown("""
        ### 🏢 A Máquina de Controle Total
        
        #### 📺 Na Série
        Whiterose controla tudo através de uma máquina quântica que pode "mudar a realidade".
        
        #### 🤔 Computação Quântica é Real?
        **✅ SIM!** Mas não como na série...
        
        #### 🔬 Realidade da Computação Quântica:
        - **Google:** Conquistou "supremacia quântica" em 2019
        - **IBM:** Tem computadores quânticos na nuvem
        - **China:** Investe bilhões em pesquisa quântica
        - **Criptografia:** Quânticos podem quebrar RSA e AES!
        
        #### ⚠️ O Perigo Real:
        **"Crypto-Apocalypse"** - Quando computadores quânticos conseguirem quebrar toda a criptografia atual, toda a internet ficará vulnerável!
        
        #### 🛡️ Soluções em Desenvolvimento:
        - **Post-Quantum Cryptography:** Algoritmos resistentes a quânticos
        - **Quantum Key Distribution:** Chaves quânticas invioláveis
        - **NIST Standards:** Novos padrões de criptografia
        
        #### 🎯 Timeline Estimada:
        - **2025-2030:** Primeiros ataques práticos a RSA-1024
        - **2030-2035:** Quebra de RSA-2048 e AES-128
        - **2035+:** Necessidade de migração completa
        """)

# ==============================================================================
# MATRIX: REALIDADE VS FICÇÃO
# ==============================================================================
elif atividade == "🔴 Matrix: Realidade vs Ficção":
    st.markdown("""
    ## 🔴 Matrix (1999): Profecias Tecnológicas que se Tornaram Realidade
    O filme que previu nosso futuro digital e suas ameaças
    """)
    
    st.markdown("""
    ### 🕳️ "Quão Profundo é o Buraco do Coelho?"
    
    #### 📱 PREVISÕES QUE SE TORNARAM REAIS
    - **Vigilância Digital Total:** NSA, câmeras faciais, smartphones
    - **Realidade Virtual:** Meta, Apple Vision Pro, VRChat
    - **IA Controlando Humanos:** Algoritmos de redes sociais
    - **Simulações Perfeitas:** Deepfakes, ChatGPT, realidade sintética
    - **Hackeamento de Cérebros:** Neuralink de Elon Musk
    - **Controle de Percepção:** Filtros bolhas, fake news
    
    #### ⚠️ AMEAÇAS CIBERNÉTICAS REAIS
    - **Agente Smith = Malware:** Se autorreplica e infecta sistemas
    - **Red Pill = Conscientização:** Educação em cybersecurity
    - **Blue Pill = Ignorância:** Usuários desprotegidos
    - **Morpheus = Mentor:** Especialistas em segurança
    - **Zion = Sistemas Seguros:** Infraestrutura protegida
    - **Máquinas = Big Tech:** Coleta massiva de dados
    
    #### 💊 ESCOLHA SUA PÍLULA
    
    **🔵 PÍLULA AZUL**
    Ignorar as ameaças, continuar vulnerável, confiar cegamente na tecnologia
    **Resultado:** Vítima de hacks, privacidade violada, dados roubados
    
    **🔴 PÍLULA VERMELHA**
    Despertar para a realidade cyber, aprender proteção, questionar tudo
    **Resultado:** Controle sobre sua segurança digital, consciência das ameaças
    
    #### 🎬 CURIOSIDADES TÉCNICAS DO FILME
    - **Código Matrix Verde:** Receitas de sushi em japonês!
    - **Efeito "Bullet Time":** 120 câmeras sincronizadas
    - **Terminal Real:** Comandos Unix reais no filme
    - **Hack da Trinity:** Exploit SSH1 CRC32 real de 1998
    - **Números Reais:** IPs e ports válidos no filme
    - **Filosofia:** Baseado em "Simulacra e Simulação" de Baudrillard
    """)

# ==============================================================================
# BLACK MIRROR: TECNOLOGIA VS HUMANIDADE
# ==============================================================================
elif atividade == "📺 Black Mirror: Tecnologia vs Humanidade":
    st.markdown("""
    ## 📺 Black Mirror: O Espelho Negro da Cybersegurança
    Como a série previu os perigos da nossa dependência tecnológica
    """)
    
    # Análise interativa por episódio
    episodio_selecionado = st.selectbox(
        "🎬 Escolha um episódio para análise técnica:",
        [
            "🐷 The National Anthem - Chantagem Digital",
            "👁️ Nosedive - Sistema de Crédito Social",
            "🎮 USS Callister - Realidade Virtual Tóxica", 
            "🤖 Metalhead - Robôs Assassinos Autônomos",
            "🏃 Shut Up and Dance - Blackmail via Webcam",
            "🧠 San Junipero - Upload de Consciência",
            "📱 Smithereens - Vício em Redes Sociais"
        ]
    )
    
    if "National Anthem" in episodio_selecionado:
        st.markdown("""
        ### 🐷 The National Anthem: Chantagem Digital
        
        #### 📡 TECNOLOGIA NO EPISÓDIO
        - **Sequestro digital:** Vídeo enviado por canais anônimos
        - **Rastreamento impossível:** Comunicação via múltiplos proxies
        - **Viralização forçada:** Spread instantâneo nas redes
        - **Deepfakes primitivos:** Manipulação de vídeo
        
        #### 🛡️ REALIDADE ATUAL
        - **Deepfakes avançados:** FaceSwap, DeepFaceLab
        - **Tor & VPNs:** Anonimato real disponível
        - **Chantagem digital:** +300% nos últimos 5 anos
        - **Viral em minutos:** Twitter, TikTok, WhatsApp
        
        #### 🚨 LIÇÕES DE CYBERSEGURANÇA
        Este episódio mostra como **chantagem digital** pode destruir vidas instantaneamente. Em 2024, vemos isso diariamente: políticos, CEOs e celebridades vítimas de deepfakes, vazamentos de dados íntimos e manipulação de imagem.
        """)
        
    elif "Nosedive" in episodio_selecionado:
        st.markdown("""
        ### 👁️ Nosedive: Sistema de Crédito Social
        
        #### 🔍 TECNOLOGIA NO EPISÓDIO
        - **App de rating:** Avaliação constante de pessoas
        - **Reconhecimento facial:** Identificação automática
        - **Score social:** Algoritmo determina valor humano
        - **Punição sistêmica:** Exclusão por baixa nota
        
        #### ⚠️ JÁ É REALIDADE!
        - **China:** Sistema de Crédito Social ativo desde 2020
        - **Sesame Credit:** Ant Financial (Alibaba)
        - **17 milhões bloqueados:** De comprar passagens aéreas
        - **Face recognition:** 200 milhões de câmeras na China
        
        #### 🚨 PERIGOS REAIS
        O episódio era **ficção científica em 2016**, mas hoje é **documentário**! A China usa IA para monitorar 1.4 bilhão de pessoas 24/7, punindo comportamentos "inadequados" com restrições automáticas de crédito, viagens e emprego.
        """)
    
    st.markdown("""
    ### 🎮 QUIZ: Black Mirror vs Realidade
    Adivinhe: Isso já aconteceu ou ainda é ficção?
    """)
    
    quiz_scenarios = [
        ("🤖 Robôs patrulhando ruas e matando pessoas", "JÁ ACONTECEU - Robôs militares autônomos usados em conflitos"),
        ("📱 App que avalia pessoas em tempo real", "JÁ ACONTECEU - Peeple app, sistemas de crédito social"),
        ("🧠 Upload de consciência para computador", "AINDA FICÇÃO - Mas Neuralink está trabalhando nisso"),
        ("👁️ Reconhecimento facial em massa", "JÁ ACONTECEU - China, Reino Unido, EUA usam extensivamente"),
        ("🎮 Pessoas presas em realidade virtual", "JÁ ACONTECEU - Vício em VR, casos de morte por exaustão")
    ]
    
    for i, (scenario, answer) in enumerate(quiz_scenarios):
        with st.expander(f"🎯 Cenário {i+1}: {scenario}"):
            guess = st.radio(f"Sua resposta para cenário {i+1}:", ["Já aconteceu", "Ainda é ficção"], key=f"quiz_{i}")
            if st.button(f"Revelar resposta {i+1}", key=f"reveal_{i}"):
                st.success(f"**Resposta:** {answer}")

# ==============================================================================
# COMPUTAÇÃO QUÂNTICA: O FUTURO DA CRIPTOGRAFIA
# ==============================================================================
elif atividade == "🔬 Computação Quântica: O Futuro da Criptografia":
    st.markdown("""
    ## 🔬 Computação Quântica: A Bomba Atômica da Criptografia
    Como computadores quânticos vão quebrar TODA a criptografia atual
    """)
    
    st.markdown("""
    ### ⏰ COUNTDOWN PARA O CRYPTOCALYPSE
    
    | Ano | Marco | Impacto |
    |-----|-------|--------|
    | **2024** | **1000+ qubits** | IBM Condor |
    | **2027** | **RSA-1024 quebrado** | Primeira vítima |
    | **2030** | **RSA-2048 vulnerável** | Pânico global |
    | **2035** | **AES-256 quebrado** | Cryptocalypse total |
    """)
    
    # Simulador quântico interativo
    st.subheader("🎮 Simulador: Quebrando RSA com Shor's Algorithm")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Escolha um número para fatorar:**
        """)
        numero = st.selectbox("Número RSA simulado:", [15, 21, 35, 77, 143, 323])
        
        if st.button("🔬 Executar Algoritmo Quântico"):
            import math
            
            # Simulação simples de fatoração
            for i in range(2, int(math.sqrt(numero)) + 1):
                if numero % i == 0:
                    fator1, fator2 = i, numero // i
                    break
            
            st.success(f"✅ **Fatoração encontrada!**")
            st.code(f"{numero} = {fator1} × {fator2}")
            st.warning("Em um computador quântico real, isso funcionaria para números com centenas de dígitos!")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(102, 0, 255, 0.1); padding: 20px; border-radius: 10px;">
            <h3 style="color: #6600ff;">⚡ Como Funciona</h3>
            <ul style="color: white;">
                <li><strong>Superposição:</strong> Qubit pode ser 0 E 1 simultaneamente</li>
                <li><strong>Emaranhamento:</strong> Qubits conectados instantaneamente</li>
                <li><strong>Interferência:</strong> Amplifica respostas corretas</li>
                <li><strong>Medição:</strong> Colapsa para resposta final</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Investimentos e empresas
    st.markdown("""
    <div style="background: linear-gradient(45deg, #1a1a2e, #16213e); padding: 25px; border-radius: 15px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-align: center;">💰 A CORRIDA QUÂNTICA BILIONÁRIA</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;">
            <div style="background: rgba(0, 0, 255, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #0066ff;">🏢 IBM</h3>
                <p style="color: white;"><strong>$6 bilhões investidos</strong></p>
                <p style="color: #ff6b35;">Condor: 1121 qubits (2024)</p>
            </div>
            <div style="background: rgba(0, 255, 0, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #00ff41;">🏢 Google</h3>
                <p style="color: white;"><strong>$10+ bilhões</strong></p>
                <p style="color: #ff6b35;">Sycamore: Supremacia quântica</p>
            </div>
            <div style="background: rgba(255, 0, 0, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ff0000;">🏢 China</h3>
                <p style="color: white;"><strong>$25 bilhões (governo)</strong></p>
                <p style="color: #ff6b35;">Maior investimento mundial</p>
            </div>
            <div style="background: rgba(255, 0, 255, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ff00ff;">🏢 Microsoft</h3>
                <p style="color: white;"><strong>Azure Quantum</strong></p>
                <p style="color: #ff6b35;">Qubits topológicos</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# BIG TECH: INVESTIMENTOS BILIONÁRIOS
# ==============================================================================
elif atividade == "💰 Big Tech: Investimentos Bilionários":
    st.markdown("""
    <div class="activity-header">
        <h1>💰 Big Tech: A Guerra Bilionária pela Cybersegurança</h1>
        <p>Quanto as gigantes da tecnologia gastam para se proteger (e nos proteger)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seletor interativo de empresa
    empresa_selecionada = st.selectbox(
        "🏢 Escolha uma Big Tech para análise financeira:",
        ["🍎 Apple", "🔍 Google", "📘 Meta", "🪟 Microsoft", "📦 Amazon", "⚡ Tesla", "🐦 Twitter/X"]
    )
    
    if "Apple" in empresa_selecionada:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #000, #333); padding: 30px; border-radius: 15px; border: 2px solid #ffffff; margin: 20px 0;">
            <h2 style="color: #ffffff; text-align: center;">🍎 APPLE: FORTALEZA DIGITAL</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #00ff41;">💰 ORÇAMENTO ANUAL</h3>
                    <div style="font-size: 2.5em; color: #ffffff;">$25B</div>
                    <p style="color: #ff6b35;">Pesquisa & Desenvolvimento</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #0066ff;">🛡️ SEGURANÇA</h3>
                    <div style="font-size: 2.5em; color: #ffffff;">$6B</div>
                    <p style="color: #ff6b35;">Apenas em cybersecurity</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #ff0000;">🏆 BUG BOUNTY</h3>
                    <div style="font-size: 2.5em; color: #ffffff;">$1.5M</div>
                    <p style="color: #ff6b35;">Máximo por vulnerabilidade</p>
                </div>
            </div>
            
            <div style="background: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #00ff41;">🔐 TECNOLOGIAS PROPRIETÁRIAS</h3>
                <ul style="color: white; line-height: 1.8;">
                    <li><strong>Secure Enclave:</strong> Chip T2/M1 para criptografia hardware</li>
                    <li><strong>Face ID:</strong> TrueDepth camera com neural networks</li>
                    <li><strong>iMessage E2E:</strong> Criptografia ponta-a-ponta nativa</li>
                    <li><strong>Differential Privacy:</strong> Coleta de dados anonimizada</li>
                    <li><strong>App Transport Security:</strong> HTTPS obrigatório</li>
                    <li><strong>iOS Sandboxing:</strong> Isolamento total de apps</li>
                </ul>
            </div>
            
            <div style="background: rgba(255, 107, 53, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ff6b35;">📊 IMPACTO NO MERCADO</h3>
                <p style="color: white; line-height: 1.8;">
                A Apple força TODO o mercado mobile a ser mais seguro. Quando eles implementam 
                uma feature (como App Tracking Transparency), <strong>$240 bilhões são perdidos</strong> 
                pela indústria de publicidade digital. Isso é PODER real!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Google" in empresa_selecionada:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #4285f4, #34a853, #fbbc05, #ea4335); padding: 30px; border-radius: 15px; margin: 20px 0;">
            <h2 style="color: white; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">🔍 GOOGLE: O GUARDIÃO DA INTERNET</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #00ff41;">🛡️ PROJECT ZERO</h3>
                    <div style="font-size: 2em; color: white;">2000+</div>
                    <p style="color: #ffffff;">Vulnerabilidades encontradas</p>
                </div>
                <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #0066ff;">💰 ORÇAMENTO</h3>
                    <div style="font-size: 2em; color: white;">$18B</div>
                    <p style="color: #ffffff;">R&D + Segurança anual</p>
                </div>
                <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #ff0000;">🏆 PROTEÇÃO</h3>
                    <div style="font-size: 2em; color: white;">4B+</div>
                    <p style="color: #ffffff;">Usuários protegidos</p>
                </div>
            </div>
            
            <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #00ff41;">🚀 TECNOLOGIAS REVOLUCIONÁRIAS</h3>
                <ul style="color: white; line-height: 1.8;">
                    <li><strong>Safe Browsing:</strong> Protege 4+ bilhões de usuários contra phishing</li>
                    <li><strong>reCAPTCHA:</strong> Distingue humanos de bots em 10 milhões de sites</li>
                    <li><strong>Certificate Transparency:</strong> Detecta certificados SSL fraudulentos</li>
                    <li><strong>Advanced Protection:</strong> Proteção militar para jornalistas/ativistas</li>
                    <li><strong>Titan Security Keys:</strong> Hardware 2FA inquebráveis</li>
                    <li><strong>BeyondCorp:</strong> Zero Trust Network modelo revolucionário</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Comparativo interativo
    st.markdown("""
    <div style="background: linear-gradient(45deg, #1a1a2e, #16213e); padding: 25px; border-radius: 15px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-align: center;">📊 COMPARATIVO: GASTOS EM CYBERSECURITY (2024)</h2>
        
        <div style="margin: 20px 0;">
            <div style="background: rgba(0, 255, 65, 0.1); padding: 10px; border-radius: 5px; margin: 5px 0;">
                <strong style="color: #00ff41;">Amazon:</strong> 
                <span style="color: white;">$14.2B/ano</span>
                <div style="background: #00ff41; height: 20px; width: 85%; border-radius: 10px;"></div>
            </div>
            <div style="background: rgba(0, 102, 255, 0.1); padding: 10px; border-radius: 5px; margin: 5px 0;">
                <strong style="color: #0066ff;">Microsoft:</strong> 
                <span style="color: white;">$12.8B/ano</span>
                <div style="background: #0066ff; height: 20px; width: 77%; border-radius: 10px;"></div>
            </div>
            <div style="background: rgba(255, 0, 0, 0.1); padding: 10px; border-radius: 5px; margin: 5px 0;">
                <strong style="color: #ff0000;">Meta:</strong> 
                <span style="color: white;">$9.5B/ano</span>
                <div style="background: #ff0000; height: 20px; width: 57%; border-radius: 10px;"></div>
            </div>
            <div style="background: rgba(255, 255, 0, 0.1); padding: 10px; border-radius: 5px; margin: 5px 0;">
                <strong style="color: #ffff00;">Tesla:</strong> 
                <span style="color: white;">$2.1B/ano</span>
                <div style="background: #ffff00; height: 20px; width: 13%; border-radius: 10px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# CRIPTOMOEDAS: REVOLUÇÃO FINANCEIRA DIGITAL
# ==============================================================================
elif atividade == "₿ Criptomoedas: Revolução Financeira Digital":
    st.markdown("""
    <div class="activity-header">
        <h1>₿ Criptomoedas: A Revolução que Mudou o Dinheiro Para Sempre</h1>
        <p>Como a criptografia criou uma nova economia de $2 trilhões</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Jogo: Adivinha o preço do Bitcoin
    st.markdown("""
    <div style="background: linear-gradient(45deg, #ff9500, #ffb340); padding: 25px; border-radius: 15px; border: 2px solid #ff9500; margin: 20px 0;">
        <h2 style="color: #000; text-align: center; font-family: 'Orbitron', monospace;">🎮 JOGO: Adivinhe o Preço do Bitcoin!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Dados históricos reais do Bitcoin (preços aproximados)
    historical_prices = {
        "2010 - Primeira compra": "$0.008",
        "2011 - Mt. Gox hack": "$32", 
        "2013 - Silk Road fechado": "$400",
        "2017 - ICO mania": "$19.783",
        "2018 - Crypto winter": "$3.200",
        "2020 - COVID-19 início": "$5.000",
        "2021 - ATH Tesla": "$68.789",
        "2022 - FTX colapso": "$16.500",
        "2024 - ETF aprovado": "$73.000"
    }
    
    evento_selecionado = st.selectbox("📅 Escolha um evento histórico:", list(historical_prices.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        guess = st.number_input("💰 Qual era o preço do Bitcoin neste evento?", min_value=0.001, max_value=100000.0, value=1000.0, step=100.0)
        
        if st.button("🎯 Verificar Resposta"):
            correct_price = historical_prices[evento_selecionado]
            st.success(f"✅ **Resposta correta:** {correct_price}")
            
            # Calcular se estava próximo
            try:
                correct_num = float(correct_price.replace('$', '').replace(',', ''))
                if abs(guess - correct_num) / correct_num < 0.1:
                    st.balloons()
                    st.success("🏆 **INCRÍVEL!** Você acertou muito próximo!")
                elif abs(guess - correct_num) / correct_num < 0.5:
                    st.warning("👍 **BOM!** Estava relativamente próximo!")
                else:
                    st.error("💀 **LONGE!** Bitcoin é muito volátil!")
            except:
                pass
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(255, 149, 0, 0.1); padding: 20px; border-radius: 10px;">
            <h3 style="color: #ff9500;">🎯 Contexto do Evento</h3>
            <p style="color: white; line-height: 1.8;">
        """, unsafe_allow_html=True)
        
        if "2010" in evento_selecionado:
            st.markdown("**Primeira compra registrada:** Laszlo Hanyecz comprou 2 pizzas por 10.000 BTC. Hoje essas pizzas valeriam $730 milhões!", unsafe_allow_html=True)
        elif "2017" in evento_selecionado:
            st.markdown("**ICO Mania:** Qualquer projeto com 'blockchain' levantava milhões. Era o faroeste das criptos!", unsafe_allow_html=True)
        elif "2024" in evento_selecionado:
            st.markdown("**ETF Aprovado:** BlackRock e outros gigantes entraram oficialmente no Bitcoin, legitimando as criptos.", unsafe_allow_html=True)
        
        st.markdown("</p></div>", unsafe_allow_html=True)
    
    # Quiz interativo sobre criptomoedas
    st.markdown("""
    <div style="background: linear-gradient(45deg, #16213e, #0f0f23); padding: 25px; border-radius: 15px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-align: center; font-family: 'Orbitron', monospace;">
            🧠 QUIZ: Você é um Crypto Expert?
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Quiz com múltipla escolha
    questions = [
        {
            "pergunta": "🤔 Quem é o criador do Bitcoin?",
            "opcoes": ["A) Elon Musk", "B) Satoshi Nakamoto", "C) Vitalik Buterin", "D) Charlie Lee"],
            "resposta": "B",
            "explicacao": "Satoshi Nakamoto é o pseudônimo da pessoa (ou grupo) que criou o Bitcoin. Sua identidade real permanece um mistério até hoje!"
        },
        {
            "pergunta": "💰 Qual é o número máximo de Bitcoins que podem existir?",
            "opcoes": ["A) 100 milhões", "B) 50 milhões", "C) 21 milhões", "D) Infinito"],
            "resposta": "C", 
            "explicacao": "Apenas 21 milhões de Bitcoins podem existir. Esta escassez programada é o que torna o Bitcoin 'ouro digital'!"
        },
        {
            "pergunta": "⚡ Qual blockchain é mais rápido?",
            "opcoes": ["A) Bitcoin (7 TPS)", "B) Ethereum (15 TPS)", "C) Solana (65,000 TPS)", "D) Cardano (250 TPS)"],
            "resposta": "C",
            "explicacao": "Solana pode processar até 65.000 transações por segundo, sendo uma das blockchains mais rápidas!"
        }
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.subheader(f"Pergunta {i+1}: {q['pergunta']}")
        
        user_answer = st.radio(f"Escolha sua resposta:", q['opcoes'], key=f"crypto_q_{i}")
        
        if st.button(f"Confirmar resposta {i+1}", key=f"crypto_submit_{i}"):
            if user_answer.startswith(q['resposta']):
                st.success(f"✅ **CORRETO!** {q['explicacao']}")
                score += 1
            else:
                st.error(f"❌ **ERRADO!** A resposta correta é {q['resposta']}. {q['explicacao']}")

# ==============================================================================
# O JOGO DA IMITAÇÃO: CRIPTOGRAFIA NA GUERRA
# ==============================================================================
elif atividade == "🎬 O Jogo da Imitação: Criptografia na Guerra":
    st.markdown("""
    <div class="activity-header">
        <h1>🎬 O Jogo da Imitação: Quando a Criptografia Salvou o Mundo</h1>
        <p>Como Alan Turing e sua equipe mudaram o curso da Segunda Guerra Mundial</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulador da Máquina Enigma
    st.markdown("""
    <div style="background: linear-gradient(45deg, #8b4513, #a0522d); padding: 30px; border-radius: 15px; border: 2px solid #8b4513; margin: 20px 0;">
        <h2 style="color: #fff; text-align: center;">🔧 SIMULADOR: Máquina Enigma Nazi</h2>
        <p style="color: #ffeb3b; text-align: center;">Experimente a máquina de criptografia que quase deu a vitória aos nazistas</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Digite sua mensagem secreta:")
        mensagem = st.text_input("Mensagem para codificar:", value="ATTACK AT DAWN", key="enigma_input")
        
        # Simulação simples da Enigma (substitution cipher)
        def simple_enigma(text):
            # Rotores simples de substituição
            rotor1 = "QWERTYUIOPASDFGHJKLZXCVBNM"
            normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            encoded = ""
            for char in text.upper():
                if char in normal:
                    idx = normal.index(char)
                    encoded += rotor1[idx]
                else:
                    encoded += char
            return encoded
        
        if st.button("🔐 Codificar com Enigma"):
            encoded = simple_enigma(mensagem)
            st.code(f"Mensagem codificada: {encoded}")
            st.info("💡 A máquina Enigma real tinha 3-4 rotores que mudavam a cada letra!")
    
    with col2:
        st.subheader("🧠 Como Turing Quebrou a Enigma:")
        st.markdown("""
        <div style="background: rgba(139, 69, 19, 0.1); padding: 20px; border-radius: 10px;">
            <ul style="color: white; line-height: 1.8;">
                <li><strong>Bombe Machine:</strong> Computador eletromecânico que testava combinações</li>
                <li><strong>Cribs:</strong> Palavras previsíveis como "WETTER" (tempo)</li>
                <li><strong>Paralelo:</strong> 200+ pessoas trabalhando em Bletchley Park</li>
                <li><strong>Estatística:</strong> Análise de frequência das letras</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quiz sobre o filme e história real
    st.markdown("""
    <div style="background: linear-gradient(45deg, #16213e, #0f0f23); padding: 25px; border-radius: 15px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-align: center; font-family: 'Orbitron', monospace;">
            🎥 QUIZ: Filme vs Realidade
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    film_questions = [
        {
            "pergunta": "🏳️‍🌈 Alan Turing foi perseguido por ser:",
            "opcoes": ["A) Comunista", "B) Homossexual", "C) Ateu", "D) Pacifista"],
            "resposta": "B",
            "explicacao": "Turing foi perseguido pela lei inglesa por homossexualidade, considerada crime na época. Ele foi castrado quimicamente e se suicidou aos 41 anos."
        },
        {
            "pergunta": "⚡ Quanto tempo a quebra da Enigma encurtou a guerra?",
            "opcoes": ["A) 6 meses", "B) 1 ano", "C) 2-4 anos", "D) 5 anos"],
            "resposta": "C",
            "explicacao": "Historiadores estimam que quebrar a Enigma encurtou a guerra em 2-4 anos, salvando milhões de vidas!"
        },
        {
            "pergunta": "🧮 A 'Bombe' de Turing era:",
            "opcoes": ["A) Uma bomba real", "B) Computador eletromecânico", "C) Código secreto", "D) Submarino"],
            "resposta": "B", 
            "explicacao": "A Bombe era um dos primeiros 'computadores' - uma máquina eletromecânica que automatizava a quebra da Enigma!"
        }
    ]
    
    for i, q in enumerate(film_questions):
        st.subheader(f"🎬 {q['pergunta']}")
        user_answer = st.radio("", q['opcoes'], key=f"film_q_{i}")
        
        if st.button(f"🎯 Revelar resposta", key=f"film_reveal_{i}"):
            if user_answer.startswith(q['resposta']):
                st.success(f"✅ **CORRETO!** {q['explicacao']}")
            else:
                st.error(f"❌ **ERRADO!** {q['explicacao']}")

# ==============================================================================
# CYBERSEGURANÇA NAS GUERRAS MODERNAS
# ==============================================================================
elif atividade == "⚔️ Cybersegurança nas Guerras Modernas":
    st.markdown("""
    <div class="activity-header">
        <h1>⚔️ Cybersegurança: O Novo Campo de Batalha Digital</h1>
        <p>Como hackers se tornaram soldados e códigos viraram armas de destruição em massa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mapa interativo de cyberataques
    st.markdown("""
    <div style="background: linear-gradient(45deg, #8b0000, #dc143c); padding: 30px; border-radius: 15px; border: 2px solid #ff0000; margin: 20px 0;">
        <h2 style="color: white; text-align: center;">🗺️ MAPA DOS CYBERATAQUES GLOBAIS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Seletor de conflito
    conflito = st.selectbox(
        "⚔️ Escolha um conflito para análise:",
        [
            "🇺🇦 Ucrânia vs Rússia (2022-2024)",
            "🇮🇷 Stuxnet vs Irã (2010)", 
            "🇰🇵 Coreia do Norte vs Sony (2014)",
            "🇨🇳 China vs EUA (Guerra Fria Digital)",
            "🇮🇱 Israel vs Hezbollah (Cyber Iron Dome)"
        ]
    )
    
    if "Ucrânia" in conflito:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #005bbb, #ffd500); padding: 25px; border-radius: 15px; border: 2px solid #005bbb; margin: 20px 0;">
            <h2 style="color: white; text-align: center;">🇺🇦 A PRIMEIRA GUERRA HÍBRIDA DA HISTÓRIA</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div style="background: rgba(255, 0, 0, 0.2); padding: 20px; border-radius: 10px;">
                    <h3 style="color: #ff0000;">🔴 ATAQUES RUSSOS</h3>
                    <ul style="color: white; line-height: 1.8;">
                        <li><strong>WhisperGate:</strong> Malware destrutivo que apaga discos</li>
                        <li><strong>HermeticWiper:</strong> Ataque a infraestrutura crítica</li>
                        <li><strong>Viasat KA-SAT:</strong> Hack de satélites de comunicação</li>
                        <li><strong>Sandworm:</strong> APT28 atacando power grids</li>
                    </ul>
                </div>
                
                <div style="background: rgba(0, 91, 187, 0.2); padding: 20px; border-radius: 10px;">
                    <h3 style="color: #005bbb;">🔵 DEFESA UCRANIANA</h3>
                    <ul style="color: white; line-height: 1.8;">
                        <li><strong>IT Army:</strong> 300K+ hackers voluntários</li>
                        <li><strong>Anonymous:</strong> Coletivo hackeando mídia russa</li>
                        <li><strong>NATO CCD:</strong> Centro de cyber defesa</li>
                        <li><strong>Starlink:</strong> Internet via satélite da SpaceX</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffff00;">📊 NÚMEROS IMPRESSIONANTES</h3>
                <ul style="color: white; line-height: 1.8;">
                    <li><strong>5000+</strong> cyberataques por dia contra a Ucrânia</li>
                    <li><strong>$100 bilhões</strong> em danos digitais estimados</li>
                    <li><strong>70%</strong> da infraestrutura crítica atacada</li>
                    <li><strong>24/7</strong> guerra cibernética paralela</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Stuxnet" in conflito:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #006633, #ff9900); padding: 25px; border-radius: 15px; border: 2px solid #006633; margin: 20px 0;">
            <h2 style="color: white; text-align: center;">🇮🇷 STUXNET: A PRIMEIRA CYBERWEAPON</h2>
            
            <div style="background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #ff9900;">🎯 COMO FUNCIONOU</h3>
                <ol style="color: white; line-height: 1.8;">
                    <li><strong>Infiltração:</strong> USB infectado em Natanz</li>
                    <li><strong>Propagação:</strong> Worm se espalhou por Windows</li>
                    <li><strong>Alvo:</strong> Controladores Siemens específicos</li>
                    <li><strong>Sabotagem:</strong> Centrifugas rodando em velocidade destrutiva</li>
                    <li><strong>Stealth:</strong> Reportava funcionamento normal</li>
                </ol>
            </div>
            
            <div style="background: rgba(255, 0, 0, 0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ff0000;">💥 RESULTADO</h3>
                <p style="color: white; line-height: 1.8;">
                <strong>1000+ centrifugas destruídas</strong> fisicamente por código malicioso. 
                O programa nuclear iraniano foi atrasado em <strong>2-3 anos</strong>. 
                Foi a primeira vez que software causou destruição física real!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Jogo: Cyber War Simulator
    st.markdown("""
    <div style="background: linear-gradient(45deg, #16213e, #0f0f23); padding: 25px; border-radius: 15px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; text-align: center; font-family: 'Orbitron', monospace;">
            🎮 CYBER WAR SIMULATOR
        </h2>
        <p style="color: white; text-align: center;">Você é um comandante cyber. Escolha suas armas digitais!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 0, 0, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #ff0000;">🚀 OFENSIVO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💣 DDoS Attack", key="ddos"):
            st.error("💥 Você derrubou os servidores inimigos! Mas eles vão voltar online...")
        if st.button("🦠 Deploy Malware", key="malware"):
            st.warning("🕷️ Malware implantado! Acesso backdoor estabelecido!")
        if st.button("📡 Jam Communications", key="jam"):
            st.info("📵 Comunicações interrompidas! Confusão nas linhas inimigas!")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(0, 0, 255, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #0066ff;">🛡️ DEFENSIVO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔥 Activate Firewall", key="firewall"):
            st.success("🛡️ Firewall ativado! Bloqueando 99% dos ataques!")
        if st.button("🔍 Deploy Honeypots", key="honeypot"):
            st.success("🍯 Honeypots ativos! Capturando hackers inimigos!")
        if st.button("⚡ Isolate Networks", key="isolate"):
            st.warning("🔒 Redes isoladas! Sistemas críticos protegidos!")
    
    with col3:
        st.markdown("""
        <div style="background: rgba(0, 255, 0, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #00ff41;">🕵️ ESPIONAGEM</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👁️ Monitor Traffic", key="monitor"):
            st.info("👀 Interceptando comunicações... Intel coletada!")
        if st.button("🔓 Social Engineering", key="social"):
            st.success("📞 CEO inimigo hackado via phishing!")
        if st.button("💾 Data Exfiltration", key="exfil"):
            st.error("💎 Documentos ultra-secretos roubados!")

# ==============================================================================
# EASTER EGG: HACK THE PLANET
# ==============================================================================
elif atividade == "🎮 Easter Egg: Hack the Planet":
    st.markdown("""
    <div class="activity-header">
        <h1>🎮 EASTER EGG: Hack the Planet!</h1>
        <p>Você encontrou o easter egg secreto! 🕹️ Prepare-se para o jogo supremo!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Efeito Matrix com CSS
    st.markdown("""
    <style>
    .matrix-bg {
        background: black;
        color: #00ff41;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .matrix-text {
        animation: matrix-fall 10s linear infinite;
    }
    
    @keyframes matrix-fall {
        0% { transform: translateY(-100vh); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    
    .hack-terminal {
        background: #000;
        color: #00ff41;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        border: 2px solid #00ff41;
        animation: glow 2s ease-in-out infinite alternate;
    }
    </style>
    
    <div class="matrix-bg">
        <div class="matrix-text">
            01001000 01100001 01100011 01101011 01100101 01110010<br>
            11000010 10110000 01000011 01111001 01100010 01100101<br>
            01110010 01001101 01100101 01101110 01110100 01101111<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hack-terminal">
        <h2>[SYSTEM ACCESS GRANTED]</h2>
        <p>>>> Initializing hack simulation...</p>
        <p>>>> Target: PENTAGON_MAINFRAME.exe</p>
        <p>>>> Status: BREACH DETECTED</p>
        <p>>>> User: Anonymous</p>
        <p>>>> Welcome to the MATRIX, Neo...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mega Quiz Master
    st.subheader("🏆 MEGA QUIZ: VOCÊ É O ULTIMATE HACKER?")
    
    ultimate_questions = [
        {
            "pergunta": "💀 Qual foi o primeiro vírus de computador da história?",
            "opcoes": ["A) Creeper (1971)", "B) Morris Worm (1988)", "C) ILOVEYOU (2000)", "D) Conficker (2008)"],
            "resposta": "A",
            "dica": "Foi criado nos anos 70 e exibia 'I'M THE CREEPER : CATCH ME IF YOU CAN'",
            "explicacao": "Creeper foi o primeiro malware autorreplicante, criado em 1971 na ARPANET!"
        },
        {
            "pergunta": "🔐 Qual algoritmo de hash é considerado 'quebrado' em 2024?", 
            "opcoes": ["A) SHA-256", "B) MD5", "C) SHA-512", "D) BLAKE3"],
            "resposta": "B",
            "dica": "Tem apenas 128 bits e é vulnerável a colisões desde 2004",
            "explicacao": "MD5 é facilmente quebrado hoje em dia. NUNCA use para segurança!"
        },
        {
            "pergunta": "🎯 Quantos zeros tem que ter no início de um hash Bitcoin válido?",
            "opcoes": ["A) Exatamente 4", "B) Pelo menos 19", "C) Varia (difficulty)", "D) Sempre 32"],
            "resposta": "C",
            "dica": "Muda a cada 2016 blocos para manter 10 minutos por bloco",
            "explicacao": "A dificuldade do Bitcoin se ajusta automaticamente! Atualmente precisa de ~19 zeros."
        },
        {
            "pergunta": "🚀 Qual empresa teve o maior vazamento de dados da história?",
            "opcoes": ["A) Equifax (147M)", "B) Yahoo (3B)", "C) LinkedIn (700M)", "D) Facebook (533M)"],
            "resposta": "B", 
            "dica": "Aconteceu em 2013 e afetou TODOS os usuários da época",
            "explicacao": "Yahoo foi hackeado em 2013 e TODOS os 3 bilhões de contas foram comprometidas!"
        }
    ]
    
    score = 0
    total_questions = len(ultimate_questions)
    
    for i, q in enumerate(ultimate_questions):
        st.markdown(f"""
        <div style="background: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #00ff41;">
            <h3 style="color: #00ff41;">Pergunta {i+1}/{total_questions}</h3>
            <h4 style="color: white;">{q['pergunta']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar dica
        if st.button(f"💡 Dica para pergunta {i+1}", key=f"hint_{i}"):
            st.info(f"🔍 **DICA:** {q['dica']}")
        
        user_answer = st.radio("Sua resposta:", q['opcoes'], key=f"ultimate_q_{i}")
        
        if st.button(f"🎯 Confirmar resposta {i+1}", key=f"ultimate_submit_{i}"):
            if user_answer.startswith(q['resposta']):
                st.success(f"✅ **CORRETO!** {q['explicacao']}")
                score += 1
                st.balloons()
            else:
                st.error(f"❌ **ERRADO!** {q['explicacao']}")
    
    # Resultado final do mega quiz
    if st.button("🏆 VER RESULTADO FINAL"):
        percentage = (score / total_questions) * 100
        
        if percentage == 100:
            st.success("🏆 **LENDÁRIO!** Você é um VERDADEIRO CYBERSECURITY MASTER!")
            st.balloons()
            st.markdown("""
            <div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white;">🎉 PARABÉNS! VOCÊ HACKEOU O SISTEMA!</h2>
                <p style="color: white; font-size: 1.2em;">Seu conhecimento em cybersegurança é INSANO!</p>
                <p style="color: white;">Título desbloqueado: 🏆 CYBER LEGENDS HALL OF FAME 🏆</p>
            </div>
            """, unsafe_allow_html=True)
        elif percentage >= 75:
            st.warning("🥈 **EXPERT!** Você domina cybersegurança!")
        elif percentage >= 50:
            st.info("🥉 **INTERMEDIÁRIO!** Continue estudando!")
        else:
            st.error("💀 **INICIANTE!** Precisa estudar mais segurança!")
    
    # Terminal secreto
    st.subheader("💻 TERMINAL SECRETO")
    command = st.text_input("root@cybermentor:~$ ", placeholder="Digite um comando...")
    
    if command:
        if command.lower() in ["help", "ajuda"]:
            st.code("""
Comandos disponíveis:
- hack: Simular um hack
- matrix: Entrar na Matrix
- bitcoin: Minerar Bitcoin
- virus: Criar vírus (simulação)
- exit: Sair do terminal
            """)
        elif command.lower() == "hack":
            st.success("🚨 ACESSO NEGADO... JUST KIDDING! 😄 Sistema hackeado com sucesso!")
        elif command.lower() == "matrix":
            st.markdown("🔴 Escolha: Pílula vermelha ou azul? A realidade te aguarda...")
        elif command.lower() == "bitcoin":
            st.info("⛏️ Minerando Bitcoin... Hash rate: 1000 TH/s... Block found! +6.25 BTC!")
        elif command.lower() == "virus":
            st.error("🦠 VÍRUS CRIADO! (Só de brincadeira, claro 😉)")
        elif command.lower() == "exit":
            st.warning("👋 Saindo do sistema... Hack concluído!")
        else:
            st.error(f"bash: {command}: command not found")

# ==============================================================================
# HACKERS ÉTICOS: GUARDIÕES DIGITAIS
# ==============================================================================
elif atividade == "🕵️‍♂️ Hackers Éticos: Guardiões Digitais":
    st.markdown("""
    <div class="activity-header">
        <h1>🕵️‍♂️ Hackers Éticos: Os Guardiões do Mundo Digital</h1>
        <p>Por que precisamos de "hackers do bem" para proteger nossa sociedade digital</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seção principal sobre hackers éticos
    st.markdown("""
    <div style="background: linear-gradient(45deg, #0f0f23, #1a1a2e, #16213e); padding: 30px; border-radius: 20px; border: 2px solid #00ff41; margin: 20px 0;">
        <h2 style="color: #00ff41; font-family: 'Orbitron', monospace; text-align: center;">
            🕵️‍♂️ Por que Precisamos de Hackers Éticos?
        </h2>
        
        <div style="color: white; line-height: 1.8; font-size: 1.1em;">
            <p><strong style="color: #ff6b35;">Hackers Éticos</strong> são os <strong>guardiões digitais</strong> do nosso mundo conectado. Eles usam as mesmas técnicas dos criminosos, mas para <strong>PROTEGER</strong> ao invés de atacar.</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 25px 0;">
                <div style="background: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 10px;">
                    <h3 style="color: #00ff41;">🛡️ O que fazem?</h3>
                    <ul>
                        <li><strong>Penetration Testing:</strong> Simulam ataques reais para encontrar vulnerabilidades</li>
                        <li><strong>Bug Bounty:</strong> Caçam falhas em sistemas para empresas como Google, Facebook</li>
                        <li><strong>Security Research:</strong> Descobrem novas ameaças antes dos criminosos</li>
                        <li><strong>Incident Response:</strong> Combatem ataques em tempo real</li>
                    </ul>
                </div>
                
                <div style="background: rgba(0, 102, 255, 0.1); padding: 20px; border-radius: 10px;">
                    <h3 style="color: #0066ff;">💰 Por que é crucial?</h3>
                    <ul>
                        <li><strong>Prejuízos evitados:</strong> Um hack pode custar até $10 milhões</li>
                        <li><strong>Reputação preservada:</strong> Vazamentos destroem confiança do cliente</li>
                        <li><strong>Conformidade legal:</strong> LGPD, GDPR exigem proteção de dados</li>
                        <li><strong>Continuidade do negócio:</strong> Evita paralisações custosas</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: rgba(255, 107, 53, 0.1); padding: 20px; border-radius: 10px; border-left: 4px solid #ff6b35; margin: 20px 0;">
                <h4 style="color: #ff6b35;">⚡ Fato Impressionante:</h4>
                <p>Um hacker ético pode ganhar <strong>mais de $500,000/ano</strong> e receber até <strong>$1 milhão</strong> por encontrar uma única vulnerabilidade crítica em grandes empresas!</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PROTEGENDO SEU COMPUTADOR
# ==============================================================================
elif atividade == "🛡️ Protegendo Seu Computador":
    st.markdown("""
    <div class="activity-header">
        <h1>🛡️ Guia Definitivo: Protegendo Seu Computador</h1>
        <p>Transforme-se de vítima em alvo impossível de hackear</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seção principal de proteção
    st.markdown("""
    <div style="background: linear-gradient(45deg, #1a1a2e, #16213e); padding: 30px; border-radius: 15px; border: 2px solid #ff6b35; margin: 20px 0;">
        <h2 style="color: #ff6b35; text-align: center; font-family: 'Orbitron', monospace;">
            🛡️ Como Proteger Seu Computador: Guia Definitivo
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="background: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #00ff41;">
                <h3 style="color: #00ff41;">🔐 Proteção Básica</h3>
                <ul style="color: white;">
                    <li><strong>Antivírus atualizado:</strong> Windows Defender + Malwarebytes</li>
                    <li><strong>Firewall ativo:</strong> Bloqueia conexões suspeitas</li>
                    <li><strong>Updates automáticos:</strong> Sistema e programas sempre atualizados</li>
                    <li><strong>Senhas fortes:</strong> 12+ caracteres, únicos por site</li>
                    <li><strong>2FA obrigatório:</strong> Autenticação em duas etapas</li>
                </ul>
            </div>
            
            <div style="background: rgba(0, 102, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #0066ff;">
                <h3 style="color: #0066ff;">🌐 Navegação Segura</h3>
                <ul style="color: white;">
                    <li><strong>HTTPS obrigatório:</strong> Só acesse sites com cadeado</li>
                    <li><strong>Downloads confiáveis:</strong> Apenas sites oficiais</li>
                    <li><strong>Email suspeito:</strong> NUNCA clique em links duvidosos</li>
                    <li><strong>WiFi público:</strong> Use VPN sempre</li>
                    <li><strong>Extensões seguras:</strong> uBlock Origin, HTTPS Everywhere</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(45deg, rgba(255, 0, 0, 0.1), rgba(255, 107, 53, 0.1)); padding: 20px; border-radius: 10px; border: 2px solid red; margin: 20px 0;">
            <h3 style="color: red; text-align: center;">🚨 SINAIS DE COMPROMISSO</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <h4 style="color: #ff6b35;">⚠️ Sintomas Críticos:</h4>
                    <ul style="color: white;">
                        <li>Lentidão súbita inexplicável</li>
                        <li>Programas abrindo sozinhos</li>
                        <li>Arquivos modificados/deletados</li>
                        <li>Tráfego de rede anômalo</li>
                        <li>Senhas não funcionando</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: #ff6b35;">🔥 Ação Imediata:</h4>
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

# ==============================================================================
# GUERRA CIBERNÉTICA CORPORATIVA
# ==============================================================================
elif atividade == "💰 Guerra Cibernética Corporativa":
    st.markdown("""
    <div class="game-card">
        <h2>💰 O Verdadeiro Custo da Insegurança Digital</h2>
        <p>Dados REAIS sobre quanto as empresas perdem por não investir em cibersegurança!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dados chocantes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="hash-result">
            <h4>💸 Custo Médio</h4>
            <h3>$4.45 MI</h3>
            <p>por vazamento de dados em 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="hash-result">
            <h4>⏰ Tempo Médio</h4>
            <h3>287 dias</h3>
            <p>para detectar uma invasão</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="hash-result">
            <h4>📈 Crescimento</h4>
            <h3>+15.3%</h3>
            <p>custos em relação a 2022</p>
        </div>
        """, unsafe_allow_html=True)
    
    caso_empresa = st.selectbox("Escolha um caso real:", [
        "🛒 Target - O Natal Hackeado (2013)",
        "🏛️ Equifax - 147 Milhões Expostos (2017)",
        "🏨 Marriott - 500 Milhões de Hóspedes (2018)",
        "🏥 Anthem - Dados de Saúde Roubados (2015)"
    ])
    
    if caso_empresa == "🛒 Target - O Natal Hackeado (2013)":
        st.markdown("""
        <div class="crime-story">
            <h3>🛒 Target: Como Hackers Roubaram o Natal</h3>
            
            <h4>💳 O Ataque</h4>
            <ul>
                <li><strong>Vítimas:</strong> 40 milhões de cartões de crédito</li>
                <li><strong>Dados roubados:</strong> 70 milhões de informações pessoais</li>
                <li><strong>Período:</strong> Black Friday até 15 de dezembro (pior época!)</li>
                <li><strong>Método:</strong> Hack via fornecedor de ar-condicionado</li>
            </ul>
            
            <h4>🎯 Como Aconteceu</h4>
            <p><strong>1. Spear Phishing:</strong> Email falso para empresa de refrigeração</p>
            <p><strong>2. Credenciais roubadas:</strong> Acesso limitado à rede Target</p>
            <p><strong>3. Escalação lateral:</strong> Movimento interno até sistemas de pagamento</p>
            <p><strong>4. Malware nos PDVs:</strong> Software capturava dados de cartões</p>
            
            <h4>💰 Prejuízos Totais</h4>
            <ul>
                <li><strong>Custos diretos:</strong> $162 milhões</li>
                <li><strong>Multas:</strong> $39 milhões</li>
                <li><strong>Queda nas vendas:</strong> -46% no 4º trimestre</li>
                <li><strong>CEO demitido:</strong> Gregg Steinhafel saiu da empresa</li>
                <li><strong>Total estimado:</strong> +$1 bilhão</li>
            </ul>
            
            <h4>🛡️ O que Poderia ter Evitado</h4>
            <ul>
                <li><strong>Segmentação de rede:</strong> $50 mil em equipamentos</li>
                <li><strong>Monitoramento 24/7:</strong> $200 mil/ano em SOC</li>
                <li><strong>Treinamento:</strong> $30 mil em conscientização</li>
                <li><strong>Total investimento:</strong> ~$500 mil vs $1 bilhão de prejuízo!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif caso_empresa == "🏛️ Equifax - 147 Milhões Expostos (2017)":
        st.markdown("""
        <div class="crime-story">
            <h3>🏛️ Equifax: O Apocalipse dos Dados Pessoais</h3>
            
            <h4>💀 O Desastre</h4>
            <ul>
                <li><strong>Vítimas:</strong> 147 milhões de americanos (quase metade da população!)</li>
                <li><strong>Dados expostos:</strong> CPF, endereços, datas de nascimento, carteiras de motorista</li>
                <li><strong>Duração:</strong> Maio a Julho 2017 (76 dias de acesso)</li>
                <li><strong>Causa:</strong> Falha em aplicar patch de segurança conhecido</li>
            </ul>
            
            <h4>🐛 A Vulnerabilidade</h4>
            <p><strong>Apache Struts CVE-2017-5638:</strong> Falha conhecida desde março 2017</p>
            <p><strong>Patch disponível:</strong> 2 meses antes do ataque</p>
            <p><strong>Equifax não aplicou:</strong> Falta de processo de atualização</p>
            
            <h4>💰 Prejuízos Históricos</h4>
            <ul>
                <li><strong>Multa inicial:</strong> $700 milhões</li>
                <li><strong>Multa adicional:</strong> $1.4 bilhão</li>
                <li><strong>Queda de ações:</strong> -35% = $5 bilhões</li>
                <li><strong>Custos de remediação:</strong> $1.6 bilhão</li>
                <li><strong>Total:</strong> +$8 bilhões!</li>
            </ul>
            
            <h4>⚖️ Consequências Pessoais</h4>
            <ul>
                <li><strong>CEO demitido:</strong> Richard Smith</li>
                <li><strong>CIO demitido:</strong> David Webb</li>
                <li><strong>CSO demitida:</strong> Susan Mauldin</li>
                <li><strong>Processo criminal:</strong> Ex-executivos presos por insider trading</li>
            </ul>
            
            <h4>🛡️ Lição Aprendida</h4>
            <p><strong>Custo do patch:</strong> $0 (grátis)</p>
            <p><strong>Tempo para aplicar:</strong> 30 minutos</p>
            <p><strong>Custo de não aplicar:</strong> $8 bilhões</p>
            <p><strong>ROI da segurança:</strong> INFINITO! 🤯</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# OFENSIVA VS PREVENTIVA
# ==============================================================================
elif atividade == "🛡️ Ofensiva vs Preventiva":
    st.markdown("""
    <div class="game-card">
        <h2>🛡️ Cibersegurança: Ofensiva vs Preventiva</h2>
        <p>Entenda a diferença entre hackear e se defender!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["⚔️ Segurança Ofensiva", "🛡️ Segurança Preventiva", "🎯 Red Team vs Blue Team"])
    
    with tab1:
        st.markdown("""
        <div class="crime-story">
            <h3>⚔️ Segurança Ofensiva (Red Team)</h3>
            <p><strong>"Para se defender do inimigo, você precisa pensar como ele"</strong></p>
            
            <h4>🎯 O que Fazem</h4>
            <ul>
                <li><strong>Penetration Testing:</strong> Hackear sistemas com permissão</li>
                <li><strong>Bug Bounty:</strong> Encontrar falhas por recompensa</li>
                <li><strong>Red Team Exercises:</strong> Simular ataques reais</li>
                <li><strong>Social Engineering:</strong> Testar fator humano</li>
            </ul>
            
            <h4>🛠️ Ferramentas do Red Team</h4>
            <ul>
                <li><strong>Kali Linux:</strong> OS completo para pentesting</li>
                <li><strong>Metasploit:</strong> Framework de exploração</li>
                <li><strong>Nmap:</strong> Scanner de rede e ports</li>
                <li><strong>Burp Suite:</strong> Teste de aplicações web</li>
                <li><strong>Cobalt Strike:</strong> Simulação de APT</li>
            </ul>
            
            <h4>💰 Quanto Ganham?</h4>
            <ul>
                <li><strong>Junior Pentester:</strong> R$ 5.000 - R$ 8.000</li>
                <li><strong>Senior Pentester:</strong> R$ 12.000 - R$ 20.000</li>
                <li><strong>Bug Bounty Hunter:</strong> $1.000 - $100.000 por bug</li>
                <li><strong>Red Team Lead:</strong> R$ 25.000 - R$ 40.000</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Mini-simulação
        with st.expander("🎮 Simulação: Sua Primeira Penetração"):
            st.markdown("**Cenário:** Você foi contratado para testar um e-commerce. Por onde começar?")
            
            fase = st.radio("Escolha sua primeira fase:", [
                "🔍 Reconhecimento (OSINT)",
                "💻 Scan de vulnerabilidades",
                "🎣 Phishing nos funcionários", 
                "🚪 Tentar SQL injection direto"
            ])
            
            if st.button("🎯 Executar Fase"):
                if fase == "🔍 Reconhecimento (OSINT)":
                    st.success("""✅ CORRETO! Metodologia OWASP PTES:
                    - 📧 Emails públicos encontrados
                    - 🌐 Subdomínios descobertos 
                    - 👥 Funcionários no LinkedIn mapeados
                    - 🛠️ Tecnologias identificadas""")
                else:
                    st.warning("⚠️ Muito agressivo! Sempre comece com reconhecimento passivo.")
    
    with tab2:
        st.markdown("""
        <div class="interactive-demo">
            <h3>🛡️ Segurança Preventiva (Blue Team)</h3>
            <p><strong>"É melhor prevenir do que remediar"</strong></p>
            
            <h4>🎯 O que Fazem</h4>
            <ul>
                <li><strong>SIEM/SOC:</strong> Monitoramento 24/7</li>
                <li><strong>Incident Response:</strong> Resposta a incidentes</li>
                <li><strong>Threat Hunting:</strong> Caça ativa a ameaças</li>
                <li><strong>Digital Forensics:</strong> Investigação pós-ataque</li>
            </ul>
            
            <h4>🛠️ Ferramentas do Blue Team</h4>
            <ul>
                <li><strong>Splunk/ELK:</strong> SIEM para correlação de logs</li>
                <li><strong>Carbon Black:</strong> EDR para endpoints</li>
                <li><strong>Wireshark:</strong> Análise de tráfego de rede</li>
                <li><strong>YARA:</strong> Detecção de malware</li>
                <li><strong>TheHive:</strong> Gerenciamento de incidentes</li>
            </ul>
            
            <h4>💰 Quanto Ganham?</h4>
            <ul>
                <li><strong>SOC Analyst L1:</strong> R$ 3.500 - R$ 6.000</li>
                <li><strong>SOC Analyst L2:</strong> R$ 6.000 - R$ 10.000</li>
                <li><strong>CISO:</strong> R$ 25.000 - R$ 50.000</li>
                <li><strong>Incident Response:</strong> R$ 15.000 - R$ 25.000</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="mini-game">
            <h3>🎯 Red Team vs Blue Team: A Batalha Eterna</h3>
            <p>Escolha seu lado e veja como seria um dia típico!</p>
        </div>
        """, unsafe_allow_html=True)
        
        lado = st.radio("Qual lado você quer conhecer?", ["🔴 Red Team", "🔵 Blue Team"])
        
        if lado == "🔴 Red Team":
            st.markdown("""
            <div class="crime-story">
                <h4>🔴 Dia de um Red Team Hacker</h4>
                <p><strong>08:00</strong> - ☕ Café e planejamento do ataque</p>
                <p><strong>09:00</strong> - 🔍 OSINT: stalkeando funcionários no LinkedIn</p>
                <p><strong>10:30</strong> - 📧 Criando emails de phishing personalizados</p>
                <p><strong>12:00</strong> - 🍕 Almoço (hackers também comem!)</p>
                <p><strong>13:00</strong> - 💻 Testando payloads no Metasploit</p>
                <p><strong>15:00</strong> - 🎭 Ligando se passando por suporte técnico</p>
                <p><strong>16:00</strong> - 🚪 Tentando acessar o prédio disfarçado</p>
                <p><strong>17:30</strong> - 📝 Documentando vulnerabilidades encontradas</p>
                <p><strong>18:00</strong> - 🍺 Happy hour falando de exploits</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="interactive-demo">
                <h4>🔵 Dia de um Blue Team Defender</h4>
                <p><strong>08:00</strong> - ☕ Café checando alertas da madrugada</p>
                <p><strong>09:00</strong> - 📊 Analisando dashboards do SIEM</p>
                <p><strong>10:30</strong> - 🚨 ALERTA! Possível malware detectado</p>
                <p><strong>11:00</strong> - 🔍 Investigando logs suspeitos</p>
                <p><strong>12:00</strong> - 🍕 Almoço rápido (emergência não espera)</p>
                <p><strong>13:00</strong> - 🧹 Limpando infecção encontrada</p>
                <p><strong>15:00</strong> - 📋 Atualizando playbooks de resposta</p>
                <p><strong>16:00</strong> - 🎯 Threat hunting proativo</p>
                <p><strong>17:30</strong> - 📝 Relatório do incidente</p>
                <p><strong>18:00</strong> - 🏠 Para casa (se não tocar o alarme!)</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🏆 Completei a Missão!"):
            if "ofensiva_preventiva" not in st.session_state.missoes_completas:
                st.session_state.missoes_completas.append("ofensiva_preventiva")
                st.session_state.pontos_crypto += 40
                st.success("🎉 Você entendeu a diferença! +40 pontos!")

# ==============================================================================
# DESAFIO FINAL
# ==============================================================================
elif atividade == "🏆 Desafio Final":
    st.markdown("""
    <div class="game-card">
        <h2>🏆 Desafio Final do CyberMentor</h2>
        <p>Prove que você domina os conceitos de criptografia!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.pontos_crypto < 50:
        st.warning("⚠️ Você precisa de pelo menos 50 pontos para fazer o desafio final. Complete mais atividades!")
    else:
        st.markdown("""
        <div class="interactive-demo">
            <h3>🎯 Missão: Decifre a Mensagem do Hacker</h3>
            <p>Um hacker interceptou esta mensagem. Usando seus conhecimentos, descubra o que ela diz!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gerar desafio complexo
        if 'desafio_final' not in st.session_state:
            mensagem_secreta_final = "CYBERMENTOR AI SECURITY MASTER"
            # Primeiro aplicar Caesar cipher, depois Base64
            caesar_shift = 13
            mensagem_caesar = ""
            for char in mensagem_secreta_final:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    mensagem_caesar += chr((ord(char) - base + caesar_shift) % 26 + base)
                else:
                    mensagem_caesar += char
            
            mensagem_base64 = base64.b64encode(mensagem_caesar.encode()).decode()
            st.session_state.desafio_final_msg = mensagem_base64
            st.session_state.desafio_final_resposta = mensagem_secreta_final
            st.session_state.desafio_final = True
        
        st.markdown(f"""
        <div class="mini-game">
            <h4>🔐 Mensagem Interceptada:</h4>
            <code>{st.session_state.desafio_final_msg}</code>
            
            <h4>🕵️ Dicas:</h4>
            <ul>
                <li>A mensagem passou por 2 transformações</li>
                <li>Uma é uma codificação comum da web</li>
                <li>A outra é um cipher clássico com shift 13</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        resposta_final = st.text_input("Digite a mensagem decifrada:", key="desafio_final")
        
        if st.button("🎯 Verificar Resposta Final"):
            if resposta_final.upper().replace(" ", "") == st.session_state.desafio_final_resposta.replace(" ", ""):
                st.success("🎉 PARABÉNS! Você é oficialmente um CYBER SECURITY MASTER!")
                st.session_state.pontos_crypto += 100
                st.session_state.nivel_usuario = "Expert"
                if "desafio_final" not in st.session_state.missoes_completas:
                    st.session_state.missoes_completas.append("desafio_final")
                st.balloons()
                
                st.markdown("""
                <div class="game-card">
                    <h3>🏆 CERTIFICADO DE CONCLUSÃO</h3>
                    <p>Você completou todos os desafios do Laboratório de Criptografia!</p>
                    <p><strong>Conceitos Dominados:</strong></p>
                    <ul>
                        <li>✅ Funções Hash (MD5, SHA-256)</li>
                        <li>✅ Segurança de Senhas</li>
                        <li>✅ Criptografia Simétrica</li>
                        <li>✅ Casos Reais de Segurança</li>
                        <li>✅ Análise de Algoritmos</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Ainda não está correto. Pense nas dicas!")

# Footer atualizado
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🛡️ <strong>CyberMentor AI</strong> - Laboratório Interativo de Criptografia</p>
    <p>Desenvolvido por <strong>Diego Fonte</strong> | 
    <a href="https://www.diegofontedev.com.br" target="_blank">www.diegofontedev.com.br</a> | 
    <a href="https://zowti.com" target="_blank">zowti.com</a></p>
    <p><small>🎮 Aprender criptografia nunca foi tão divertido!</small></p>
</div>
""", unsafe_allow_html=True)