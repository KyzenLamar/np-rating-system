# np_calculations.py
import pandas as pd
import json
import np_constants as c


# --- Допоміжні функції ---
def safe_get(data_row, column_name, default_value=0):
    """Безпечно отримує значення з pd.Series."""
    if column_name not in data_row.index or pd.isna(data_row[column_name]):
        return default_value
    return data_row[column_name]


# def parse_json_details(json_string, default_value=None):
#     """Безпечно парсить JSON-рядок."""
#     if default_value is None:
#         default_value = []
#     try:
#         if pd.isna(json_string) or not json_string:
#             return default_value
#         return json.loads(json_string)
#     except (json.JSONDecodeError, TypeError):
#         return default_value

def parse_json_details(json_value, default_value=None):
    """Безпечно повертає список словників з JSON-поля.
       Приймає рядок JSON, list, dict, число або NaN."""
    import pandas as pd, json

    if default_value is None:
        default_value = []

    # 1) None / NaN / порожньо
    if json_value is None or (isinstance(json_value, float) and pd.isna(json_value)):
        return default_value

    # 2) Якщо це вже Python-структура
    if isinstance(json_value, list):
        return json_value
    if isinstance(json_value, dict):
        return [json_value]
    if isinstance(json_value, (int, float)):
        # Число нам не підходить як список деталей → повертаємо порожній список
        return default_value

    # 3) Якщо це рядок — пробуємо парсити
    try:
        s = str(json_value).strip()
        if not s:
            return default_value
        parsed = json.loads(s)
        if isinstance(parsed, dict):
            return [parsed]
        if isinstance(parsed, list):
            return parsed
        return default_value
    except Exception:
        return default_value


# --- Функції розрахунку балів за Додатками для НП ---

def calculate_np_pp_scores(row: pd.Series) -> float:
    """Розраховує бали для Додатку 1.2: Постійні показники (ПП) для НП."""
    total = 0.0
    if safe_get(row, c.NP_COL_PP_KVAL_KANDYDAT, False): total += c.NP_POINTS_PP_KVAL_KANDYDAT
    if safe_get(row, c.NP_COL_PP_KVAL_PHD_ABROAD, False): total += c.NP_POINTS_PP_KVAL_PHD_ABROAD
    if safe_get(row, c.NP_COL_PP_KVAL_DOCTOR, False): total += c.NP_POINTS_PP_KVAL_DOCTOR
    if safe_get(row, c.NP_COL_PP_VZVAN_STARSH_DOSL, False): total += c.NP_POINTS_PP_VZVAN_STARSH_DOSL
    if safe_get(row, c.NP_COL_PP_VZVAN_DOTSENT, False): total += c.NP_POINTS_PP_VZVAN_DOTSENT
    if safe_get(row, c.NP_COL_PP_VZVAN_PROFESOR, False): total += c.NP_POINTS_PP_VZVAN_PROFESOR
    if safe_get(row, c.NP_COL_PP_DERZH_PREMIYA, False): total += c.NP_POINTS_PP_DERZH_PREMIYA
    if safe_get(row, c.NP_COL_PP_POCHESNE_ZVANNYA, False): total += c.NP_POINTS_PP_POCHESNE_ZVANNYA
    if safe_get(row, c.NP_COL_PP_NAGORODY_VRU_KMU, False): total += c.NP_POINTS_PP_NAGORODY_VRU_KMU
    if safe_get(row, c.NP_COL_PP_NAGORODY_ORDER, False): total += c.NP_POINTS_PP_NAGORODY_ORDER
    if safe_get(row, c.NP_COL_PP_NAGORODY_VIDOVI, False): total += c.NP_POINTS_PP_NAGORODY_VIDOVI
    if safe_get(row, c.NP_COL_PP_NAGORODY_VIKNU, False): total += c.NP_POINTS_PP_NAGORODY_VIKNU
    if safe_get(row, c.NP_COL_PP_NAN_CHLEN, False): total += c.NP_POINTS_PP_NAN_CHLEN
    if safe_get(row, c.NP_COL_PP_NAN_CHLEN_KOR, False): total += c.NP_POINTS_PP_NAN_CHLEN_KOR
    if safe_get(row, c.NP_COL_PP_NAN_HALUZEVI_AKADEMIYI, False): total += c.NP_POINTS_PP_NAN_HALUZEVI_AKADEMIYI
    if safe_get(row, c.NP_COL_PP_NAN_HROMADSKI, False): total += c.NP_POINTS_PP_NAN_HROMADSKI
    if safe_get(row, c.NP_COL_PP_STATUS_UBD, False): total += c.NP_POINTS_PP_STATUS_UBD
    total += int(safe_get(row, c.NP_COL_PP_NAVCHANNYA_NATO_KILKIST, 0)) * c.NP_POINTS_PP_NAVCHANNYA_NATO_PER_EVENT
    total += int(safe_get(row, c.NP_COL_PP_VNG_OKP_DNIV, 0)) * c.NP_POINTS_PP_VNG_OKP_PER_DAY
    lang_level = safe_get(row, c.NP_COL_PP_INOZEMNA_MOVA_RIVEN, "Немає")
    total += c.NP_POINTS_PP_INOZEMNA_MOVA.get(lang_level, 0)
    return total


