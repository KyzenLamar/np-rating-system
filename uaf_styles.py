import streamlit as st

def load_css():
    css = """
        <style>
          :root{
            --olive:#6A653A;
            --gold:#F39200;
            --gold-color:#F39200;
            --text:#ffffff;
            --step-light-bg:#F7F6F2;
            --border-color:#E0DDD7;
          }

          /* ===== Sidebar ===== */
          [data-testid="stSidebar"]{
            background: var(--olive) !important;
            color: var(--text) !important;
          }
          [data-testid="stSidebar"] [data-testid="stSidebarContent"]{
            padding-top: .75rem !important;
          }

          .uaf-nav-title{
            display:flex;align-items:center;gap:.5rem;
            font-weight:700;font-size:1.4rem;letter-spacing:.3px;color:var(--text);
            margin:.25rem 0 1rem 0;
          }
          .uaf-trident{
            width:24px;height:24px;display:inline-block;background:var(--gold);
            mask:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23fff" d="M12 2c2.8 2.1 4.4 4.7 4.7 8.1l2.2-2v7.3l-2.2-1.9c-.4 3.6-2.1 6.4-4.7 8.5c-2.6-2-4.3-4.9-4.7-8.5L5 15.4V8.1l2.3 2C7.6 6.7 9.2 4.1 12 2z"/></svg>') center/contain no-repeat;
            -webkit-mask:inherit;
          }
          .uaf-user{
            background: rgba(46,125,50,.18);
            border: 1px solid rgba(255,255,255,.15);
            color: #eaffea; border-radius:10px;
            padding:.6rem .75rem; margin:.25rem 0 1rem 0; font-weight:600;
          }
          .uaf-user b{ color:#fff }

          /* ===== Cards ===== */
          [data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"]{
            background-color: var(--step-light-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,.06) !important;
            padding: 1rem 1rem .5rem 1rem !important;
          }

          /* ===== Buttons ===== */
          .stButton>button[kind="primary"]{
            background-color:var(--gold); color:#3E3C36; border:none;
          }
          .stButton>button[kind="primary"]:hover{
            background-color:#fff; color:#3E3C36;
          }

          /* Заголовки */
          h1,h2{ color:var(--gold) }
          h3{ color:var(--olive) !important }

          /* --- СТИЛІ ДЛЯ RADIO --- */
           .stRadio > label {
              font-size: 1.1rem !important;
              font-weight: 500;
              color: #FFFFFF !important;
              cursor: pointer;
          }

          /* Підсвічування при наведенні */
            .stRadio > label:hover {
               color: var(--gold-color) !important;
          }

            /* Активний вибраний пункт */
            .stRadio > div[role="radiogroup"] > label[data-selected="true"] {
               color: var(--gold-color) !important;
               font-weight: 600 !important;
          }

          /* --- Універсальна стилізація ВСІХ кнопок --- */
          .stButton>button {
              border-color: var(--gold-color);
              color: var(--gold-color);
          }
          .stButton>button:hover {
              border-color: #FFFFFF;
              color: #FFFFFF;
              background-color: var(--gold-color);
          }

          /* Тризуб перед заголовком сайдбару */
          [data-testid="stSidebar"] h2::before{
           content:"";
           display:inline-block; width:20px; height:20px; margin-right:8px; vertical-align:-3px;
           background: var(--gold-color);
           mask:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23fff" d="M12 2c2.8 2.1 4.4 4.7 4.7 8.1l2.2-2v7.3l-2.2-1.9c-.4 3.6-2.1 6.4-4.7 8.5c-2.6-2-4.3-4.9-4.7-8.5L5 15.4V8.1l2.3 2C7.6 6.7 9.2 4.1 12 2z"/></svg>') center/contain no-repeat;
           -webkit-mask:inherit;
          }
           [data-testid="stSidebar"] h2{
           color:#fff !important; letter-spacing:.3px; margin-bottom:.5rem;
          }

          /* Перефарбування блока st.sidebar.success(...) */
           [data-testid="stSidebar"] .stAlert{
           background: rgba(46,125,50,.18) !important;
           border: 1px solid rgba(255,255,255,.15) !important;
           color: #eaffea !important; 
           border-radius:10px; padding:.6rem .75rem;
          }
           [data-testid="stSidebar"] .stAlert p{
           color:#fff !important; font-weight:600; margin:0;
          }
          /* ====== st.radio у САЙДБАРІ (wide-compat) ====== */

          /* Заголовок "Оберіть розділ:" */
           [data-testid="stSidebar"] .stRadio > label,
           [data-testid="stSidebar"] [data-testid="stRadio"] > label{
           color:#fff !important;
           font-size:1.08rem !important;
           font-weight:700 !important;
           letter-spacing:.2px;
           margin-bottom:.5rem;
          }

    /* Контейнер опцій */
    [data-testid="stSidebar"] .stRadio [role="radiogroup"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"],
    [data-testid="stSidebar"] [data-baseweb="radiogroup"]{
      display:flex; flex-direction:column; gap:.6rem;
    }

    /* Кожна опція як «піллюля» */
    [data-testid="stSidebar"] .stRadio [role="radio"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"],
    [data-testid="stSidebar"] [data-baseweb="radio"]{
      position:relative;
      display:flex !important; align-items:center; gap:.6rem;
      padding:.62rem .8rem;
      border:1px solid rgba(255,255,255,.22);
      border-radius:12px;
      background:rgba(255,255,255,.05);
      transition:all .15s ease-in-out;
      cursor:pointer;
    }

    /* Прибрати стандартну «крапку» (усі варіанти DOM) */
    [data-testid="stSidebar"] .stRadio [role="radio"] > div:first-child,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] > div:first-child,
    [data-testid="stSidebar"] [data-baseweb="radio"] svg{
      display:none !important;
    }

    /* Текст опції */
    [data-testid="stSidebar"] .stRadio [role="radio"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] p,
    [data-testid="stSidebar"] [data-baseweb="radio"] p{
      margin:0; color:#fff !important; font-size:1.03rem; font-weight:600;
    }

    /* Ховер */
    [data-testid="stSidebar"] .stRadio [role="radio"]:hover,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover{
      border-color:#fff; background:rgba(255,255,255,.10);
    }

    /* Активна (вибрана) */
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"]{
      border-color:var(--gold-color) !important;
      background:rgba(243,146,0,.18) !important;
      box-shadow:inset 0 0 0 1px var(--gold-color) !important;
    }

    /* Клавіатурний фокус */
    [data-testid="stSidebar"] .stRadio [role="radio"]:focus,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:focus,
    [data-testid="stSidebar"] [data-baseweb="radio"]:focus{
      outline:2px solid var(--gold-color); outline-offset:2px;
    }

    /* Іконки-«маски» (кастомні, без файлів) */
    [data-testid="stSidebar"] .stRadio [role="radio"]::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]::before,
    [data-testid="stSidebar"] [data-baseweb="radio"]::before{
      content:"";
      width:18px; height:18px; flex:0 0 18px;
      background:#fff; opacity:.9;
      mask:center/contain no-repeat; -webkit-mask:center/contain no-repeat;
    }

    /* 1 — Головна (будинок) */
    [data-testid="stSidebar"] .stRadio [role="radio"]:nth-of-type(1)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:nth-of-type(1)::before,
    [data-testid="stSidebar"] [data-baseweb="radiogroup"] > *:nth-child(1)::before{
      mask:url('🏠');
      -webkit-mask:url("🏠");
    }

    /* 2 — Введення/Редагування (олівець) */
    [data-testid="stSidebar"] .stRadio [role="radio"]:nth-of-type(2)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:nth-of-type(2)::before,
    [data-testid="stSidebar"] [data-baseweb="radiogroup"] > *:nth-child(2)::before{
      mask:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23fff" d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83l3.75 3.75l1.83-1.83z"/></svg>');
      -webkit-mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%23fff' d='M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83l3.75 3.75l1.83-1.83z'/></svg>");
    }

    /* Активна іконка — золота */
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"]::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"]::before,
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"]::before{
      background:var(--gold-color) !important;
    }
    /* --- Прибити стандартний квадрат/крапку BaseWeb у st.sidebar.radio --- */
    [data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child,
    [data-testid="stSidebar"] .stRadio [role="radio"] > div:first-child,
    [data-testid="stSidebar"] [data-baseweb="radio"] svg{
      display:none !important;
      width:0 !important; height:0 !important;
      margin:0 !important; padding:0 !important;
      background:transparent !important; border:0 !important;
    }

    /* --- Додаємо акуратний індикатор стану замість нього --- */
    [data-testid="stSidebar"] [data-baseweb="radio"],
    [data-testid="stSidebar"] .stRadio [role="radio"]{
      position:relative;
      padding-left: .9rem; /* місце під індикатор */
    }
    [data-testid="stSidebar"] [data-baseweb="radio"]::before,
    [data-testid="stSidebar"] .stRadio [role="radio"]::before{
      content:"";
      position:absolute; left:.55rem; /* підрівняй при потребі */
      width:10px; height:10px; border-radius:50%;
      background:transparent;
      box-shadow:0 0 0 2px rgba(255,255,255,.75) inset;
    }
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"]::before,
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"]::before{
      background: var(--gold-color);
      box-shadow: 0 0 0 2px var(--gold-color) inset;
    }

    /* === RADIO: hover/active = як кнопка "Вийти" === */
    [data-testid="stSidebar"] .stRadio [role="radio"]:hover,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover{
      background: var(--gold-color) !important;
      border-color: #FFFFFF !important;
      box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stRadio [role="radio"]:hover p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover p,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover p{
      color: #FFFFFF !important;
    }
    /* наш круглий індикатор під час hover — біла окантовка */
    [data-testid="stSidebar"] .stRadio [role="radio"]:hover::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover::before,
    [data-testid="stSidebar"] [data-baseweb="radio"]:hover::before{
      background: transparent !important;
      box-shadow: 0 0 0 2px #FFFFFF inset !important;
    }

    /* ВИБРАНИЙ пункт — теж «золотий» */
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"]{
      background: var(--gold-color) !important;
      border-color: #FFFFFF !important;
      box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] p,
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] p{
      color: #FFFFFF !important;
    }
    /* індикатор активного — біла «кулька» */
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"]::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"]::before,
    [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"]::before{
      background: #FFFFFF !important;
      box-shadow: 0 0 0 2px #FFFFFF inset !important;
    }
    /* ===== Login selectbox: ліворуч, звужений, з підсвіткою ===== */
    /* ===== Selectbox на екрані входу ===== */
    div[data-baseweb="select"] {
        max-width: 560px;        /* ширина (можеш змінювати під себе) */
        border: 2px solid var(--gold-color) !important;
        border-radius: 12px !important;
        background: rgba(243,146,0,0.05) !important;
        transition: all 0.2s ease;
    }
    
    /* hover */
    div[data-baseweb="select"]:hover {
        border-color: #fff !important;
        background: rgba(243,146,0,0.12) !important;
    }
    
    /* focus */
    div[data-baseweb="select"]:focus-within {
        border-color: var(--gold-color) !important;
        box-shadow: 0 0 0 2px rgba(243,146,0,0.4);
    }
    /* Стилізація кнопки OAuth */
    .uaf-login-button .stButton > button {
        background-color: var(--gold) !important;
        color: #3E3C36 !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: auto !important;
        display: inline-block !important;
    }
    
    .uaf-login-button .stButton > button:hover {
        background-color: #fff !important;
        color: #3E3C36 !important;
    }
    
    .uaf-login-button .stButton > button img {
        vertical-align: middle !important;
        margin-right: 8px !important;
    }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)