import os
import pandas as pd
import re
def read_input_data(consultation_name, model_name, demo, mode = 'theme_extraction'):
    # output and input paths
    input_path = os.path.join('data', consultation_name, 'input', 'input_file.xlsx')
    s_q_map_path = os.path.join('data', consultation_name, 'input', 'sheet_question_mapping.xlsx')
    xls = pd.ExcelFile(input_path)
    sheet_names = xls.sheet_names
    dataframes = {f'{name}': pd.read_excel(xls, sheet_name=name) for name in sheet_names}
    
    dataframes['df_q1'].loc[dataframes['df_q1']['mcq_response'] == 'Strongly agree', 'mcq_response'] = 'Agree'
    dataframes['df_q1'].loc[dataframes['df_q1']['mcq_response'] == 'Strongly disagree', 'mcq_response'] = 'Disagree'
       
    # Check if all dataframes first column is id
    for key, df in dataframes.items():
        if df.columns[0] != 'id':
            raise ValueError(f'First column of dataframe {key} is not "id"')
    
    # Rename the second column in each dataframe to 'response', and the third column (if it exists) to 'mcq_response'
    for key, df in dataframes.items():
        # Check n of unique values in the mcq_response column
        if 'mcq_response' in df.columns:
            if len(df['mcq_response'].unique()) > 10:
                raise ValueError(f'Number of unique values in the mcq_response column of df {key} exceeds 10. Please check the data to make sure this in fact is the appopriate column.')

    # If demo is True, only extract low-level insights from the first 10 rows of each dataframe
    if demo['boolean']==True:
        for key, df in dataframes.items():
            df = df.sample(demo['n_examples'])
            df.sort_values(by='id', inplace=True)
            df.reset_index(drop=True, inplace=True)
            dataframes[key] = df
    
    # Read in the sheet-question mapping (to be included in the prompt)
    s_q_map = pd.read_excel(s_q_map_path)
    s_q_map_dict = {key: value for key, value in s_q_map.iloc[:, :2].values}

    # Create the output directory and path
    themes = {}
    if mode != 'theme_extraction':
        try:
            themes_input_path = os.path.join('data', f'{consultation_name}/output/insight_{model_name}.xlsx')
            xls = pd.ExcelFile(themes_input_path)
            sheet_names = xls.sheet_names
            themes = {f'{name}': pd.read_excel(xls, sheet_name=name) for name in sheet_names}
        except:
            print('No themes found for this model') 
    return dataframes, themes, s_q_map_dict                                               

def clean_gpt_3_output():
     ## make the format of all equal? like strip for example?
    model = 'gpt-35-turbo-16k' ## clean the insight file 
    consultation_names = ['turing_consultation', 'synthetic_consultation']
    for consultation_name in consultation_names:
            output_dir = os.path.join('data', 'Brute_force')
            insight_path = os.path.join(output_dir, f'2024-09-08_{consultation_name}/insight_gpt-35-turbo-16k.xlsx')
            insight_xlsx = pd.ExcelFile(insight_path)
            responses_writer = pd.ExcelWriter(insight_path.replace('insight','clean_insight'))
            sheet_names = insight_xlsx.sheet_names
            insight_dataframes = {f'{name}': pd.read_excel(insight_xlsx, sheet_name=name) for name in sheet_names}
            for df_name in insight_dataframes.keys():
                insight_df = insight_dataframes[df_name]
                for index, row in insight_df.iterrows():
                    themes_list = re.findall(r"'([^']*)'", row['themes1'])
                    for theme in themes_list:
                        insight_df.loc[index, f'themes{themes_list.index(theme)+1}'] = theme
                insight_df.to_excel(responses_writer, sheet_name=df_name, index=False)
            responses_writer.close()
    return None
def clean_output():
    # output and input paths
    consultation_names = ['turing_consultation', 'synthetic_consultation']
    models = ['gpt-4','gpt-4o','gpt-4o-mini', 'gpt-35-turbo-16k', 'llama-3-8b-instruct','llama-3-70b-instruct', 'llama-2-70b-chat']
    llamas = ['llama-2-70b-chat']
    for model in llamas:
        for consultation_name in consultation_names:
            output_dir = os.path.join('data', 'Brute_force')
            insight_path = os.path.join(output_dir, f'2024-09-08_{consultation_name}/insight_{model}.xlsx')
            response_path = os.path.join(output_dir, consultation_name, f'response_result_{model}.xlsx')
            responses_writer = pd.ExcelWriter(response_path.replace('response_result','clean_response'))
            insight_xlsx = pd.ExcelFile(insight_path)
            response_xlsx = pd.ExcelFile(response_path)
            sheet_names = response_xlsx.sheet_names
            insight_dataframes = {f'{name}': pd.read_excel(insight_xlsx, sheet_name=name) for name in sheet_names}
            response_dataframes = {f'{name}': pd.read_excel(response_xlsx, sheet_name=name) for name in sheet_names}
            print(consultation_name, model)
            for df_name in insight_dataframes.keys():
                insight_df = insight_dataframes[df_name]
                response_df = response_dataframes[df_name]
                choices = insight_df['choice']
                theme_columns = [column for column in insight_df.columns if 'theme' in column]
                for choice in choices:
                    insight_dict = insight_df.loc[insight_df['choice']==choice ,theme_columns].to_dict(orient='records')[0]
                    insight_dict = {key.replace('themes', 'theme_'):value.replace('.','') for key, value in insight_dict.items() if not pd.isnull(value)}
                    a = response_df.loc[response_df['mcq_response']==choice, ['theme(s)','id']]
                    for index, row in a.iterrows():
                        if not pd.isnull(row['theme(s)']):
                            for key, value in insight_dict.items():
                                value = value.strip().replace("'",'')
                                row['theme(s)'] = row['theme(s)'].replace(value, f'{key}')
                            if 'theme_' not in row['theme(s)']:
                                row['theme(s)'] = re.sub(r'\b\d+\b', lambda x: f'theme_{x.group()}', row['theme(s)'])
                            row['theme(s)'] = row['theme(s)'].replace('\'','')
                            row['theme(s)'] = row['theme(s)'].replace('"','')
                            if '[' not in row['theme(s)']:
                                row['theme(s)'] = '[' + row['theme(s)'] + ']'
                            response_df.loc[response_df['id']==row['id'], 'theme(s)'] = str(row['theme(s)'])
                response_df.to_excel(responses_writer, sheet_name=df_name, index=False)
            responses_writer.close()
if __name__ == "__main__":
    clean_output()            