# app_np.py
import streamlit as st
import pandas as pd
import altair as alt
import json
import np_constants as c
import np_data_manager as dm
import np_calculations as calc
from uaf_styles import load_css
from pathlib import Path
import base64
from datetime import datetime
import datetime as dt
from oauth_google import ensure_login, logout_button, _google_userinfo_via_button


# --- КОНФІГУРАЦІЯ АДМІНІСТРАТОРІВ ---
# Впишіть сюди ПІБ тих, хто буде мати права адміністратора
ADMIN_USERS = ["Пампуха Ігор Володимирович", "Логунов Ігор Юрійович", "Білан Максим Борисович",
               "Карпенко Андрій Олексійович"]


# --- Налаштування сторінки ---
st.set_page_config(layout="wide", page_title="Система оцінювання НП", page_icon="favicon.ico")

# 🔽 Додаємо утиліту для підміни заголовків
def with_pretty_headers(df: pd.DataFrame) -> pd.DataFrame:
    labels = getattr(c, "COLUMN_LABELS", {})
    return df.rename(columns=lambda col: labels.get(col, col))


def favicon_data_uri(path: str = "favicon.ico") -> str:
    p = Path(path)
    with p.open("rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    # MIME для .ico
    return f"data:image/x-icon;base64,{b64}"


def ui_bool(label: str, df: pd.DataFrame, row_idx, col_key: str, pib: str, period: str):
    """
    Уніфікований чекбокс для бінарних полів.
    - Глобально-унікальний key (щоб не злипався стан).
    - Жорстке приведення до bool на вході, і запис 0/1 на виході.
    """
    st_key = f"chk::{col_key}::{pib}::{period}"

    # поточне значення з DF → у чистий bool
    raw = df.at[row_idx, col_key] if col_key in df.columns else 0
    try:
        base_bool = bool(int(raw)) if pd.notna(raw) else False
    except Exception:
        base_bool = False  # на всяк випадок

    checked = st.checkbox(label, value=base_bool, key=st_key)
    df.at[row_idx, col_key] = 1 if checked else 0
    return checked

def ui_bool_form(col_key: str, label: str) -> bool:
    """
    Чекбокс для форм введення (працює з st.session_state.np_form_data).
    - Глобально-унікальний ключ на основі (col_key, ПІБ, період).
    - Жорстко приводить збережене значення до bool, зберігає 0/1 у np_form_data.
    """
    import math

    form_data = st.session_state.np_form_data

    pib = str(form_data.get(c.COL_PIB, st.session_state.get("selected_pib", "")))
    period = str(form_data.get(c.NP_COL_PERIOD, st.session_state.get("selected_period", "")))
    st_key = f"chk::{col_key}::{pib}::{period}"

    raw = form_data.get(col_key, 0)

    # -> чистий bool
    base = False
    try:
        if raw is None:
            base = False
        elif isinstance(raw, bool):
            base = raw
        elif isinstance(raw, (int, float)):
            base = (not (isinstance(raw, float) and math.isnan(raw))) and (int(raw) != 0)
        else:
            s = str(raw).strip().lower()
            base = s in ("1", "true", "так", "yes", "y", "on")
    except Exception:
        base = False

    checked = st.checkbox(label, value=base, key=st_key)
    form_data[col_key] = 1 if checked else 0
    return checked

def _form_keys_suffix():
    fd = st.session_state.np_form_data
    pib = str(fd.get(c.COL_PIB, st.session_state.get("selected_pib", "")))
    period = str(fd.get(c.NP_COL_PERIOD, st.session_state.get("selected_period", "")))
    return pib, period

def ui_int_form(col_key: str, label: str, min_value: int = 0, step: int = 1) -> int:
    """number_input для цілих у формі"""
    import math
    fd = st.session_state.np_form_data
    pib, period = _form_keys_suffix()
    st_key = f"num::{col_key}::{pib}::{period}"
    raw = fd.get(col_key, 0)
    try:
        val = 0 if raw is None or (isinstance(raw, float) and math.isnan(raw)) else int(raw)
    except Exception:
        val = 0
    out = st.number_input(label, value=val, min_value=min_value, step=step, key=st_key)
    fd[col_key] = int(out)
    return int(out)

def ui_float_form(col_key: str, label: str, min_value: float = 0.0, step: float = 0.1) -> float:
    """number_input для float у формі (напр., індекс Гірша)"""
    import math
    fd = st.session_state.np_form_data
    pib, period = _form_keys_suffix()
    st_key = f"numf::{col_key}::{pib}::{period}"
    raw = fd.get(col_key, 0.0)
    try:
        val = 0.0 if raw is None or (isinstance(raw, float) and math.isnan(raw)) else float(raw)
    except Exception:
        val = 0.0
    out = st.number_input(label, value=val, min_value=min_value, step=step, key=st_key, format="%.2f")
    fd[col_key] = float(out)
    return float(out)

def ui_json_form(col_key: str, label: str, hint: str = "[]", height: int = 120) -> str:
    """text_area для JSON-деталей (статті/доповіді/монографії/редколегії тощо) з легкою валідацією"""
    import json
    fd = st.session_state.np_form_data
    pib, period = _form_keys_suffix()
    st_key = f"json::{col_key}::{pib}::{period}"
    val = fd.get(col_key, "[]")
    if not isinstance(val, str):
        try:
            val = json.dumps(val, ensure_ascii=False)
        except Exception:
            val = "[]"
    txt = st.text_area(label, value=val, key=st_key, height=height, placeholder=hint)
    # м’яка валідація
    try:
        parsed = json.loads((txt or "").strip() or "[]")
        ok = isinstance(parsed, (list, dict))
    except Exception:
        ok = False
    if ok:
        fd[col_key] = txt.strip()
        st.caption("✅ JSON валідний")
    else:
        st.caption("⚠️ Очікується JSON (список або об’єкт). Напр.: [ {\"type\":\"Фахові України\",\"count\":2} ]")
    return txt

def ui_text_form(col_key: str, label: str, placeholder: str = "", max_chars: int = 300) -> str:
    """text_input для форм (рядкові значення), унікальний key = col_key+pib+period"""
    fd = st.session_state.np_form_data
    pib = str(fd.get(c.COL_PIB, st.session_state.get("selected_pib", "")))
    period = str(fd.get(c.NP_COL_PERIOD, st.session_state.get("selected_period", "")))
    st_key = f"txt::{col_key}::{pib}::{period}"
    val = fd.get(col_key, "")
    out = st.text_input(label, value=str(val) if val is not None else "", key=st_key, placeholder=placeholder, max_chars=max_chars)
    fd[col_key] = out.strip()
    return fd[col_key]

def humanize_bools(df: pd.DataFrame) -> pd.DataFrame:
    """Замінює boolean-ish значення на 'Так'/'Ні' лише в тих стовпцях, де це справді булі."""
    df_copy = df.copy()

    def is_booleanish(series: pd.Series) -> bool:
        # приводимо все до нижнього регістру рядком і перевіряємо унікальні значення
        vals = series.dropna().astype(str).str.strip().str.lower().unique()
        # порожній стовпець не чіпаємо
        if len(vals) == 0:
            return False
        # булевий тип одразу ОК
        if series.dtype == bool:
            return True
        # тільки якщо всі значення з набору true/false/1/0
        return set(vals).issubset({"true", "false", "1", "0"})

    def map_boolish(x):
        if isinstance(x, bool):
            return "Так" if x else "Ні"
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return x
        s = str(x).strip().lower()
        if s in ("true", "1"):
            return "Так"
        if s in ("false", "0"):
            return "Ні"
        return x

    for col in df_copy.columns:
        if is_booleanish(df_copy[col]):
            df_copy[col] = df_copy[col].map(map_boolish)

    return df_copy

# --- CSS СТИЛІЗАЦІЯ ЗА БРЕНДБУКОМ ЗСУ ---

load_css()

# --- КІНЕЦЬ БЛОКУ СТИЛІВ ---

# --- Ініціалізація ---
if 'np_structure' not in st.session_state:
    st.session_state.np_structure = dm.load_np_structure()
if 'np_ratings' not in st.session_state:
    st.session_state.np_ratings = dm.initialize_np_ratings_df(st.session_state.np_structure)

# Ініціалізація стану входу
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Ініціалізація стану форми
if 'current_np_pib' not in st.session_state:
    st.session_state.current_np_pib = None
if 'np_form_data' not in st.session_state:
    st.session_state.np_form_data = {}
# Ініціалізація для JSON полів
if 'np_ntr_articles_list' not in st.session_state: st.session_state.np_ntr_articles_list = []
if 'np_ntr_reports_list' not in st.session_state: st.session_state.np_ntr_reports_list = []
if 'np_ntr_mono_solo_list' not in st.session_state: st.session_state.np_ntr_mono_solo_list = []
if 'np_ntr_mono_team_list' not in st.session_state: st.session_state.np_ntr_mono_team_list = []
if 'np_ntr_review_articles_list' not in st.session_state: st.session_state.np_ntr_review_articles_list = []
if 'np_or_conferences_list' not in st.session_state: st.session_state.np_or_conferences_list = []
if 'np_or_olympiads_list' not in st.session_state: st.session_state.np_or_olympiads_list = []
if 'np_or_editorial_list' not in st.session_state: st.session_state.np_or_editorial_list = []


# --- Функції завантаження та оновлення даних ---
def get_current_np_data_row(pib):
    """Отримує поточний рядок даних для НП та ініціалізує session_state для форми."""
    if pib and not st.session_state.np_ratings.empty and pib in st.session_state.np_ratings[c.COL_PIB].values:
        np_data_row = st.session_state.np_ratings[st.session_state.np_ratings[c.COL_PIB] == pib].iloc[0].copy()
        st.session_state.np_form_data = np_data_row.to_dict()
        # Парсинг JSON полів
        st.session_state.np_ntr_articles_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_NTR_STATTI_DETAILS_JSON, '[]'))
        st.session_state.np_ntr_reports_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_NTR_DOPOVIDI_DETAILS_JSON, '[]'))
        st.session_state.np_ntr_mono_solo_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_NTR_MONO_ODNOOSIBNA_DETAILS_JSON, '[]'))
        st.session_state.np_ntr_mono_team_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_NTR_MONO_KOLEKTYVNA_DETAILS_JSON, '[]'))
        st.session_state.np_ntr_review_articles_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_NTR_RECENZ_STATTI_DETAILS_JSON, '[]'))
        st.session_state.np_or_conferences_list = calc.parse_json_details(
            st.session_state.np_form_data.get(c.NP_COL_OR_KONFERENTSII_DETAILS_JSON, '[]'))
    elif pib != st.session_state.current_np_pib:
        st.session_state.np_form_data = {}
        st.session_state.np_ntr_articles_list = []
        st.session_state.np_ntr_reports_list = []
        st.session_state.np_ntr_mono_solo_list = []
        st.session_state.np_ntr_mono_team_list = []
        st.session_state.np_ntr_review_articles_list = []
        st.session_state.np_or_conferences_list = []
    st.session_state.current_np_pib = pib


