import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import plotly.express as px

#----------------------------------------------------------------------#
#  FUNÇÕES PARA A FERRAMENTA 1: ANÁLISE DE CSVS ACADÉMICOS             #
#----------------------------------------------------------------------#

def processa_oferta(df, nome_arquivo):
    """
    Processa o DataFrame de oferta de turmas, exibe uma tabela e um gráfico opcional.

    Args:
        df (pd.DataFrame): O DataFrame carregado do arquivo CSV de oferta.
        nome_arquivo (str): O nome do arquivo original para exibição.
    """
    st.header(f"Tabela 1: Análise de Oferta de Turmas")
    st.subheader(f"(Arquivo: {nome_arquivo})")

    # Define as colunas esperadas no arquivo de oferta.
    colunas_oferta = ["Unidade Academica", "Ano", "Periodo", "Codigo Componente", "Componente Curricular", "Ch Teorica", "Ch Pratica", "Ch Total", "Codigo Turma", "Vagas Ofertadas", "Vagas Nucleo Livre", "Total Matriculados", "Curso Responsavel Oferta", "Docentes", "Qtd Docentes", "Puramente Nucleo Livre", "Situacao Turma", "Data Inicio Aulas", "Data Fim Aulas", "Data Cadastro"]
    
    # Verifica se todas as colunas necessárias estão presentes.
    colunas_faltantes = [col for col in colunas_oferta if col not in df.columns]
    if not colunas_faltantes:
        df_extraido = df[colunas_oferta]
        
        # Widgets da barra lateral para personalização da tabela.
        with st.sidebar.expander("⚙️ Personalizar Tabela de Oferta", expanded=True):
            colunas_selecionadas = [col for col in colunas_oferta if st.checkbox(col, value=True, key=f"oferta_{col}")]
        
        if not colunas_selecionadas:
            st.warning("Selecione pelo menos uma coluna para exibir a tabela.")
            return

        # Exibe o DataFrame com as colunas selecionadas e ordenadas.
        df_agrupado = df_extraido[colunas_selecionadas].sort_values(by=colunas_selecionadas[0])
        st.dataframe(df_agrupado)

        # Nova aba de filtros para os gráficos na barra lateral
        with st.sidebar.expander("📊 Filtros dos Gráficos de Oferta"):
            # Filtros para Gráfico de Barras
            st.subheader("Gráfico de Barras")
            eixo_x_bar = st.selectbox("Selecione a coluna para o eixo X (Barra):", colunas_selecionadas, key='oferta_x_bar')
            eixo_y_bar = st.selectbox("Selecione a coluna para o eixo Y (Barra):", colunas_selecionadas, key='oferta_y_bar')

            # Filtros para Gráfico de Linhas
            st.subheader("Gráfico de Linhas")
            eixo_x_line = st.selectbox("Selecione a coluna para o eixo X (Linha):", colunas_selecionadas, key='oferta_x_line')
            eixo_y_line = st.selectbox("Selecione a coluna para o eixo Y (Linha):", colunas_selecionadas, key='oferta_y_line')

            # Filtros para Gráfico de Pizza
            st.subheader("Gráfico de Pizza")
            eixo_pizza = st.selectbox("Selecione a coluna para o gráfico de Pizza:", colunas_selecionadas, key='oferta_pizza')

        # Exibição dos gráficos
        st.header("Gráficos de Oferta")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Barras
            if eixo_x_bar and eixo_y_bar:
                st.subheader(f"Gráfico de Barras: {eixo_y_bar} por {eixo_x_bar}")
                try:
                    if pd.api.types.is_numeric_dtype(df_agrupado[eixo_y_bar]):
                        chart_data = df_agrupado.groupby(eixo_x_bar)[eixo_y_bar].sum().reset_index()
                    else:
                        chart_data = df_agrupado.groupby(eixo_x_bar)[eixo_y_bar].count().reset_index()
                    fig = px.bar(chart_data, x=eixo_x_bar, y=eixo_y_bar)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Não foi possível gerar o gráfico de barras: {e}")

        with col2:
            # Gráfico de Linhas
            if eixo_x_line and eixo_y_line:
                st.subheader(f"Gráfico de Linhas: {eixo_y_line} por {eixo_x_line}")
                try:
                    if pd.api.types.is_numeric_dtype(df_agrupado[eixo_y_line]):
                        chart_data = df_agrupado.groupby(eixo_x_line)[eixo_y_line].sum().reset_index()
                    else:
                        chart_data = df_agrupado.groupby(eixo_x_line)[eixo_y_line].count().reset_index()
                    fig = px.line(chart_data, x=eixo_x_line, y=eixo_y_line)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Não foi possível gerar o gráfico de linhas: {e}")

        # Gráfico de Pizza
        if eixo_pizza:
            st.subheader(f"Gráfico de Pizza: {eixo_pizza}")
            try:
                chart_data = df_agrupado[eixo_pizza].value_counts().reset_index()
                chart_data.columns = [eixo_pizza, 'Contagem']
                fig = px.pie(chart_data, names=eixo_pizza, values='Contagem')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Não foi possível gerar o gráfico de pizza: {e}")

    else:
        st.error(f"Erro no Arquivo 1 '{nome_arquivo}': Faltam as colunas: {', '.join(colunas_faltantes)}.")

