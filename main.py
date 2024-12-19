import camelot
import pandas as pd

pdf_file_name = 'test.pdf'

tables = camelot.read_pdf(pdf_file_name, pages='all', flavor='stream', strip_text='\n')

print(tables)

for index, table in enumerate(tables):
    table.df.to_csv('table_' + str(index) + '.csv', index=False)
