import gspread
from google.oauth2.service_account import Credentials
from app.config import GOOGLE_CREDS_PATH, SPREADSHEET_NAME


class SheetsService:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=scopes
        )
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(SPREADSHEET_NAME).sheet1

    def get_all_posts(self):
        rows = self.sheet.get_all_values()
        headers = rows[0]
        data_rows = rows[1:]
        posts = [dict(zip(headers, row)) for row in data_rows]
        return posts

    # 🔹 Метод для обновления статуса
    def update_status(self, row_number, new_status):
        """
        row_number: номер строки в Google Sheets (считая с 1)
        new_status: строка, которую ставим в колонку Статус (H)
        """
        self.sheet.update(f"H{row_number}", [[new_status]])

    # 🔹 Метод для обновления любой ячейки
    def update_cell(self, row_number, col_letter, value):
        """
        row_number: номер строки (считая с 1)
        col_letter: буква колонки (например 'I' для telegram_message_id)
        value: значение для записи
        """
        self.sheet.update(f"{col_letter}{row_number}", [[value]])