# --- Функція візуалізації ---
def display_scores_summary(pib):
    """Відображає діаграму з поточними балами та порівнянням для обраного НП."""
    if pib and not st.session_state.np_ratings.empty and pib in st.session_state.np_ratings[c.COL_PIB].values:
        # Отримуємо дані для поточного користувача
        scores = st.session_state.np_ratings[st.session_state.np_ratings[c.COL_PIB] == pib].iloc[0]
        chart_data = {
            "Постійні показники (ПП)": scores.get(c.NP_COL_PP_TOTAL, 0),
            "Наукова діяльність (НТР)": scores.get(c.NP_COL_NTR_TOTAL, 0),
            "Організаційна діяльність (ОР)": scores.get(c.NP_COL_OR_TOTAL, 0),
        }
        total_score = scores.get(c.NP_COL_IB_TOTAL, 0)

        # Розрахунок середніх балів по всім НП для порівняння
        avg_scores = st.session_state.np_ratings[[c.NP_COL_PP_TOTAL, c.NP_COL_NTR_TOTAL, c.NP_COL_OR_TOTAL]].mean().to_dict()

        # Поєднуємо дані в DataFrame
        df_chart = pd.DataFrame({
            "Категорія": list(chart_data.keys()),
            "Ваші бали": list(chart_data.values()),
            "Середні бали": [avg_scores.get(col, 0) for col in chart_data.keys()]
        })

        # Візуалізація з Altair
        base = alt.Chart(df_chart).encode(
            x=alt.X("Категорія:N", axis=alt.Axis(labelAngle=0)),
            tooltip=["Категорія", alt.Tooltip("Ваші бали:Q", format=".2f"), alt.Tooltip("Середні бали:Q", format=".2f")]
        ).properties(height=300, width=300)

        bars = base.mark_bar(opacity=0.7).encode(
            y=alt.Y("Ваші бали:Q", title="Бали"),
            color=alt.value("#FFD700")  # Золотий колір
        )

        avg_line = base.mark_rule(color="#808080").encode(
            y="Середні бали:Q",
            size=alt.value(2)
        )

        chart = (bars + avg_line).interactive()

        st.subheader(f"Поточний рейтинг: {total_score:.2f} балів")
        st.altair_chart(chart, use_container_width=True)

        # Додатковий інсайт
        st.text(f"Порівняння: Ви перевищуєте середній бал у {sum(1 for v, a in zip(chart_data.values(), avg_scores.values()) if v > a)} із 3 категорій.")


