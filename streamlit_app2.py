import streamlit as st
from auth import login, verify_token
import streamlit_ace as st_ace
import streamlit as st
import sqlite3
import pandas as pd
import base64
import time

# Função para verificar o token JWT em cada rota protegida
def verify_access():
    token = st.session_state.token  # Obtém o token armazenado na sessão
    
    if not token:  # Se o token não estiver presente, redirecione para a página de login
        st.error("Você não está autenticado. Faça login para acessar esta página.")
        st.markdown('<meta http-equiv="refresh" content="5; URL=/" />', unsafe_allow_html=True)  # Redireciona para a página de login em 5 segundos
        st.stop()  # Interrompe a execução do restante do código

    # Verifica se o token é válido
    decoded_token = verify_token(token)
    if not decoded_token:  # Se o token não for válido, redirecione para a página de login
        st.error("Sessão expirada ou token inválido. Faça login novamente.")
        st.markdown('<meta http-equiv="refresh" content="5; URL=/" />', unsafe_allow_html=True)  # Redireciona para a página de login em 5 segundos
        st.stop()  # Interrompe a execução do restante do código


def create_table():
    # Conecta ao banco de dados
    conn = sqlite3.connect('dados_formulario.db')
    cursor = conn.cursor()

    # Verifica se a tabela já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='formulario'")
    table_exists = cursor.fetchone()

    # Cria a tabela se não existir
    if not table_exists:
        cursor.execute('''
            CREATE TABLE formulario (
                id INTEGER PRIMARY KEY,
                Processo TEXT,
                Interessado TEXT,
                Especificações TEXT,
                Marcador TEXT,
                Resoluções TEXT,
                Data_protocolo DATE,
                Data_recebimento_solicitacao DATE,
                Doc_SEI1 TEXT,
                Remetente_unidade TEXT,
                Data_resposta DATE,
                Doc_SEI2 TEXT,
                Data_status DATE,
                Status TEXT
            )
        ''')

    # Commita as mudanças e fecha a conexão
    conn.commit()
    conn.close()

# Defina o tempo limite da sessão em segundos (por exemplo, 10 minutos)
session_timeout = 600

def login():
    # Inicialize o estado da sessão se não estiver inicializado
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.last_active_time = time.time()

    # Verificar se o estado de login está armazenado na sessão
    is_logged_in = st.session_state.is_logged_in

    # Verificar se a sessão expirou
    if not is_logged_in and time.time() - st.session_state.last_active_time > session_timeout:
        st.session_state.is_logged_in = False

    # Se já estiver logado, não precisa mostrar o formulário de login
    if is_logged_in:
        st.session_state.last_active_time = time.time()  # Atualiza o tempo de última atividade
        return True

    # Formulário de login
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if username == "gessica.rossi" and password == "05052023":  
            st.session_state.is_logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos. Por favor, tente novamente.")

    return False



def logout():
    st.session_state.is_logged_in = False
    st.session_state.last_active_time = time.time()  # Atualiza o tempo de última atividade
    st.markdown('<meta http-equiv="refresh" content="0; URL=/" />', unsafe_allow_html=True)
    return True


