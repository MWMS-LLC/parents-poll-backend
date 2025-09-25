# import_setup.py to parents_db

import psycopg2
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def clean_csv_value(value):
    """Clean CSV values and handle multi-line content"""
    if value is None:
        return None
    value = str(value).strip().replace('\ufeff', '')
    if '\n' in value:
        value = value.replace('\n', ' ')
    return value

def import_setup_data():
    """Import CSV data into PostgreSQL database for parents"""

    DATABASE_URL = os.getenv('DATABASE_URL')
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to parents_db")

        # Truncate tables before import
        cursor.execute("TRUNCATE TABLE options RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE questions RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE blocks RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE categories RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE soundtracks RESTART IDENTITY CASCADE;")
        conn.commit()
        print("✅ Existing parent data truncated")

        # Import categories
        print("📁 Importing categories...")
        with open('../data/categories.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO categories (category_name, category_text, version, uuid)
                    VALUES (%s, %s, %s, %s)
                """, (
                    clean_csv_value(row['category_name']),
                    clean_csv_value(row.get('category_text', '')),
                    clean_csv_value(row.get('version', '')),
                    clean_csv_value(row.get('uuid', ''))
                ))
        print("    ✅ Categories imported")

        # Import blocks
        print("📁 Importing blocks...")
        with open('../data/blocks.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO blocks (category_id, category_name, block_number, block_code, block_text, version, uuid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(row['category_id']),
                    clean_csv_value(row.get('category_name', '')),
                    int(row['block_number']),
                    clean_csv_value(row['block_code']),
                    clean_csv_value(row['block_text']),
                    clean_csv_value(row.get('version', '')),
                    clean_csv_value(row.get('uuid', ''))
                ))
        print("    ✅ Blocks imported")

        # Import questions
        print("📁 Importing questions...")
        with open('../data/questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO questions (question_code, question_number, question_text,
                                            category_id, category_name, is_start_question, parent_question_id,
                                            check_box, max_select, block_number, block_text, color_code, version)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    clean_csv_value(row['question_code']),
                    int(row['question_number']),
                    clean_csv_value(row['question_text']),
                    int(row['category_id']),
                    clean_csv_value(row.get('category_name', '')),
                    row.get('is_start_question', 'false').lower() == 'true',
                    int(row['parent_question_id']) if row.get('parent_question_id') and row.get('parent_question_id').strip() else None,
                    row.get('check_box', 'false').lower() == 'true',
                    int(row.get('max_select', 1)) if row.get('max_select') and row.get('max_select').strip() else 1,
                    int(row['block_number']),
                    clean_csv_value(row.get('block_text', '')),
                    clean_csv_value(row.get('color_code', '')),
                    clean_csv_value(row.get('version', ''))
                ))
        print("    ✅ Questions imported")

        # Import options
        print("📁 Importing options...")
        with open('../data/options.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO options (category_id, category_name, block_number, block_text,
                                         question_code, question_number, question_text,
                                         check_box, max_select,
                                         option_select, option_code, option_text,
                                         response_message, companion_advice, tone_tag,
                                         next_question_id, version)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(row['category_id']),
                    clean_csv_value(row.get('category_name', '')),
                    int(row['block_number']),
                    clean_csv_value(row['block_text']),
                    clean_csv_value(row['question_code']),
                    int(row['question_number']),
                    clean_csv_value(row['question_text']),
                    row.get('check_box', 'false').lower() == 'true',
                    int(row.get('max_select', 1)) if row.get('max_select') and row.get('max_select').strip() else 1,
                    clean_csv_value(row['option_select']),
                    clean_csv_value(row['option_code']),
                    clean_csv_value(row['option_text']),
                    clean_csv_value(row.get('response_message', '')),
                    clean_csv_value(row.get('companion_advice', '')),
                    clean_csv_value(row.get('tone_tag', '')),
                    int(row['next_question_id']) if row.get('next_question_id') and row.get('next_question_id').strip() else None,
                    clean_csv_value(row.get('version', ''))
                ))
        print("    ✅ Options imported")

        # Commit
        conn.commit()
        print("✅ All parent data imported successfully!")

        # Summary counts
        for table in ["categories", "blocks", "questions", "options"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"  {table.capitalize()}: {cursor.fetchone()[0]}")

    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import_setup_data()
