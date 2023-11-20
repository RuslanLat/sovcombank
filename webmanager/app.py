import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_option_menu import option_menu
import requests
import folium
import flexpolyline as fp
from streamlit_folium import st_folium
import httpx
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import authenticate as stauth
import json

st.set_page_config(
    page_title="Свокомбанк технологии, Сервис автоматического распределения задач",
    page_icon="images/logo2.png",
    layout="wide",
)  # layout = "wide"

names = ["Manager Manager", "Manager Manager"]
emails = ["admin", "user"]
passwords = ["admin", "user"]

credentials = {
    "usernames": {
        emails[0]: {"name": names[0], "password": "admin"},
        emails[1]: {"name": names[1], "password": "user"},
    }
}

authenticator = stauth.Authenticate(
    credentials, "task_treker", "abcdef", cookie_expiry_days=30
)


def refresh():
    Server.get_current()._reloader.reload()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("css/style.css")

# host = "http://127.0.0.1:8080/"
host = "http://46.243.201.104:8080/"

client = httpx.Client()
data = {"login": "user", "password": "user"}
client.post(host + "user.login", data=data)


def get_todo_list(data):
    r = client.get(
        host + "todo.list",
        params=data,
    )
    df = pd.DataFrame(r.json()["data"]["todos"])

    return df


def get_user_list():
    r = client.get(host + "user.list")
    df = pd.DataFrame(r.json()["data"]["users"])
    return df


styles = {
    "container": {"padding": "0!important", "background-color": "#fafafa"},
    "icon": {
        "color": "#a31b1b",
        "font-size": "20px",
        "--hover-color": "#cccccc",
    },
    "nav-link": {
        "color": "black",
        "font-size": "15px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#cccccc",
    },
    "nav-link-selected": {
        "color": "#ffffff",
        "background-color": "#032480",
    },
}

HERE_API_KEY = "ваш ключ HERE API"

col1, col2, col3 = st.columns([3, 3, 3])
with col2:
    name, authentication_status, username = authenticator.login(
        "Вход в систему", "main"
    )

    if authentication_status == False:
        st.error("Имя пользователя/пароль являются не верными")

    if authentication_status == None:
        st.warning("Введите имя пользователя и пароль")