def main():
    if not login():
        return

    # Botão de logout
    if st.sidebar.button("Logout"):
        logout()
        return

    menu_option = st.sidebar.selectbox("Menu", ["Cadastrar Processo", "Consultar Processo","Visualizar Todos os Registros", "Baixar Dados como CSV"])

    if menu_option == "Cadastrar Processo":
        st.empty()
        st.markdown(f'<h1 style="text-align: center; width: 100%;">Cadastrar Processo SEI</h1>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 1 - Identificação.")
        # Dados do Formulário
        processo = st.text_input("Processo", value="")
        interessado = st.text_input("Interessado", value="")
        especificacoes = st.text_area("Especificações", value="")
        marcador_options = ["Opção 1", "Opção 2", "Opção 3"]  
        marcador = st.selectbox("Marcador", options=marcador_options)
        resolucoes = st.text_area("Resoluções", value="")

        st.markdown("---")
        st.markdown("### 2 - Solicitação (Quem nos demanda).")

        data_protocolo = st.date_input("Data Protocolo", value=None)
        data_recebimento_solicitacao = st.date_input("Data Recebimento / Solicitação", value=None)
        doc_sei1 = st.text_input("Doc. SEI 1", value="")
        remetente_unidade = st.text_input("Remetente / Unidade", value="")
        data_resposta = st.date_input("Data Resposta", value=None)
        doc_sei2 = st.text_input("Doc. SEI 2", value="")

        st.markdown("---")
        st.markdown("### 3 - Encerramento")

        status = st.text_input("Status", value="")
        data_status = st.date_input("Data Status", value=None)

        if st.button("Enviar"):
            # Conecta ao banco de dados
            conn = sqlite3.connect('dados_formulario.db')
            cursor = conn.cursor()

            # Insere os dados do formulário na tabela
            cursor.execute('''
                INSERT INTO formulario (
                    Processo, Interessado, Especificações,
                    Marcador, Resoluções, Data_protocolo,
                    Data_recebimento_solicitacao, Doc_SEI1,
                    Remetente_unidade, Data_resposta,
                    Doc_SEI2, Data_status, Status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                processo, interessado, especificacoes,
                marcador, resolucoes, data_protocolo,
                data_recebimento_solicitacao, doc_sei1,
                remetente_unidade, data_resposta,
                doc_sei2, data_status, status
            ))

            # Commita as mudanças no banco de dados
            conn.commit()

            # Fecha a conexão
            conn.close()

            st.success("Dados enviados com sucesso!")

            # Limpa os campos do formulário
            st.empty()

    elif menu_option == "Consultar Processo":
        st.header("Consulta de Dados por Número de Processo")

        # Número do processo para consulta
        numero_processo_consulta = st.text_input("Digite o número do processo:")

        if st.button("Consultar"):
            # Conecta ao banco de dados
            conn = sqlite3.connect('dados_formulario.db')

            # Query para selecionar os dados do processo especificado
            query = f"SELECT * FROM formulario WHERE Processo = '{numero_processo_consulta}'"

            # Executa a query e obtém os dados
            df = pd.read_sql(query, conn)

            # Fecha a conexão
            conn.close()

            # Verifica se há resultados da consulta
            if df.empty:
                st.warning("Nenhum registro encontrado para o número de processo especificado.")
            else:
                # Exibe os dados com título e descrição
                for index, row in df.iterrows():
                    st.subheader(f"Número do Processo: {row['Processo']}")
                    st.write(f"**Interessado:** {row['Interessado']}")
                    st.write(f"**Especificações:** {row['Especificações']}")
                    st.write(f"**Marcador:** {row['Marcador']}")
                    st.write(f"**Resoluções:** {row['Resoluções']}")
                    st.write(f"**Data Protocolo:** {row['Data_protocolo']}")
                    st.write(f"**Data Recebimento / Solicitação:** {row['Data_recebimento_solicitacao']}")
                    st.write(f"**Doc. SEI 1:** {row['Doc_SEI1']}")
                    st.write(f"**Remetente / Unidade:** {row['Remetente_unidade']}")
                    st.write(f"**Data Resposta:** {row['Data_resposta']}")
                    st.write(f"**Doc. SEI 2:** {row['Doc_SEI2']}")
                    st.write(f"**Status:** {row['Status']}")
                    st.write(f"**Data Status:** {row['Data_status']}")
                    st.markdown("---")

    elif menu_option == "Baixar Dados como CSV":
        st.title("Baixar Dados como CSV")

        # Conecta ao banco de dados
        conn = sqlite3.connect('dados_formulario.db')

        # Query para selecionar todos os dados da tabela
        query = "SELECT * FROM formulario"

        # Executa a query e obtém os dados
        df = pd.read_sql(query, conn)

        # Formatar as datas antes de salvar como CSV
        df['Data_protocolo'] = pd.to_datetime(df['Data_protocolo']).dt.strftime('%d/%m/%Y')
        df['Data_recebimento_solicitacao'] = pd.to_datetime(df['Data_recebimento_solicitacao']).dt.strftime('%d/%m/%Y')
        df['Data_resposta'] = pd.to_datetime(df['Data_resposta']).dt.strftime('%d/%m/%Y')
        df['Data_status'] = pd.to_datetime(df['Data_status']).dt.strftime('%d/%m/%Y')

        # Fecha a conexão
        conn.close()

        # Botão para baixar os dados como arquivo CSV
        if st.button("Baixar Dados como CSV"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="dados_formulario.csv">Baixar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

    elif menu_option == "Visualizar Todos os Registros":
        st.header("Todos os Registros do Banco de Dados")

        # Conecta ao banco de dados
        conn = sqlite3.connect('dados_formulario.db')

        # Query para selecionar todos os dados da tabela
        query = "SELECT * FROM formulario"

        # Executa a query e obtém os dados
        df = pd.read_sql(query, conn)

        # Fecha a conexão
        conn.close()

        # Verifica se há resultados da consulta
        if df.empty:
            st.warning("Nenhum registro encontrado no banco de dados.")
        else:
            # Exibe os dados em uma tabela
            st.write(df)

if __name__ == "__main__":
    create_table()
    main()
