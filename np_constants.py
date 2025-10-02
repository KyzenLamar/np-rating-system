# np_constants.py

# ==============================================================================
# КОНСТАНТИ ДЛЯ НАУКОВИХ ПРАЦІВНИКІВ (НП)
# (Згідно з наказом від 29.07.2025 №141-1)
# ==============================================================================

# --- Загальні назви стовпців ---
COL_PIB = "ПІБ"
COL_POSITION = "Посада"

# --- Назви стовпців для агрегованих балів (НП) ---
NP_COL_PP_TOTAL = "НП_Пп_загалом"
NP_COL_NTR_TOTAL = "НП_Нтр_загалом"
NP_COL_OR_TOTAL = "НП_Ор_загалом"
NP_COL_IB_TOTAL = "НП_Іб_загальний_бал"
NP_COL_PERIOD = "Період"

# --- ДОДАТОК 1.2 (НП): ПОСТІЙНІ ПОКАЗНИКИ (ПП) ---
NP_COL_PP_KVAL_KANDYDAT = "НП_Пп_1_ква_кандидат_наук"
NP_POINTS_PP_KVAL_KANDYDAT = 25
NP_COL_PP_KVAL_PHD_ABROAD = "НП_Пп_1_ква_phd_abroad"
NP_POINTS_PP_KVAL_PHD_ABROAD = 25
NP_COL_PP_KVAL_DOCTOR = "НП_Пп_1_ква_доктор_наук"
NP_POINTS_PP_KVAL_DOCTOR = 50

NP_COL_PP_VZVAN_STARSH_DOSL = "НП_Пп_2_взван_старший_дослідник"
NP_POINTS_PP_VZVAN_STARSH_DOSL = 25
NP_COL_PP_VZVAN_DOTSENT = "НП_Пп_2_взван_доцент"
NP_POINTS_PP_VZVAN_DOTSENT = 25
NP_COL_PP_VZVAN_PROFESOR = "НП_Пп_2_взван_професор"
NP_POINTS_PP_VZVAN_PROFESOR = 50

NP_COL_PP_DERZH_PREMIYA = "НП_Пп_3_держ_премія"
NP_POINTS_PP_DERZH_PREMIYA = 50

NP_COL_PP_POCHESNE_ZVANNYA = "НП_Пп_4_почесне_звання"
NP_POINTS_PP_POCHESNE_ZVANNYA = 50

NP_COL_PP_NAGORODY_VRU_KMU = "НП_Пп_5_нагороди_ВРУ_КМУ"
NP_POINTS_PP_NAGORODY_VRU_KMU = 15
NP_COL_PP_NAGORODY_ORDER = "НП_Пп_5_нагороди_орден"
NP_POINTS_PP_NAGORODY_ORDER = 25
NP_COL_PP_NAGORODY_VIDOVI = "НП_Пп_5_нагороди_відові"
NP_POINTS_PP_NAGORODY_VIDOVI = 5
NP_COL_PP_NAGORODY_VIKNU = "НП_Пп_5_нагороди_ВІКНУ"
NP_POINTS_PP_NAGORODY_VIKNU = 3

NP_COL_PP_NAN_CHLEN = "НП_Пп_6_нан_дійсний_член"
NP_POINTS_PP_NAN_CHLEN = 50
NP_COL_PP_NAN_CHLEN_KOR = "НП_Пп_6_нан_член_кореспондент"
NP_POINTS_PP_NAN_CHLEN_KOR = 40
NP_COL_PP_NAN_HALUZEVI_AKADEMIYI = "НП_Пп_6_нан_галузеві_академії"
NP_POINTS_PP_NAN_HALUZEVI_AKADEMIYI = 40
NP_COL_PP_NAN_HROMADSKI = "НП_Пп_6_нан_громадські_організації"
NP_POINTS_PP_NAN_HROMADSKI = 30

NP_COL_PP_STATUS_UBD = "НП_Пп_7_статус_УБД"
NP_POINTS_PP_STATUS_UBD = 10

NP_COL_PP_NAVCHANNYA_NATO_KILKIST = "НП_Пп_8_навчання_НАТО_кількість"
NP_POINTS_PP_NAVCHANNYA_NATO_PER_EVENT = 5