# --- UI Функції для форм ---
def render_np_pp_form():
    with st.expander("Додаток 1.2: Постійні показники (ПП)", expanded=False):
        # --- Пара 1 & 2 ---
        col1, col2 = st.columns(2, border=True)

        with col1:
            st.subheader("🎓 1. Науковий ступінь")
            st.markdown("---")

            st.session_state.np_form_data[c.NP_COL_PP_KVAL_KANDYDAT] = ui_bool_form(
                c.NP_COL_PP_KVAL_KANDYDAT,
                "Диплом кандидата наук (доктора філософії)"
            )

            st.session_state.np_form_data[c.NP_COL_PP_KVAL_PHD_ABROAD] = ui_bool_form(
                c.NP_COL_PP_KVAL_PHD_ABROAD,
                "Закордонний диплом PhD"
            )

            st.session_state.np_form_data[c.NP_COL_PP_KVAL_DOCTOR] = ui_bool_form(
                c.NP_COL_PP_KVAL_DOCTOR,
                "Диплом доктора наук"
            )


        with col2:
            st.subheader("👨🏽‍🎓 2. Вчене звання")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_VZVAN_STARSH_DOSL] = ui_bool_form(
                c.NP_COL_PP_VZVAN_STARSH_DOSL,
                "Старший дослідник (СНС)",
                )
            st.session_state.np_form_data[c.NP_COL_PP_VZVAN_DOTSENT] = ui_bool_form(
                c.NP_COL_PP_VZVAN_DOTSENT,
                "Доцент",
                )
            st.session_state.np_form_data[c.NP_COL_PP_VZVAN_PROFESOR] = ui_bool_form(
                c.NP_COL_PP_VZVAN_PROFESOR,
                "Професор",
                )
        st.markdown("---")

        # --- Пара 3 & 4 ---

        col1, col2 = st.columns(2, border=True)
        with col1:

            st.subheader("🏅 3. Державна премія")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_DERZH_PREMIYA] = ui_bool_form(
                c.NP_COL_PP_DERZH_PREMIYA,
                "Лауреат Державної премії"
                )

        with col2:

            st.subheader("🎖️ 4. Почесне звання")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_POCHESNE_ZVANNYA] = ui_bool_form(
                c.NP_COL_PP_POCHESNE_ZVANNYA,
                "Наявність почесного звання (Заслужений діяч, винахідник, юрист тощо)")

        st.markdown("---")

        # --- Пара 5 & 6 ---

        col1, col2 = st.columns(2, border=True)
        with col1:

            st.subheader("🏆 5. Нагороди")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_NAGORODY_VRU_KMU] = ui_bool_form(
                c.NP_COL_PP_NAGORODY_VRU_KMU, "Грамота ВРУ / КМУ")
            st.session_state.np_form_data[c.NP_COL_PP_NAGORODY_ORDER] = ui_bool_form(
                c.NP_COL_PP_NAGORODY_ORDER, "Орден (державна нагорода)")
            st.session_state.np_form_data[c.NP_COL_PP_NAGORODY_VIDOVI] = ui_bool_form(
                c.NP_COL_PP_NAGORODY_VIDOVI, "Заохочення від командувачів видів, родів військ (сил)")
            st.session_state.np_form_data[c.NP_COL_PP_NAGORODY_VIKNU] = ui_bool_form(
                c.NP_COL_PP_NAGORODY_VIKNU, "Заохочення від начальника Військового інституту")

        with col2:

            st.subheader("🏛️ 6. Членство в академіях наук")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_NAN_CHLEN] = ui_bool_form(
                c.NP_COL_PP_NAN_CHLEN, "Дійсний член НАНУ")
            st.session_state.np_form_data[c.NP_COL_PP_NAN_CHLEN_KOR] = ui_bool_form(
                c.NP_COL_PP_NAN_CHLEN_KOR, "Член-кореспондент НАНУ")
            st.session_state.np_form_data[c.NP_COL_PP_NAN_HALUZEVI_AKADEMIYI] = ui_bool_form(c.NP_COL_PP_NAN_HALUZEVI_AKADEMIYI,
                "Член галузевої академії наук")
            st.session_state.np_form_data[c.NP_COL_PP_NAN_HROMADSKI] = ui_bool_form(c.NP_COL_PP_NAN_HROMADSKI,
                "Член наукової громадської організації")
        st.markdown("---")

        # --- Пара 7 & 8 ---

        col1, col2 = st.columns(2, border=True)
        with col1:

            st.subheader("🛡️ 7. Статус УБД")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_STATUS_UBD] = ui_bool_form(c.NP_COL_PP_STATUS_UBD,
                "Наявність статусу учасника бойових дій")

        with col2:

            st.subheader("🌐 8. Участь у міжнародних військових навчаннях НАТО")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_NAVCHANNYA_NATO_KILKIST] = ui_int_form(
                c.NP_COL_PP_NAVCHANNYA_NATO_KILKIST,
                "Кількість навчань",
                min_value=0,
                step=1
            )
        st.markdown("---")

        # --- Пара 9 & 10 ---

        col1, col2 = st.columns(2, border=True)
        with col1:

            st.subheader("👨‍💻 9. Член воєнно-наукової групи на ОКП бригади")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_PP_VNG_OKP_DNIV] = ui_int_form(
                c.NP_COL_PP_VNG_OKP_DNIV,
                "Кількість днів у складі ВНГ",
                min_value=0, step=1
            )


        with col2:

            st.subheader("🗣️ 10. Рівень володіння іноземною мовою")
            st.markdown("---")
            lang_levels = list(c.NP_POINTS_PP_INOZEMNA_MOVA.keys())
            current_level = st.session_state.np_form_data.get(
                c.NP_COL_PP_INOZEMNA_MOVA_RIVEN,
                lang_levels[0] if lang_levels else "Немає"
            )
            st.session_state.np_form_data[c.NP_COL_PP_INOZEMNA_MOVA_RIVEN] = st.selectbox(
                "Рівень СМП (CEFR)",
                options=lang_levels,
                index=lang_levels.index(current_level) if current_level in lang_levels else 0
            )

