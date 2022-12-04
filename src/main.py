# 1. DBデータ取得
# 2. spreadsheet作成
# 3. spreadsheetにデータ書き込み

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class GetDataToSpreadsheet:
    def main(self):
        engine = self.connect_db()
        results = self.data_fetch(engine)
        print(results)

    def connect_db(self):
        database = "sqlite:///sampledb.sqlite3"
        engine = create_engine(database, echo=False)
        return engine

    def data_fetch(self, engine):
        sql = text("select num, name from member;")
        return list(engine.execute(sql))


if __name__ == "__main__":
    get_data_to_spreadsheet = GetDataToSpreadsheet()
    get_data_to_spreadsheet.main()
