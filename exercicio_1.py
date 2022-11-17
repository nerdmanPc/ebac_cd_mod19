import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

custom_params = {'axes.spines.right': False, 'axes.spines.top': False}
sns.set_theme(style='ticks', rc=custom_params)

def multiselect_filter(dados, coluna, selecionados):
    if 'all' in selecionados:
        return dados
    else:
        return dados[dados[coluna].isin(selecionados)]

def main():

    st.set_page_config(
        page_title='Telemarketing analisys',
        page_icon='./img/telmarketing_icon.png',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.write('# Telemarketing analisys')
    st.markdown('---')

    image = Image.open('./img/Bank-Branding.jpg')
    st.sidebar.image(image)

    bank_raw = pd.read_csv('./data/input/bank-additional-full.csv', sep=';')
    bank = bank_raw.copy()

    with st.sidebar.form(key='filter'):

        #IDADES
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        ages = st.slider(
            label='Idade',
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            step=1
        )

        #PROFISSÕES
        jobs_list = bank_raw['job'].unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.multiselect('Profissões', jobs_list, ['all'])

        #ESTADO CIVIL
        marital_list = bank_raw['marital'].unique().tolist()
        marital_list.append('all')
        marital_selected = st.multiselect('Estado civil', marital_list, ['all'])

        #DEFAULT?
        default_list = bank_raw['default'].unique().tolist()
        default_list.append('all')
        default_selected = st.multiselect('Default?', default_list, ['all'])

        #TEM FINANCIAMENTO IMOBILIÁRIO?
        housing_list = bank_raw['housing'].unique().tolist()
        housing_list.append('all')
        housing_selected = st.multiselect('Tem financ. imob.?', housing_list, ['all'])

        #TEM EMPRÉSTIMO?
        loan_list = bank_raw['loan'].unique().tolist()
        loan_list.append('all')
        loan_selected = st.multiselect('Tem empréstimo?', loan_list, ['all'])

        #MEIO DE CONTATO
        contact_list = bank_raw['contact'].unique().tolist()
        contact_list.append('all')
        contact_selected = st.multiselect('Meio de contato', contact_list, ['all'])

        #MÊS DE CONTATO
        month_list = bank_raw['month'].unique().tolist()
        month_list.append('all')
        month_selected = st.multiselect('Mês de contato', month_list, ['all'])

        #DIA DA SEMANA
        day_of_week_list = bank_raw['day_of_week'].unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected = st.multiselect('Dia da semana', day_of_week_list, ['all'])

        #FILTROS
        bank = (
            bank.query('age >= @ages[0] and age <= @ages[1]')
            .pipe(multiselect_filter, 'job', jobs_selected)
            .pipe(multiselect_filter, 'marital', marital_selected)
            .pipe(multiselect_filter, 'default', default_selected)
            .pipe(multiselect_filter, 'housing', housing_selected)
            .pipe(multiselect_filter, 'loan', loan_selected)
            .pipe(multiselect_filter, 'contact', contact_selected)
            .pipe(multiselect_filter, 'month', month_selected)
            .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
        )
        #bank = bank[(bank['age'] >= ages[0]) & (bank['age'] <= ages[1])]
        #bank = multiselect_filter(bank, 'job', jobs_selected)
        bank.reset_index(inplace=True, drop=True)

        submit_button = st.form_submit_button(label='Aplicar')

    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown('---')

    st.write('## Proporção de aceitação')

    #PLOTS

    fig, ax = plt.subplots(1, 2, figsize=(5, 3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize=True)*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
    sns.barplot(
        x=bank_raw_target_perc.index,
        y=bank_raw_target_perc,
        ax=ax[0]
    )
    ax[0].bar_label(ax[0].containers[0])
    ax[0].set_title('Dados brutos', fontweight='bold')


    bank_target_perc = bank.y.value_counts(normalize=True)*100
    bank_target_perc = bank_target_perc.sort_index()
    sns.barplot(
        x=bank_target_perc.index,
        y=bank_target_perc,
        ax=ax[1]
    )
    ax[1].bar_label(ax[1].containers[0])
    ax[1].set_title('Dados filtrados', fontweight='bold')

    st.pyplot(plt)

    #st.write(bank)

main()