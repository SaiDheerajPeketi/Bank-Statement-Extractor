import camelot
import pandas as pd

pdf_file_name = 'test.pdf'

tables = camelot.read_pdf(pdf_file_name, pages='all', flavor='stream')

print(tables)

for table in tables:
    print(table.df)