NP_COL_PP_VNG_OKP_DNIV = "НП_Пп_9_ВНГ_ОКП_днів"
NP_POINTS_PP_VNG_OKP_PER_DAY = 5

NP_COL_PP_INOZEMNA_MOVA_RIVEN = "НП_Пп_10_іноземна_мова_рівень"
NP_POINTS_PP_INOZEMNA_MOVA = {
    "Немає": 0, "СМП 1 / А2 (CEFR)": 10, "СМП 1+ / В1 (CEFR)": 20,
    "СМП 2 / В2 (CEFR)": 30, "СМП 2+ / С1 (CEFR)": 40, "СМП 3 / С2 (CEFR)": 50,
}

# --- ДОДАТОК 1.3 (НП): НАУКОВА (НАУКОВО-ТЕХНІЧНА) ДІЯЛЬНІСТЬ (НТР) ---
NP_COL_NTR_ZAHYST_DOCTORSKA = "НП_Нтр_1_захист_докторська"
NP_POINTS_NTR_ZAHYST_DOCTORSKA = 50
NP_COL_NTR_ZAHYST_PHD = "НП_Нтр_1_захист_phd"
NP_POINTS_NTR_ZAHYST_PHD = 30

NP_COL_NTR_NAUK_KONSULT_ADYUNKT_KILKIST = "НП_Нтр_2_наук_консульт_адюнкт_кількість"
NP_POINTS_NTR_NAUK_KONSULT_ADYUNKT = 45
NP_COL_NTR_NAUK_KONSULT_DOCTORANT_KILKIST = "НП_Нтр_2_наук_консульт_докторант_кількість"
NP_POINTS_NTR_NAUK_KONSULT_DOCTORANT = 50

NP_COL_NTR_OPONUVANNYA_DOCTOR_NAUK_KILKIST = "НП_Нтр_3_опонування_доктор_наук_кількість"
NP_POINTS_NTR_OPONUVANNYA_DOCTOR_NAUK = 40
NP_COL_NTR_OPONUVANNYA_PHD_KILKIST = "НП_Нтр_3_опонування_phd_кількість"
NP_POINTS_NTR_OPONUVANNYA_PHD = 20

NP_COL_NTR_RECENZ_DYSERT_DOCTOR_NAUK_KILKIST = "НП_Нтр_4_реценз_дисерт_доктор_наук_кількість"
NP_POINTS_NTR_RECENZ_DYSERT_DOCTOR_NAUK = 10
NP_COL_NTR_RECENZ_DYSERT_PHD_KILKIST = "НП_Нтр_4_реценз_дисерт_phd_кількість"
NP_POINTS_NTR_RECENZ_DYSERT_PHD = 5

NP_COL_NTR_PIDHOT_AKTU_VPROVADZH_KILKIST = "НП_Нтр_5_підгот_акту_впровадж_кількість"
NP_POINTS_NTR_PIDHOT_AKTU_VPROVADZH = 5

NP_COL_NTR_NDR_DERZH_KERIVNYK_KILKIST = "НП_Нтр_6_НДР_держ_керівник_кількість"
NP_POINTS_NTR_NDR_DERZH_KERIVNYK = 40
NP_COL_NTR_NDR_DERZH_VYKONAVETS_KILKIST = "НП_Нтр_6_НДР_держ_виконавець_кількість"
NP_POINTS_NTR_NDR_DERZH_VYKONAVETS = 20
NP_COL_NTR_NDR_MIZHNAR_KERIVNYK_KILKIST = "НП_Нтр_6_НДР_міжнар_керівник_кількість"
NP_POINTS_NTR_NDR_MIZHNAR_KERIVNYK = 50
NP_COL_NTR_NDR_MIZHNAR_VYKONAVETS_KILKIST = "НП_Нтр_6_НДР_міжнар_виконавець_кількість"
NP_POINTS_NTR_NDR_MIZHNAR_VYKONAVETS = 30

NP_COL_NTR_OZ_VIDPOV_VYKONAVETS_KILKIST = "НП_Нтр_7_ОЗ_відпов_виконавець_кількість"
NP_POINTS_NTR_OZ_VIDPOV_VYKONAVETS = 35
NP_COL_NTR_OZ_VYKONAVETS_KILKIST = "НП_Нтр_7_ОЗ_виконавець_кількість"
NP_POINTS_NTR_OZ_VYKONAVETS = 15

