import streamlit as st
import sqlite3
import pandas as pd
import base64

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
                Unidade TEXT,
                Interessado TEXT,
                Especificações TEXT,
                Resoluções TEXT,
                Marcador TEXT,
                Data_protocolo DATE,
                Data_recebido DATE,
                Remetente_Unidade TEXT,
                Num_Documento TEXT,
                Prazo DATE,
                Devoluitiva TEXT,
                Doc_SEI TEXT,
                Data_envio DATE,
                Unidade_devoluitiva TEXT,
                Data_De_Retorno DATE,
                Status TEXT
            )
        ''')

    # Commita as mudanças e fecha a conexão
    conn.commit()
    conn.close()

def main():

    # Menu lateral
    menu_option = st.sidebar.selectbox("Menu", ["Cadastrar Processo", "Consultar Processo","Visualizar Todos os Registros", "Baixar Dados como CSV"])
        

    if menu_option == "Cadastrar Processo":
        st.empty()
        st.markdown(f'<h1 style="text-align: center; width: 100%;">Cadastrar Processo SEI</h1>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 1 - Identificação.")
        # Dados do Formulário
        processo = st.text_input("Processo")
        unidade = st.text_input("Unidade")
        interessado = st.text_input("Interessado")
        especificacoes = st.text_area("Especificações")
        resolucoes = st.text_area("Resoluções")
        marcador = st.text_input("Marcador")

        st.markdown("---")
        st.markdown("### 2 - Solicitação (Quem nos demanda).")

        data_protocolo = st.date_input("Data Protocolo", None)
        data_recebido = st.date_input("Data Recebido", None)
        remetente_unidade = st.text_input("Remetente Unidade")
        num_documento = st.text_input("Nº Documento")
        prazo = st.date_input("Prazo", None)

        st.markdown("---")
        st.markdown("### 3 - Devolutiva - (Nossa Resposta)")

        devoluitiva = st.text_input("Devoluitiva - Nossa Resposta")
        doc_sei = st.text_input("Doc. SEI")
        data_envio = st.date_input("Data Envio", None)
        unidade_devoluitiva = st.text_input("Unidade Devoluitiva")

        st.markdown("---")
        st.markdown("### 4 - Encerramento")

        data_De_retorno = st.date_input("Data de Retorno", None)
        status = st.text_input("Status")

        if st.button("Enviar"):
            # Conecta ao banco de dados
            conn = sqlite3.connect('dados_formulario.db')
            cursor = conn.cursor()

            # Insere os dados do formulário na tabela
            cursor.execute('''
                INSERT INTO formulario (
                    Processo, Unidade, Interessado,
                    Especificações, Resoluções, Marcador,
                    Data_protocolo, Data_recebido,
                    Remetente_Unidade, Num_Documento, Prazo,
                    Devoluitiva, Doc_SEI, Data_envio, Unidade_devoluitiva,
                    Data_De_retorno, Status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                processo, unidade, interessado,
                especificacoes, resolucoes, marcador,
                data_protocolo, data_recebido,
                remetente_unidade, num_documento, prazo,
                devoluitiva, doc_sei, data_envio, unidade_devoluitiva,
                data_De_retorno, status
            ))

            # Commita as mudanças no banco de dados
            conn.commit()

            # Fecha a conexão
            conn.close()

            st.success("Dados enviados com sucesso!")

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
                    st.write(f"**Unidade:** {row['Unidade']}")
                    st.write(f"**Interessado:** {row['Interessado']}")
                    st.write(f"**Especificações:** {row['Especificações']}")
                    st.write(f"**Resoluções:** {row['Resoluções']}")
                    st.write(f"**Marcador:** {row['Marcador']}")
                    st.write(f"**Data Protocolo:** {row['Data_protocolo']}")
                    st.write(f"**Data Recebido:** {row['Data_recebido']}")
                    st.write(f"**Remetente Unidade:** {row['Remetente_Unidade']}")
                    st.write(f"**Nº Documento:** {row['Num_Documento']}")
                    st.write(f"**Prazo:** {row['Prazo']}")
                    st.write(f"**Devoluitiva:** {row['Devoluitiva']}")
                    st.write(f"**Doc. SEI:** {row['Doc_SEI']}")
                    st.write(f"**Data Envio:** {row['Data_envio']}")
                    st.write(f"**Unidade Devoluitiva:** {row['Unidade_devoluitiva']}")
                    st.write(f"**Data De Retorno:** {row['Data_De_Retorno']}")
                    st.write(f"**Status:** {row['Status']}")
                    # if st.button("Excluir este registro", key=f"delete_{row['id']}", help="Clique para excluir este registro"): 
                    #     conn = sqlite3.connect('dados_formulario.db')
                    #     cursor = conn.cursor()
                    #     cursor.execute(f"DELETE FROM formulario WHERE id={row['id']}")
                    #     conn.commit()
                    #     conn.close()
                    #     st.success("Registro excluído com sucesso!")
                        
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
        df['Data_recebido'] = pd.to_datetime(df['Data_recebido']).dt.strftime('%d/%m/%Y')
        df['Data_envio'] = pd.to_datetime(df['Data_envio']).dt.strftime('%d/%m/%Y')
        df['Data_De_Retorno'] = pd.to_datetime(df['Data_De_Retorno']).dt.strftime('%d/%m/%Y')
        df['Prazo'] = pd.to_datetime(df['Prazo']).dt.strftime('%d/%m/%Y')

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

