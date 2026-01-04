<p align="center">
  <img src="Banner_Projeto.png" alt="Banner do Projeto" width="100%">
</p>

# 📄 Extrator de Dados de Comprovantes Bancários

Um script inteligente em Python que **lê comprovantes bancários em PDF**, extrai informações importantes como **razão social**, **valor** e **data de pagamento**, mesmo com variações no layout dos boletos. Tudo isso de forma automática — com os arquivos já **renomeados** no padrão certo!

---

## 🚀 Funcionalidades

✅ Identifica a Razão Social (nome da empresa)  
✅ Extrai o valor do pagamento com precisão  
✅ Detecta a data de pagamento mesmo quando aparece como `(=)`, `:` ou em outra linha ("Operação efetuada em")  
✅ Renomeia os arquivos PDF com as informações extraídas  
✅ Suporte a vários tipos de comprovantes (boleto, TED, PIX, etc.)

---

## 🧠 Como Funciona

1. O script analisa o texto dos PDFs.
2. Usa **expressões regulares (Regex)** para identificar:
   - Razão Social
   - Valor pago
   - Data do pagamento
3. Se a data estiver no formato estranho (como `(=) Data de pagamento`) ou em outra linha, ele ainda encontra!
4. O nome do arquivo é atualizado automaticamente para:


# Sistema de Comprovantes - Engefic Engenharia

Sistema automatizado para renomeação de comprovantes bancários do Itaú.

## Acesso
- Login com conta Google Workspace @engefic.com.br
- Processamento local e seguro
- Sem armazenamento de dados

## Suporte
- Email: ti@engefic.com.br
- Ramal: 1234
```

---

## 📝 **ETAPA 2: Criar Conta no GitHub (Gratuito)**

1. **Acesse:** https://github.com
2. Clique em **"Sign up"** (Cadastrar)
3. Preencha:
   - Email: (seu email pessoal ou corporativo)
   - Senha: (crie uma senha segura)
   - Username: `engefic-ti` (ou qualquer nome)
4. Verifique seu email
5. ✅ **Pronto! Conta criada**

---

## 📤 **ETAPA 3: Fazer Upload dos Arquivos no GitHub**

### **Passo 3.1: Criar repositório**

1. No GitHub, clique no **"+"** no canto superior direito
2. Escolha **"New repository"**
3. Preencha:
   - **Repository name:** `comprovantes-engefic`
   - **Description:** Sistema de comprovantes Engefic
   - **Deixe como:** Public ✅
4. Clique em **"Create repository"**

### **Passo 3.2: Fazer upload dos arquivos**

1. Na página do repositório, clique em **"uploading an existing file"**
2. Arraste os 3 arquivos para a área:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. No campo de baixo escreva: `Primeira versão`
4. Clique em **"Commit changes"**
5. ✅ **Arquivos enviados!**

---

## 🚀 **ETAPA 4: Deploy no Streamlit Cloud (Gratuito)**

### **Passo 4.1: Criar conta no Streamlit**

1. **Acesse:** https://share.streamlit.io
2. Clique em **"Sign up"**
3. Escolha **"Continue with GitHub"**
4. Autorize o Streamlit a acessar seu GitHub
5. ✅ **Conta conectada!**

### **Passo 4.2: Criar o app**

1. No Streamlit Cloud, clique em **"New app"**
2. Preencha:
   - **Repository:** `engefic-ti/comprovantes-engefic` (selecione o seu)
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** `comprovantes-engefic` (você pode escolher)
3. Clique em **"Deploy!"**
4. ⏳ **Aguarde 2-3 minutos...**
5. ✅ **App online!**

Seu link será algo como:
```
https://comprovantes-engefic.streamlit.app
```

---

## 🔐 **ETAPA 5: Configurar Google Workspace (Opcional - Avançado)**

Para integração OAuth REAL com Google (login automático), você precisará:

### **Passo 5.1: Criar projeto no Google Cloud**

1. **Acesse:** https://console.cloud.google.com
2. Clique em **"Select a project"** → **"New Project"**
3. Nome: `Comprovantes Engefic`
4. Clique em **"Create"**

### **Passo 5.2: Ativar Google OAuth**

1. No menu lateral, vá em **"APIs & Services"** → **"Credentials"**
2. Clique em **"Create Credentials"** → **"OAuth client ID"**
3. Escolha **"Web application"**
4. Preencha:
   - **Name:** `Engefic Comprovantes`
   - **Authorized redirect URIs:** 
```
     https://comprovantes-engefic.streamlit.app