NP_COL_NTR_STANDART_KERIVNYK_KILKIST = "НП_Нтр_7_стандарт_керівник_кількість"
NP_POINTS_NTR_STANDART_KERIVNYK = 30
NP_COL_NTR_STANDART_VIDPOV_VYKONAVETS_KILKIST = "НП_Нтр_7_стандарт_відпов_виконавець_кількість"
NP_POINTS_NTR_STANDART_VIDPOV_VYKONAVETS = 20
NP_COL_NTR_STANDART_VYKONAVETS_KILKIST = "НП_Нтр_7_стандарт_виконавець_кількість"
NP_POINTS_NTR_STANDART_VYKONAVETS = 10

NP_COL_NTR_STATTI_DETAILS_JSON = "НП_Нтр_8_статті_деталі_json"
NP_POINTS_NTR_STATTI_SCOPUS_Q1 = 50
NP_POINTS_NTR_STATTI_SCOPUS_Q2 = 45
NP_POINTS_NTR_STATTI_SCOPUS_Q3 = 40
NP_POINTS_NTR_STATTI_SCOPUS_Q4 = 35
NP_POINTS_NTR_STATTI_INSHI_MIZHNAR_BAZY_ZAKORDONNI = 50
NP_POINTS_NTR_STATTI_INSHI_MIZHNAR_BAZY_VITCHYZNYANI = 40
NP_POINTS_NTR_STATTI_ZAKORDONNI_NEINDEX = 30
NP_POINTS_NTR_STATTI_FAHOVI_UKRAINA = 20
NP_POINTS_NTR_STATTI_NEFAHOVI_UKRAINA = 5

NP_COL_NTR_DOPOVIDI_DETAILS_JSON = "НП_Нтр_9_доповіді_деталі_json"
NP_POINTS_NTR_DOPOVIDI_TEZY_MIZHNARODNI = 15
NP_POINTS_NTR_DOPOVIDI_TEZY_VSEUKRAINSKI = 10
NP_POINTS_NTR_DOPOVIDI_TEZY_MIZHVUZIVSKI = 5

NP_COL_NTR_PATENT_KILKIST = "НП_Нтр_10_патент_кількість"
NP_POINTS_NTR_PATENT = 50
NP_COL_NTR_KORYSNA_MODEL_KILKIST = "НП_Нтр_10_корисна_модель_кількість"
NP_POINTS_NTR_KORYSNA_MODEL = 30

NP_COL_NTR_AVTORSKE_PRAVO_KILKIST = "НП_Нтр_11_авторське_право_кількість"
NP_POINTS_NTR_AVTORSKE_PRAVO = 15

NP_COL_NTR_MONO_ODNOOSIBNA_DETAILS_JSON = "НП_Нтр_12_моно_одноосібна_деталі_json"
NP_POINTS_NTR_MONO_ODNOOSIBNA_INOZEMNE_PER_SHEET = 35
NP_POINTS_NTR_MONO_ODNOOSIBNA_UKRAINSKE_PER_SHEET = 30

NP_COL_NTR_MONO_KOLEKTYVNA_DETAILS_JSON = "НП_Нтр_13_моно_колективна_деталі_json"
NP_POINTS_NTR_MONO_KOLEKTYVNA_INOZEMNE_PER_SHEET = 30
NP_POINTS_NTR_MONO_KOLEKTYVNA_UKRAINSKE_PER_SHEET = 25

NP_COL_NTR_RECENZ_MONO_KILKIST = "НП_Нтр_14_реценз_моно_кількість"
NP_POINTS_NTR_RECENZ_MONO = 10

NP_COL_NTR_RECENZ_STATTI_DETAILS_JSON = "НП_Нтр_15_реценз_статті_деталі_json"
NP_POINTS_NTR_RECENZ_STATTI_SCOPUS_A = 30
NP_POINTS_NTR_RECENZ_STATTI_FAHOVE_B = 15
NP_POINTS_NTR_RECENZ_STATTI_ZAKORDONNE_INSHI = 10

