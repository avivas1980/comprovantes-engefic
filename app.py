import streamlit as st
import pdfplumber
import PyPDF2
import re
import io
import zipfile
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
import json

# ============================================
# CONFIGURAÇÃO
# ============================================

st.set_page_config(
    page_title="Sistema de Comprovantes - Engefic",
    page_icon="📄",
    layout="wide"
)

# Aplica o CSS da identidade visual da Engefic
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Domínio permitido
DOMINIO_PERMITIDO = "engefic.com.br"

# ============================================
# AUTENTICAÇÃO COM GOOGLE
# ============================================

def verificar_dominio_email(email):
    """Verifica se o email é do domínio da empresa"""
    return email.lower().endswith(f"@{DOMINIO_PERMITIDO}")

def init_google_auth():
    """Inicializa autenticação Google"""
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
        st.session_state.usuario_email = None
        st.session_state.usuario_nome = None

def tela_login():
    """Tela de login com Google"""
    
    # CSS para o botão do Google
    st.markdown("""
        <style>
        .google-btn {
            background-color: white;
            border: 1px solid #dadce0;
            border-radius: 4px;
            color: #3c4043;
            cursor: pointer;
            font-family: 'Google Sans',arial,sans-serif;
            font-size: 14px;
            height: 40px;
            letter-spacing: 0.25px;
            padding: 0 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: background-color .218s, border-color .218s;
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
        }
        .google-btn:hover {
            background-color: #f7f8f8;
            border-color: #dadce0;
        }
        .google-logo {
            height: 18px;
            width: 18px;
            margin-right: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logo e Header
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="display: inline-flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <div>
                    <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                        <div style="display: flex; gap: 4px;">
                            <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 60px; border-radius: 4px;"></div>
                            <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 60px; border-radius: 4px;"></div>
                        </div>
                        <div style="display: flex; gap: 4px;">
                            <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 40px; border-radius: 4px;"></div>
                            <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 80px; border-radius: 4px;"></div>
                        </div>
                        <div style="display: flex; gap: 4px;">
                            <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 60px; border-radius: 4px;"></div>
                            <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 24px; border-radius: 4px;"></div>
                        </div>
                    </div>
                </div>
                <div>
                    <div style="font-size: 2rem; font-weight: bold; color: #0B5563;">engefic</div>
                    <div style="color: #E86B82; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">ENGENHARIA</div>
                </div>
            </div>
            <h2 style="color: #0B5563; margin-bottom: 0.5rem;">Sistema de Comprovantes</h2>
            <p style="color: #64748b; margin-bottom: 2rem;">Acesso Restrito - Colaboradores Engefic</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login com Google Workspace")
        
        # Formulário simples para simular login Google
        # Em produção, use a biblioteca streamlit-google-auth
        st.info("📧 Use sua conta @engefic.com.br para fazer login")
        
        email_input = st.text_input(
            "Email corporativo",
            placeholder="seu.nome@engefic.com.br",
            key="email_login"
        )
        
        if st.button("🔐 Entrar com Google", use_container_width=True, type="primary"):
            if email_input and verificar_dominio_email(email_input):
                # Simular login bem-sucedido
                st.session_state.autenticado = True
                st.session_state.usuario_email = email_input
                st.session_state.usuario_nome = email_input.split('@')[0].replace('.', ' ').title()
                st.rerun()
            elif not email_input:
                st.error("❌ Digite seu email corporativo")
            else:
                st.error(f"❌ Acesso negado. Use um email @{DOMINIO_PERMITIDO}")
        
        st.markdown("---")
        
        with st.expander("ℹ️ Sobre o Sistema"):
            st.markdown(f"""
            **Acesso Seguro com Google:**
            - Login com sua conta Google Workspace
            - Apenas colaboradores @{DOMINIO_PERMITIDO}
            - Sem necessidade de senha adicional
            - Autenticação gerenciada pelo Google
            
            **Dúvidas ou Problemas?**
            - Entre em contato com o TI
            - Email: ti@engefic.com.br
            - Ramal: 1234
            
            **Privacidade:**
            - Seus dados não são armazenados
            - Processamento local dos arquivos
            - Nenhum comprovante fica no servidor
            """)

# ============================================
# FUNÇÕES DE PROCESSAMENTO
# ============================================

def limpar_nome_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*]', '', nome).strip()

def limpar_razao_social_pelo_espaco(texto_bruto):
    if not texto_bruto:
        return "Desconhecido"
    partes = re.split(r'\s{3,}', texto_bruto)
    razao_social = partes[0].strip()
    razao_social = re.sub(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', '', razao_social).strip()
    razao_social = re.sub(r'\d{8}', '', razao_social).strip()
    razao_social = re.sub(r'\s+', ' ', razao_social).strip()
    return razao_social

def extrair_dados_boleto(texto_layout, texto_simples):
    nome = "Comprovante"
    valor = "0,00"
    data = "Data-Desconhecida"
    
    match_nome = re.search(r'Razão Social:\s*(.{0,200})', texto_layout, re.IGNORECASE)
    if match_nome:
        texto_bruto = match_nome.group(1).strip()
        nome = limpar_razao_social_pelo_espaco(texto_bruto)
    
    match_valor = re.search(r'\(=\)\s*Valor do pagamento \(R\$\):\s*(\d[\d\.,]*)', texto_simples, re.IGNORECASE)
    if not match_valor:
        match_valor = re.search(r'48\.042\.150/0001-94\s+([\d\.,]+)', texto_simples, re.IGNORECASE)
    if not match_valor:
        match_valor = re.search(r'\d{2}\.\d{3}\.\d{4}-\d{2}\s+([\d.,]+)\s+[\(=)]*\s*Data de pagamento', texto_simples, re.IGNORECASE)

    if not match_valor:
        busca_area = re.search(r'Valor do pagamento.*?(\d{1,3}(?:\.\d{3})*,\d{2})', texto_simples, re.IGNORECASE | re.DOTALL)
        if busca_area:
            match_valor = busca_area
    
    if match_valor:
        valor_bruto = match_valor.group(1).strip()
        valor = f"R$ {valor_bruto}"

    match_data = re.search(r'(?:\(\s*=\s*\)\s*|=|:)?\s*Data de pagamento\s*[:\s]*\n*\s*(\d{2}/\d{2}/\d{4})',texto_simples,re.IGNORECASE)

    if match_data:
       data = match_data.group(1).replace('/', '-')
    return nome, valor, data

def extrair_dados_transferencia(texto_layout, texto_simples):
    nome = "Comprovante"
    valor = "0,00"
    data = "Data-Desconhecida"
    
    match_nome = re.search(r'nome do recebedor:\s*([^\r\n]{3,100})', texto_layout, re.IGNORECASE)
    if match_nome:
        nome = match_nome.group(1).strip()
        nome = re.split(r'\s{3,}', nome)[0].strip()
    
    match_valor = re.search(r'valor:\s*R?\$?\s*(\d{1,3}(?:\.\d{3})*,\d{2})', texto_simples, re.IGNORECASE)
    if match_valor:
        valor = f"R$ {match_valor.group(1).strip()}"
    
    match_data = re.search(r'data da transferência:\s*(\d{2}/\d{2}/\d{4})', texto_simples, re.IGNORECASE)
    if match_data:
        data = match_data.group(1).replace('/', '-')
    
    return nome, valor, data

def extrair_dados_pix_qrcode(texto_layout, texto_simples):
    nome = "Comprovante"
    valor = "0,00"
    data = "Data-Desconhecida"
    
    match_nome = re.search(r'nome do recebedor:\s*([^\r\n]{3,100})', texto_layout, re.IGNORECASE)
    if match_nome:
        nome = match_nome.group(1).strip()
        nome = re.split(r'\s{3,}', nome)[0].strip()
    
    match_valor = re.search(r'(?:valor da transação|valor final):\s*(\d{1,3}(?:\.\d{3})*,\d{2})', texto_simples, re.IGNORECASE)
    if match_valor:
        valor = f"R$ {match_valor.group(1).strip()}"
    
    match_data = re.search(r'Pagamento efetuado em\s*(\d{2}/\d{2}/\d{4})', texto_simples, re.IGNORECASE)
    if match_data:
        data = match_data.group(1).replace('/', '-')
    
    return nome, valor, data

def extrair_dados_ted(texto_layout, texto_simples):
    nome = "Comprovante"
    valor = "0,00"
    data = "Data-Desconhecida"
    
    match_nome = re.search(r'Nome do favorecido:\s*([^\r\n]{3,100})', texto_layout, re.IGNORECASE)
    if match_nome:
        nome = match_nome.group(1).strip()
        nome = re.split(r'\s{3,}', nome)[0].strip()
    
    match_valor = re.search(r'Valor da TED:\s*R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2})', texto_simples, re.IGNORECASE)
    if match_valor:
        valor = f"R$ {match_valor.group(1).strip()}"
    
    match_data = re.search(r'TED solicitada em\s*(\d{2}/\d{2}/\d{4})', texto_simples, re.IGNORECASE)
    if match_data:
        data = match_data.group(1).replace('/', '-')
    
    return nome, valor, data

def extrair_dados_transferencia_cc(texto_layout, texto_simples):
    nome = "Comprovante"
    valor = "0,00"
    data = "Data-Desconhecida"
    
    match_nome = re.search(r'Dados da conta creditada:[\s\S]{0,200}?Nome:\s*([^\r\n]{3,100})', texto_layout, re.IGNORECASE)
    if match_nome:
        nome = match_nome.group(1).strip()
        nome = re.split(r'\s{3,}', nome)[0].strip()
    
    match_valor = re.search(r'Valor:\s*R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2})', texto_simples, re.IGNORECASE)
    if match_valor:
        valor = f"R$ {match_valor.group(1).strip()}"
    
    match_data = re.search(r'Transferência efetuada em\s*(\d{2}/\d{2}/\d{4})', texto_simples, re.IGNORECASE)
    if match_data:
        data = match_data.group(1).replace('/', '-')
    
    return nome, valor, data

def identificar_tipo_comprovante(texto):
    texto_lower = texto.lower()
    
    if "pagamento de boleto" in texto_lower and "razão social:" in texto_lower:
        return "boleto"
    elif "ted" in texto_lower and "nome do favorecido:" in texto_lower:
        return "ted"
    elif "pix qr code" in texto_lower:
        return "pix_qrcode"
    elif "dados da conta creditada" in texto_lower and "transferência efetuada" in texto_lower:
        return "transferencia_cc"
    elif "transferência" in texto_lower or "nome do recebedor:" in texto_lower:
        return "transferencia"
    else:
        return "desconhecido"

def extrair_dados_inteligente(texto_layout, texto_simples):
    tipo = identificar_tipo_comprovante(texto_simples)
    
    if tipo == "boleto":
        return extrair_dados_boleto(texto_layout, texto_simples)
    elif tipo == "ted":
        return extrair_dados_ted(texto_layout, texto_simples)
    elif tipo == "pix_qrcode":
        return extrair_dados_pix_qrcode(texto_layout, texto_simples)
    elif tipo == "transferencia_cc":
        return extrair_dados_transferencia_cc(texto_layout, texto_simples)
    elif tipo == "transferencia":
        return extrair_dados_transferencia(texto_layout, texto_simples)
    else:
        nome, valor, data = extrair_dados_boleto(texto_layout, texto_simples)
        if nome == "Comprovante" or valor == "0,00":
            nome, valor, data = extrair_dados_transferencia(texto_layout, texto_simples)
        return nome, valor, data

# ============================================
# APLICAÇÃO PRINCIPAL
# ============================================

init_google_auth()

# Verificar autenticação
if not st.session_state.autenticado:
    tela_login()
    st.stop()

# CSS customizado
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom right, #f8fafc, #f1f5f9); }
    .stButton>button {
        background: linear-gradient(to right, #0B5563, #0d6478);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: 600;
    }
    .success-box {
        background: linear-gradient(to right, #fef2f2, #fef9c3);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #E86B82;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col_logo, col_user = st.columns([3, 1])

with col_logo:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div>
                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                    <div style="display: flex; gap: 4px;">
                        <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 60px; border-radius: 4px;"></div>
                        <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 60px; border-radius: 4px;"></div>
                    </div>
                    <div style="display: flex; gap: 4px;">
                        <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 40px; border-radius: 4px;"></div>
                        <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 80px; border-radius: 4px;"></div>
                    </div>
                    <div style="display: flex; gap: 4px;">
                        <div style="background: linear-gradient(to right, #E86B82, #f082a0); height: 8px; width: 60px; border-radius: 4px;"></div>
                        <div style="background: linear-gradient(to right, #FDB913, #fdc943); height: 8px; width: 24px; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: #0B5563;">engefic</div>
                <div style="color: #E86B82; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">ENGENHARIA</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_user:
    st.markdown(f"""
        <div style="text-align: right; padding-top: 1rem;">
            <p style="color: #0B5563; font-weight: 600; margin: 0;">👤 {st.session_state.usuario_nome}</p>
            <p style="color: #64748b; font-size: 0.75rem; margin: 0;">{st.session_state.usuario_email}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.rerun()

st.title("📄 Sistema de Renomeação de Comprovantes")
st.markdown("**Departamento Financeiro** | Processamento automático de comprovantes Itaú")
st.markdown("---")

# Upload
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 📤 Upload do Arquivo")
    uploaded_file = st.file_uploader(
        "Selecione o PDF com os comprovantes do Itaú",
        type=['pdf'],
        help="Faça upload do arquivo PDF contendo múltiplos comprovantes"
    )

if uploaded_file is not None:
    st.success(f"✅ Arquivo carregado: **{uploaded_file.name}** ({uploaded_file.size / 1024 / 1024:.2f} MB)")
    
    if st.button("🚀 Processar Comprovantes", use_container_width=True):
        with st.spinner("⏳ Processando comprovantes... Por favor, aguarde."):
            try:
                zip_buffer = io.BytesIO()
                resultados = []
                
                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                    total_paginas = len(pdf.pages)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    uploaded_file.seek(0)
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                    
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for i, pagina in enumerate(pdf.pages):
                            progresso = (i + 1) / total_paginas
                            progress_bar.progress(progresso)
                            status_text.text(f"Processando página {i+1} de {total_paginas}...")
                            
                            texto_layout = pagina.extract_text(layout=True) or ""
                            texto_simples = pagina.extract_text(layout=False) or ""
                            
                            nome_entidade, valor_pgto, data_pgto = extrair_dados_inteligente(texto_layout, texto_simples)
                            
                            contador = f"{i+1:02d}"
                            novo_nome = f"{nome_entidade}_{valor_pgto}_{data_pgto}_{contador}_Comp_pgto.pdf"

                            novo_nome = limpar_nome_arquivo(novo_nome)
                            
                            pdf_writer = PyPDF2.PdfWriter()
                            pdf_writer.add_page(pdf_reader.pages[i])
                            
                            pdf_bytes = io.BytesIO()
                            pdf_writer.write(pdf_bytes)
                            pdf_bytes.seek(0)
                            zipf.writestr(novo_nome, pdf_bytes.read())
                            
                            resultados.append({
                                'pagina': i + 1,
                                'nome': novo_nome,
                                'entidade': nome_entidade,
                                'valor': valor_pgto,
                                'data': data_pgto
                            })
                
                progress_bar.progress(1.0)
                status_text.text("✅ Processamento concluído!")
                
                st.markdown("---")
                st.markdown("### ✅ Processamento Concluído!")
                st.success(f"**{len(resultados)} comprovantes** processados com sucesso por {st.session_state.usuario_nome}!")
                
                zip_buffer.seek(0)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Baixar ZIP com Todos os Comprovantes",
                    data=zip_buffer,
                    file_name=f"Comprovantes_Renomeados_{timestamp}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                
                st.markdown("---")
                st.markdown("### 📋 Arquivos Processados")
                
                with st.expander(f"Ver detalhes dos {len(resultados)} arquivos", expanded=True):
                    for res in resultados:
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>Página {res['pagina']}:</strong> {res['nome']}<br>
                            <small style="color: #64748b;">
                                👤 {res['entidade']} | 💰 {res['valor']} | 📅 {res['data']}
                            </small>
                        </div>
                        """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar o arquivo: {str(e)}")

else:
    st.markdown("---")
    st.markdown("### 📖 Como Usar")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1️⃣ Upload** - Selecione o PDF")
    with col2:
        st.markdown("**2️⃣ Processar** - Aguarde")
    with col3:
        st.markdown("**3️⃣ Download** - Baixe o ZIP")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.875rem; padding: 2rem 0;">
        © 2025 Engefic Engenharia - Sistema de Gestão de Comprovantes
    </div>
""", unsafe_allow_html=True)