def processa_matricula(df, nome_arquivo):
    """
    Processa o DataFrame de matrícula de alunos, exibe uma tabela e um gráfico opcional.

    Args:
        df (pd.DataFrame): O DataFrame carregado do arquivo CSV de matrícula.
        nome_arquivo (str): O nome do arquivo original para exibição.
    """
    st.header(f"Tabela 2: Análise de Matrículas de Alunos")
    st.subheader(f"(Arquivo: {nome_arquivo})")

    # Define as colunas esperadas no arquivo de matrícula.
    colunas_matricula = ["Matricula", "Curso", "Grau Academico", "Unidade Oferta Disciplina", "Unidade Aluno", "Ano Ingresso", "Semestre Ingresso", "Codigo", "Disciplina", "Ano Disciplina", "Periodo", "Nucleo", "Notas", "Situacao", "Mge", "ID"]
    
    # Verifica se todas as colunas necessárias estão presentes.
    colunas_faltantes = [col for col in colunas_matricula if col not in df.columns]
    if not colunas_faltantes:
        df_extraido = df[colunas_matricula]

        # Widgets da barra lateral para personalização da tabela.
        with st.sidebar.expander("⚙️ Personalizar Tabela de Matrícula", expanded=True):
            colunas_selecionadas = [col for col in colunas_matricula if st.checkbox(col, value=True, key=f"matricula_{col}")]
            remover_duplicadas = st.checkbox("Remover matrículas duplicadas", key='remove_duplicates_matricula')

        # Garante que pelo menos uma coluna foi selecionada.
        if not colunas_selecionadas:
            st.warning("Selecione pelo menos uma coluna para exibir a tabela.")
            return

        df_agrupado = df_extraido[colunas_selecionadas].sort_values(by=colunas_selecionadas[0])
        
        if remover_duplicadas:
            if 'Matricula' in df_agrupado.columns:
                registros_antes = len(df_agrupado)
                df_agrupado.drop_duplicates(subset=['Matricula'], keep='first', inplace=True)
                registros_depois = len(df_agrupado)
                st.info(f"{registros_antes - registros_depois} matrículas duplicadas foram removidas. {registros_depois} registros únicos restantes.")
            else:
                st.warning("A coluna 'Matricula' deve ser selecionada para remover duplicatas.")
        
        st.dataframe(df_agrupado)

        # Nova aba de filtros para os gráficos na barra lateral
        with st.sidebar.expander("📊 Filtros dos Gráficos de Matrícula"):
            # Filtros para Gráfico de Barras
            st.subheader("Gráfico de Barras")
            eixo_x_bar_mat = st.selectbox("Selecione a coluna para o eixo X (Barra):", colunas_selecionadas, key='matricula_x_bar')
            eixo_y_bar_mat = st.selectbox("Selecione a coluna para o eixo Y (Barra):", colunas_selecionadas, key='matricula_y_bar')

            # Filtros para Gráfico de Linhas
            st.subheader("Gráfico de Linhas")
            eixo_x_line_mat = st.selectbox("Selecione a coluna para o eixo X (Linha):", colunas_selecionadas, key='matricula_x_line')
            eixo_y_line_mat = st.selectbox("Selecione a coluna para o eixo Y (Linha):", colunas_selecionadas, key='matricula_y_line')

            # Filtros para Gráfico de Pizza
            st.subheader("Gráfico de Pizza")
            eixo_pizza_mat = st.selectbox("Selecione a coluna para o gráfico de Pizza:", colunas_selecionadas, key='matricula_pizza')

        # Exibição dos gráficos
        st.header("Gráficos de Matrícula")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Barras
            if eixo_x_bar_mat and eixo_y_bar_mat:
                st.subheader(f"Gráfico de Barras: {eixo_y_bar_mat} por {eixo_x_bar_mat}")
                try:
                    if eixo_y_bar_mat == 'Matricula':
                        chart_data = df_agrupado.groupby(eixo_x_bar_mat)[eixo_y_bar_mat].nunique().reset_index()
                    elif pd.api.types.is_numeric_dtype(df_agrupado[eixo_y_bar_mat]):
                        chart_data = df_agrupado.groupby(eixo_x_bar_mat)[eixo_y_bar_mat].sum().reset_index()
                    else:
                        chart_data = df_agrupado.groupby(eixo_x_bar_mat)[eixo_y_bar_mat].count().reset_index()
                    fig = px.bar(chart_data, x=eixo_x_bar_mat, y=eixo_y_bar_mat)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Não foi possível gerar o gráfico de barras: {e}")

        with col2:
            # Gráfico de Linhas
            if eixo_x_line_mat and eixo_y_line_mat:
                st.subheader(f"Gráfico de Linhas: {eixo_y_line_mat} por {eixo_x_line_mat}")
                try:
                    if eixo_y_line_mat == 'Matricula':
                        chart_data = df_agrupado.groupby(eixo_x_line_mat)[eixo_y_line_mat].nunique().reset_index()
                    elif pd.api.types.is_numeric_dtype(df_agrupado[eixo_y_line_mat]):
                        chart_data = df_agrupado.groupby(eixo_x_line_mat)[eixo_y_line_mat].sum().reset_index()
                    else:
                        chart_data = df_agrupado.groupby(eixo_x_line_mat)[eixo_y_line_mat].count().reset_index()
                    fig = px.line(chart_data, x=eixo_x_line_mat, y=eixo_y_line_mat)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Não foi possível gerar o gráfico de linhas: {e}")

        # Gráfico de Pizza
        if eixo_pizza_mat:
            st.subheader(f"Gráfico de Pizza: Contagem de Alunos por {eixo_pizza_mat}")
            try:
                if 'Matricula' in df_agrupado.columns:
                    if eixo_pizza_mat == 'Matricula':
                        st.warning("Gráfico de pizza de matrículas individuais não é informativo. Selecione outra coluna para agrupar.")
                    else:
                        chart_data = df_agrupado.groupby(eixo_pizza_mat)['Matricula'].nunique().reset_index()
                        fig = px.pie(chart_data, names=eixo_pizza_mat, values='Matricula')
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Para contar alunos únicos, por favor inclua a coluna 'Matricula' na sua seleção de colunas da tabela.")
                    # Fallback para contagem de ocorrências se 'Matricula' não estiver disponível
                    chart_data = df_agrupado[eixo_pizza_mat].value_counts().reset_index()
                    chart_data.columns = [eixo_pizza_mat, 'Contagem']
                    fig = px.pie(chart_data, names=eixo_pizza_mat, values='Contagem')
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Não foi possível gerar o gráfico de pizza: {e}")
    else:
        st.error(f"Erro no Arquivo 2 '{nome_arquivo}': Faltam as colunas: {', '.join(colunas_faltantes)}.")