NP_COL_NTR_KERIVNYTSTVO_NDR_KURSANTIV_KILKIST = "НП_Нтр_16_керівництво_НДР_курсантів_кількість"
NP_POINTS_NTR_KERIVNYTSTVO_NDR_KURSANTIV = 5

NP_COL_NTR_PIDHOT_PEREMOZH_VSEUKR_KILKIST = "НП_Нтр_17_підгот_перемож_всеукр_кількість"
NP_POINTS_NTR_PIDHOT_PEREMOZH_VSEUKR = 20
NP_COL_NTR_PIDHOT_PEREMOZH_VNUTRISH_KILKIST = "НП_Нтр_17_підгот_перемож_внутріш_кількість"
NP_POINTS_NTR_PIDHOT_PEREMOZH_VNUTRISH = 10

NP_COL_NTR_PIDHOT_PEREMOZH_OLIMPIADA_KILKIST = "НП_Нтр_18_підгот_перемож_олімпіада_кількість"
NP_POINTS_NTR_PIDHOT_PEREMOZH_OLIMPIADA = 20

NP_COL_NTR_PIDHOT_KOMANDY_PEREMOZH_KILKIST = "НП_Нтр_19_підгот_команди_перемож_кількість"
NP_POINTS_NTR_PIDHOT_KOMANDY_PEREMOZH = 20

NP_COL_NTR_PIDHOT_PEREMOZH_OBL_AKADEM_KILKIST = "НП_Нтр_20_підгот_перемож_обл_академ_кількість"
NP_POINTS_NTR_PIDHOT_PEREMOZH_OBL_AKADEM = 10

NP_COL_NTR_VYDANNYA_PIDRUCHNYK_KILKIST = "НП_Нтр_21_видання_підручник_кількість"
NP_COL_NTR_VYDANNYA_PIDRUCHNYK_ID = "НП_Нтр_21_видання_підручник_ID"
NP_POINTS_NTR_VYDANNYA_PIDRUCHNYK = 50
NP_COL_NTR_VYDANNYA_POSIBNYK_KILKIST = "НП_Нтр_21_видання_посібник_кількість"
NP_COL_NTR_VYDANNYA_POSIBNYK_ID = "НП_Нтр_21_видання_посібник_ID"
NP_POINTS_NTR_VYDANNYA_POSIBNYK = 40
NP_COL_NTR_VYDANNYA_DOVIDNYK_KILKIST = "НП_Нтр_21_видання_довідник_кількість"
NP_COL_NTR_VYDANNYA_DOVIDNYK_ID = "НП_Нтр_21_видання_довідник_ID"
NP_POINTS_NTR_VYDANNYA_DOVIDNYK = 30
NP_COL_NTR_VYDANNYA_ZBIRNYK_KILKIST = "НП_Нтр_21_видання_збірник_кількість"
NP_COL_NTR_VYDANNYA_ZBIRNYK_ID = "НП_Нтр_21_видання_збірник_ID"
NP_POINTS_NTR_VYDANNYA_ZBIRNYK = 30

NP_COL_NTR_HIRSCH_INDEX_VALUE = "НП_Нтр_22_індекс_Гірша_значення"
NP_COL_NTR_HIRSCH_PROFILE_ID  = "НП_Нтр_22_Гірш_ID"
NP_POINTS_NTR_HIRSCH_INDEX_MULTIPLIER = 10

NP_COL_NTR_SPIKER_KILKIST = "НП_Нтр_23_спікер_кількість"
NP_POINTS_NTR_SPIKER = 10

NP_COL_NTR_RAZOVI_RADY_GOLOVA_KILKIST = "НП_Нтр_24_разові_ради_голова_кількість"
NP_POINTS_NTR_RAZOVI_RADY_GOLOVA = 15
NP_COL_NTR_RAZOVI_RADY_CHLEN_KILKIST = "НП_Нтр_24_разові_ради_член_кількість"
NP_POINTS_NTR_RAZOVI_RADY_CHLEN = 10

NP_COL_NTR_SPEC_RADY_KAND_KILKIST = "НП_Нтр_25_спец_ради_канд_кількість"
NP_POINTS_NTR_SPEC_RADY_KAND = 8
NP_COL_NTR_SPEC_RADY_DOCTOR_KILKIST = "НП_Нтр_25_спец_ради_доктор_кількість"
NP_POINTS_NTR_SPEC_RADY_DOCTOR = 10

