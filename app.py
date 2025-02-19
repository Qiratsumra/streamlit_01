import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup the page
st.set_page_config(page_title='Data Sweeper', layout='centered')

# Custom CSS
st.markdown(
    '''
    <style>
    .stApp {
        background-color: #A0D8F1;
        color: white;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Title and Description
st.title('💿 Data Sweeper by Qirat Saeed!')
st.write("Transform your files into 'CSV' and 'Excel' format with built-in data cleaning and visualization.")

# File uploader
upload_files = st.file_uploader(
    "Upload your files (Only CSV and Excel files are allowed)", 
    type=['csv', 'xlsx'], 
    accept_multiple_files=True
)

if upload_files:
    for file in upload_files:
        # Get file extension
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file, engine="openpyxl")  # ✅ Added 'openpyxl' engine
        else:
            st.error(f'Unsupported file type: {file_ext}')
            continue

        # Display uploaded file info
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # Convert to KB

        # Display preview of data
        st.subheader('🔍 Preview of the DataFrame')
        st.dataframe(df.head())

        # Data Cleaning Options
        if st.checkbox(f'🛠️ Clean Data for {file.name}'):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f'❌ Remove Duplicates from {file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.write('✔ Duplicates Removed!')

            with col2:
                if st.button(f'❔ Fill Missing Values in {file.name}'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('✔ Missing Values Filled!')

        # Column Selection
        st.subheader('🎯 Select Columns to Keep')
        selected_columns = st.multiselect(f'Choose Columns from {file.name}', df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader('📊 Data Visualization')
        if st.checkbox(f'Show Data Visualization for {file.name}'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader('✨ Conversion Options')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, '.csv')
                mime_type = 'text/csv'
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False, engine="openpyxl")  # ✅ Ensured 'openpyxl' is used
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            buffer.seek(0)
            st.download_button(
                label=f'⬇ Download {file.name} as {conversion_type}',
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success('🎉🎊 All files processed successfully!')
