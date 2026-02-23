import os
import re
import tempfile
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests


class GoogleClient:
    def __init__(self, credentials_file):
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/documents.readonly']
        )
        self.sheets = build('sheets', 'v4', credentials=self.creds)
        self.docs = build('docs', 'v1', credentials=self.creds)
        print("✅ Авторизация OK")

    def read_sheet(self, sheet_id, range_):
        rows = self.sheets.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_).execute().get('values', [])
        print(f"✅ Прочитано {len(rows)} строк")
        return rows

    def update_cell(self, sheet_id, row, col, value):
        self.sheets.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=f'Лист1!{col}{row}',
            valueInputOption='RAW', body={'values': [[value]]}
        ).execute()
        print(f"✅ {col}{row} = {value}")

    def get_text_from_doc(self, doc_url):
        doc_id = re.search(r'/document/d/([^/]+)', doc_url).group(1)
        doc = self.docs.documents().get(documentId=doc_id).execute()
        text = ''.join(
            para_elem['textRun']['content']
            for element in doc['body']['content']
            if 'paragraph' in element
            for para_elem in element['paragraph']['elements']
            if 'textRun' in para_elem
        )
        print(f"✅ Текст документа ({len(text)} символов)")
        return text

    def download_media(self, media_url):
        if not media_url:
            return None
        try:
            session = requests.Session()
            session.trust_env = False  # игнорируем системные прокси
            r = session.get(media_url, stream=True, timeout=10)
            r.raise_for_status()
            ext = media_url.split('.')[-1].split('?')[0][:5] or 'jpg'
            path = os.path.join(tempfile.gettempdir(),
                                f"media_{datetime.now().timestamp()}.{ext}")
            with open(path, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            print(f"✅ Медиа: {path}")
            return path
        except Exception as e:
            print(f"❌ Ошибка медиа: {e}")
            return None
