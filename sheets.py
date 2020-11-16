from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

class SheetDriver:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.ID = '1kCCLRpFxTEChTQeAWq_ndqPykZ9qz3Ab3mxZC1vQUx0'
        self.RANGE = 'A:DDD'
        self.rows = 0
        self.columns = 0

    def createService(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES) # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def read(self):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.ID, range=self.RANGE).execute()
        self.data = result.get('values', [])

        self.rows = len(self.data)
        self.columns = 0 if self.rows == 0 else len(self.data[0])

        if not self.data:
            print('No data found.')
        return self.data

    def Export_Data_To_Sheets(self, df, torange):
        self.service.spreadsheets().values().update(
            spreadsheetId=self.ID,
            valueInputOption='RAW',
            range=torange,
            body=dict(
                majorDimension='ROWS',
                values=df.T.reset_index().T.values.tolist())
        ).execute()
        print('Sheet successfully Updated')

    def addHeaders(self, headers):
        if self.data:
            row = [""] * ((len(headers)-1) * 4 + 1)
            for i in range(len(headers)):
                row[(i-1) * 4 + 1] = headers[i]

        else:
            row = self.data[0] + [""] * (len(headers) * 4)
            for i in range(len(headers)):
                row[len(self.data[0]) + 4*i + 3] = headers[i]

        self.service.spreadsheets().values().update(
            spreadsheetId=self.ID,
            valueInputOption='RAW',
            range='A:DDDD',
            body=dict(
                majorDimension='ROWS',
                values=row)
        ).execute()

if __name__ == '__main__':
    driver = SheetDriver()
    driver.createService()
    print(driver.read())
    print(driver.rows, driver.columns)
    driver.addHeaders(["yksi", "kaksi"])


#createService()
#x = read()
#df=pd.DataFrame(x[1:], columns=x[0])
#print(df)
#print(x)
#Export_Data_To_Sheets(df, 'A2:C12')
