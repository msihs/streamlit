import streamlit as st
import pandas as pd
import numpy as np
import zipfile as zf
import os

#@st.cache
def load_df(DCA_file, DE_file):
    #if DCA_file:
    file_suffix = os.path.splitext(DCA_file.name)[1]
    if file_suffix == '.zip':
        zipFile = zf.ZipFile(DCA_file) # DCA_EUR_all.csv/DCA_fore_all.csv
        dfNew = pd.read_csv(zipFile.open('DCA_EUR_all.csv'))
        dfNew['apiNum'] = dfNew['prod_id'].str.lstrip('api').astype(int)
        #st.write(dfNew.head())
        dfHdr = pd.read_csv(zipFile.open('DCA_EF_hdr.csv'))
    #else if file_suffix == 'csv':
    #    dfNew = pd.read_csv() #TODO

    #if DE_file:
    file_suffix = os.path.splitext(DE_file.name)[1]
    if file_suffix == '.csv':
        dfOld = pd.read_csv(DE_file)

    # st.write(dfNew)
    # st.write(dfOld)
    # st.write(dfHdr)
    # return null
    df = pd.merge(dfNew, dfOld, how='left', on='apiNum', suffixes=('', '_old'))
    return pd.merge(df, dfHdr, how='left', on='prod_id', suffixes=('', '_hdr'))

with st.sidebar.beta_expander('Upload DCA file'):
    DCA_file = st.file_uploader("DCA All, i.e. NEW data file (.zip):")
if DCA_file: st.sidebar.write(f"DCA file: {DCA_file.name}")

with st.sidebar.beta_expander('Upload DE file'):
    DE_file = st.file_uploader("DE, i.e. Old data file (.csv):")

if DE_file: st.sidebar.write(f"DE file: {DE_file.name}")

col1, col2 = st.beta_columns((1,1))
import plotly_express as px

if DCA_file and DE_file:

    df_all = load_df(DCA_file, DE_file)
    play_label_options = st.sidebar.multiselect('Which play_label?', list(df_all['play_label'].unique()), default=['Eagleford Shale'])
    play_type_options = st.sidebar.multiselect('Which play_type?', list(df_all['play_type'].unique()), default=['Shale'])
    drill_type_options = st.sidebar.multiselect('Which drill_type?', list(df_all['drill_type'].unique()), default=['V', 'H', 'D'])
    is_active_options = st.sidebar.multiselect('Which is_active?', list(df_all['is_active'].unique()), default=[1, 0])
    prod_type_options = st.sidebar.multiselect('Which prod_type?', list(df_all['prod_type'].unique()), default=['OIL', 'GAS'])
    well_type_options = st.sidebar.multiselect('Which well_type?', list(df_all['well_type'].unique()), default=['Conventional','Unconventional'])

    df_filtered = df_all[
        (df_all['play_label'].isin(play_label_options)) &
        (df_all['play_type'].isin(play_type_options)) &
        (df_all['drill_type'].isin(drill_type_options)) &
        (df_all['is_active'].isin(is_active_options)) &
        (df_all['prod_type'].isin(prod_type_options)) &
        (df_all['well_type'].isin(well_type_options))
    ]
    
    with col1: st.plotly_chart(px.scatter(
        df_filtered, x='eur_hist_liquids', y='eur_liquids_raw'),  
        use_container_width=True
    )
    with col2: st.plotly_chart(px.scatter(
        df_filtered, x='eur_partition_date_beg_liquids', y='eur_partition_date_beg_liquids_raw'),
        use_container_width=True
    )

    if st.checkbox('Show dataframe'):
        st.write(df_filtered)

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
)

_max_width_()