# --- ДОДАТОК 1.4 (НП): ОРГАНІЗАЦІЙНА ТА ІННОВАЦІЙНА ДІЯЛЬНІСТЬ (ОР) ---
NP_COL_OR_VIYSK_PROF_ORIENT_DNIV = "НП_Ор_1_військ_проф_орієнт_днів"
NP_POINTS_OR_VIYSK_PROF_ORIENT_PER_DAY = 5

NP_COL_OR_KOMISII_MON_ZAHODIV = "НП_Ор_2_комісії_МОН_заходів"
NP_POINTS_OR_KOMISII_MON_PER_EVENT = 6

NP_COL_OR_DIYALNIST_RADY_VIKNU_ZASIDAN = "НП_Ор_3_діяльність_ради_ВІКНУ_засідань"
NP_POINTS_OR_DIYALNIST_RADY_VIKNU_PER_MEETING = 4
NP_MAX_POINTS_OR_DIYALNIST_RADY_VIKNU_PER_YEAR = 30

NP_COL_OR_VCHENA_RADA_CHLEN_ZASIDAN = "НП_Ор_4_вчена_рада_член_засідань"
NP_POINTS_OR_VCHENA_RADA_CHLEN_PER_MEETING = 3
NP_COL_OR_VCHENA_RADA_SEKRETAR_ZASIDAN = "НП_Ор_4_вчена_рада_секретар_засідань"
NP_POINTS_OR_VCHENA_RADA_SEKRETAR_PER_MEETING = 10

NP_COL_OR_EKSPERT_KOMISII_ZASIDAN = "НП_Ор_5_експерт_комісії_засідань"
NP_POINTS_OR_EKSPERT_KOMISII_PER_MEETING = 3
NP_MAX_POINTS_OR_EKSPERT_KOMISII_PER_YEAR = 30

NP_COL_OR_KONFERENTSII_DETAILS_JSON = "НП_Ор_6_конференції_деталі_json"
NP_POINTS_OR_KONFERENTSII_GOLOVA_ORGKOM = 30
NP_POINTS_OR_KONFERENTSII_GOLOVA_SEKCII = 25
NP_POINTS_OR_KONFERENTSII_CHLEN_ORGKOM = 10
NP_MAX_EVENTS_OR_KONFERENTSII_PER_YEAR = 4

NP_COL_OR_OLIMPIADY_DETAILS_JSON = "НП_Ор_7_олімпіади_деталі_json"
NP_POINTS_OR_OLIMPIADY_VSEUKR_MIZHNAR = 20
NP_POINTS_OR_OLIMPIADY_VIKNU = 10
NP_POINTS_OR_OLIMPIADY_EKSPERT_PER_WORK = 3
NP_MAX_POINTS_OR_OLIMPIADY_PER_YEAR = 20

NP_COL_OR_REDKOLEGIYI_DETAILS_JSON = "НП_Ор_8_редколегії_деталі_json"
NP_POINTS_OR_REDKOLEGIYI_SCOPUS_WOS = 30
NP_POINTS_OR_REDKOLEGIYI_ZAKORDONNI_INDEX = 20
NP_POINTS_OR_REDKOLEGIYI_UKR_FAHOVI = 10

NP_COL_OR_FORMUVANNYA_VISNYK_KILKIST = "НП_Ор_9_формування_вісник_кількість"
NP_POINTS_OR_FORMUVANNYA_VISNYK = 20
NP_COL_OR_FORMUVANNYA_ZBIRNYK_VIKNU_KILKIST = "НП_Ор_9_формування_збірник_ВІКНУ_кількість"
NP_POINTS_OR_FORMUVANNYA_ZBIRNYK_VIKNU = 20

NP_COL_OR_OZ_INSHI_ARK_NPP = "НП_Ор_11_ОЗ_інші_арк_НПП"
NP_COL_OR_OZ_INSHI_VIDSOTOK_U_NPP = "НП_Ор_11_ОЗ_інші_відсоток_НПП"
NP_POINTS_OR_OZ_INSHI_BASE_PER_SHEET = 10

