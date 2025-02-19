import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure the Streamlit app's appearance and layout
# 'page_title' sets the browser tab title
# 'layout="wide"' allows more horizontal space, improving the display for tables and graphs
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for styling the app with dark mode aesthetics
# This enhances the UI by setting background colors, button styles, and text formatting
st.markdown(
    """
    <style>
    .stApp{
    background-color:#A0D8F1
    }
        .block-container {
            padding: 3rem 2rem;  /* Padding around main container for spacing */
            border-radius: 12px;  /* Rounds the corners of the container */
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);  /* Adds subtle shadow for depth */
        }
        h1, h2, h3, h4, h5, h6 {
            color:rgb(16, 18, 19);  /* Light blue color for headings to stand out */
        }
        .stButton>button {
            border: none;
            border-radius: 8px;  /* Rounds button edges */
            background-color:rgb(99, 133, 161);  /* Primary blue for buttons */
            color: white;  /* White text for contrast */
            padding: 0.75rem 1.5rem;  /* Enlarges button for better interaction */
            font-size: 1rem;  /* Readable button text */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);  /* Shadow for button depth */
        }
        .stButton>button:hover {
            background-color: #005a9e;  /* Darker blue on hover for visual feedback */
            cursor: pointer;
        }
        .stDataFrame, .stTable {
            border-radius: 10px;  /* Smooth edges for data tables and frames */
            overflow: hidden;  /* Prevents data from overflowing the container */
        }
        .css-1aumxhk, .css-18e3th9 {
            text-align: left;
            color: white;  /* Ensures all standard text is white for readability */
        }
        .stRadio>label {
            font-weight: bold;
            color: white;
        }
        .stCheckbox>label {
            color: white;
        }
        .stDownloadButton>button {
            background-color: #28a745;  /* Green color for download buttons */
            color: white;
        }
        .stDownloadButton>button:hover {
            background-color: #218838;  /* Darker green on hover for download buttons */
        }
    </style>
    """,
    unsafe_allow_html=True  # 'unsafe_allow_html' permits raw HTML/CSS embedding in the Streamlit app
)

# Display the main app title and introductory text
st.title("Advanced Data Sweeper")  # Large, eye-catching title
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader widget that accepts CSV and Excel files
# 'accept_multiple_files=True' allows batch uploading multiple files at once
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Processing logic for uploaded files (if any files are uploaded)
if uploaded_files:
    for file in uploaded_files:
        # Extract the file extension to determine if it's CSV or Excel
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        # Read the uploaded file into a pandas DataFrame based on its extension
        if file_extension == ".csv":
            df = pd.read_csv(file)  # Read CSV files
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)  # Read Excel files
        else:
            # Show an error message if the file type is unsupported
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        # Display uploaded file information (name and size)
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB

        # Preview the first 5 rows of the uploaded file
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())  # Display a scrollable preview of the data
        
        # Section for data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)  # Split cleaning options into two columns
            with col1:
                # Button to remove duplicate rows from the DataFrame
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                # Button to fill missing numeric values with column means
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values in Numeric Columns Filled with Column Means!")

        # Section to choose specific columns to convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]  # Filters the DataFrame to the selected columns
        
        # Visualization section for uploaded data
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart
        
        # Section to choose file conversion type (CSV or Excel)
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Creates in-memory buffer for file output
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download button for the converted file
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")  # Display success message when all files are processed






































# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO
# # Setup the page
# st.set_page_config(page_title='Data Sweeper', layout='centered')

# # Custom css
# st.markdown(
#     '''
#     <style>
#     .stApp{
#        background-color: #A0D8F1;
#        color:white
#     }
#     </style>
#     ''',
#     unsafe_allow_html=True
# )

# # Title and Description value:
# st.title('💿 Data Sweeper by Qirat Saeed!')
# st.write('Transform your files into \'CV\' and \'Excel\' formate with build-in data cleaning and visualization.')

# # File uploader
# upload_files  = st.file_uploader('Upload your files \'Only CSV and Excel\' formate files are allowed', type=['cvs','xlsx'], accept_multiple_files=True)
# if upload_files:
#     for file in upload_files:
#         # file data show in lower case
#         file_ext = os.path.splitext(file.name)[-1].lower()

#         if file_ext == '.cvs':
#             df = pd.read_csv(file)
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(file)
#         else:
#             st.error(f'Unspported file-type: {file_ext}')
#             continue

#          # Display uploaded file information (name and size)
#         st.write(f"**📄 File Name:** {file.name}")
#         st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB

#         # Get Files Details:
#         st.write('🔍 Preview the He ad of the DataFrame')
#         st.dataframe(df.head())

#         # Data Cleaning Option
#         if st.subheader(st.checkbox(f'Cleaning Data for {file.name} file')):
#             col1 , col2 = st.columns(2)

#             # for Column 1 Data
#             with col1:
#                 if st.button(f'Remove Duplicates from the: {file.name} file'):
#                     df.drop_duplicates(inplace=True)
#                     st.write(f'✔ Duplicates Removed!')
#             with col2 :
#                 if st.button(f'❔ Fill missing values from {file.name} file'):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write('✔ Missing Values have been filled! ')
        
#         st.subheader('🎯 Select the colums to keep ')
#         columns = st.multiselect(f'Choose Colums from {file.name}',df.columns,default=df.columns)
#         df = df[columns]

#         # Data Visualization
#         st.subheader('📊 Data Visualization')
#         if st.checkbox(f'Shows Data Visualization for {file.name}'):
#             st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        
#         # Converstion Option
#         st.subheader('✨ Converstion Options:')
#         converstion_types = st.radio(f'Convert {file.name} into: ', ['CVS','Excel'], key=file.name)

#         if st.button(f'Convert {file.name}'):
#             buffer = BytesIO()
#             if converstion_types == 'CSV':
#                 df.to_csv(buffer,index=False)
#                 file_name = file.name.replace(file_ext,'.csv')
#                 mine_type = 'text/csv'
#             elif converstion_types == 'Excel':
#                 df.to_excel(buffer , index=False)
#                 file_name = file.name.replace(file_ext,'.xlsx')
#                 mine_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#             buffer.seek(0)
#             st.download_button(label=f'Download {file.name} as {converstion_types}',
#             data = buffer,
#             file_name = file.name,
#             mine = mine_type 
#             )


# st.success('🎉🎊 All files processed successfully!')