def render_np_ntr_form():
    with st.expander("Додаток 1.3: Наукова діяльність (НТР)", expanded=False):

        # --- Пара 1 & 2 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🎓 1. Завершення та захист")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_ZAHYST_DOCTORSKA] = ui_bool_form(
                c.NP_COL_NTR_ZAHYST_DOCTORSKA, "Захист докторської дисертації"
            )
            st.session_state.np_form_data[c.NP_COL_NTR_ZAHYST_PHD] = ui_bool_form(
                c.NP_COL_NTR_ZAHYST_PHD, "Захист дисертації доктора філософії"
            )

        with col2:
            st.subheader("🧑‍🏫 2. Наукове консультування")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_NAUK_KONSULT_ADYUNKT_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NAUK_KONSULT_ADYUNKT_KILKIST, "К-сть ад’юнктів (аспірантів)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_NAUK_KONSULT_DOCTORANT_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NAUK_KONSULT_DOCTORANT_KILKIST, "К-сть докторантів", min_value=0, step=1
            )

        st.markdown("---")

        # --- Пара 3 & 4 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🧐 3. Опонування дисертацій")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_OPONUVANNYA_DOCTOR_NAUK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_OPONUVANNYA_DOCTOR_NAUK_KILKIST, "К-сть дисертацій доктора наук", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_OPONUVANNYA_PHD_KILKIST] = ui_int_form(
                c.NP_COL_NTR_OPONUVANNYA_PHD_KILKIST, "К-сть дисертацій доктора філософії", min_value=0, step=1
            )

        with col2:
            st.subheader("✍️ 4. Рецензування дисертацій")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_RECENZ_DYSERT_DOCTOR_NAUK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_RECENZ_DYSERT_DOCTOR_NAUK_KILKIST, "К-сть рецензій на дис. доктора наук",
                min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_RECENZ_DYSERT_PHD_KILKIST] = ui_int_form(
                c.NP_COL_NTR_RECENZ_DYSERT_PHD_KILKIST, "К-сть рецензій на дис. PhD", min_value=0, step=1
            )

        st.markdown("---")

        # --- Пара 5 & 6 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("✅ 5. Підготовка акту впровадження")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_AKTU_VPROVADZH_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_AKTU_VPROVADZH_KILKIST, "Кількість актів (голова комісії)", min_value=0, step=1
            )

        with col2:
            st.subheader("🔬 6. Виконання НДР")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_NDR_DERZH_KERIVNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NDR_DERZH_KERIVNYK_KILKIST, "НДР держ. (керівник)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_NDR_DERZH_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NDR_DERZH_VYKONAVETS_KILKIST, "НДР держ. (виконавець)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_NDR_MIZHNAR_KERIVNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NDR_MIZHNAR_KERIVNYK_KILKIST, "НДР міжнар. (керівник)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_NDR_MIZHNAR_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_NDR_MIZHNAR_VYKONAVETS_KILKIST, "НДР міжнар. (виконавець)", min_value=0, step=1
            )

        st.markdown("---")

        # --- Пара 7 & 8 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📝 7. Виконання ОЗ / Розробка стандарту")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_OZ_VIDPOV_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_OZ_VIDPOV_VYKONAVETS_KILKIST, "ОЗ (відповідальний виконавець)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_OZ_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_OZ_VYKONAVETS_KILKIST, "ОЗ (виконавець)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_STANDART_KERIVNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_STANDART_KERIVNYK_KILKIST, "Стандарт (керівник)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_STANDART_VIDPOV_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_STANDART_VIDPOV_VYKONAVETS_KILKIST, "Стандарт (відповідальний)", min_value=0, step=1
            )
            st.session_state.np_form_data[c.NP_COL_NTR_STANDART_VYKONAVETS_KILKIST] = ui_int_form(
                c.NP_COL_NTR_STANDART_VYKONAVETS_KILKIST, "Стандарт (виконавець)", min_value=0, step=1
            )
        with col2:
            st.subheader("📄 8. Підготовка та видання наукової статті")
            st.markdown("---")
            NEUTRAL_LABEL = "— не обрано —"
            article_type_options = [NEUTRAL_LABEL, "Scopus Q1", "Scopus Q2", "Scopus Q3", "Scopus Q4",
                                    "Інші міжнародні бази (закордонні)", "Інші міжнародні бази (вітчизняні)",
                                    "Закордонні (неіндексовані)", "Фахові України", "Нефахові України"]

            cols = st.columns([3, 1])
            new_article_type = cols[0].selectbox("Тип статті", options=article_type_options,
                                                 key="np_new_article_type")
            new_article_count = cols[1].number_input("Кількість", min_value=1, step=1,
                                                     key="np_new_article_count")
            if st.button("Додати статті", key="np_add_article"):
                if new_article_type != NEUTRAL_LABEL:
                    st.session_state.np_ntr_articles_list.append(
                        {"type": new_article_type, "count": new_article_count})
                    st.rerun()
                else:
                    st.warning("Оберіть тип статті перш ніж дотати статтю")
            if st.session_state.np_ntr_articles_list:
                st.write("Додані статті:")
                for i, article in enumerate(st.session_state.np_ntr_articles_list):
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"**Тип:** {article['type']}")
                    cols[1].write(f"**К-сть:** {article['count']}")
                    if cols[2].button("🗑️", key=f"np_del_article_{i}"):
                        st.session_state.np_ntr_articles_list.pop(i)
                        st.rerun()

        st.markdown("---")
        # --- Пара 9 & 10 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🎤 9. Доповіді на наукових заходах")
            st.markdown("---")
            NEUTRAL_LABEL = "— не обрано —"
            report_type_options = [NEUTRAL_LABEL, "Тези міжнародних конференцій", "Тези всеукраїнських конференцій",
                                   "Тези міжвузівських (вузівських) конференцій"]

            cols_rep = st.columns([3, 1])
            new_report_type = cols_rep[0].selectbox("Тип доповіді", options=report_type_options,
                                                    key="np_new_report_type")
            new_report_count = cols_rep[1].number_input("Кількість", min_value=1, step=1,
                                                        key="np_new_report_count")
            if st.button("Додати доповідь", key="np_add_report"):
                if new_report_type != NEUTRAL_LABEL:
                    st.session_state.np_ntr_reports_list.append(
                        {"type": new_report_type, "count": new_report_count})
                    st.rerun()
                else:
                    st.warning("Оберіть тип доповіді перш ніж додати доповідь")
            if st.session_state.np_ntr_reports_list:
                st.write("Додані доповіді:")
                for i, report in enumerate(st.session_state.np_ntr_reports_list):
                    cols_rep_disp = st.columns([3, 1, 1])
                    cols_rep_disp[0].write(f"**Тип:** {report['type']}")
                    cols_rep_disp[1].write(f"**К-сть:** {report['count']}")
                    if cols_rep_disp[2].button("🗑️", key=f"np_del_report_{i}"):
                        st.session_state.np_ntr_reports_list.pop(i)
                        st.rerun()
        with col2:
            st.subheader("💡 10. Отримання патенту / моделі")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PATENT_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PATENT_KILKIST, "Кількість патентів", min_value=0, step=1)

            st.session_state.np_form_data[c.NP_COL_NTR_KORYSNA_MODEL_KILKIST] = ui_int_form(c.NP_COL_NTR_KORYSNA_MODEL_KILKIST,
                "Кількість корисних моделей", min_value=0, step=1)

        st.markdown("---")
        # --- Пара 11 & 12 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("©️ 11. Авторське право")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_AVTORSKE_PRAVO_KILKIST] = ui_int_form(
                c.NP_COL_NTR_AVTORSKE_PRAVO_KILKIST,
                "Кількість свідоцтв", min_value=0, step=1)
        with col2:
            st.subheader("📖 12. Видання одноосібної монографії")
            st.markdown("---")
            NEUTRAL_LABEL = "— не обрано —"
            mono_solo_type_options = [NEUTRAL_LABEL, "в іноземному видавництві", "в українському видавництві"]
            cols_mono_s = st.columns([3, 1])
            new_mono_solo_type = cols_mono_s[0].selectbox("Тип видавництва", options=mono_solo_type_options,
                                                          key="np_new_mono_solo_type")
            new_mono_solo_sheets = cols_mono_s[1].number_input("К-сть авторських аркушів", min_value=0.1,
                                                               step=0.1, format="%.1f",
                                                               key="np_new_mono_solo_sheets")
            if st.button("Додати монографію", key="np_add_mono_solo"):
                if new_mono_solo_type != NEUTRAL_LABEL:
                    st.session_state.np_ntr_mono_solo_list.append(
                        {"type": new_mono_solo_type, "sheets": new_mono_solo_sheets})
                    st.rerun()
                else:
                    st.warning("Оберіть тип видавництва перш ніж додавати монографію.")
            if st.session_state.np_ntr_mono_solo_list:
                st.write("Додані монографії:")
                for i, mono in enumerate(st.session_state.np_ntr_mono_solo_list):
                    cols_mono_s_disp = st.columns([3, 1, 1])
                    cols_mono_s_disp[0].write(f"**Тип:** {mono['type']}")
                    cols_mono_s_disp[1].write(f"**Аркушів:** {mono['sheets']}")
                    if cols_mono_s_disp[2].button("🗑️", key=f"np_del_mono_solo_{i}"):
                        st.session_state.np_ntr_mono_solo_list.pop(i)
                        st.rerun()

        st.markdown("---")
        # --- Пара 13 & 14 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📚 13. Розділ у колективній монографії")
            st.markdown("---")

            NEUTRAL_LABEL = "— не обрано —"
            mono_team_type_options = [
                NEUTRAL_LABEL,
                "в іноземному видавництві",
                "в українському видавництві",
            ]

            cols_mono_t = st.columns([2, 1, 1])

            new_mono_team_type = cols_mono_t[0].selectbox(
                "Тип видавництва", options=mono_team_type_options, index=0,
                key="np_new_mono_team_type",
            )

            new_mono_team_sheets = cols_mono_t[1].number_input(
                "К-сть авт. аркушів", min_value=0.1, step=0.1, format="%.1f",
                key="np_new_mono_team_sheets",
            )

            new_mono_team_authors = cols_mono_t[2].number_input(
                "К-сть співавторів", min_value=1, step=1,
                key="np_new_mono_team_authors",
            )

            if st.button("Додати розділ", key="np_add_mono_team"):
                if new_mono_team_type != NEUTRAL_LABEL:
                    st.session_state.np_ntr_mono_team_list.append(
                        {
                            "type": new_mono_team_type,
                            "sheets": new_mono_team_sheets,
                            "authors": new_mono_team_authors,
                        }
                    )
                    st.rerun()
                else:
                    st.warning("Оберіть тип видавництва перш ніж додавати розділ.")

            if st.session_state.np_ntr_mono_team_list:
                st.write("Додані розділи:")
                for i, mono in enumerate(st.session_state.np_ntr_mono_team_list):
                    cols_mono_t_disp = st.columns([2, 1, 1, 1])
                    cols_mono_t_disp[0].write(f"**Тип:** {mono['type']}")
                    cols_mono_t_disp[1].write(f"**Аркушів:** {mono['sheets']}")
                    cols_mono_t_disp[2].write(f"**Співавторів:** {mono['authors']}")
                    if cols_mono_t_disp[3].button("🗑️", key=f"np_del_mono_team_{i}"):
                        st.session_state.np_ntr_mono_team_list.pop(i)
                        st.rerun()

        with col2:
            st.subheader("🔎 14. Рецензування монографії / підручника")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_RECENZ_MONO_KILKIST] = ui_int_form(
                c.NP_COL_NTR_RECENZ_MONO_KILKIST,
                "Кількість рецензій", min_value=0, step=1)

        st.markdown("---")

        # --- Пара 15 & 16 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🖋️ 15. Рецензування статті")
            st.markdown("---")
            NEUTRAL_LABEL = "— не обрано —"
            review_type_options = [NEUTRAL_LABEL, "Scopus, WoS, фахове видання категорії А",
                                   "фахове видання України категорії Б",
                                   "закордонне видання, індексоване в інших базах"]

            cols_rev = st.columns([3, 1])
            new_review_type = cols_rev[0].selectbox("Тип видання", options=review_type_options,
                                                    key="np_new_review_type")
            new_review_count = cols_rev[1].number_input("Кількість", min_value=1, step=1,
                                                        key="np_new_review_count")
            if st.button("Додати рецензію", key="np_add_review"):
                if new_review_type != NEUTRAL_LABEL:
                    st.session_state.np_ntr_review_articles_list.append(
                        {"type": new_review_type, "count": new_review_count})
                    st.rerun()
                else:
                    st.warning("Оберіть тип видання перщ ніж додати рецензію")
            if st.session_state.np_ntr_review_articles_list:
                st.write("Додані рецензії:")
                for i, review in enumerate(st.session_state.np_ntr_review_articles_list):
                    cols_rev_disp = st.columns([3, 1, 1])
                    cols_rev_disp[0].write(f"**Тип:** {review['type']}")
                    cols_rev_disp[1].write(f"**К-сть:** {review['count']}")
                    if cols_rev_disp[2].button("🗑️", key=f"np_del_review_{i}"):
                        st.session_state.np_ntr_review_articles_list.pop(i)
                        st.rerun()
        with col2:
            st.subheader("👨‍🏫 16. Керівництво науковою роботою курсантів")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_KERIVNYTSTVO_NDR_KURSANTIV_KILKIST] = ui_int_form(
                c.NP_COL_NTR_KERIVNYTSTVO_NDR_KURSANTIV_KILKIST,
                "Кількість документів (статті, тези, роботи на конкурс тощо)", min_value=0, step=1)

        st.markdown("---")
        # --- Пара 17 & 18 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🏆 17. Підготовка переможців конкурсів")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_PEREMOZH_VSEUKR_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_PEREMOZH_VSEUKR_KILKIST,
                "К-сть переможців Всеукраїнського конкурсу", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_PEREMOZH_VNUTRISH_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_PEREMOZH_VNUTRISH_KILKIST,
                "К-сть переможців внутрішнього конкурсу", min_value=0, step=1)
        with col2:
            st.subheader("🏅 18. Підготовка переможців олімпіад")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_PEREMOZH_OLIMPIADA_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_PEREMOZH_OLIMPIADA_KILKIST,
                "К-сть переможців міжнародних/Всеукраїнських олімпіад", min_value=0, step=1)

        st.markdown("---")
        # --- Пара 19 & 20 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🥇 19. Підготовка команди-переможниці")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_KOMANDY_PEREMOZH_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_KOMANDY_PEREMOZH_KILKIST,
                "К-сть команд-переможниць змагань", min_value=0, step=1)
        with col2:
            st.subheader("🎖️ 20. Підготовка переможців обласних конкурсів")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_PIDHOT_PEREMOZH_OBL_AKADEM_KILKIST] = ui_int_form(
                c.NP_COL_NTR_PIDHOT_PEREMOZH_OBL_AKADEM_KILKIST,
                "К-сть переможців обласного, академічного конкурсу", min_value=0, step=1)

        st.markdown("---")
        # --- Пара 21 & 22 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📔 21. Видавнича діяльність")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_PIDRUCHNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_VYDANNYA_PIDRUCHNYK_KILKIST,
                "Підручники", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_PIDRUCHNYK_ID] = ui_text_form(
                c.NP_COL_NTR_VYDANNYA_PIDRUCHNYK_ID, "Назва підручника"
            )
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_POSIBNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_VYDANNYA_POSIBNYK_KILKIST,
                "Навчальні посібники", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_POSIBNYK_ID] = ui_text_form(
                c.NP_COL_NTR_VYDANNYA_POSIBNYK_ID, "Назва посібника"
            )
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_DOVIDNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_VYDANNYA_DOVIDNYK_KILKIST,
                "Довідники", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_DOVIDNYK_ID] = ui_text_form(
                c.NP_COL_NTR_VYDANNYA_DOVIDNYK_ID, "Назва довідника"
            )
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_ZBIRNYK_KILKIST] = ui_int_form(
                c.NP_COL_NTR_VYDANNYA_ZBIRNYK_KILKIST, "Збірники", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_VYDANNYA_ZBIRNYK_ID] = ui_text_form(
                c.NP_COL_NTR_VYDANNYA_ZBIRNYK_ID, "Назва збірника"
            )
        with col2:
            st.subheader("📈 22. Індекс Гірша (Scopus/WoS)")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_HIRSCH_INDEX_VALUE] = ui_int_form(
                c.NP_COL_NTR_HIRSCH_INDEX_VALUE,
                "Значення індексу 'n'",
                min_value=0, step=1)

            # Нове поле для ID Гірша
            st.session_state.np_form_data[c.NP_COL_NTR_HIRSCH_PROFILE_ID] = ui_text_form(
                c.NP_COL_NTR_HIRSCH_PROFILE_ID, "ID профілю (Scopus / WoS)")

        st.markdown("---")

        # --- Пара 23 & 24 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🗣️ 23. Спікер за запрошенням")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_SPIKER_KILKIST] = ui_int_form(
                c.NP_COL_NTR_SPIKER_KILKIST, "Кількість заходів",
                min_value=0, step=1)
        with col2:
            # --- Блок 24-25, окремо, оскільки він один ---
            st.subheader("🏛️ 24-25. Робота в радах")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_NTR_RAZOVI_RADY_GOLOVA_KILKIST] = ui_int_form(
                c.NP_COL_NTR_RAZOVI_RADY_GOLOVA_KILKIST,
                "Разові ради (голова)", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_RAZOVI_RADY_CHLEN_KILKIST] = ui_int_form(
                c.NP_COL_NTR_RAZOVI_RADY_CHLEN_KILKIST,
                "Разові ради (член)", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_SPEC_RADY_KAND_KILKIST] = ui_int_form(
                c.NP_COL_NTR_SPEC_RADY_KAND_KILKIST,
                "Спец. ради (канд.)", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_NTR_SPEC_RADY_DOCTOR_KILKIST] = ui_int_form(
                c.NP_COL_NTR_SPEC_RADY_DOCTOR_KILKIST,
                "Спец. ради (докт.)", min_value=0, step=1)


