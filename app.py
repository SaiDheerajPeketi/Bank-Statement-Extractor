import streamlit as st
import pandas as pd
import camelot
import tempfile
import os
from preprocessor import optional_decrypt_pdf, is_valid_date, is_valid_date_or_empty, extract_opening_balance_info, \
    extract_closing_balance_info


def process_pdf(uploaded_file, bank, password=None):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        if password:
            optional_decrypt_pdf(tmp_path, password)

        table_columns = ['DATE', 'NARRATION', 'CHQ.NO.', 'WITHDRAWAL (DR)', 'DEPOSIT (CR)', 'BALANCE']

        if bank == "Bank 1":
            tables = camelot.read_pdf(tmp_path, pages='all', flavor='stream')
            user_name = 'SAI DHEERAJ PEKETI'
            new_rows = []
            for index, table in enumerate(tables):
                if table.df.iloc[0, 0] == user_name:
                    print(f'Table_{index + 1}: {table.df.shape[1]}')
                    current_table_df = table.df.iloc[2:].reset_index(drop=True)
                    print(current_table_df.columns)
                    if table.df.shape[1] == 7:
                        current_table_df.loc[current_table_df[1] != '', 2] = current_table_df[1]
                        current_table_df.drop([1], axis=1, inplace=True)
                    elif table.df.shape[1] == 6:
                        invalid_dates = ~current_table_df[0].apply(is_valid_date_or_empty)
                        current_table_df.loc[invalid_dates, 1] = current_table_df.loc[invalid_dates, 0]
                        current_table_df.loc[invalid_dates, 0] = ''
                    current_table_df.reset_index(drop=True, inplace=True)
                    current_table_df.columns = table_columns
                    i = 0

                    while i < len(current_table_df):
                        if is_valid_date(current_table_df.iloc[i, 0]):
                            new_rows.append({
                                'DATE': current_table_df.iloc[i, 0],
                                'NARRATION': current_table_df.iloc[i, 1],
                                'CHQ.NO.': current_table_df.iloc[i, 2],
                                'WITHDRAWAL (DR)': current_table_df.iloc[i, 3],
                                'DEPOSIT (CR)': current_table_df.iloc[i, 4],
                                'BALANCE': current_table_df.iloc[i, 5]
                            })
                            i += 1
                        else:
                            if i + 1 < len(current_table_df) and i + 2 < len(current_table_df):
                                new_rows.append({
                                    'DATE': current_table_df.iloc[i + 1, 0],
                                    'NARRATION': current_table_df.iloc[i, 1] + current_table_df.iloc[i + 2, 1],
                                    'CHQ.NO.': current_table_df.iloc[i + 1, 2],
                                    'WITHDRAWAL (DR)': current_table_df.iloc[i + 1, 3],
                                    'DEPOSIT (CR)': current_table_df.iloc[i + 1, 4],
                                    'BALANCE': current_table_df.iloc[i + 1, 5]
                                })
                            i += 3
            if len(new_rows) != 0:
                table_df = pd.DataFrame(new_rows)
                table_df['WITHDRAWAL (DR)'] = pd.to_numeric(table_df['WITHDRAWAL (DR)'], errors='coerce')
                table_df['DEPOSIT (CR)'] = pd.to_numeric(table_df['DEPOSIT (CR)'], errors='coerce')

        elif bank == "Bank 2":
            tables = camelot.read_pdf(tmp_path, pages='all', flavor='lattice', strip_text='\n')
            new_rows = []
            for index, table in enumerate(tables):
                if index >= 3:
                    print(f'Table_{index + 1}: {table.df.shape[0]}')
                    isOpening, date, description, amount = extract_opening_balance_info(table.df.iloc[0, 0])
                    if isOpening:
                        new_rows.append({
                            'DATE': description + ' on ' + str(date) + ':      ' + str(amount),
                            'NARRATION': '',
                            'CHQ.NO.': '',
                            'WITHDRAWAL (DR)': '',
                            'DEPOSIT (CR)': '',
                            'BALANCE': ''
                        })
                    current_table_df = table.df.iloc[1:].reset_index(drop=True)
                    print(current_table_df.columns)
                    table_columns = ['DATE', 'NARRATION', 'CHQ.NO.', 'WITHDRAWAL (DR)', 'DEPOSIT (CR)', 'BALANCE']
                    current_table_df.reset_index(drop=True, inplace=True)
                    current_table_df.columns = table_columns
                    i = 0
                    while i < len(current_table_df):
                        if i == len(current_table_df) - 1:
                            text = extract_closing_balance_info(table.df.iloc[i + 1, 0])
                            if text:
                                new_rows.append({
                                    'DATE': text,
                                    'NARRATION': '',
                                    'CHQ.NO.': '',
                                    'WITHDRAWAL (DR)': '',
                                    'DEPOSIT (CR)': '',
                                    'BALANCE': ''
                                })
                                break
                        new_rows.append({
                            'DATE': current_table_df.iloc[i, 0],
                            'NARRATION': current_table_df.iloc[i, 1],
                            'CHQ.NO.': current_table_df.iloc[i, 2],
                            'WITHDRAWAL (DR)': current_table_df.iloc[i, 3],
                            'DEPOSIT (CR)': current_table_df.iloc[i, 4],
                            'BALANCE': current_table_df.iloc[i, 5]
                        })
                        i += 1

            if len(new_rows) != 0:
                table_df = pd.DataFrame(new_rows)
                table_df.columns = table_columns
                table_df['WITHDRAWAL (DR)'] = pd.to_numeric(table_df['WITHDRAWAL (DR)'], errors='coerce')
                table_df['DEPOSIT (CR)'] = pd.to_numeric(table_df['DEPOSIT (CR)'], errors='coerce')
        else:
            raise ValueError("Unsupported bank selection.")

        # Clean up the temporary file
        os.unlink(tmp_path)
        return table_df

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
        # Ensure temporary file is cleaned up even if an error occurs
        if 'tmp_path' in locals():
            os.unlink(tmp_path)
        return pd.DataFrame()


st.title("Bank Statement PDF Processor")

uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

bank = st.selectbox("Select your bank", options=["Bank 1", "Bank 2"])

password = st.text_input("Enter PDF password (if applicable)", type="password")

if st.button("Process"):
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            df = process_pdf(uploaded_file, bank, password)
        if not df.empty:
            st.success("PDF processed successfully!")
            st.dataframe(df)
        else:
            st.error("Failed to process the PDF. Please check the file and options.")
    else:
        st.warning("Please upload a PDF file before pressing Process.")