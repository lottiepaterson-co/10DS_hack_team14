import pandas as pd

def ingest_polling_spreadsheet(excel_file) -> str:

    xls = pd.ExcelFile(excel_file)

    combined_df = pd.DataFrame()

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df.to_string(index=False, na_rep="")