def render_np_or_form():
    with st.expander("Додаток 1.4: Організаційна діяльність (ОР)", expanded=False):

        # --- Пара 1 & 2 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🧭 1. Військово-професійна орієнтація")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_VIYSK_PROF_ORIENT_DNIV] = ui_int_form(c.NP_COL_OR_VIYSK_PROF_ORIENT_DNIV,
                "Кількість днів відряджень",
                min_value=0, step=1)
        with col2:
            st.subheader("🤝 2. Робота в комісіях МОН")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_KOMISII_MON_ZAHODIV] = ui_int_form(c.NP_COL_OR_KOMISII_MON_ZAHODIV,
                "Кількість заходів",
                min_value=0, step=1)

        st.markdown("---")

        # --- Пара 3 & 4 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📚 3. Діяльність у науково-методичних радах")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_DIYALNIST_RADY_VIKNU_ZASIDAN] = ui_int_form(
                c.NP_COL_OR_DIYALNIST_RADY_VIKNU_ZASIDAN,
                "Кількість засідань (не більше 30 балів)",
                min_value=0, step=1)
        with col2:
            st.subheader("🏛️ 4. Робота у складі вченої ради")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_VCHENA_RADA_CHLEN_ZASIDAN] = ui_int_form(
                c.NP_COL_OR_VCHENA_RADA_CHLEN_ZASIDAN,
                "К-сть засідань (член ради)",
                min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_OR_VCHENA_RADA_SEKRETAR_ZASIDAN] = ui_int_form(
                c.NP_COL_OR_VCHENA_RADA_SEKRETAR_ZASIDAN,
                "К-сть засідань (секретар)",
                min_value=0, step=1)

        st.markdown("---")

        # --- Пара 5 & 6 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📋 5. Робота в експертних, конкурсних комісіях")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_EKSPERT_KOMISII_ZASIDAN] = ui_int_form(
                c.NP_COL_OR_EKSPERT_KOMISII_ZASIDAN,
                "Кількість засідань (не більше 30 балів)",
                min_value=0, step=1)

        with col2:
            st.subheader("🌐 6. Організація та проведення конференцій")
            st.markdown("---")

            NEUTRAL_LABEL = "— не обрано —"
            conf_role_options = [
                NEUTRAL_LABEL,
                "голова оргкомітету",
                "голова секції",
                "член оргкомітету, секретар секції"
            ]

            cols = st.columns([3, 1])
            new_conf_role = cols[0].selectbox(
                "Роль у конференції", options=conf_role_options, index=0, key="np_new_conf_role"
            )
            new_conf_count = cols[1].number_input(
                "Кількість", min_value=1, step=1, key="np_new_conf_count"
            )

            if st.button("Додати участь у конференції", key="np_add_conf"):
                if new_conf_role != NEUTRAL_LABEL:
                    st.session_state.np_or_conferences_list.append(
                        {"role": new_conf_role, "count": new_conf_count}
                    )
                    st.rerun()
                else:
                    st.warning("Будь ласка, оберіть роль перед додаванням.")

            if st.session_state.np_or_conferences_list:
                st.write("Додана участь у конференціях:")
                for i, conf in enumerate(st.session_state.np_or_conferences_list):
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"**Роль:** {conf['role']}")
                    cols[1].write(f"**К-сть:** {conf['count']}")
                    if cols[2].button("🗑️", key=f"np_del_conf_{i}"):
                        st.session_state.np_or_conferences_list.pop(i)
                        st.rerun()

        st.markdown("---")
        # --- Пара 7 & 8 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🏆 7. Організація та проведення олімпіад")
            st.markdown("---")
            olymp_role_options = ["— не обрано —",
                                  "всеукраїнських та міжнародних",
                                  "Військового інституту (факультету)",
                                  "експерти з оцінювання робіт"]

            cols = st.columns([3, 1])
            new_olymp_role = cols[0].selectbox("Рівень олімпіади/конкурсу", options=olymp_role_options,
                                               key="np_new_olymp_role",
                                               label_visibility="collapsed")
            new_olymp_count = cols[1].number_input("Кількість", min_value=1, step=1, key="np_new_olymp_count",
                                                   label_visibility="collapsed")

            if st.button("Додати участь в олімпіаді", key="np_add_olymp"):
                if new_olymp_role != "— не обрано —":  # ✅ захист від додавання пустого
                    st.session_state.np_or_olympiads_list.append(
                        {"role": new_olymp_role, "count": new_olymp_count})
                    st.rerun()
                else:
                    st.warning("Будь ласка, оберіть конкретний рівень олімпіади.")

            if st.session_state.np_or_olympiads_list:
                st.write("Додана участь в олімпіадах/конкурсах:")
                for i, olymp in enumerate(st.session_state.np_or_olympiads_list):
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"**Рівень:** {olymp['role']}")
                    cols[1].write(f"**К-сть:** {olymp['count']}")
                    if cols[2].button("🗑️", key=f"np_del_olymp_{i}"):
                        st.session_state.np_or_olympiads_list.pop(i)
                        st.rerun()

        with col2:
            st.subheader("🖋️ 8. Робота у редакційних колегіях")
            st.markdown("---")
            NEUTRAL_LABEL = "— не обрано —"
            editorial_role_options = [
                NEUTRAL_LABEL,
                "виданнях, що індексуються в Scopus та WoS",
                "в закордонних виданнях, індексованих наукометричними базами",
                "українських фахових виданнях",
            ]

            cols = st.columns([3, 1])

            new_editorial_role = cols[0].selectbox(
                "Тип видання", options=editorial_role_options,
                index=0,  # нейтральний варіант за замовчуванням
                key="np_new_editorial_role", label_visibility="collapsed")

            new_editorial_count = cols[1].number_input(
                "Кількість", min_value=1, step=1, key="np_new_editorial_count", label_visibility="collapsed")

            if st.button("Додати участь у редколегії", key="np_add_editorial"):
                if new_editorial_role != NEUTRAL_LABEL:
                    st.session_state.np_or_editorial_list.append(
                        {"role": new_editorial_role, "count": new_editorial_count}
                    )
                    st.rerun()
                else:
                    st.warning("Оберіть тип видання перш ніж додавати запис.")

            if st.session_state.np_or_editorial_list:
                st.write("Додана участь у редколегіях:")
                for i, editorial in enumerate(st.session_state.np_or_editorial_list):
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"**Тип:** {editorial['role']}")
                    cols[1].write(f"**К-сть:** {editorial['count']}")
                    if cols[2].button("🗑️", key=f"np_del_editorial_{i}"):
                        st.session_state.np_or_editorial_list.pop(i)
                        st.rerun()

        st.markdown("---")

        # --- Пара 9 & 11 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("📰 9. Робота з формування наукових видань")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_FORMUVANNYA_VISNYK_KILKIST] = ui_int_form(
                c.NP_COL_OR_FORMUVANNYA_VISNYK_KILKIST,
                "Вісник КНУ (к-сть видань)", min_value=0, step=1)
            st.session_state.np_form_data[c.NP_COL_OR_FORMUVANNYA_ZBIRNYK_VIKNU_KILKIST] = ui_int_form(
                c.NP_COL_OR_FORMUVANNYA_ZBIRNYK_VIKNU_KILKIST,
                "Збірник праць ВІ (к-сть видань)", min_value=0, step=1)
        with col2:
            st.subheader("📝 11. Виконання оперативних завдань (поза НДР)")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_OZ_INSHI_ARK_NPP] = ui_float_form(c.NP_COL_OR_OZ_INSHI_ARK_NPP,
                "Кількість авторських аркушів", min_value=0.0, step=0.1)

        st.markdown("---")

        # --- Пара 12 & 13 ---
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.subheader("🗣️ 12. Лінгвістичне забезпечення (усний переклад)")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_LINGVO_USNYJ_DNIV] = ui_int_form(c.NP_COL_OR_LINGVO_USNYJ_DNIV,
                "Кількість робочих днів", min_value=0, step=1)
        with col2:
            st.subheader("✍️ 13. Лінгвістичне забезпечення (письмовий переклад)")
            st.markdown("---")
            st.session_state.np_form_data[c.NP_COL_OR_LINGVO_PYSPOVYJ_STORINOK] = ui_int_form(
                c.NP_COL_OR_LINGVO_PYSPOVYJ_STORINOK,
                "Кількість перекладацьких сторінок (порції по 4)", min_value=0, step=1)

        st.markdown("---")

        # --- Пара 14 & ---
        with st.container(border=True):
            st.subheader("📈 14. Проходження курсів підвищення кваліфікації")
            st.markdown("---")

            # === НАЗВИ КУРСІВ ===
            st.caption("Додайте назви курсів (не впливають на бали, зберігаються довідково).")

            # ініціалізація списку у session_state
            if "np_or_courses_list" not in st.session_state:
                st.session_state.np_or_courses_list = []

                # Поля вводу (назва + кількість) в один рядок
            col_course, col_count = st.columns([3, 1])
            with col_course:
                new_course = st.text_input("Назва курсу", key="or_course_title")
            with col_count:
                new_count = ui_int_form(
                    c.NP_COL_OR_PIDV_KVAL_KILKIST,
                    "Кількість сертифікатів",
                    min_value=0,
                    step=1
                )
            st.session_state.np_form_data[c.NP_COL_OR_PIDV_KVAL_KILKIST] = new_count

            cols_btn = st.columns([1, 1, 3])
            if cols_btn[0].button("➕ Додати курс"):
                if new_course.strip():
                    st.session_state.np_or_courses_list.append({
                        "title": new_course.strip(),
                        "count": new_count
                    })
                    st.success("Курс додано.")
                else:
                    st.warning("Вкажіть назву курсу.")

            if cols_btn[1].button("🗑️ Очистити курси"):
                st.session_state.np_or_courses_list = []
                st.info("Список очищено.")

            # Показати існуючі курси
            if st.session_state.np_or_courses_list:
                for i, item in enumerate(st.session_state.np_or_courses_list):
                    cc1, cc2, cc3 = st.columns([6, 2, 1])
                    cc1.write(f"📘 {item.get('title', '')}")
                    cc2.write(f"Кількість: {item.get('count', 0)}")
                    if cc3.button("✖", key=f"del_or_course_{i}"):
                        st.session_state.np_or_courses_list.pop(i)
                        st.rerun()
            else:
                st.info("Курси ще не додані.")


