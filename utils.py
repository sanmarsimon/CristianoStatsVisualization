import pandas as pd


def extract_title(title):
    title = title.strip()
    title = title.replace(" ", "")
    if title[-1].isdigit():
        return title[:-2]
    
    return title


def format_dataframe(df):
    for title in df.columns:
        if title.startswith("Unnamed"):
            df.rename(columns={title: df[title][0]}, inplace=True)
        else:
            head_title = extract_title(title)
            df.rename(columns={title: head_title  + '.' + str(df[title][0])}, inplace=True)
    df = df.drop([0])
    
    return df


def get_data_from_file(file_path):  

    # read the excel file using the pandas ExcelFile method and assign it to the variable xls
    xls = pd.ExcelFile(file_path) 
    sheetX = xls.parse(0) 
    
    return sheetX 