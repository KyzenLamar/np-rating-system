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

def _default_value_for_column(col_name: str):
    """
    Визначає дефолт за назвою:
    - JSON-поля -> '[]'
    - селект у ПП_10 (рівень мови) -> "Немає"
    - текстові ідентифікатори (ID, DOI, URL, PROFILE, RID, SCOPUS, WOS) -> ""
    - все інше -> 0
    """
    name_low = str(col_name).lower()

    if col_name.endswith("_JSON") or name_low.endswith("_json"):
        return '[]'
    if col_name.startswith("НП_Пп_10_"):
        return "Немає"

    # евристика для текстових:
    key_substr = ("id", "doi", "url", "profile", "rid", "scopus", "wos")
    if any(k in name_low for k in key_substr):
        return ""

    return 0

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Гарантує наявність усіх колонок із c.ALL_NP_RATING_COLUMNS із коректними дефолтами.
    Повертає той самий df (модифікований) для зручності ланцюжків викликів.
    """
    for col_name in c.ALL_NP_RATING_COLUMNS:
        if col_name not in df.columns:
            df[col_name] = _default_value_for_column(col_name)
    # Заповнити NaN відповідним типо-дефолтом
    for col_name in df.columns:
        default_val = _default_value_for_column(col_name)
        df[col_name] = df[col_name].fillna(default_val)
    return df


def initialize_np_ratings_df(df_np_structure):
    """Ініціалізує DataFrame для рейтингів НП."""
    df_ratings_existing = load_np_ratings()

    if df_np_structure.empty:
        # Але навіть якщо структура порожня — повернемо існуючі + ensure_columns
        return ensure_columns(df_ratings_existing)

    df_current_pibs = df_np_structure[[c.COL_PIB]].copy()

    if not df_ratings_existing.empty:
        df_final_ratings = pd.merge(df_current_pibs, df_ratings_existing, on=c.COL_PIB, how='left')
    else:
        df_final_ratings = df_current_pibs.copy()

    # Період за замовчуванням
    if c.NP_COL_PERIOD not in df_final_ratings.columns:
        df_final_ratings[c.NP_COL_PERIOD] = str(datetime.now().year)

    # Гарантуємо всі колонки і дефолти
    df_final_ratings = ensure_columns(df_final_ratings)
    return df_final_ratings


def migrate_fill_default_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Якщо немає колонки Період — додасть її.
    Якщо у деяких рядках Період порожній — заповнить поточним роком.
    """
    year_str = str(datetime.now().year)
    if c.NP_COL_PERIOD not in df.columns:
        df[c.NP_COL_PERIOD] = year_str
    df[c.NP_COL_PERIOD] = df[c.NP_COL_PERIOD].astype(str).replace({"": year_str, "nan": year_str})
    return df

def upsert_np_row(df: pd.DataFrame, row_dict: dict) -> pd.DataFrame:
    """
    Оновлює або додає рядок за ключем (ПІБ, Період).
    - df: поточний датафрейм із рейтингами
    - row_dict: дані з форми (включно з c.COL_PIB і c.NP_COL_PERIOD)
    Повертає оновлений df.
    """
    if df is None or df.empty:
        df = pd.DataFrame(columns=[c.COL_PIB, c.NP_COL_PERIOD])

    # гарантія колонок (раптом нові NP_COL_* з'явились)
    df = ensure_columns(df)

    pib = str(row_dict.get(c.COL_PIB, "")).strip()
    period = str(row_dict.get(c.NP_COL_PERIOD, "")).strip()

    if not pib or not period:
        # нічого не робимо, повертаємо як є
        return df

    # індекс запису
    mask = (df[c.COL_PIB].astype(str) == pib) & (df[c.NP_COL_PERIOD].astype(str) == period)
    if not mask.any():
        # додаємо новий рядок-скелет із дефолтами
        new_row = {col: _default_value_for_column(col) for col in c.ALL_NP_RATING_COLUMNS}
        new_row[c.COL_PIB] = pib
        new_row[c.NP_COL_PERIOD] = period
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        mask = (df[c.COL_PIB].astype(str) == pib) & (df[c.NP_COL_PERIOD].astype(str) == period)

    # апдейтимо значення з форми (тільки відомі колонки)
    idx = df[mask].index[0]
    for k, v in row_dict.items():
        if k in df.columns:
            df.at[idx, k] = v

    # підчищаємо NaN → дефолт
    df = ensure_columns(df)

    return df