# --- Головна функція для відображення форми ---
def render_np_input_form_main():
    pib = st.session_state.current_np_pib
    if not pib:
        st.warning("Будь ласка, оберіть наукового працівника.")
        return

    st.header(f"Введення даних: {pib}")

    # Візуалізація
    display_scores_summary(pib)
    st.markdown("---")

    render_np_pp_form()
    render_np_ntr_form()
    render_np_or_form()

    st.markdown("---")

    # --- ЗБЕРЕЖЕННЯ ДАНИХ ЗА ОБРАНИЙ РІК ---
    if st.button("💾 Зберегти дані за обраний рік"):
        # 1) Серіалізувати всі JSON-списки у форму
        st.session_state.np_form_data[c.NP_COL_NTR_STATTI_DETAILS_JSON] = json.dumps(
            st.session_state.np_ntr_articles_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_NTR_DOPOVIDI_DETAILS_JSON] = json.dumps(
            st.session_state.np_ntr_reports_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_NTR_MONO_ODNOOSIBNA_DETAILS_JSON] = json.dumps(
            st.session_state.np_ntr_mono_solo_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_NTR_MONO_KOLEKTYVNA_DETAILS_JSON] = json.dumps(
            st.session_state.np_ntr_mono_team_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_NTR_RECENZ_STATTI_DETAILS_JSON] = json.dumps(
            st.session_state.np_ntr_review_articles_list, ensure_ascii=False)

        st.session_state.np_form_data[c.NP_COL_OR_KONFERENTSII_DETAILS_JSON] = json.dumps(
            st.session_state.np_or_conferences_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_OR_OLIMPIADY_DETAILS_JSON] = json.dumps(
            st.session_state.np_or_olympiads_list, ensure_ascii=False)
        st.session_state.np_form_data[c.NP_COL_OR_REDKOLEGIYI_DETAILS_JSON] = json.dumps(
            st.session_state.np_or_editorial_list, ensure_ascii=False)

        # 2) Зібрати form_row і гарантувати ПІБ + Період
        form_row = dict(st.session_state.np_form_data)
        form_row[c.COL_PIB] = form_row.get(c.COL_PIB) or st.session_state.get("selected_pib", "")
        form_row[c.NP_COL_PERIOD] = form_row.get(c.NP_COL_PERIOD) or st.session_state.get("selected_period", "")

        if not form_row[c.COL_PIB] or not form_row[c.NP_COL_PERIOD]:
            st.error("Спочатку оберіть ПІБ і рік (період).")
        else:
            # 3) Порахувати підсумкові бали для цього рядка
            #    (робимо тимчасову Series по всіх колонках, щоб калькулятор мав усе необхідне)
            tmp = pd.Series(form_row)
            tmp = tmp.reindex(st.session_state.np_ratings.columns, fill_value=0)
            updated = calc.calculate_all_scores_for_np(tmp)

            for col in [c.NP_COL_PP_TOTAL, c.NP_COL_NTR_TOTAL, c.NP_COL_OR_TOTAL, c.NP_COL_IB_TOTAL]:
                form_row[col] = updated.get(col, 0)

            # 4) Upsert по (ПІБ, Період)
            st.session_state.np_ratings = dm.upsert_np_row(st.session_state.np_ratings, form_row)

            # 5) Зберегти файл
            dm.save_np_ratings(st.session_state.np_ratings)

            st.success(f"Збережено: {form_row[c.COL_PIB]} — {form_row[c.NP_COL_PERIOD]}")
            st.rerun()


