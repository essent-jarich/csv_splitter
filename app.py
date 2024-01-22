import pandas as pd
import streamlit as st

st.write("# CSV uploader for when you can't split columns")
st.write(
    """
    This simple app will take your CSV, look for any columns with a new line in, 
    and transform this column into new columns so you can work with it in Excel again.
    This app idea orginated from the fact that the data to columns functionality in Excel
    was not working for us. There should be a way to make CTRL + J work as a delimiter,
    but it was less work to make a quick streamlit app.
    """
)

file = st.file_uploader("Upload your CSV here", type='csv')
if file:
    df = pd.read_csv(file, encoding='unicode_escape')

    st.write("## This is what your data looks like")
    st.write(df.head())

    df_original = df.copy()

    for column in df.columns:
        if df[column].dtype in [object, str]:
            splitted = df[column].str.split('\n', expand=True)
            width_df = splitted.shape[1]
            if width_df > 1:
                df = pd.concat([df, splitted], axis=1)
    
    if df_original.equals(df):
        st.write("### No columns with blank lines detected")

    else:
        st.write("## This is what the transformed data looks like")
        st.write(df.head())

        csv = df.to_csv().encode('utf-8')

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='your_data.csv',
            mime='text/csv',
        )