if authentication_status == True:
    st.markdown(
        f"""
        <style>
            section[data-testid="stSidebar"] .css-ng1t4o {{width: 18rem;}}
            section[data-testid="stSidebar"] .css-1d391kg {{width: 18rem;}}
        </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        image = Image.open("images/logo1.png")
        st.sidebar.image(image, width=200)

        st.sidebar.title(f"Добро пожаловать\n{name}!")
        authenticator.logout("Выйти", "sidebar")
        st.write("##")
        selected = option_menu(
            None,
            ["О программе", "Задача", "Список задач", "Маршрут", "Помощь", "Контакты"],
            icons=[
                "cast",
                "activity",
                "list-task",
                "map",
                "question-circle",
                "envelope-paper",
            ],
            menu_icon="cast",
            default_index=1,
            styles=styles,
        )
    if selected == "О программе":
        st.markdown(
            """Сервис автоматического распределения задач для выездных сотрудников банка.<br>
            Cистема автоматического распределения задач на рабочую неделю<br>
            с построением оптимального маршрута посещения объектов сотрудником банка.""",
            unsafe_allow_html=True,
        )

    if selected == "Задача":
        df_user = get_user_list()
        df_user["full_name"] = (
            df_user["surname"] + " " + df_user["name"] + " " + df_user["patronymic"]
        )
        user_options = df_user["full_name"]
        full_name = st.selectbox(
            label="Cотрудник",
            options=user_options,
            placeholder="Выбирете сотрудника ...",
            index=0,
            help="выбирете сотрудника",
            key="full_name",
        )
        data = {
            "surname": full_name.split()[0],
            "name": full_name.split()[1],
            "patronymic": full_name.split()[2],
        }
        st.write("#### Текущая задача")
        st.divider()
        df = get_todo_list(data)
        problem = df["problem"].iloc[0]
        partner = df["partner"].iloc[0]
        adresse = df["partner_addresse"].iloc[0]
        st.write(f"Задача: {problem}")
        st.write(f"Партнёр: {partner}")
        st.write(f"Адрес: {adresse}")
        st.divider()
        expander2 = st.expander("Памятка")
        expander2.markdown("* выехать на точку")
        expander2.markdown("* стимулировать выдачу")
        text_input = st.text_area("Комментарий", help="оставьте комментарий")
        comlect = st.button("Выполнено", type="primary")
        if comlect:
            client.put(
                host + "todo.update",
                data={
                    "surname": data["surname"],
                    "name": data["name"],
                    "patronymic": data["patronymic"],
                    "partner": partner,
                    "message": text_input,
                },
            )
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    if selected == "Список задач":
        df_user = get_user_list()
        df_user["full_name"] = (
            df_user["surname"] + " " + df_user["name"] + " " + df_user["patronymic"]
        )
        user_options = df_user["full_name"]
        full_name = st.selectbox(
            label="Cотрудник",
            options=user_options,
            placeholder="Выбирете сотрудника ...",
            index=0,
            help="выбирете сотрудника",
            key="full_name",
        )
        data = {
            "surname": full_name.split()[0],
            "name": full_name.split()[1],
            "patronymic": full_name.split()[2],
        }
        st.divider()
        current_data = f"{datetime.now().date():%d-%m-%Y}"
        st.write(f"#### План на {current_data}")
        st.divider()
        df = get_todo_list(data)
        for p, g, m in df[["problem", "partner", "partner_addresse"]].values:
            st.write(f"Задача: {p}")
            st.write(f"Партнёр: {g}")
            st.write(f"Адрес: {m}")
            st.divider()

    if selected == "Маршрут":
        df_user = get_user_list()
        df_user["full_name"] = (
            df_user["surname"] + " " + df_user["name"] + " " + df_user["patronymic"]
        )
        user_options = df_user["full_name"]
        full_name = st.selectbox(
            label="Cотрудник",
            options=user_options,
            placeholder="Выбирете сотрудника ...",
            index=0,
            help="выбирете сотрудника",
            key="full_name",
        )
        data = {
            "surname": full_name.split()[0],
            "name": full_name.split()[1],
            "patronymic": full_name.split()[2],
        }
        st.write("#### Маршрут")
        df = get_todo_list(data)

        # url = "http://api.lbs.yandex.net/geolocation"
        # data = {"common": {
        #             "version": "1.0",
        #             "api_key": "ваш ключ Yandex API Геолокатор",
        #         }
        #     }
        # r = requests.post(url, data={'json': json.dumps(data)}, timeout=5)
        # lat = r.json()["position"]["latitude"]
        # lon = r.json()["position"]["longitude"]
        
        lat = df["lat"].unique()[0]
        lon = df["lon"].unique()[0]
        addrese = df["addresse"].unique()[0]
        url = f"https://router.hereapi.com/v8/routes?origin={lat},{lon}&transportMode=car&destination="
        points_user = df[["partner", "partner_addresse", "partner_lat", "partner_lon"]]
        for i in range(len(points_user)):
            if i == 0:
                url += ",".join([str(points_user.iloc[i]["partner_lat"]), str(points_user.iloc[i]["partner_lon"])])
            else:
                url += "&via=" + ",".join([str(points_user.iloc[i]["partner_lat"]), str(points_user.iloc[i]["partner_lon"])])
        url += f"&return=polyline,summary&apiKey={HERE_API_KEY}"
        r = requests.get(url)
        polylines = r.json()["routes"][0]["sections"]
        polylines = [fp.decode(polyline["polyline"]) for polyline in polylines]
        m = folium.Map(location=[lat, lon], zoom_start=11)
        pushpin = folium.features.CustomIcon(
                "images/logo2.png", icon_size=(30, 30)
            )
        popup = folium.Popup(addrese, max_width=200)
        folium.Marker(
                [lat, lon], tooltip="офис", icon=pushpin, popup=popup
            ).add_to(m)
        for polyline in polylines:
            folium.PolyLine(
                polyline, color="blue", weight=5, tooltip="ваш маршрут на сегодня"
            ).add_to(m)
        for toultip, addrese, lat, lon in points_user.values:
            pushpin = folium.features.CustomIcon(
                "images/khalva.png", icon_size=(30, 30)
            )
            popup = folium.Popup(addrese, max_width=200)
            folium.Marker(
                [lat, lon], tooltip=f"Точка №{toultip}", icon=pushpin, popup=popup
            ).add_to(m)
        st_data = st_folium(m)

    if selected == "Помощь":
        st.link_button(
            "Чат с поддержкой", "https://t.me/sovcom_tech", use_container_width=True
        )
        st.link_button(
            "Позвонить в поддержку", "tel:+7 (495) 745-84-23", use_container_width=True
        )

    if selected == "Контакты":
        st.write("#### Контакты")
        st.divider()
        st.write("Руслан Латипов")
        st.write(
            """
        Python developer 

        Зеленодольск, Татарстан"""
        )
        st.write(
            """<p><img src="data:image/jpeg;base64,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" width="25" height="25" align="middle" /> 
        @rus_lat116</p>""",
            unsafe_allow_html=True,
        )
        st.divider()
        st.write("Юрий Дон")
        st.write(
            """
        Data science 

        Краснодар, Краснодарский край"""
        )

        st.write(
            """<p><img src="data:image/jpeg;base64,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" width="25" height="25" align="middle" /> 
        @Yuriy_Nikitich</p>""",
            unsafe_allow_html=True,
        )
        st.divider()
        st.write("Татьяна Моисеева")
        st.write(
            """
        Data science 

        Москва, Московская область"""
        )

        st.write(
            """<p><img src="data:image/jpeg;base64,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" width="25" height="25" align="middle" /> 
        @Estochka</p>""",
            unsafe_allow_html=True,
        )