#----------------------------------------------------------------------#
#  FUNÇÕES PARA A FERRAMENTA 2: ANÁLISE DE EXCEL                       #
#----------------------------------------------------------------------#

def find_latest_year(df):
    years = set()
    for col in df.columns:
        match = re.match(r'(\d{4})/\d', str(col[1]))
        if match:
            years.add(int(match.group(1)))
    return max(years) if years else None

def process_dataframe(df):
    title = "Análise de Matrículas (TAM)"
    latest_year = find_latest_year(df)
    if not latest_year:
        st.error(f"Não foi possível encontrar colunas com o formato 'ano/semestre' (ex: 2025/1) na aba 'TAM'.")
        return None, None, None

    academic_unit_col = df.columns[0]
    col_g_sem1 = ('NamatG', f'{latest_year}/1')
    col_md_sem1 = ('NamatM+NamatD', f'{latest_year}/1')
    col_g_sem2 = ('NamatG', f'{latest_year}/2')
    col_md_sem2 = ('NamatM+NamatD', f'{latest_year}/2')

    required_cols = [col_g_sem1, col_md_sem1]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Erro: Nem todas as colunas necessárias (NamatG, NamatM+NamatD) foram encontradas para o primeiro semestre. Verifique o arquivo.")
        return None, None, None

    data_slice = df.head(8)
    result_df = pd.DataFrame({'Unidade Acadêmica': data_slice[academic_unit_col]})
    
    namatg_sem1 = data_slice[col_g_sem1].fillna(0)
    namatmd_sem1 = data_slice[col_md_sem1].fillna(0)
    result_df[f'NamatG {latest_year}/1'] = namatg_sem1
    result_df[f'NamatM+NamatD {latest_year}/1'] = namatmd_sem1
    result_df[f'NamatU {latest_year}/1'] = namatg_sem1.astype(int) + namatmd_sem1.astype(int)

    if col_g_sem2 in df.columns and col_md_sem2 in df.columns and data_slice[col_g_sem2].count() > 0:
        namatg_sem2 = data_slice[col_g_sem2].fillna(0)
        namatmd_sem2 = data_slice[col_md_sem2].fillna(0)
        result_df[f'NamatG {latest_year}/2'] = namatg_sem2
        result_df[f'NamatM+NamatD {latest_year}/2'] = namatmd_sem2
        result_df[f'NamatU {latest_year}/2'] = namatg_sem2.astype(int) + namatmd_sem2.astype(int)
    
    summary_df = result_df[['Unidade Acadêmica', f'NamatU {latest_year}/1']]
    if f'NamatU {latest_year}/2' in result_df.columns:
        summary_df[f'NamatU {latest_year}/2'] = result_df[f'NamatU {latest_year}/2']

    return summary_df, result_df.set_index('Unidade Acadêmica'), title

