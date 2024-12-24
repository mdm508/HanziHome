import json
import sqlite3
import os

class DatabaseController:
    DB_PATH = 'database.db'
    JSON_PATH = 'dictionary.json' # where intial character data lives
    SQL_PATH = 'create_tables.sql'

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.ensure_tables_exist()
        if self.database_is_empty():
            self.load_json_into_database()

    def ensure_tables_exist(self):
        """
        calling this function when sql tables don't exist will cause the tables to be created.
        otherwise nothing happens.
        """
        with open(self.SQL_PATH, 'r') as file:
            sql_script = file.read()
        self.conn.executescript(sql_script)

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor

    def database_is_empty(self):
        result = self.execute_query("SELECT COUNT(*) FROM characters").fetchone()
        return result[0] == 0

    def load_json_into_database(self):
        try:
            with open(self.JSON_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)

            insert_characters = """
                INSERT INTO characters (hanzi, definition, decomposition, radical, keyword, rth, pinyin, ipa, zhuyin, matches)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            insert_etymology = """
                INSERT INTO Etymology (hanzi, type, hint, phonetic, semantic)
                VALUES (?, ?, ?, ?, ?)"""

            self.conn.execute('BEGIN TRANSACTION')
            for entry in data.values():
                self.cursor.execute(insert_characters, (
                    entry['character'],
                    entry.get('definition'),
                    entry['decomposition'],
                    entry['radical'],
                    entry.get('keyword'),
                    entry.get('rth_index'),
                    json.dumps(entry['pinyin']),
                    json.dumps(entry['ipa']),
                    json.dumps(entry['zhuyin']),
                    json.dumps(entry['matches'])
                ))

                if 'etymology' in entry and 'type' in entry['etymology']:
                    etymology = entry['etymology']
                    self.cursor.execute(insert_etymology, (
                        entry['character'],
                        etymology['type'],
                        etymology.get('hint'),
                        etymology.get('phonetic'),
                        etymology.get('semantic')
                    ))

            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()

    def fetch_character(self, character):
        sql = "SELECT * FROM characters WHERE hanzi = ?"
        result = self.execute_query(sql, (character,)).fetchone()
        return dict(result) if result else None

    def fetch_rth_hanzi(self):
        sql = "SELECT rth, hanzi, keyword, zhuyin FROM characters WHERE rth IS NOT NULL ORDER BY rth ASC"
        results = self.execute_query(sql).fetchall()
        return [dict(row) for row in results]

    def fetch_keyword(self, character):
        sql = "SELECT keyword FROM characters WHERE hanzi = ?"
        result = self.execute_query(sql, (character,)).fetchone()
        return result['keyword'] if result else None

    def update_keyword(self, keyword_id, updated_keyword):
        sql = "UPDATE characters SET keyword = ? WHERE hanzi = ?"
        try:
            self.execute_query(sql, (updated_keyword, keyword_id))
            self.export_to_json()
            return {'success': True, 'message': 'Keyword updated successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Update failed: {e}'}

    def export_to_json(self):
        sql = """
            SELECT c.*, e.type, e.hint, e.phonetic, e.semantic
            FROM characters AS c
            LEFT JOIN etymology AS e ON c.hanzi = e.hanzi"""
        results = self.execute_query(sql).fetchall()

        data = {}
        for row in results:
            character = row['hanzi']
            if character not in data:
                data[character] = {
                    'character': character,
                    'definition': row['definition'],
                    'decomposition': row['decomposition'],
                    'radical': row['radical'],
                    'keyword': row['keyword'],
                    'rth': row['rth'],
                    'pinyin': json.loads(row['pinyin']),
                    'ipa': json.loads(row['ipa']),
                    'zhuyin': json.loads(row['zhuyin']),
                    'matches': json.loads(row['matches']),
                    'etymology': {}
                }
            if row['type']:
                data[character]['etymology'] = {
                    'type': row['type'],
                    'hint': row['hint'],
                    'phonetic': row['phonetic'],
                    'semantic': row['semantic']
                }

        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        local_file = 'hanzidict.json'
        if os.getenv('HEROKU'):
            print(json_data)
        else:
            with open(local_file, 'w', encoding='utf-8') as file:
                file.write(json_data)

    def close(self):
        self.conn.close()

# Example usage
if __name__ == '__main__':
    db = DatabaseController()
    db.export_to_json()
    print(db.fetch_character('二'))
    db.close()