# --- Навігація та логіка розділів ---
# --- Екран входу ---
def login_screen():
    icon_uri = favicon_data_uri("favicon.ico")
    st.markdown(
        f"""<div style="display:flex;align-items:center;gap:18px;">
                <img src="{icon_uri}" width="50" height="50" />
                <span style="font-size:2.4rem;font-weight:700;color:black;">Система рейтингового оцінювання НП</span>
            </div>""",
        unsafe_allow_html=True
    )
    st.header("Вхід до системи")

    if st.session_state.np_structure.empty:
        st.error("Список наукових працівників порожній. Зверніться до адміністратора.")
        return

    admin_pibs = set(ADMIN_USERS)
    ensure_login(st.session_state.np_structure, admin_pibs=admin_pibs)

    if st.session_state.get("logged_in_user"):
        st.success(f"Вітаємо, {st.session_state.logged_in_user}! Ви успішно увійшли.")
    else:
        left, _ = st.columns([6, 6])
        with left:
            st.markdown('<div id="login-google" class="uaf-login-button">', unsafe_allow_html=True)
            userinfo = _google_userinfo_via_button(button_label="🔐 Увійти з Google")
            st.markdown('</div>', unsafe_allow_html=True)
        st.info("Увійдіть через Google (домен @knu.ua).")

    logout_button("Вийти")

    st.markdown('<div class="uaf-login-placeholder"></div>', unsafe_allow_html=True)


