# oauth_google.py
from __future__ import annotations
import os
from typing import Optional

import requests
import streamlit as st
from streamlit_oauth import OAuth2Component

# Google endpoints / scopes
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPE_STR = "openid email profile"  # важливо: один рядок, не список

DEFAULT_ADMIN_EMAILS = {"admin@knu.ua"}  # за потреби змінюй/винеси у secrets

def _cfg():
    """
    Обрати профіль OAuth зі secrets.toml за змінною середовища APP_ENV.
    APP_ENV=prod -> [google_oauth_prod], інакше [google_oauth_dev].
    """
    profile = os.getenv("APP_ENV", "dev")
    key = "google_oauth_prod" if profile == "prod" else "google_oauth_dev"
    try:
        return st.secrets[key]
    except Exception as e:
        st.error(f"Не знайдено секцію [{key}] у .streamlit/secrets.toml")
        raise e


def _google_userinfo_via_button(button_label: str = "Увійти з Google"):

    # Малює кнопку OAuth. Повертає словник userinfo (email, name, ...), коли авторизація завершена.
    # Якщо користувач ще не натискав — повертає None.

    cfg = _cfg()

    oauth2 = OAuth2Component(
        cfg["client_id"],
        cfg["client_secret"],
        GOOGLE_AUTH_URL,
        GOOGLE_TOKEN_URL,
        None,  # refresh_token_endpoint
        None,  # revoke_token_endpoint
    )

    # Перевіряємо, чи є код у query_params (callback від Google)
    code = st.query_params.get("code")
    state = st.session_state.get("oauth_state", str(os.urandom(16).hex()))
    st.session_state["oauth_state"] = state

    if code:
        # Обробка callback
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": cfg["client_id"],
                "client_secret": cfg["client_secret"],
                "redirect_uri": cfg["redirect_uri"],
                "grant_type": "authorization_code",
            }
        ).json()
        if "access_token" in token_response:
            userinfo = requests.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token_response['access_token']}"}
            ).json()
            st.query_params.clear()  # Очищаємо параметри після обробки
            return userinfo
    else:
        # Виклик кнопки для авторизації
        result = oauth2.authorize_button(
            button_label,
            cfg["redirect_uri"],
            GOOGLE_SCOPE_STR,
            pkce="S256",
            icon="https://developers.google.com/identity/images/g-logo.png",
            use_container_width=False,
            key="google_oauth_btn"
        )
        if result and "token" in result:
            token = result["token"]["access_token"]
            userinfo = requests.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token}"}
            ).json()
            return userinfo
    return None


def ensure_login(np_structure_df, admin_emails: Optional[set[str]] = None, admin_pibs: Optional[set[str]] = None):
    if st.session_state.get("logged_in_user"):
        return

    # st.header("Вхід до системи")
    st.info("Увійдіть через Google (домен @knu.ua).")

    userinfo = _google_userinfo_via_button()
    if not userinfo:
        st.stop()

    email = (userinfo.get("email") or "").strip().lower()
    if not email:
        st.error("Не вдалося отримати email від Google.")
        st.stop()

    if not userinfo.get("email_verified", False):
        st.error("Ваш email у Google не верифіковано. Завершіть верифікацію акаунта.")
        st.stop()

    cfg = _cfg()
    allowed_domain = (cfg.get("allowed_domain") or "").lower()
    if allowed_domain and not email.endswith("@" + allowed_domain):
        st.error(f"Доступ дозволено лише для домену @{allowed_domain}. Ваш email: {email}")
        st.stop()

    if "Пошта" not in np_structure_df.columns:
        st.error("У структурі НП відсутня колонка 'Пошта'. Додайте її для авторизації за email.")
        st.stop()

    matches = np_structure_df[np_structure_df["Пошта"].str.lower().fillna("") == email]
    if matches.empty:
        st.error(f"Email {email} не знайдено у переліку НП. Зверніться до адміністратора.")
        st.stop()

    pib = matches.iloc[0]["ПІБ"]
    st.session_state.logged_in_user = pib
    # st.session_state.is_admin = (email in (admin_emails or DEFAULT_ADMIN_EMAILS))
    if admin_pibs:
        st.session_state.is_admin = pib in admin_pibs
    else:
        st.session_state.is_admin = (email in (admin_emails or DEFAULT_ADMIN_EMAILS))

    st.success(f"Вхід успішний. Ви увійшли як: **{pib}**")
    st.rerun()

def logout_button(label: str = "Вийти"):
    if st.sidebar.button(label):
        for k in ("logged_in_user", "is_admin"):
            st.session_state.pop(k, None)
        st.rerun()