NP_COL_OR_LINGVO_USNYJ_DNIV = "НП_Ор_12_лінгво_усний_днів"
NP_POINTS_OR_LINGVO_USNYJ_PER_DAY = 7

NP_COL_OR_LINGVO_PYSPOVYJ_STORINOK = "НП_Ор_13_лінгво_письмовий_сторінок"
NP_POINTS_OR_LINGVO_PYSPOVYJ_PER_4_PAGES = 5

NP_COL_OR_PIDV_KVAL_KILKIST = "НП_Ор_14_підв_квал_кількість"
NP_POINTS_OR_PIDV_KVAL_PER_COURSE = 5

# NP_COL_OR_PIDV_KVAL_KILKIST = "НП_Ор_15_підвищення_кваліфікації_кількість"  # вже є
# NP_COL_OR_PIDV_KVAL_DETAILS_JSON = "НП_Ор_15_підвищення_кваліфікації_деталі_JSON"

# --- Список усіх стовпців для даних НП ---
ALL_NP_RATING_COLUMNS = [] # Буде заповнено в data_manager.py


# ======================================================================
# ЛЮДСЬКІ НАЗВИ ДЛЯ ВІДОБРАЖЕННЯ (UI/Експорт)
# ======================================================================

COLUMN_LABELS = {
    # --- Загальні ---
    COL_PIB: "ПІБ",
    COL_POSITION: "Посада",
    NP_COL_PERIOD: "Період",

    # --- Агреговані бали ---
    NP_COL_PP_TOTAL: "Постійні показники (ПП), бал",
    NP_COL_NTR_TOTAL: "Наукова діяльність (НТР), бал",
    NP_COL_OR_TOTAL: "Організаційна діяльність (ОР), бал",
    NP_COL_IB_TOTAL: "Індивідуальний бал (ІБ), сумарно",

    # --- Додаток 1.2: Постійні показники (ПП) ---
    NP_COL_PP_KVAL_KANDYDAT: "Диплом кандидата наук (PhD, Україна)",
    NP_COL_PP_KVAL_PHD_ABROAD: "Закордонний диплом PhD",
    NP_COL_PP_KVAL_DOCTOR: "Диплом доктора наук",
    NP_COL_PP_VZVAN_STARSH_DOSL: "Вчене звання – старший дослідник",
    NP_COL_PP_VZVAN_DOTSENT: "Вчене звання – доцент",
    NP_COL_PP_VZVAN_PROFESOR: "Вчене звання – професор",
    NP_COL_PP_DERZH_PREMIYA: "Лауреат Державної премії",
    NP_COL_PP_POCHESNE_ZVANNYA: "Почесне звання",
    NP_COL_PP_NAGORODY_VRU_KMU: "Нагороди: ВРУ / КМУ / Подяка Прем’єра",
    NP_COL_PP_NAGORODY_ORDER: "Нагороди: Орден (державна нагорода)",
    NP_COL_PP_NAGORODY_VIDOVI: "Нагороди: від командувачів видів, родів військ",
    NP_COL_PP_NAGORODY_VIKNU: "Нагороди: від начальника ВІКНУ",
    NP_COL_PP_NAN_CHLEN: "Членство: дійсний член НАНУ",
    NP_COL_PP_NAN_CHLEN_KOR: "Членство: член-кореспондент НАНУ",
    NP_COL_PP_NAN_HALUZEVI_AKADEMIYI: "Членство: галузеві академії наук",
    NP_COL_PP_NAN_HROMADSKI: "Членство: наукові громадські організації",
    NP_COL_PP_STATUS_UBD: "Статус УБД / миротворчі місії",
    NP_COL_PP_NAVCHANNYA_NATO_KILKIST: "Участь у навчаннях НАТО (к-сть)",
    NP_COL_PP_VNG_OKP_DNIV: "Членство у ВНГ на ОКП (днів)",
    NP_COL_PP_INOZEMNA_MOVA_RIVEN: "Рівень володіння іноземною мовою (CEFR)",

    # --- Додаток 1.3: Наукова діяльність (НТР) ---
    NP_COL_NTR_ZAHYST_DOCTORSKA: "Захист докторської дисертації",
    NP_COL_NTR_ZAHYST_PHD: "Захист дисертації PhD",
    NP_COL_NTR_NAUK_KONSULT_ADYUNKT_KILKIST: "Наукове консультування ад’юнктів (к-сть)",
    NP_COL_NTR_NAUK_KONSULT_DOCTORANT_KILKIST: "Наукове консультування докторантів (к-сть)",
    NP_COL_NTR_OPONUVANNYA_DOCTOR_NAUK_KILKIST: "Опонування докторських дисертацій (к-сть)",
    NP_COL_NTR_OPONUVANNYA_PHD_KILKIST: "Опонування PhD дисертацій (к-сть)",
    NP_COL_NTR_RECENZ_DYSERT_DOCTOR_NAUK_KILKIST: "Рецензування дисертацій доктора наук (к-сть)",
    NP_COL_NTR_RECENZ_DYSERT_PHD_KILKIST: "Рецензування дисертацій PhD (к-сть)",
    NP_COL_NTR_PIDHOT_AKTU_VPROVADZH_KILKIST: "Підготовка акту впровадження (к-сть)",

    NP_COL_NTR_NDR_DERZH_KERIVNYK_KILKIST: "НДР державні (керівник) (к-сть)",
    NP_COL_NTR_NDR_DERZH_VYKONAVETS_KILKIST: "НДР державні (виконавець) (к-сть)",
    NP_COL_NTR_NDR_MIZHNAR_KERIVNYK_KILKIST: "НДР міжнародні (керівник) (к-сть)",
    NP_COL_NTR_NDR_MIZHNAR_VYKONAVETS_KILKIST: "НДР міжнародні (виконавець) (к-сть)",

    NP_COL_NTR_OZ_VIDPOV_VYKONAVETS_KILKIST: "ОЗ (відповідальний виконавець) (к-сть)",
    NP_COL_NTR_OZ_VYKONAVETS_KILKIST: "ОЗ (виконавець) (к-сть)",

    NP_COL_NTR_STANDART_KERIVNYK_KILKIST: "Розробка стандарту (керівник) (к-сть)",
    NP_COL_NTR_STANDART_VIDPOV_VYKONAVETS_KILKIST: "Розробка стандарту (відповідальний виконавець) (к-сть)",
    NP_COL_NTR_STANDART_VYKONAVETS_KILKIST: "Розробка стандарту (виконавець) (к-сть)",

    NP_COL_NTR_STATTI_DETAILS_JSON: "Статті (деталі, JSON)",
    NP_COL_NTR_DOPOVIDI_DETAILS_JSON: "Доповіді (деталі, JSON)",

    NP_COL_NTR_PATENT_KILKIST: "Патенти (к-сть)",
    NP_COL_NTR_KORYSNA_MODEL_KILKIST: "Корисні моделі (к-сть)",
    NP_COL_NTR_AVTORSKE_PRAVO_KILKIST: "Авторське право (свідоцтва, к-сть)",

    NP_COL_NTR_MONO_ODNOOSIBNA_DETAILS_JSON: "Монографії одноосібні (деталі, JSON)",
    NP_COL_NTR_MONO_KOLEKTYVNA_DETAILS_JSON: "Монографії колективні (деталі, JSON)",
    NP_COL_NTR_RECENZ_MONO_KILKIST: "Рецензування монографій (к-сть)",
    NP_COL_NTR_RECENZ_STATTI_DETAILS_JSON: "Рецензування статей (деталі, JSON)",

    NP_COL_NTR_KERIVNYTSTVO_NDR_KURSANTIV_KILKIST: "Керівництво НДР курсантів (к-сть)",

    NP_COL_NTR_HIRSCH_INDEX_VALUE: "Індекс Гірша (значення)",
    NP_COL_NTR_HIRSCH_PROFILE_ID:  "Індекс Гірша: профіль / ID / URL",
    NP_COL_NTR_SPIKER_KILKIST: "Спікер на наукових заходах (к-сть)",

    NP_COL_NTR_PIDHOT_PEREMOZH_VNUTRISH_KILKIST: "Підготовка переможців внутрішніх конкурсів (к-сть)",
    NP_COL_NTR_PIDHOT_PEREMOZH_VSEUKR_KILKIST: "Підготовка переможців всеукраїнських конкурсів (к-сть)",
    NP_COL_NTR_PIDHOT_PEREMOZH_OLIMPIADA_KILKIST: "Підготовка переможців олімпіад (к-сть)",
    NP_COL_NTR_PIDHOT_KOMANDY_PEREMOZH_KILKIST: "Підготовка команд-переможців (к-сть)",
    NP_COL_NTR_PIDHOT_PEREMOZH_OBL_AKADEM_KILKIST: "Підготовка переможців обласних/академічних конкурсів (к-сть)",

    NP_COL_NTR_VYDANNYA_PIDRUCHNYK_KILKIST: "Видання підручника (к-сть)",
    NP_COL_NTR_VYDANNYA_PIDRUCHNYK_ID: "Підручники (назва)",
    NP_COL_NTR_VYDANNYA_POSIBNYK_KILKIST: "Видання навчального посібника (к-сть)",
    NP_COL_NTR_VYDANNYA_POSIBNYK_ID: "Навчальні посібники (назви)",
    NP_COL_NTR_VYDANNYA_DOVIDNYK_KILKIST: "Видання довідника (к-сть)",
    NP_COL_NTR_VYDANNYA_DOVIDNYK_ID: "Довідники (назви)",
    NP_COL_NTR_VYDANNYA_ZBIRNYK_KILKIST: "Видання збірника (к-сть)",
    NP_COL_NTR_VYDANNYA_ZBIRNYK_ID: "Збірники (назви)",

    NP_COL_NTR_RAZOVI_RADY_GOLOVA_KILKIST: "Разові спецради (голова, к-сть)",
    NP_COL_NTR_RAZOVI_RADY_CHLEN_KILKIST: "Разові спецради (член, к-сть)",
    NP_COL_NTR_SPEC_RADY_KAND_KILKIST: "Спеціалізовані вчені ради: кандидат наук (к-сть)",
    NP_COL_NTR_SPEC_RADY_DOCTOR_KILKIST: "Спеціалізовані вчені ради: доктор наук (к-сть)",

    # --- Додаток 1.4: Організаційна та інноваційна діяльність (ОР) ---
    NP_COL_OR_VIYSK_PROF_ORIENT_DNIV: "Військово-професійна орієнтація молоді (днів)",
    NP_COL_OR_KOMISII_MON_ZAHODIV: "Участь у комісіях МОН та інших міністерств (к-сть заходів)",
    NP_COL_OR_DIYALNIST_RADY_VIKNU_ZASIDAN: "Діяльність у радах ВІКНУ (засідань)",
    NP_COL_OR_VCHENA_RADA_CHLEN_ZASIDAN: "Вчена рада (член, засідань)",
    NP_COL_OR_VCHENA_RADA_SEKRETAR_ZASIDAN: "Вчена рада (секретар, засідань)",
    NP_COL_OR_EKSPERT_KOMISII_ZASIDAN: "Експертні комісії (засідань)",
    NP_COL_OR_KONFERENTSII_DETAILS_JSON: "Організація конференцій (деталі, JSON)",
    NP_COL_OR_OLIMPIADY_DETAILS_JSON: "Організація олімпіад/конкурсів (деталі, JSON)",
    NP_COL_OR_REDKOLEGIYI_DETAILS_JSON: "Редколегії видань (деталі, JSON)",
    NP_COL_OR_FORMUVANNYA_VISNYK_KILKIST: "Підготовка видань «Вісник» (к-сть)",
    NP_COL_OR_FORMUVANNYA_ZBIRNYK_VIKNU_KILKIST: "Підготовка збірника ВІКНУ (к-сть)",
    NP_COL_OR_OZ_INSHI_ARK_NPP: "Оперативні завдання: інші (арк. НПП)",
    NP_COL_OR_OZ_INSHI_VIDSOTOK_U_NPP: "Оперативні завдання: інші (% НПП)",
    NP_COL_OR_LINGVO_USNYJ_DNIV: "Лінгвістичне забезпечення: усний переклад (днів)",
    NP_COL_OR_LINGVO_PYSPOVYJ_STORINOK: "Лінгвістичне забезпечення: письмовий переклад (сторінок)",
    NP_COL_OR_PIDV_KVAL_KILKIST: "Курси підвищення кваліфікації (к-сть)",
}