# --- Основний додаток ---
def main_app():
    icon_uri = favicon_data_uri("favicon.ico")
    st.sidebar.markdown(

        f"""<div style="display:flex;align-items:center;gap:8px;">
                <img src="{icon_uri}" width="30" height="30" />
                <span style="font-size:1.4rem;font-weight:700;color:white;">Навігація</span>
            </div>
            """,
        unsafe_allow_html=True
    )
    ensure_login(st.session_state.np_structure)

    st.sidebar.success(f"Ви увійшли як: **{st.session_state.logged_in_user}**")

    if st.session_state.is_admin:
        st.sidebar.warning("Ви в режимі адміністратора.")

    # Визначення доступних опцій меню
    if st.session_state.is_admin:
        menu_options = ["🏠 Головна", "📝 Введення/Редагування даних", "📊 Загальний рейтинг НП", "⚙️ Управління НП"]
    else:
        menu_options = ["🏠 Головна", "📝 Введення/Редагування даних"]

    choice = st.sidebar.radio("Оберіть розділ:", menu_options)


    if st.sidebar.button("Вийти"):
        st.session_state.logged_in_user = None
        st.session_state.is_admin = False
        st.rerun()

    if choice == "🏠 Головна":
        st.title("Головна сторінка")
        st.write(f"Вітаємо, {st.session_state.logged_in_user}!")
        st.info("Скористайтеся меню ліворуч для навігації.")

    elif choice == "📝 Введення/Редагування даних":
        if st.session_state.is_admin:
            pib_list = sorted(st.session_state.np_structure[c.COL_PIB].tolist())
            selected_pib_index = pib_list.index(
                st.session_state.current_np_pib) if st.session_state.current_np_pib in pib_list else 0
            selected_pib = st.selectbox("Оберіть НП для редагування (режим адміністратора):", pib_list,
                                        index=selected_pib_index)
        else:
            selected_pib = st.session_state.logged_in_user

        # 2) Рік/період — ЛИШЕ тут
        period_options = [str(y) for y in range(2023, 2031)]
        current_period = st.session_state.get("selected_period")
        default_index = period_options.index(current_period) if current_period in period_options else len(
            period_options) - 1
        selected_period = st.selectbox("Оберіть рік (період) для внесення даних:", period_options,
                                       index=default_index)
        st.session_state.selected_period = selected_period

        if selected_pib != st.session_state.current_np_pib:
            get_current_np_data_row(selected_pib)
            st.rerun()

        if not st.session_state.np_form_data or st.session_state.np_form_data.get(c.COL_PIB) != selected_pib:
            get_current_np_data_row(selected_pib)

        # 4) Гарантуємо, що у формі є ПІБ і Період
        st.session_state.np_form_data[c.COL_PIB] = selected_pib
        st.session_state.np_form_data[c.NP_COL_PERIOD] = selected_period

        render_np_input_form_main()

    elif choice == "📊 Загальний рейтинг НП" and st.session_state.is_admin:
        st.header("Загальний рейтинг Наукових Працівників")

        # ==== Фільтр періодів (років) для перегляду ====
        # 1) Витягаємо роки як ЧИСЛА (коерсимо все зайве), потім робимо рядки

        df = st.session_state.np_ratings.copy()

        # Коерсимо до чисел і чистимо сміття
        years_num = pd.to_numeric(df[c.NP_COL_PERIOD], errors="ignore")

        # Якщо після ignore лишилися рядки — коерсимо ще раз
        if years_num.dtype == "O":
            years_num = pd.to_numeric(df[c.NP_COL_PERIOD].astype(str).str.replace(",", ".").str.strip(),
                                      errors="coerce")

        # Фільтр валідних років: без NaN/0, у розумному діапазоні
        this_year = dt.datetime.now().year
        years_num = years_num.dropna()
        years_num = years_num.astype(float)

        valid_years = years_num[(years_num >= 2000) & (years_num <= this_year + 1)].astype(int)
        all_years = sorted(valid_years.unique())  # [2023, 2024, 2025]
        all_years_str = [str(y) for y in all_years]  # ['2023','2024','2025']

        # Якщо раптом даних немає — не падаємо
        if not all_years_str:
            all_years_str = [str(this_year)]

        default_years = all_years_str[-3:] if len(all_years_str) >= 3 else all_years_str

        selected_years = st.multiselect(
            "Оберіть роки для аналізу",
            options=all_years_str,
            default=default_years,
            key="ui_years_filter_general_rating",
        )

        if not selected_years:
            st.info("Роки не обрано — показуємо останній доступний рік.")
            selected_years = [all_years_str[-1]]

        # Перерахуємо бали, а потім відфільтруємо по обраних роках
        full_ratings = st.session_state.np_ratings.copy()
        for i, row in full_ratings.iterrows():
            full_ratings.iloc[i] = calc.calculate_all_scores_for_np(row)

        full_ratings[c.NP_COL_PERIOD] = pd.to_numeric(full_ratings[c.NP_COL_PERIOD], errors="coerce").astype("Int64")
        full_ratings = full_ratings[full_ratings[c.NP_COL_PERIOD].isin(pd.Series(selected_years).astype(int))]
        full_ratings[c.NP_COL_PERIOD] = full_ratings[c.NP_COL_PERIOD].astype(str)

        # ==== Фільтр по НП ====
        pib_list = sorted(full_ratings[c.COL_PIB].dropna().unique().tolist())
        selected_pibs = st.multiselect("Оберіть НП для аналізу", pib_list, default=pib_list[:5])

        filtered_ratings = full_ratings[full_ratings[c.COL_PIB].isin(selected_pibs)]

        # ==== Тип графіка ====
        # chart_type = st.selectbox("Тип графіка", ["bar", "pie", "line"], index=0)
        chart_type = st.selectbox("Тип графіка", ["гістограма", "кругова діаграма", "лінійна діаграма"], index=0)

        if chart_type == "гістограма":
            bar_chart = alt.Chart(filtered_ratings).transform_joinaggregate(
                mean_IB_total=f"mean({c.NP_COL_IB_TOTAL})"
            ).mark_bar(opacity=0.7).encode(
                x=alt.X(c.COL_PIB, sort='-y', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y(c.NP_COL_IB_TOTAL, title="Бали (ІБ = ПП + НТР + ОР)"),
                color=alt.condition(
                    alt.datum[c.NP_COL_IB_TOTAL] > alt.datum.mean_IB_total,
                    alt.value("#FFD700"), alt.value("#808080")
                ),
                tooltip=[c.COL_PIB, alt.Tooltip(c.NP_COL_IB_TOTAL, format=".2f")]
            ).properties(height=400, width=800)
            st.altair_chart(bar_chart, use_container_width=True)

        elif chart_type == "кругова діаграма":
            pie_df = pd.DataFrame({
                "Категорія": ["ПП", "НТР", "ОР"],
                "Бали": [
                    filtered_ratings[c.NP_COL_PP_TOTAL].sum(),
                    filtered_ratings[c.NP_COL_NTR_TOTAL].sum(),
                    filtered_ratings[c.NP_COL_OR_TOTAL].sum()
                ]
            })
            pie_chart = alt.Chart(pie_df).mark_arc().encode(
                theta="Бали:Q",
                color=alt.Color("Категорія:N", scale=alt.Scale(range=["#FFD700", "#3E3C36", "#228B22"])),
                tooltip=["Категорія", "Бали"]
            ).properties(title="Розподіл балів за блоками")
            st.altair_chart(pie_chart, use_container_width=True)

        elif chart_type == "лінійна діаграма":
            if filtered_ratings.empty:
                st.warning("Немає даних для побудови динаміки за обрані роки/НП.")
            else:
                # групуємо середній ІБ по роках (за потреби можна робити по кожному ПІБ окремо)
                dyn = (
                    filtered_ratings
                    .groupby([c.NP_COL_PERIOD, c.COL_PIB], as_index=False)[c.NP_COL_IB_TOTAL]
                    .mean()
                    .sort_values([c.COL_PIB, c.NP_COL_PERIOD])
                )

                n_periods = dyn[c.NP_COL_PERIOD].nunique()
                if n_periods < 2:
                    st.info("Для ліній по кожному НП оберіть щонайменше два роки.")
                    chart = alt.Chart(dyn).mark_point(size=80).encode(
                        x=c.NP_COL_PERIOD, y=c.NP_COL_IB_TOTAL, color=c.COL_PIB,
                        tooltip=[c.COL_PIB, c.NP_COL_PERIOD, alt.Tooltip(c.NP_COL_IB_TOTAL, format=".2f")]
                    )
                else:
                    chart = alt.Chart(dyn).mark_line(strokeWidth=3).encode(
                        x=c.NP_COL_PERIOD, y=c.NP_COL_IB_TOTAL, color=c.COL_PIB,
                        tooltip=[c.COL_PIB, c.NP_COL_PERIOD, alt.Tooltip(c.NP_COL_IB_TOTAL, format=".2f")]
                    )
                st.altair_chart(chart.properties(height=300), use_container_width=True)

        st.markdown("---")
        # 🔹 Готуємо версію тільки для показу/експорту
        df_view = with_pretty_headers(humanize_bools(filtered_ratings))

        # 📋 Таблиця з красивими заголовками і «Так/Ні» замість True/False
        st.dataframe(df_view, use_container_width=True)

        # ⬇️ Кнопка для завантаження CSV у читабельному вигляді
        csv_hr = df_view.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            "⬇️ Завантажити CSV",
            csv_hr,
            "рейтинг_наукових_працівників.csv",
            "text/csv"
        )


    elif choice == "⚙️ Управління НП" and st.session_state.is_admin:
        st.header("Управління списком Наукових Працівників")
        with st.expander("➕ Додати нового НП"):
            new_pib = st.text_input("ПІБ")
            new_pos = st.text_input("Посада")
            if st.button("Додати"):
                if new_pib and new_pos and new_pib not in st.session_state.np_structure[c.COL_PIB].values:
                    new_row = pd.DataFrame([{'ПІБ': new_pib, 'Посада': new_pos}])
                    st.session_state.np_structure = pd.concat([st.session_state.np_structure, new_row], ignore_index=True)
                    dm.save_np_structure(st.session_state.np_structure)
                    st.session_state.np_ratings = dm.initialize_np_ratings_df(st.session_state.np_structure)
                    dm.save_np_ratings(st.session_state.np_ratings)
                    st.success(f"Додано: {new_pib}")
                    st.rerun()
                else:
                    st.warning("Заповніть всі поля або такий ПІБ вже існує.")

        st.dataframe(st.session_state.np_structure)

# --- Головний роутер додатку ---
if c.NP_COL_PERIOD not in st.session_state.np_ratings.columns:
    st.session_state.np_ratings[c.NP_COL_PERIOD] = str(datetime.now().year)
    dm.save_np_ratings(st.session_state.np_ratings)

if st.session_state.logged_in_user is None:
    login_screen()
else:
    main_app()