def find_column(df, keyword):
    for col in df.columns:
        if keyword in str(col[0]) or keyword in str(col[1]):
            return col
    return None

def process_taa_sheet(df):
    title = "Análise da Taxa de Aprovação (TAA)"
    unit_col = df.columns[0]
    total_col = find_column(df, 'Total')
    de_outras_col = find_column(df, 'De outras UAs')

    if not all([total_col, de_outras_col]):
        st.error(f"Erro: Não foi possível encontrar colunas contendo as palavras-chave: Total, De outras UAs. Verifique o arquivo.")
        return None, None, None

    data_slice = df.head(8)
    result_df = pd.DataFrame({
        'Unidade Acadêmica': data_slice[unit_col],
        'Total': data_slice[total_col],
        'De outras UAs': data_slice[de_outras_col]
    })
    result_df.dropna(subset=['Unidade Acadêmica'], inplace=True)
    summary_df = result_df[['Unidade Acadêmica', 'Total']].rename(columns={'Total': 'Total (TAA)'})
    return summary_df, result_df.set_index('Unidade Acadêmica'), title

def process_chmt_sheet(df):
    title = "Análise de Carga Horária Média Total (CHMT)"
    unit_col = df.columns[0]
    workload_keyword = 'Carga horária docente efetivamente ministrada'
    workload_col = find_column(df, workload_keyword)

    if not workload_col:
        st.error(f"Erro: Não foi possível encontrar uma coluna contendo '{workload_keyword}'. Verifique o arquivo.")
        return None, None, None

    data_slice = df.head(8)
    result_df = pd.DataFrame({
        'Unidade Acadêmica': data_slice[unit_col],
        'Carga Horária Ministrada': data_slice[workload_col]
    })
    result_df.dropna(subset=['Unidade Acadêmica'], inplace=True)
    summary_df = result_df.rename(columns={'Carga Horária Ministrada': 'Carga horária docente efetivamente ministrada (CHMT)'})
    return summary_df, result_df.set_index('Unidade Acadêmica'), title

