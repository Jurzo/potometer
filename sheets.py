import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1kCCLRpFxTEChTQeAWq_ndqPykZ9qz3Ab3mxZC1vQUx0'
SAMPLE_RANGE_NAME = 'A1:C11'

def createService():
    global service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

def read():
    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')
    return values_input

def Export_Data_To_Sheets(df, torange):
    response_date = service.spreadsheets().values().update(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range=torange,
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated')

createService()
x = read()

df=pd.DataFrame(x[1:], columns=x[0])
print(df)
print(x)
Export_Data_To_Sheets(df, 'A2:C12')