def calculate_np_ntr_scores(row: pd.Series) -> float:
    """Розраховує бали для Додатку 1.3: Наукова діяльність (НТР) для НП."""
    total = 0.0

    # 1. Захист
    if safe_get(row, c.NP_COL_NTR_ZAHYST_DOCTORSKA, False): total += c.NP_POINTS_NTR_ZAHYST_DOCTORSKA
    if safe_get(row, c.NP_COL_NTR_ZAHYST_PHD, False): total += c.NP_POINTS_NTR_ZAHYST_PHD

    # 2. Наукове консультування
    total += int(safe_get(row, c.NP_COL_NTR_NAUK_KONSULT_ADYUNKT_KILKIST, 0)) * c.NP_POINTS_NTR_NAUK_KONSULT_ADYUNKT
    total += int(safe_get(row, c.NP_COL_NTR_NAUK_KONSULT_DOCTORANT_KILKIST, 0)) * c.NP_POINTS_NTR_NAUK_KONSULT_DOCTORANT

    # 3. Опонування
    total += int(
        safe_get(row, c.NP_COL_NTR_OPONUVANNYA_DOCTOR_NAUK_KILKIST, 0)) * c.NP_POINTS_NTR_OPONUVANNYA_DOCTOR_NAUK
    total += int(safe_get(row, c.NP_COL_NTR_OPONUVANNYA_PHD_KILKIST, 0)) * c.NP_POINTS_NTR_OPONUVANNYA_PHD

    # 4. Рецензування дисертацій
    total += int(
        safe_get(row, c.NP_COL_NTR_RECENZ_DYSERT_DOCTOR_NAUK_KILKIST, 0)) * c.NP_POINTS_NTR_RECENZ_DYSERT_DOCTOR_NAUK
    total += int(safe_get(row, c.NP_COL_NTR_RECENZ_DYSERT_PHD_KILKIST, 0)) * c.NP_POINTS_NTR_RECENZ_DYSERT_PHD

    # 5. Акт впровадження
    total += int(safe_get(row, c.NP_COL_NTR_PIDHOT_AKTU_VPROVADZH_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_AKTU_VPROVADZH

    # 6. НДР
    total += int(safe_get(row, c.NP_COL_NTR_NDR_DERZH_KERIVNYK_KILKIST, 0)) * c.NP_POINTS_NTR_NDR_DERZH_KERIVNYK
    total += int(safe_get(row, c.NP_COL_NTR_NDR_DERZH_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_NDR_DERZH_VYKONAVETS
    total += int(safe_get(row, c.NP_COL_NTR_NDR_MIZHNAR_KERIVNYK_KILKIST, 0)) * c.NP_POINTS_NTR_NDR_MIZHNAR_KERIVNYK
    total += int(safe_get(row, c.NP_COL_NTR_NDR_MIZHNAR_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_NDR_MIZHNAR_VYKONAVETS

    # 7. ОЗ та Стандарти
    total += int(safe_get(row, c.NP_COL_NTR_OZ_VIDPOV_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_OZ_VIDPOV_VYKONAVETS
    total += int(safe_get(row, c.NP_COL_NTR_OZ_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_OZ_VYKONAVETS
    total += int(safe_get(row, c.NP_COL_NTR_STANDART_KERIVNYK_KILKIST, 0)) * c.NP_POINTS_NTR_STANDART_KERIVNYK
    total += int(
        safe_get(row, c.NP_COL_NTR_STANDART_VIDPOV_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_STANDART_VIDPOV_VYKONAVETS
    total += int(safe_get(row, c.NP_COL_NTR_STANDART_VYKONAVETS_KILKIST, 0)) * c.NP_POINTS_NTR_STANDART_VYKONAVETS

    # 8. Статті
    articles_raw = safe_get(row, c.NP_COL_NTR_STATTI_DETAILS_JSON, '[]')
    # articles = parse_json_details(safe_get(row, c.NP_COL_NTR_STATTI_DETAILS_JSON, '[]'))
    articles = parse_json_details(articles_raw, [])
    article_points_map = {
        "Scopus Q1": c.NP_POINTS_NTR_STATTI_SCOPUS_Q1, "Scopus Q2": c.NP_POINTS_NTR_STATTI_SCOPUS_Q2,
        "Scopus Q3": c.NP_POINTS_NTR_STATTI_SCOPUS_Q3, "Scopus Q4": c.NP_POINTS_NTR_STATTI_SCOPUS_Q4,
        "Інші міжнародні бази (закордонні)": c.NP_POINTS_NTR_STATTI_INSHI_MIZHNAR_BAZY_ZAKORDONNI,
        "Інші міжнародні бази (вітчизняні)": c.NP_POINTS_NTR_STATTI_INSHI_MIZHNAR_BAZY_VITCHYZNYANI,
        "Закордонні (неіндексовані)": c.NP_POINTS_NTR_STATTI_ZAKORDONNI_NEINDEX,
        "Фахові України": c.NP_POINTS_NTR_STATTI_FAHOVI_UKRAINA,
        "Нефахові України": c.NP_POINTS_NTR_STATTI_NEFAHOVI_UKRAINA
    }
    if isinstance(articles, dict):
        articles = [articles]
    if not isinstance(articles, list):
        articles = []

    for article in articles:
        t = (article or {}).get("type", "")
        cnt = int((article or {}).get("count", 0) or 0)
        total += cnt * article_points_map.get(t, 0)

    # for article in articles:
    #     total += int(article.get("count", 0)) * article_points_map.get(article.get("type"), 0)

    # if isinstance(articles, (list, tuple)) and articles:  # Якщо список і не порожній
    #     for article in articles:
    #         total += int(article.get("count", 0)) * article_points_map.get(article.get("type"), 0)
    # else:
    #     # Якщо число або порожній/None, додаємо 0 (або множимо на коефіцієнт, наприклад, articles * 1, якщо це кількість)
    #     total += 0  # Швидкий фікс: ігноруємо

    # 9. Доповіді
    reports_raw = safe_get(row, c.NP_COL_NTR_DOPOVIDI_DETAILS_JSON, '[]')
    # reports = parse_json_details(safe_get(row, c.NP_COL_NTR_DOPOVIDI_DETAILS_JSON),'[]')
    reports = parse_json_details(reports_raw, [])
    report_points_map = {
        "Тези міжнародних конференцій": c.NP_POINTS_NTR_DOPOVIDI_TEZY_MIZHNARODNI,
        "Тези всеукраїнських конференцій": c.NP_POINTS_NTR_DOPOVIDI_TEZY_VSEUKRAINSKI,
        "Тези міжвузівських (вузівських) конференцій": c.NP_POINTS_NTR_DOPOVIDI_TEZY_MIZHVUZIVSKI
    }
    if isinstance(reports, dict):
        reports = [reports]
    if not isinstance(reports, list):
        reports = []

    for rep in reports:
        t = (rep or {}).get("type", "")
        cnt = int((rep or {}).get("count", 0) or 0)
        total += cnt * report_points_map.get(t, 0)

    # for report in reports:
    #     total += int(report.get("count", 0)) * report_points_map.get(report.get("type"), 0)

    # 10, 11. Патенти, авторське право
    total += int(safe_get(row, c.NP_COL_NTR_PATENT_KILKIST, 0)) * c.NP_POINTS_NTR_PATENT
    total += int(safe_get(row, c.NP_COL_NTR_KORYSNA_MODEL_KILKIST, 0)) * c.NP_POINTS_NTR_KORYSNA_MODEL
    total += int(safe_get(row, c.NP_COL_NTR_AVTORSKE_PRAVO_KILKIST, 0)) * c.NP_POINTS_NTR_AVTORSKE_PRAVO

    # 12, 13. Монографії
    # 12. Одноосібна монографія
    mono_solo = parse_json_details(safe_get(row, c.NP_COL_NTR_MONO_ODNOOSIBNA_DETAILS_JSON), [])
    for mono in mono_solo:
        sheets = float(mono.get("sheets", 0))
        if mono.get("type") == "в іноземному видавництві":
            total += sheets * c.NP_POINTS_NTR_MONO_ODNOOSIBNA_INOZEMNE_PER_SHEET
        elif mono.get("type") == "в українському видавництві":
            total += sheets * c.NP_POINTS_NTR_MONO_ODNOOSIBNA_UKRAINSKE_PER_SHEET

    # 13. Колективна монографія
    mono_team = parse_json_details(safe_get(row, c.NP_COL_NTR_MONO_KOLEKTYVNA_DETAILS_JSON), [])
    for mono in mono_team:
        sheets = float(mono.get("sheets", 0))
        authors = max(1, int(mono.get("authors", 1)))
        if mono.get("type") == "в іноземному видавництві":
            total += (sheets * c.NP_POINTS_NTR_MONO_KOLEKTYVNA_INOZEMNE_PER_SHEET) / authors
        elif mono.get("type") == "в українському видавництві":
            total += (sheets * c.NP_POINTS_NTR_MONO_KOLEKTYVNA_UKRAINSKE_PER_SHEET) / authors

    # 14. Рецензування монографій
    total += int(safe_get(row, c.NP_COL_NTR_RECENZ_MONO_KILKIST, 0)) * c.NP_POINTS_NTR_RECENZ_MONO

    # 15. Рецензування статей
    reviews = parse_json_details(safe_get(row, c.NP_COL_NTR_RECENZ_STATTI_DETAILS_JSON),[])
    review_points_map = {
        "Scopus, WoS, фахове видання категорії А": c.NP_POINTS_NTR_RECENZ_STATTI_SCOPUS_A,
        "фахове видання України категорії Б": c.NP_POINTS_NTR_RECENZ_STATTI_FAHOVE_B,
        "закордонне видання, індексоване в інших базах": c.NP_POINTS_NTR_RECENZ_STATTI_ZAKORDONNE_INSHI
    }
    for review in reviews:
        total += int(review.get("count", 0)) * review_points_map.get(review.get("type"), 0)

    # 16. Керівництво НДР курсантів
    total += int(
        safe_get(row, c.NP_COL_NTR_KERIVNYTSTVO_NDR_KURSANTIV_KILKIST, 0)) * c.NP_POINTS_NTR_KERIVNYTSTVO_NDR_KURSANTIV

    # 17. Підготовка переможців конкурсів
    total += int(safe_get(row, c.NP_COL_NTR_PIDHOT_PEREMOZH_VSEUKR_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_PEREMOZH_VSEUKR
    total += int(
        safe_get(row, c.NP_COL_NTR_PIDHOT_PEREMOZH_VNUTRISH_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_PEREMOZH_VNUTRISH

    # 18. Підготовка переможців олімпіад
    total += int(
        safe_get(row, c.NP_COL_NTR_PIDHOT_PEREMOZH_OLIMPIADA_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_PEREMOZH_OLIMPIADA

    # 19. Підготовка команди-переможниці
    total += int(
        safe_get(row, c.NP_COL_NTR_PIDHOT_KOMANDY_PEREMOZH_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_KOMANDY_PEREMOZH

    # 20. Підготовка переможців обласних конкурсів
    total += int(
        safe_get(row, c.NP_COL_NTR_PIDHOT_PEREMOZH_OBL_AKADEM_KILKIST, 0)) * c.NP_POINTS_NTR_PIDHOT_PEREMOZH_OBL_AKADEM

    # 21. Видавнича діяльність
    total += int(safe_get(row, c.NP_COL_NTR_VYDANNYA_PIDRUCHNYK_KILKIST, 0)) * c.NP_POINTS_NTR_VYDANNYA_PIDRUCHNYK
    total += int(safe_get(row, c.NP_COL_NTR_VYDANNYA_POSIBNYK_KILKIST, 0)) * c.NP_POINTS_NTR_VYDANNYA_POSIBNYK
    total += int(safe_get(row, c.NP_COL_NTR_VYDANNYA_DOVIDNYK_KILKIST, 0)) * c.NP_POINTS_NTR_VYDANNYA_DOVIDNYK
    total += int(safe_get(row, c.NP_COL_NTR_VYDANNYA_ZBIRNYK_KILKIST, 0)) * c.NP_POINTS_NTR_VYDANNYA_ZBIRNYK

    # 22. Індекс Гірша
    total += int(safe_get(row, c.NP_COL_NTR_HIRSCH_INDEX_VALUE, 0)) * c.NP_POINTS_NTR_HIRSCH_INDEX_MULTIPLIER

    # 23. Спікер за запрошенням
    total += int(safe_get(row, c.NP_COL_NTR_SPIKER_KILKIST, 0)) * c.NP_POINTS_NTR_SPIKER

    # 24. Робота в разових радах
    total += int(safe_get(row, c.NP_COL_NTR_RAZOVI_RADY_GOLOVA_KILKIST, 0)) * c.NP_POINTS_NTR_RAZOVI_RADY_GOLOVA
    total += int(safe_get(row, c.NP_COL_NTR_RAZOVI_RADY_CHLEN_KILKIST, 0)) * c.NP_POINTS_NTR_RAZOVI_RADY_CHLEN

    # 25. Робота в спецрадах
    total += int(safe_get(row, c.NP_COL_NTR_SPEC_RADY_KAND_KILKIST, 0)) * c.NP_POINTS_NTR_SPEC_RADY_KAND
    total += int(safe_get(row, c.NP_COL_NTR_SPEC_RADY_DOCTOR_KILKIST, 0)) * c.NP_POINTS_NTR_SPEC_RADY_DOCTOR

    return total


def calculate_np_or_scores(row: pd.Series) -> float:
    """Розраховує бали для Додатку 1.4: Організаційна діяльність (ОР) для НП."""
    total = 0.0

    # 1, 2. Орієнтація, комісії
    total += int(safe_get(row, c.NP_COL_OR_VIYSK_PROF_ORIENT_DNIV, 0)) * c.NP_POINTS_OR_VIYSK_PROF_ORIENT_PER_DAY
    total += int(safe_get(row, c.NP_COL_OR_KOMISII_MON_ZAHODIV, 0)) * c.NP_POINTS_OR_KOMISII_MON_PER_EVENT

    # 3. Діяльність у радах ВІКНУ (з лімітом)
    rady_points = int(
        safe_get(row, c.NP_COL_OR_DIYALNIST_RADY_VIKNU_ZASIDAN, 0)) * c.NP_POINTS_OR_DIYALNIST_RADY_VIKNU_PER_MEETING
    total += min(rady_points, c.NP_MAX_POINTS_OR_DIYALNIST_RADY_VIKNU_PER_YEAR)

    # 4. Вчена рада
    total += int(safe_get(row, c.NP_COL_OR_VCHENA_RADA_CHLEN_ZASIDAN, 0)) * c.NP_POINTS_OR_VCHENA_RADA_CHLEN_PER_MEETING
    total += int(
        safe_get(row, c.NP_COL_OR_VCHENA_RADA_SEKRETAR_ZASIDAN, 0)) * c.NP_POINTS_OR_VCHENA_RADA_SEKRETAR_PER_MEETING

    # 5. Експертні комісії (з лімітом)
    ekspert_points = int(
        safe_get(row, c.NP_COL_OR_EKSPERT_KOMISII_ZASIDAN, 0)) * c.NP_POINTS_OR_EKSPERT_KOMISII_PER_MEETING
    total += min(ekspert_points, c.NP_MAX_POINTS_OR_EKSPERT_KOMISII_PER_YEAR)

    # 6. Організація конференцій (з лімітом на кількість заходів)
    conferences = parse_json_details(safe_get(row, c.NP_COL_OR_KONFERENTSII_DETAILS_JSON), [])
    conf_points_map = {
        "голова оргкомітету": c.NP_POINTS_OR_KONFERENTSII_GOLOVA_ORGKOM,
        "голова секції": c.NP_POINTS_OR_KONFERENTSII_GOLOVA_SEKCII,
        "член оргкомітету, секретар секції": c.NP_POINTS_OR_KONFERENTSII_CHLEN_ORGKOM
    }
    total_conf_events = sum(int(conf.get("count", 0)) for conf in conferences)
    if total_conf_events > c.NP_MAX_EVENTS_OR_KONFERENTSII_PER_YEAR:
        # Пропорційно зменшуємо бали, якщо перевищено ліміт заходів
        for conf in conferences:
            points = int(conf.get("count", 0)) * conf_points_map.get(conf.get("role"), 0)
            total += points * (c.NP_MAX_EVENTS_OR_KONFERENTSII_PER_YEAR / total_conf_events)
    else:
        for conf in conferences:
            total += int(conf.get("count", 0)) * conf_points_map.get(conf.get("role"), 0)

    # 7. Організація олімпіад (з лімітом на бали)
    olympiads = parse_json_details(safe_get(row, c.NP_COL_OR_OLIMPIADY_DETAILS_JSON), [])
    olymp_points_map = {
        "всеукраїнських та міжнародних": c.NP_POINTS_OR_OLIMPIADY_VSEUKR_MIZHNAR,
        "Військового інституту (факультету)": c.NP_POINTS_OR_OLIMPIADY_VIKNU,
        "експерти з оцінювання робіт": c.NP_POINTS_OR_OLIMPIADY_EKSPERT_PER_WORK
    }
    olymp_points = 0
    for olymp in olympiads:
        olymp_points += int(olymp.get("count", 0)) * olymp_points_map.get(olymp.get("role"), 0)
    total += min(olymp_points, c.NP_MAX_POINTS_OR_OLIMPIADY_PER_YEAR)

    # 8. Робота у редколегіях
    editorials = parse_json_details(safe_get(row, c.NP_COL_OR_REDKOLEGIYI_DETAILS_JSON), [])
    editorial_points_map = {
        "виданнях, що індексуються в Scopus та WoS": c.NP_POINTS_OR_REDKOLEGIYI_SCOPUS_WOS,
        "в закордонних виданнях, індексованих наукометричними базами": c.NP_POINTS_OR_REDKOLEGIYI_ZAKORDONNI_INDEX,
        "українських фахових виданнях": c.NP_POINTS_OR_REDKOLEGIYI_UKR_FAHOVI
    }
    for editorial in editorials:
        total += int(editorial.get("count", 0)) * editorial_points_map.get(editorial.get("role"), 0)

    # 9. Формування видань
    total += int(safe_get(row, c.NP_COL_OR_FORMUVANNYA_VISNYK_KILKIST, 0)) * c.NP_POINTS_OR_FORMUVANNYA_VISNYK
    total += int(
        safe_get(row, c.NP_COL_OR_FORMUVANNYA_ZBIRNYK_VIKNU_KILKIST, 0)) * c.NP_POINTS_OR_FORMUVANNYA_ZBIRNYK_VIKNU

    # 11. ОЗ поза НДР
    total += float(safe_get(row, c.NP_COL_OR_OZ_INSHI_ARK_NPP, 0.0)) * c.NP_POINTS_OR_OZ_INSHI_BASE_PER_SHEET

    # 12. Усний переклад
    total += int(safe_get(row, c.NP_COL_OR_LINGVO_USNYJ_DNIV, 0)) * c.NP_POINTS_OR_LINGVO_USNYJ_PER_DAY

    # 13. Письмовий переклад
    total += int(safe_get(row, c.NP_COL_OR_LINGVO_PYSPOVYJ_STORINOK, 0)) * c.NP_POINTS_OR_LINGVO_PYSPOVYJ_PER_4_PAGES

    # 14. Підвищення кваліфікації
    total += int(
        safe_get(row, c.NP_COL_OR_PIDV_KVAL_KILKIST, 0)) * c.NP_POINTS_OR_PIDV_KVAL_PER_COURSE

    return total


# --- Головна функція розрахунку для одного НП ---
def calculate_all_scores_for_np(npp_data_row: pd.Series) -> pd.Series:
    """Розраховує всі агреговані бали та загальний бал для одного НП."""
    updated_row = npp_data_row.copy()

    updated_row[c.NP_COL_PP_TOTAL] = calculate_np_pp_scores(updated_row)
    updated_row[c.NP_COL_NTR_TOTAL] = calculate_np_ntr_scores(updated_row)
    updated_row[c.NP_COL_OR_TOTAL] = calculate_np_or_scores(updated_row)

    ib_total = (updated_row[c.NP_COL_PP_TOTAL] +
                updated_row[c.NP_COL_NTR_TOTAL] +
                updated_row[c.NP_COL_OR_TOTAL])
    updated_row[c.NP_COL_IB_TOTAL] = ib_total

    return updated_row
