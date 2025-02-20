import streamlit as st
import pandas as pd
import os
from  io import BytesIO

st.set_page_config(page_title='Data Sweeper', layout='wide')

# Custom CSS
st.markdown(
    '''
    <style>
    .stApp{
       background-color: #A0D8F1;
       color:white
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Title and description
st.title('💿 Data Sweeper By Qirat Saeed')
st.write('Transform your files between CSV and Excel formates with built-in data cleaning and visualization ')

# file uploader
file_uploader = st.file_uploader('Upload your files (accepts CSV or Excel):' ,type=['cvs','xlsx'], accept_multiple_files=(True))

if file_uploader:
    for file in file_uploader:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df =  pd.read_csv(file)
        elif file_ext == ".xlsx":
            df =pd.read_excel(file)
        else :
            st.error(f'Unsupported file type {file_ext}')
            continue
        # file details:
        st.write('🔍 Preview the head of the Data frame')
        st.dataframe(df.head())

        # data cleaning options
        st.subheader('🎯 Data Cleaning Options')
        if st.checkbox(f'Clean data for {file.name}'):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f'Remove duplicates from the file: {file.name}'):
                    df.drop_duplicates(inplace=True)
            with col2:
                if st.button(f'Fill missing values for {file.name}'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('✔ Missing Values have been filled!')
        st.header('🎯 Select the column to keep')
        columns = st.multiselect(f'Choose columns for {file.name}', df.columns,default=df.columns)
        df = df[columns]

        # Data Visualization

        st.subheader('📊 Data Visualization')
        if st.checkbox(f'Show Visualization for {file.name}'):
            st.bar_chart(df.select_dtypes(includes='number').iloc[:,:2])
        

        # Converstion Options
        st.subheader('✨ Converstion Options')
        converstion_type= st.radio(f'Converts {file.name} to:', ['CVS','Excel'],key=file.name)
        if st.button(f'Convert {file.name}'):
            buffer= BytesIO()
            if converstion_type == 'CSV':
                df.to_csv(buffer, index= False)
                file_name= file.name.replace(file_ext,'.csv')
                mine_type= 'text/csv'
            elif converstion_type == 'Excel':
                df.to_excel(buffer,index=False)
                file_name= file.name.replace(file_ext,'.xlsx')
                mine_type= 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)

            st.download_button(
                label=f'Download {file.name} as {converstion_type}',
                data=buffer,
                file_name=file_name,
                mime= mine_type
            )


st.success('🎉 All files processed successfully')
                