def process_pep_sheet(df):
    title = "Análise de Pesquisa e Extensão (PEP)"
    unit_col = df.columns[0]
    pesquisa_col = find_column(df, 'Pesquisa')
    extensao_col = find_column(df, 'Extensão')

    if not all([pesquisa_col, extensao_col]):
        st.error(f"Erro: Não foi possível encontrar colunas contendo as palavras-chave: Pesquisa, Extensão. Verifique o arquivo.")
        return None, None, None

    data_slice = df.head(8)
    sum_series = data_slice[pesquisa_col].fillna(0) + data_slice[extensao_col].fillna(0)
    result_df = pd.DataFrame({
        'Unidade Acadêmica': data_slice[unit_col],
        'Pesquisa': data_slice[pesquisa_col],
        'Extensão': data_slice[extensao_col],
        'Total': sum_series
    })
    result_df.dropna(subset=['Unidade Acadêmica'], inplace=True)
    summary_df = result_df[['Unidade Acadêmica', 'Total']].rename(columns={'Total': 'Total (PEP)'})
    return summary_df, result_df.set_index('Unidade Acadêmica'), title

def process_lic_sheet(df):
    title = "Análise de Cursos de Licenciatura (LIC)"
    if 'Licenciaturas' not in df.columns:
        st.error("A coluna 'Licenciaturas' não foi encontrada na aba 'LIC'. Por favor, verifique o arquivo.")
        return None, None, None
    elif len(df.columns) == 0:
        st.error("A planilha parece estar vazia.")
        return None, None, None
    else:
        unidade_col = df.columns[0]

        def contar_cursos(cursos):
            if isinstance(cursos, str) and cursos.strip() not in ['--', '-']:
                lista_cursos = [curso.strip() for curso in cursos.split(',') if curso.strip()]
                return len(lista_cursos)
            return 0

        df['Contagem'] = df['Licenciaturas'].apply(contar_cursos)

        def agg_licenciaturas(series):
            all_courses = []
            for item in series:
                if isinstance(item, str) and item.strip() not in ['--', '-']:
                    courses_in_item = [curso.strip() for curso in item.split(',') if curso.strip()]
                    all_courses.extend(courses_in_item)
            unique_courses = list(dict.fromkeys(all_courses))
            return ', '.join(unique_courses)

        resultado = df.groupby(unidade_col).agg(
            Licenciaturas_agrupadas=('Licenciaturas', agg_licenciaturas),
            Contagem_total=('Contagem', 'sum')
        ).reset_index()
        
        resultado = resultado.rename(columns={
            unidade_col: 'Unidade Acadêmica',
            'Licenciaturas_agrupadas': 'Licenciaturas',
            'Contagem_total': 'LIC'
        })
        
        resultado_display = resultado[['Unidade Acadêmica', 'Licenciaturas', 'LIC']]
        summary_df = resultado[['Unidade Acadêmica', 'LIC']]
        return summary_df, resultado_display.set_index('Unidade Acadêmica'), title

