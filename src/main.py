from sqlalchemy import create_engine
from sqlalchemy.sql import text
from google.oauth2 import service_account
import gspread


class GetDataToSpreadsheet:
    def main(self):
        engine = self.connect_db()
        results = self.data_fetch(engine)

        formated_results = [self.to_values(result) for result in results]

        credentials = self.get_credentials()
        self.create_spreadsheet(credentials, formated_results)

    def connect_db(self):
        database = "sqlite:///sampledb.sqlite3"
        engine = create_engine(database, echo=False)

        return engine

    def data_fetch(self, engine):
        sql = text("select num, name from member;")
        results = engine.execute(sql)

        return results

    def get_credentials(self):
        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        credentials = service_account.Credentials.from_service_account_file(
            "secrets.json", scopes=scopes
        )

        return credentials

    def create_spreadsheet(self, credentials, formated_results):
        gspread_credentials = gspread.authorize(credentials)
        spreadsheet = gspread_credentials.create("sample spreadsheet")

        # NOTE: replace mail address
        spreadsheet.share("example@example.com", perm_type="user", role="writer")

        response = spreadsheet.values_update(
            "Sheet1!A1",
            params={
                "valueInputOption": "RAW",
            },
            body={"values": formated_results},
        )

        print(response)

        return response

    # NOTE: 以下から拝借。
    # gspread(およびgspread_dataframe)の利用方法について - Pirika Developers Blog
    # https://devblog.pirika.org/entry/2022/03/29/113000
    @staticmethod
    def to_values(data) -> list:
        return [
            data.num,
            data.name,
        ]


if __name__ == "__main__":
    get_data_to_spreadsheet = GetDataToSpreadsheet()
    get_data_to_spreadsheet.main()
