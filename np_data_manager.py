# np_data_manager.py
from datetime import datetime
import pandas as pd
import json
import os
import np_constants as c
import threading

DATA_DIR = "data_np"  # Окрема папка для даних НП
NP_RATINGS_FILE = os.path.join(DATA_DIR, "ratings_np_data.csv")
#NP_STRUCTURE_FILE = os.path.join(DATA_DIR, "Структура_НП.json")
NP_STRUCTURE_FILE = os.path.join(DATA_DIR, "Структура_НП_тест.json")


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# Locks для конкурентного доступу
ratings_lock = threading.Lock()
structure_lock = threading.Lock()

def get_all_np_defined_columns():
    """Збирає всі NP_COL_* константи."""
    all_cols = [c.COL_PIB]
    for const_name in dir(c):
        if const_name.startswith("NP_COL_"):
            all_cols.append(getattr(c, const_name))
    return list(set(all_cols))


c.ALL_NP_RATING_COLUMNS = get_all_np_defined_columns()


def load_np_structure():
    """Завантажує структуру наукових працівників з JSON файлу."""
    try:
        with open(NP_STRUCTURE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        return pd.DataFrame(columns=[c.COL_PIB, c.COL_POSITION])


def save_np_structure(df):
    """Зберігає структуру наукових працівників у JSON файл."""
    with structure_lock:  # Блокуємо файл
        df.to_json(NP_STRUCTURE_FILE, force_ascii=False, orient='records', indent=2)


def load_np_ratings():
    """Завантажує дані оцінювання НП з CSV файлу."""
    if os.path.exists(NP_RATINGS_FILE) and os.path.getsize(NP_RATINGS_FILE) > 0:
        return pd.read_csv(NP_RATINGS_FILE)
    return pd.DataFrame()


def save_np_ratings(df_ratings):
    """Зберігає дані оцінювання НП у CSV файл."""
    with ratings_lock:  # Блокуємо файл
        df_ratings.to_csv(NP_RATINGS_FILE, index=False, encoding='utf-8')


def initialize_np_ratings_df(df_np_structure):
    """Ініціалізує DataFrame для рейтингів НП."""
    df_ratings_existing = load_np_ratings()

    if df_np_structure.empty:
        return df_ratings_existing

    df_current_pibs = df_np_structure[[c.COL_PIB]].copy()

    if not df_ratings_existing.empty:
        df_final_ratings = pd.merge(df_current_pibs, df_ratings_existing, on=c.COL_PIB, how='left')
    else:
        df_final_ratings = df_current_pibs.copy()

    # Додаємо колонку NP_COL_PERIOD, якщо її немає
    if c.NP_COL_PERIOD not in df_final_ratings.columns:
        df_final_ratings[c.NP_COL_PERIOD] = str(datetime.now().year)

    for col_name in c.ALL_NP_RATING_COLUMNS:
        if col_name not in df_final_ratings.columns:
            # Проста логіка для значень за замовчуванням
            if col_name.endswith("_JSON"):
                df_final_ratings[col_name] = '[]'
            elif col_name.startswith("НП_Пп_10_"):
                df_final_ratings[col_name] = "Немає"
            else:
                df_final_ratings[col_name] = 0

    df_final_ratings = df_final_ratings.fillna(0)
    return df_final_ratings