def process_cc_sheet(df):
    title = "Análise de CC Médio (CC)"
    unidade_col_name = df.columns[0]
    cc_medio_col_name = 'CC médio'

    if cc_medio_col_name not in df.columns:
        st.error(f"A coluna '{cc_medio_col_name}' não foi encontrada na aba 'CC'. Por favor, verifique o arquivo.")
        return None, None, None
    elif len(df.columns) == 0:
        st.error("A planilha parece estar vazia.")
        return None, None, None
    else:
        resultado = df[[unidade_col_name, cc_medio_col_name]]
        resultado = resultado.dropna(subset=[unidade_col_name])
        resultado = resultado[~resultado[unidade_col_name].astype(str).str.startswith('Fonte:')]
        resultado = resultado.rename(columns={unidade_col_name: 'Unidade Acadêmica'})
        summary_df = resultado.rename(columns={'CC médio': 'CC médio (CC)'})
        return summary_df, resultado.set_index('Unidade Acadêmica'), title

def process_lab_sheet(df):
    title = "Análise de Laboratórios (LAB)"
    unidade_col_name = df.columns[0]
    lab_col_name = 'Laboratórios'

    if lab_col_name not in df.columns:
        st.error(f"A coluna '{lab_col_name}' não foi encontrada na aba 'LAB'. Por favor, verifique o arquivo.")
        return None, None, None
    elif len(df.columns) == 0:
        st.error("A planilha parece estar vazia.")
        return None, None, None
    else:
        resultado = df[[unidade_col_name, lab_col_name]]
        resultado = resultado.dropna(subset=[unidade_col_name])
        resultado = resultado[~resultado[unidade_col_name].astype(str).str.startswith('Fonte:')]
        resultado = resultado.rename(columns={unidade_col_name: 'Unidade Acadêmica'})
        summary_df = resultado.rename(columns={'Laboratórios': 'Laboratórios (LAB)'})
        return summary_df, resultado.set_index('Unidade Acadêmica'), title

def process_tdu_sheet(df):
    title = "Total de Docentes da Unidade (TDU)"
    FATOR_20H = 0.60
    FATOR_40H = 1.00
    FATOR_DE = 1.65

    try:
        df = df.dropna(how='all', axis=1)
        num_cols = len(df.columns)
        col_names = ['Unidade', '20H', '40H', 'DE', '#Docentes']
        df.columns = col_names[:num_cols]

        colunas_numericas = ['20H', '40H', 'DE']
        for col in colunas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        df = df.dropna(subset=colunas_numericas)
        
        for col in colunas_numericas:
            df[col] = df[col].astype(int)
        
        df['TDU Calculado'] = (df['20H'] * FATOR_20H) + \
                              (df['40H'] * FATOR_40H) + \
                              (df['DE'] * FATOR_DE)
        
        summary_df = df[['Unidade', '#Docentes']].rename(columns={'Unidade': 'Unidade Acadêmica', '#Docentes': '#Discentes (TDU)'})
        
        display_df = df.set_index('Unidade')
        
        return summary_df, display_df, title

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a aba 'TDU': {e}")
        return None, None, None

