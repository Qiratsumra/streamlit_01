import streamlit as st
import pandas as pd
import os
from io import BytesIO
# Setup the page
st.set_page_config(page_title='Data Sweeper', layout='centered')

# Custom css
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

# Title and Description value:
st.title('💿 Data Sweeper by Qirat Saeed!')
st.write('Transform your files into \'CV\' and \'Excel\' formate with build-in data cleaning and visualization.')

# File uploader
upload_files  = st.file_uploader('Upload your files \'Only CSV and Excel\' formate files are allowed', type=['csv','xlsx'], accept_multiple_files=True)
if upload_files:
    for file in upload_files:
        # file data show in lower case
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f'Unspported file-type: {file_ext}')
            continue

         # Display uploaded file information (name and size)
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB

        # Get Files Details:
        st.write('🔍 Preview the He ad of the DataFrame')
        st.dataframe(df.head())

        # Data Cleaning Option
        if st.subheader(st.checkbox(f'Cleaning Data for {file.name} file')):
            col1 , col2 = st.columns(2)

            # for Column 1 Data
            with col1:
                if st.button(f'Remove Duplicates from the: {file.name} file'):
                    df.drop_duplicates(inplace=True)
                    st.write(f'✔ Duplicates Removed!')
            with col2 :
                if st.button(f'❔ Fill missing values from {file.name} file'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('✔ Missing Values have been filled! ')
        
        st.subheader('🎯 Select the colums to keep ')
        columns = st.multiselect(f'Choose Colums from {file.name}',df.columns,default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader('📊 Data Visualization')
        if st.checkbox(f'Shows Data Visualization for {file.name}'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        
        # Converstion Option
        st.subheader('✨ Converstion Options:')
        converstion_types = st.radio(f'Convert {file.name} into: ', ['CSV','Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            if converstion_types == 'CSV':
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,'.csv')
                mine_type = 'text/csv'
            elif converstion_types == 'Excel':
                df.to_excel(buffer , index=False)
                file_name = file.name.replace(file_ext,'.xlsx')
                mine_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)
            st.download_button(label=f'Download {file.name} as {converstion_types}',
            data = buffer,
            file_name = file.name,
            mine = mine_type 
            )


st.success('🎉🎊 All files processed successfully!')