#----------------------------------------------------------------------#
#  FUNÇÃO PRINCIPAL DA APLICAÇÃO (com integrações)                     #
#----------------------------------------------------------------------#
def main():
    """
    Função principal que executa a aplicação Streamlit, controla a navegação
    e o fluxo de dados entre as ferramentas.
    """
    st.title("Painel de Análise de Dados")
    st.sidebar.title("Menu de Ferramentas")
    
    opcoes = {
        'Analisador de CSVs Acadêmicos': '📊 Analisador de CSVs Acadêmicos',
        'Analisador de Excel Acadêmico': '📄 Analisador de Excel Acadêmico'
    }
    escolha_formatada = st.sidebar.selectbox(
        "Selecione a ferramenta:",
        list(opcoes.values())
    )
    ferramenta_escolhida = [k for k, v in opcoes.items() if v == escolha_formatada][0]

    if ferramenta_escolhida == 'Analisador de CSVs Acadêmicos':
        # Lógica para a Ferramenta 1: Analisador de CSVs
        st.header("Analisador de CSVs Acadêmicos")
        st.markdown("Carregue os arquivos CSV para gerar as tabelas de Oferta e Matrícula.")
        with st.sidebar.expander("📂 Carregar Arquivos CSV", expanded=True):
            arquivo_1 = st.file_uploader("1º Arquivo (Oferta de Turmas)", type=["csv"], key="csv1")
            arquivo_2 = st.file_uploader("2º Arquivo (Matrícula de Alunos)", type=["csv"], key="csv2")
        try:
            if arquivo_1:
                df_oferta = pd.read_csv(arquivo_1)
                processa_oferta(df_oferta, arquivo_1.name)
            st.markdown("---")
            if arquivo_2:
                df_matricula = pd.read_csv(arquivo_2)
                processa_matricula(df_matricula, arquivo_2.name)
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os arquivos CSV: {e}")

    elif ferramenta_escolhida == 'Analisador de Excel Acadêmico':
        st.header("Analisador de Excel Acadêmico")
        st.markdown("Carregue o arquivo Excel para gerar a tabela consolidada.")
        with st.sidebar.expander("📂 Carregar Arquivo Excel", expanded=True):
            arquivo_excel = st.file_uploader("Selecione o arquivo (.xlsx)", type="xlsx", key="excel1")

        if arquivo_excel:
            try:
                xls = pd.ExcelFile(arquivo_excel)
                sheet_names = xls.sheet_names
                
                summary_dfs = []
                detailed_data = []

                sheet_processors = {
                    'TAM': (lambda: pd.read_excel(arquivo_excel, sheet_name='TAM', header=[0, 1], engine='openpyxl'), process_dataframe),
                    'TDU': (lambda: pd.read_excel(arquivo_excel, sheet_name='TDU', engine='openpyxl', skiprows=3, header=None), process_tdu_sheet),
                    'TAA': (lambda: pd.read_excel(arquivo_excel, sheet_name='TAA', header=[0, 1], engine='openpyxl'), process_taa_sheet),
                    'CHMT': (lambda: pd.read_excel(arquivo_excel, sheet_name='CHMT', header=[0, 1], engine='openpyxl'), process_chmt_sheet),
                    'PEP': (lambda: pd.read_excel(arquivo_excel, sheet_name='PEP', header=[0, 1], engine='openpyxl'), process_pep_sheet),
                    'LIC': (lambda: pd.read_excel(arquivo_excel, sheet_name='LIC', engine='openpyxl'), process_lic_sheet),
                    'CC': (lambda: pd.read_excel(arquivo_excel, sheet_name='CC', engine='openpyxl'), process_cc_sheet),
                    'LAB': (lambda: pd.read_excel(arquivo_excel, sheet_name='LAB', engine='openpyxl'), process_lab_sheet)
                }

                for sheet_name, (reader, processor) in sheet_processors.items():
                    if sheet_name in sheet_names:
                        df = reader()
                        summary_df, detailed_df, title = processor(df)
                        if summary_df is not None:
                            summary_dfs.append(summary_df)
                            if detailed_df is not None:
                                detailed_data.append((title, detailed_df))

                if summary_dfs:
                    final_df = summary_dfs[0]
                    for df in summary_dfs[1:]:
                        final_df = pd.merge(final_df, df, on='Unidade Acadêmica', how='outer')
                    
                    cols = final_df.columns.tolist()
                    if '#Discentes (TDU)' in cols and 'Total (TAA)' in cols:
                        cols.insert(cols.index('#Discentes (TDU)'), cols.pop(cols.index('Total (TAA)')))
                        final_df = final_df[cols]
                        total_taa = pd.to_numeric(final_df['Total (TAA)'], errors='coerce').fillna(0)
                        discentes_tdu = pd.to_numeric(final_df['#Discentes (TDU)'], errors='coerce').fillna(0)
                        final_df['RAPT'] = (total_taa / discentes_tdu).replace([np.inf, -np.inf], 0).fillna(0)

                    st.subheader("Tabela Resumo")
                    st.dataframe(final_df.set_index('Unidade Acadêmica'))

                    with st.expander("Mostrar tabelas detalhadas"):
                        for title, df_to_display in detailed_data:
                            st.subheader(title)
                            st.dataframe(df_to_display)

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        else:
            st.info("Por favor, anexe um arquivo .xlsx para iniciar a análise.")

if __name__ == "__main__":
    main()
