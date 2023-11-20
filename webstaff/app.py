import math
import streamlit as st
import httpx
import json
import pandas as pd
import random
import folium
from streamlit_folium import st_folium, folium_static
from yandex_geocoder import Client

# import streamlit_authenticator as stauth
# import streamlit.components.v1 as components
from PIL import Image
from streamlit_option_menu import option_menu

# from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from st_aggrid import AgGrid, JsCode, ColumnsAutoSizeMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import authenticate as stauth


st.set_page_config(
    page_title="Свокомбанк технологии, Сервис автоматического распределения задач",
    page_icon="images/logo2.png",
    layout="wide",
)  # layout = "wide"

with open("css/AG_GRID_LOCALE_RU.txt", "r") as f:
    AG_CRID_LOCALE_RU = json.load(f)


names = ["Admin Admin", "Admin Admin"]
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


graide_dict = {"Синьор": "1, 2, 3", "Мидл": "2, 3", "Джун": "3"}

office_dict = {
    "Краснодар, Красная, д. 139": "офис_1",
    "Краснодар, В.Н. Мачуги, 41": "офис_2",
    "Краснодар, Красных Партизан, 321": "офис_3",
}


def total_func(row, hours=False):
    if hours:
        res = 0.0
    else:
        res = ""
    if row["функция_3"] == 1:
        if hours:
            res += 1.5
        else:
            res = "1,2,3"
    if row["функция_2"] == 1:
        if hours:
            res += 2
        else:
            res = "1,2"

    if row["функция_1"] == 1:
        if hours:
            res += 4
        else:
            res = "1"

    return res


# def calculate_distance(x1, y1, x2, y2):
#     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#     return distance


# def get_coordinates(addresse):
#     coordinates = client1.coordinates(addresse)

#     return coordinates


def priority_func(data, func):
    df_func = data[data[func] == 1].sort_values(
        by="одобренные но не выданные карты", ascending=False
    )
    # Нахождение максимального и минимального значения в столбце
    max_value = df_func["одобренные но не выданные карты"].max()
    min_value = df_func["одобренные но не выданные карты"].min()

    data[f"приоритет {func}"] = round(
        df_func["одобренные но не выданные карты"].apply(
            lambda x: (x - min_value) / (max_value - min_value) * len(df_func) + 1
        ),
        2,
    )

    return data


# Основная функция распределения точек между офисами и грейдами
def get_coordinate(
    df, num_office, func_list, func_priority, office_numbers, hours_points
):
    # создаем датасета для функциональности 1
    data = df.copy()
    # норма офисов на все офисы выбранного грейда где есть эти грейды по количеству часов
    len_grade = round(office_numbers * 8 / hours_points)
    # количество офисов данного грейда отсортированные по приоритетности с выбранной функцией
    points = data[data[func_list[0]] == 1].sort_values(
        by=func_priority[0], ascending=False
    )
    # если количество часов в офиса больше чем часов положенных на 2 офиса возращаем len_grade, если нет количество офисов с данной функцией
    data_len = (
        len_grade
        if (len(points) * hours_points) > (8 * office_numbers)
        else len(points)
    )

    # количество точек необходимых для данного грейда или сколько есть в датасете
    points = points[:data_len]
    # определяем норму часов на 1 агента
    normal_hours = (
        9
        if len(points) * hours_points >= 8 * office_numbers
        else math.ceil(len(points) * hours_points / office_numbers) + 1
    )

    coordinate = list()
    adress = list()
    task = list()
    lenth = list()
    hours_list = list()
    hours = 0
    df_office_mng = points.sort_values(by=num_office)
    adr = num_office[:-2]
    idx = list()
    i = 0

    # Определяем координаты точек для заданного офиса по главномуу возможному/доступному для грейда приоритету
    while (len(df_office_mng) > 0) and (hours <= normal_hours):
        # присваиваем индекс минимальным растоянием
        index = df_office_mng.index[i]
        hours_agent = df_office_mng.loc[index]["кол-во часов на точке"]
        duration = df_office_mng.loc[index][f"{adr}_y"]

        if (hours + hours_agent + duration) > normal_hours:
            break
        else:
            lat_lon = [df_office_mng.loc[index]["lat"], df_office_mng.loc[index]["lon"]]
            coordinate.append(lat_lon)
            task.append(df_office_mng.loc[index]["кто может ехать"])
            adress_point = df_office_mng.loc[index]["Адрес точки, г. Краснодар"]
            adress.append(adress_point)
            lenth.append(df_office_mng.loc[index][f"{adr}_x"])
            hours = hours + hours_agent + duration
            hours_list.append(hours_agent + duration)
            idx.append(index)
            points = points.drop(index=index)
            data = data.drop(index=index)

            df_office_mng = points.sort_values(by=f"{adress_point}_x")
            adr = adress_point

    # Если часов не достаточно по основному приоритету ищем в приоритете на 1 грейд ниже
    if hours < 9 and len(func_list) > 2:
        points = data[data[func_list[1]] == 1].sort_values(
            by=func_priority[1], ascending=False
        )
        # points['близкий офис'] = points[office_list].idxmin(axis=1)
        df_office_mng = points.sort_values(by=num_office)
        while (len(df_office_mng) > 0) and (hours < normal_hours):
            # присваиваем индекс минимальным растоянием
            index = df_office_mng.index[i]
            hours_agent = df_office_mng.loc[index]["кол-во часов на точке"]
            duration = df_office_mng.loc[index][f"{adr}_y"]
            if (hours + hours_agent + duration) > normal_hours:
                break
            else:
                lat_lon = [
                    df_office_mng.loc[index]["lat"],
                    df_office_mng.loc[index]["lon"],
                ]
                coordinate.append(lat_lon)
                adress_point = df_office_mng.loc[index]["Адрес точки, г. Краснодар"]
                adress.append(adress_point)
                lenth.append(df_office_mng.loc[index][f"{adr}_x"])
                task.append(df_office_mng.loc[index]["кто может ехать"])
                hours = hours + hours_agent + duration
                hours_list.append(hours_agent + duration)

                idx.append(index)
                data = data.drop(index=index)
                points = points.drop(index=index)

                df_office_mng = points.sort_values(by=f"{adress_point}_x")
                adr = adress_point

    # Если часов не достаточно по основному приоритету ищем в приоритете на 2 грейда ниже
    if hours < 9 and len(func_list) > 2:
        points = data[data[func_list[2]] == 1].sort_values(
            by=func_priority[2], ascending=False
        )
        # points['близкий офис'] = points[office_list].idxmin(axis=1)
        df_office_mng = points.sort_values(by=num_office)

        while (len(df_office_mng) != 0) and (hours < normal_hours):
            # присваиваем индекс минимальным растоянием
            index = df_office_mng.index[i]
            hours_agent = df_office_mng.loc[index]["кол-во часов на точке"]
            duration = df_office_mng.loc[index][f"{adr}_y"]
            if (hours + hours_agent + duration) >= normal_hours:
                break
            else:
                lat_lon = [
                    df_office_mng.loc[index]["lat"],
                    df_office_mng.loc[index]["lon"],
                ]
                coordinate.append(lat_lon)
                adress_point = df_office_mng.loc[index]["Адрес точки, г. Краснодар"]
                adress.append(adress_point)
                lenth.append(df_office_mng.loc[index][f"{adr}_x"])
                task.append(df_office_mng.loc[index]["кто может ехать"])
                hours = hours + hours_agent + duration
                hours_list.append(hours_agent + duration)

                idx.append(index)

                data = data.drop(index=index)
                points = points.drop(index=index)

                df_office_mng = points.sort_values(by=f"{adress_point}_x")
                adr = adress_point

    return {
        "hours": hours_list,
        "coordinate": coordinate,
        "task": task,
        "adress": adress,
        "lenth": lenth,
        "idx": idx,
    }


# Для добавления значений в датасет агентов
def put_data(df, manager, hours, lenth, coordinate, task, adress):
    df.loc[df["ФИО"] == manager, "часы работы"] = sum(hours)
    df.loc[df["ФИО"] == manager, "список времени"] = df.loc[
        df["ФИО"] == manager, "список времени"
    ].map(lambda x: hours)
    df.loc[df["ФИО"] == manager, "общее растояние (км)"] = sum(lenth)
    df.loc[df["ФИО"] == manager, "список растояние (км)"] = df.loc[
        df["ФИО"] == manager, "список растояние (км)"
    ].map(lambda x: lenth)
    df.loc[df["ФИО"] == manager, "куда ехать координаты"] = df.loc[
        df["ФИО"] == manager, "куда ехать координаты"
    ].map(lambda x: coordinate)
    df.loc[df["ФИО"] == manager, "куда ехать адрес"] = df.loc[
        df["ФИО"] == manager, "куда ехать адрес"
    ].map(lambda x: adress)
    df.loc[df["ФИО"] == manager, "задачи на точке"] = df.loc[
        df["ФИО"] == manager, "задачи на точке"
    ].map(lambda x: list(map(replace_value, task)))
    return df


if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        columns=[
            "№ точки",
            "Наименование города",
            "Адрес",
            "Карты и материалы доставлены?",
            "Кол-во дней после выдачи последней карты",
            "Кол-во одобренных заявок",
            "Кол-во выданных карт",
        ]
    )

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


def get_rank_list():
    r = client.get(host + "rank.list")

    df = pd.DataFrame(r.json()["data"]["ranks"]).rename(
        columns={"rank": "Наименование грейда"}
    )

    return df


def get_position_list():
    r = client.get(host + "position.list")
    df = pd.DataFrame(r.json()["data"]["positions"]).rename(
        columns={"position": "Наименование должности"}
    )
    return df


def get_user_list():
    r = client.get(host + "user.list")
    df = pd.DataFrame(r.json()["data"]["users"]).rename(
        columns={"surname": "Фамилия", "name": "Имя", "patronymic": "Отчество"}
    )

    return df


def get_job_list():
    r = client.get(host + "job.list")
    df = pd.DataFrame(r.json()["data"]["user_jobs"]).rename(
        columns={
            "name": "Имя",
            "surname": "Фамилия",
            "position": "Должность",
            "rank": "Грейд",
            "city": "Город",
            "addresse": "Адрес",
            "lon": "Долгота",
            "lat": "Широта",
            "patronymic": "Отчество",
        }
    )
    return df


def get_partner_list():
    r = client.get(host + "partner.list")
    df = pd.DataFrame(r.json()["data"]["partners"]).rename(
        columns={
            "partner": "Номер точки",
            "data_connect": "Когда подключена",
            "city": "Наименование города",
            "addresse": "Адрес",
            "lat": "Долгота",
            "lon": "Широта",
        }
    )
    return df


def get_partner_param_list():
    r = client.get(host + "partner.param.list")
    df = pd.DataFrame(r.json()["data"]["partner_params"]).rename(
        columns={
            "created_at": "Дата создания записи",
            "partner": "Номер точки",
            "data_connect": "Когда подключена",
            "city": "Наименование города",
            "addresse": "Адрес",
            "delivered": "Карты и материалы доставлены?",
            "num_days": "Кол-во дней после выдачи последней карты",
            "num_applications": "Кол-во одобренных заявок",
            "num_cards": "Кол-во выданных карт",
        }
    )
    return df


def get_product_list():
    r = client.get(host + "product.list")
    df = pd.DataFrame(r.json()["data"]["products"]).rename(
        columns={"product": "Содержание задачи", "description": "Памятка"}
    )
    return df


def get_addresse_list():
    r = client.get(host + "addresse.list")
    df = pd.DataFrame(r.json()["data"]["addresses"])
    return df


def get_problem_list():
    r = client.get(host + "problem.list")
    df = pd.DataFrame(r.json()["data"]["problems"]).rename(
        columns={
            "problem_type": "Тип",
            "problem": "Название задачи",
            "priority": "Приоритет",
            "lead_time": "Время выполнения",
            "condition_one": "Условие назначения 1",
            "condition_two": "Условие назначения 2",
            "rank": "Требуемый уровень сотрудника",
        }
    )

    return df


def get_office_list():
    r = client.get(host + "office.list")
    df = pd.DataFrame(r.json()["data"]["offices"]).rename(
        columns={
            "city": "Наименование города",
            "addresse": "Адрес",
            "lat": "Долгота",
            "lon": "Широта",
        }
    )
    return df


def make_form(form_name, pars_field):
    position_form = st.form(form_name)

    if pars_field == "грейд":
        label = position_form.text_input(
            label=f"Добавить/удалить {pars_field}",
            placeholder=f"Введите наименование {pars_field}а ...",
            help=f"введите наименование {pars_field}а",
        )
    else:
        label = position_form.text_input(
            label=f"Добавить/удалить {pars_field}ь",
            placeholder=f"Введите наименование {pars_field}и ...",
            help=f"введите наименование {pars_field}и",
        )
    submitted1 = position_form.radio(
        "Добавить/удалить",
        ["Добавить", "Удалить"],
        horizontal=True,
        label_visibility="collapsed",
    )
    submitted = position_form.form_submit_button("сохранить")

    return position_form, label, submitted, submitted1


def plot_table(df, key):
    gd = GridOptionsBuilder.from_dataframe(df, columns_auto_size_mode=0)
    gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True)
    # for colname in df.columns:
    #     gd.configure_columns(colname, wrapText=True)
    #     gd.configure_columns(colname, autoHeight=True)
    gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
    gd.configure_default_column(editable=True)
    gd.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=10,
    )
    gridoptions = gd.build()

    aggrid = AgGrid(
        df,
        gridOptions=gridoptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        theme="alpine",
        key=key,
    )
    return aggrid


def plot_change_table(df, key):
    js = JsCode(
        """
            function(e) {
                let api = e.api;     
                let sel = api.getSelectedRows();
                api.applyTransaction({remove: sel});
            };
            """
    )

    gd = GridOptionsBuilder.from_dataframe(df, columns_auto_size_mode=0)
    gd.configure_pagination(
        enabled=True, paginationAutoPageSize=False, paginationPageSize=10
    )
    gd.configure_grid_options(stopEditingWhenCellsLoseFocus=True)  # , rowHeight=80
    gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    gd.configure_grid_options(onRowSelected=js, pre_selected_rows=[])
    gridoptions = gd.build()
    grid_table = AgGrid(
        df,
        gridOptions=gridoptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme="alpine",
        key=key,
    )

    return grid_table


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("css/style.css")

col1, col2, col3 = st.columns([3, 3, 3])
with col2:
    name, authentication_status, username = authenticator.login(
        "Вход в систему", "main"
    )

    if authentication_status == False:
        st.error("Имя пользователя/пароль являются не верными")

    if authentication_status == None:
        st.warning("Введите имя пользователя и пароль")

col1, col2, col3 = st.columns([2, 3, 2])
if authentication_status == True:
    # st.markdown(
    #     f"""
    #     <style>
    #         section[data-testid="stSidebar"] .css-ng1t4o {{width: 41rem;}}
    #         section[data-testid="stSidebar"] .css-1d391kg {{width: 41rem;}}
    #     </style>
    # """,
    #     unsafe_allow_html=True,
    # )

    with st.sidebar:
        image = Image.open("images/logo1.png")
        st.sidebar.image(image, width=200)

        st.sidebar.title(f"Добро пожаловать\n{name}!")
        authenticator.logout("Выйти", "sidebar")
        st.write("##")
        selected = option_menu(
            None,
            ["О программе", "Справочники", "Задачи", "Аналитика", "Контакты"],
            icons=["cast", "database", "list-task", "bar-chart", "envelope-paper"],
            menu_icon="cast",
            default_index=0,
            styles=styles,
        )

    # host = "http://127.0.0.1:8080/"
    host = "http://46.243.201.104:8080/"

    client = httpx.Client()
    data = {"login": "user", "password": "user"}
    client.post(host + "user.login", data=data)

    if selected == "О программе":
        st.markdown(
            """Сервис автоматического распределения задач для выездных сотрудников банка.<br>
            Система автоматического распределения задач на рабочую неделю<br>
            с построением оптимального маршрута посещения объектов сотрудником банка.""",
            unsafe_allow_html=True,
        )

    if selected == "Справочники":
        with st.expander("Филиалы"):
            col1, col2, col3 = st.columns(3)
            with col2:
                branch_form = st.form("branch_form")
                branch_form.write("Добавить/удалить филиал")
                city = branch_form.text_input(
                    label="Наименование города",
                    placeholder="Введите наименование города ...",
                    help="введите наименование города",
                    key="city",
                )
                addresse = branch_form.text_input(
                    label="Адресс",
                    placeholder="Введите адрес ...",
                    help="введите адрес",
                    key="addresse",
                )
                submitted1 = branch_form.radio(
                    "Добавить/удалить",
                    ["Добавить", "Удалить"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                submitted = branch_form.form_submit_button("сохранить")

            col1, col2, col3 = st.columns((1, 3, 1))
            with col2:
                if submitted and submitted1 == "Добавить":
                    client.post(
                        host + "addresse.add", data={"city": city, "addresse": addresse}
                    )
                    client.post(
                        host + "office.add", data={"city": city, "addresse": addresse}
                    )
                    df = get_office_list()
                    aggrid = plot_table(df, key="1a")
                elif submitted and submitted1 == "Удалить":
                    client.delete(
                        host + "office.delete",
                        params={"city": city, "addresse": addresse},
                    )
                    df = get_office_list()
                    aggrid = plot_table(df, key="1b")
                else:
                    df = get_office_list()
                    aggrid = plot_table(df, key="1c")

        with st.expander("Персонал"):
            selected2 = option_menu(
                None,
                ["Должности", "Грейды", "Сотрудники", "Штат"],
                icons=["layers", "view-list", "people", "diagram-3"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles=styles,
            )
            if selected2 == "Должности":
                col1, col2, col3 = st.columns(3)
                with col2:
                    position_form, label, submitted, submitted1 = make_form(
                        "position_form", "должност"
                    )
                    if submitted and submitted1 == "Добавить":
                        client.post(host + "position.add", data={"position": label})
                        df = get_position_list()
                        aggrid = plot_table(df, key="2a")
                    elif submitted and submitted1 == "Удалить":
                        client.delete(
                            host + "position.delete", params={"position": label}
                        )
                        df = get_position_list()
                        aggrid = plot_table(df, key="2b")
                    else:
                        df = get_position_list()
                        aggrid = plot_table(df, key="2c")
            if selected2 == "Грейды":
                col1, col2, col3 = st.columns(3)
                with col2:
                    position_form, label, submitted, submitted1 = make_form(
                        "rank_form", "грейд"
                    )
                    if submitted and submitted1 == "Добавить":
                        client.post(host + "rank.add", data={"rank": label})
                        df = get_rank_list()
                        aggrid = plot_table(df, key="3a")
                    elif submitted and submitted1 == "Удалить":
                        client.delete(host + "rank.delete", params={"rank": label})
                        df = get_rank_list()
                        aggrid = plot_table(df, key="3b")
                    else:
                        df = get_rank_list()
                        aggrid = plot_table(df, key="3c")
            if selected2 == "Сотрудники":
                col1, col2, col3 = st.columns(3)
                with col2:
                    user_form = st.form("user_form")
                    user_form.write("Добавить/удалить сотрудника")
                    surname = user_form.text_input(
                        label="Фамилия сотрудника",
                        placeholder="Введите фамилию сотрудника ...",
                        help="введите фамилию сотрудника",
                        key="surname",
                    )
                    name = user_form.text_input(
                        label="Имя сотрудника",
                        placeholder="Введите имя сотрудника ...",
                        help="введите имя сотрудника",
                        key="name",
                    )
                    patronymic = user_form.text_input(
                        label="Отчество сотрудника",
                        placeholder="Введите отчество сотрудника ...",
                        help="введите отчество сотрудника",
                        key="patronymic",
                    )
                    submitted1 = user_form.radio(
                        "Добавить/удалить",
                        ["Добавить", "Удалить"],
                        horizontal=True,
                        label_visibility="collapsed",
                    )
                    submitted = user_form.form_submit_button("сохранить")

                    if submitted and submitted1 == "Добавить":
                        client.post(
                            host + "user.add",
                            data={
                                "surname": surname,
                                "name": name,
                                "patronymic": patronymic,
                            },
                        )
                        df = get_user_list()
                        aggrid = plot_table(df, key="4a")
                    elif submitted and submitted1 == "Удалить":
                        client.delete(
                            host + "user.delete",
                            params={
                                "surname": surname,
                                "name": name,
                                "patronymic": patronymic,
                            },
                        )
                        df = get_user_list()
                        aggrid = plot_table(df, key="4b")
                    else:
                        df = get_user_list()
                        aggrid = plot_table(df, key="4c")
            if selected2 == "Штат":
                col1, col2, col3 = st.columns(3)
                with col2:
                    job_form = st.form("job_form")
                    job_form.write("Добавить/удалить сотрудника")

                    df_user = get_user_list()
                    df_user["full_name"] = (
                        df_user["Фамилия"]
                        + " "
                        + df_user["Имя"]
                        + " "
                        + df_user["Отчество"]
                    )
                    user_options = df_user["full_name"]
                    rank_options = get_rank_list()["Наименование грейда"]
                    position_options = get_position_list()["Наименование должности"]
                    df_office = get_office_list()
                    df_office["office"] = (
                        df_office["Наименование города"] + ", " + df_office["Адрес"]
                    )
                    office_options = df_office["office"]

                    full_name = job_form.selectbox(
                        label="Cотрудник",
                        options=user_options,
                        placeholder="Выбирете сотрудника ...",
                        index=None,
                        help="выбирете сотрудника",
                        key="full_name",
                    )
                    office_job = job_form.selectbox(
                        label="Локация",
                        options=office_options,
                        placeholder="Выбирете локацию сотрудника ...",
                        index=None,
                        help="выбирете локацию сотрудника",
                        key="office_job",
                    )
                    position = job_form.selectbox(
                        label="Должность сотрудника",
                        options=position_options,
                        index=None,
                        placeholder="Выбирете должность сотрудника ...",
                        help="выбирете должность сотрудника",
                        key="position",
                    )
                    rank = job_form.selectbox(
                        label="Грейд сотрудника",
                        options=rank_options,
                        index=None,
                        placeholder="Выбирете грейд сотрудника ...",
                        help="выбирете грейд сотрудника",
                        key="rank",
                    )
                    submitted1 = job_form.radio(
                        "Добавить/удалить",
                        ["Добавить", "Удалить"],
                        horizontal=True,
                        label_visibility="collapsed",
                    )
                    submitted = job_form.form_submit_button("сохранить")

                if submitted and submitted1 == "Добавить":
                    client.post(
                        host + "job.id.add",
                        data={
                            "surname": full_name.split()[0],
                            "name": full_name.split()[1],
                            "patronymic": full_name.split()[2],
                            "city": office_job.split(", ")[0],
                            "addresse": ", ".join(office_job.split(", ")[1:]),
                            "rank": rank,
                            "position": position,
                        },
                    )
                    df = get_job_list()
                    aggrid = plot_table(df, key="5a")
                elif submitted and submitted1 == "Удалить":
                    client.delete(
                        host + "job.delete",
                        params={
                            "surname": full_name.split()[0],
                            "name": full_name.split()[1],
                            "patronymic": full_name.split()[2],
                        },
                    )
                    df = get_job_list()
                    aggrid = plot_table(df, key="5b")
                else:
                    df = get_job_list()
                    aggrid = plot_table(df, key="5c")
        with st.expander("Партнёры"):
            col1, col2, col3 = st.columns(3)
            with col2:
                partner_form = st.form("partner_form")
                partner_form.write("Добавить/удалить филиал")
                partner = partner_form.text_input(
                    label="Номер точки",
                    placeholder="Введите номер точки ...",
                    help="введите номер точки",
                    key="partner",
                )
                data_connect = partner_form.text_input(
                    label="Когда подключена точка",
                    placeholder="Введите когда подключена точка ...",
                    help="введите когда подключена точка",
                    key="data_connect",
                )
                city_partner = partner_form.text_input(
                    label="Наименование города",
                    placeholder="Введите наименование города ...",
                    help="введите наименование города",
                    key="city_partner",
                )
                addresse_partner = partner_form.text_input(
                    label="Адресс",
                    placeholder="Введите адрес ...",
                    help="введите адрес",
                    key="addresse_partner",
                )
                submitted1 = partner_form.radio(
                    "Добавить/удалить",
                    ["Добавить", "Удалить"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                submitted = partner_form.form_submit_button("сохранить")
            if submitted and submitted1 == "Добавить":
                client.post(
                    host + "addresse.add",
                    data={"city": city_partner, "addresse": addresse_partner},
                )
                client.post(
                    host + "partner.add",
                    data={
                        "partner": partner,
                        "data_connect": data_connect,
                        "city": city_partner,
                        "addresse": addresse_partner,
                    },
                )
                df = get_partner_list()
                aggrid = plot_table(df, key="6a")
            elif submitted and submitted1 == "Удалить":
                client.delete(host + "partner.delete", params={"partner": partner})
                df = get_partner_list()
                aggrid = plot_table(df, key="6b")
            else:
                df = get_partner_list()
                aggrid = plot_table(df, key="6c")

        with st.expander("Задачи"):
            col1, col2, col3 = st.columns(3)
            with col2:
                problem_form = st.form("problem_form")
                problem_form.write("Добавить/удалить задачу")

                problem_type = problem_form.text_input(
                    label="Тип задачи",
                    placeholder="Введите тип задачи ...",
                    help="введите тип задачи",
                    key="problem_type",
                )
                problem = problem_form.text_input(
                    label="Название задачи",
                    placeholder="Введите название задачи ...",
                    help="введите название задачи",
                    key="problem",
                )
                priority = problem_form.text_input(
                    label="Приоритет",
                    placeholder="Введите приоритет ...",
                    help="введите приоритет",
                    key="priority",
                )
                lead_time = problem_form.text_input(
                    label="Время выполнения",
                    placeholder="Введите время выполнения ...",
                    help="введите время выполнения",
                    key="lead_time",
                )
                condition_one = problem_form.text_input(
                    label="Условное значение 1",
                    placeholder="Введите условное значение 1 ...",
                    help="введите условное значение 1",
                    key="condition_one",
                )
                condition_two = problem_form.text_input(
                    label="Условное значение 2",
                    placeholder="Введите условное значение 2 ...",
                    help="введите условное значение 2",
                    key="condition_two",
                )
                rank_type = problem_form.text_input(
                    label="Требуемый уровень сотрудника",
                    placeholder="Введите требуемый уровень сотрудника ...",
                    help="введите требуемый уровень сотрудника",
                    key="rank_type",
                )
                submitted1 = problem_form.radio(
                    "Добавить/удалить",
                    ["Добавить", "Удалить"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                submitted = problem_form.form_submit_button("сохранить")

            if submitted and submitted1 == "Добавить":
                client.post(
                    host + "problem.add",
                    data={
                        "problem_type": int(problem_type),
                        "problem": problem,
                        "priority": priority,
                        "lead_time": lead_time,
                        "condition_one": condition_one,
                        "condition_two": condition_two,
                        "rank": rank_type,
                    },
                )
                df = get_problem_list()
                aggrid = plot_table(df, key="7a")
            elif submitted and submitted1 == "Удалить":
                client.delete(
                    host + "problem.delete",
                    params={"problem": problem},
                )
                df = get_problem_list()
                aggrid = plot_table(df, key="7b")
            else:
                df = get_problem_list()
                aggrid = plot_table(df, key="7c")

    if selected == "Задачи":
        selected2 = option_menu(
            None,
            ["Загрузка файла", "Ручной ввод", "Из базы данных"],
            icons=["file-earmark-excel", "receipt", "cloud-download"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles=styles,
        )
        if selected2 == "Загрузка файла":
            col1, col2, col3 = st.columns(3)
            with col2:
                uploaded_file = st.file_uploader(
                    "Загрузка файла", type=["xls", "xlsx"], help="загрузите файл"
                )
            if uploaded_file:
                df_points = pd.read_excel(uploaded_file, sheet_name=0, na_filter=True)
                df_points = df_points.drop(index=[16, 17])

                js = JsCode(
                    """
            function(e) {
                let api = e.api;     
                let sel = api.getSelectedRows();
                api.applyTransaction({remove: sel});
            };
            """
                )

                gd = GridOptionsBuilder.from_dataframe(
                    df_points, columns_auto_size_mode=0
                )
                gd.configure_pagination(
                    enabled=True, paginationAutoPageSize=False, paginationPageSize=10
                )
                gd.configure_grid_options(
                    stopEditingWhenCellsLoseFocus=True
                )  # , rowHeight=80
                gd.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
                gd.configure_default_column(editable=True, groupable=True)
                gd.configure_selection(selection_mode="multiple", use_checkbox=True)
                gd.configure_grid_options(onRowSelected=js, pre_selected_rows=[])
                gridoptions = gd.build()
                grid_table = AgGrid(
                    df_points,
                    gridOptions=gridoptions,
                    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    allow_unsafe_jscode=True,
                    theme="alpine",
                )

                df_addresse = get_addresse_list()

                df_addresse["Адрес локации"] = (
                    df_addresse["city"] + ", " + df_addresse["addresse"]
                )
                predict = st.button("Спланировать задачи")
                if predict:
                    df_manager = pd.read_excel(uploaded_file, sheet_name=2)
                    df_manager["функции"] = df_manager["Грейд"].map(graide_dict)
                    df_manager["офис"] = df_manager["Адрес локации"].map(office_dict)
                    df_manager = df_manager.merge(df_addresse, on="Адрес локации")

                    # df_manager["coordinates"] = df_manager["Адрес локации"].map(
                    #     lambda x: client1.coordinates(x)
                    # )
                    # df_manager["lat"] = df_manager.coordinates.map(lambda x: x[1])
                    # df_manager["lon"] = df_manager.coordinates.map(lambda x: x[0])
                    df_manager["часы работы"] = 0
                    df_manager["список времени"] = [[] for _ in range(len(df_manager))]
                    df_manager["общее растояние (км)"] = 0
                    df_manager["список растояние (км)"] = [
                        [] for _ in range(len(df_manager))
                    ]
                    df_manager["куда ехать адрес"] = [
                        [] for _ in range(len(df_manager))
                    ]
                    df_manager["куда ехать координаты"] = [
                        [] for _ in range(len(df_manager))
                    ]
                    df_manager["задачи на точке"] = [[] for _ in range(len(df_manager))]

                    df_points1 = grid_table.data
                    df_points1["одобренные но не выданные карты"] = (
                        df_points1["Кол-во одобренных заявок"]
                        - df_points1["Кол-во выданных карт"]
                    )
                    df_points1["переход со вчерашнего дня"] = 0
                    df_points1["функция_1"] = (
                        (
                            (df_points1["Кол-во дней после выдачи последней карты"] > 7)
                            & (df_points1["Кол-во одобренных заявок"] > 0)
                        )
                        | (df_points1["Кол-во дней после выдачи последней карты"] > 14)
                    ) * 1
                    df_points1.loc[5, "функция_1"] = 0

                    df_points1["функция_2"] = (
                        (df_points1["Кол-во выданных карт"] > 0)
                        & (
                            df_points1["Кол-во выданных карт"]
                            / df_points1["Кол-во одобренных заявок"]
                            < 0.5
                        )
                    ) * 1
                    df_points1["функция_3"] = (
                        (df_points1["Когда подключена точка?"] == "вчера")
                        | (df_points1["Карты и материалы доставлены?"] == "нет")
                    ) * 1

                    df_points1["кто может ехать"] = df_points1[
                        ["функция_1", "функция_2", "функция_3"]
                    ].apply(total_func, axis=1)
                    df_points1["кол-во часов на точке"] = df_points1[
                        ["функция_1", "функция_2", "функция_3"]
                    ].apply(lambda x: total_func(x, hours=True), axis=1)

                    df_points1 = df_points1.merge(
                        df_addresse,
                        left_on="Адрес точки, г. Краснодар",
                        right_on="addresse",
                    )

                    # df_points1["coordinates"] = df_points1[
                    #     "Адрес точки, г. Краснодар"
                    # ].map(lambda x: client1.coordinates(f"Краснодар, {x}"))
                    # df_points1["lat"] = df_points1.coordinates.map(lambda x: x[1])
                    # df_points1["lon"] = df_points1.coordinates.map(lambda x: x[0])

                    df_pivot_length = pd.read_csv("data/4_ver_df_pivot_length.csv")
                    df_pivot_dur = pd.read_csv("data/4_ver_df_pivot_dur.csv")
                    # Удаляем не коректные адреса

                    df_points1 = pd.merge(
                        df_points1,
                        df_pivot_length,
                        on="Адрес точки, г. Краснодар",
                        how="inner",
                    )
                    df_points1 = pd.merge(
                        df_points1,
                        df_pivot_dur,
                        on="Адрес точки, г. Краснодар",
                        how="inner",
                    )

                    for col in ["функция_1", "функция_2", "функция_3"]:
                        df_points1 = priority_func(df_points1, col)
                        df_points1 = df_points1.fillna(0.0)

                    # df_points1 = df_points1[df_points1["функция_3"] == 1].sort_values(
                    #     by="приоритет функция_3", ascending=False
                    # )

                    #             df_points1["офис_1"] = df_points1[["lat", "lon"]].apply(
                    #                 lambda x: calculate_distance(
                    #                     38.977047, 45.04496, float(x.lon), float(x.lat)
                    #                 ),
                    #                 axis=1,
                    #             )
                    #             df_points1["офис_2"] = df_points1[["lat", "lon"]].apply(
                    #                 lambda x: calculate_distance(
                    #                     39.071711, 45.012835, float(x.lon), float(x.lat)
                    #                 ),
                    #                 axis=1,
                    #             )
                    #             df_points1["офис_3"] = df_points1[["lat", "lon"]].apply(
                    #                 lambda x: calculate_distance(
                    #                     38.941986, 45.053773, float(x.lon), float(x.lat)
                    #                 ),
                    #                 axis=1,
                    #             )

                    task_dict = {
                        "1": "Выезд на точку для стимулирования выдач",
                        "1,2": "Обучение агента",
                        "1,2,3": "Доставка карт и материалов",
                    }

                    def replace_value(value):
                        return task_dict.get(value, value)

                    # Офис 1S
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_1_x",
                        func_list=["функция_1", "функция_2", "функция_3"],
                        func_priority=[
                            "приоритет функция_1",
                            "приоритет функция_2",
                            "приоритет функция_3",
                        ],
                        office_numbers=2,
                        hours_points=4,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_1")
                        & (df_manager["Грейд"] == "Синьор"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )
                    # Офис 2S
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_2_x",
                        func_list=["функция_1", "функция_2", "функция_3"],
                        func_priority=[
                            "приоритет функция_1",
                            "приоритет функция_2",
                            "приоритет функция_3",
                        ],
                        office_numbers=1,
                        hours_points=4,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_2")
                        & (df_manager["Грейд"] == "Синьор"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )
                    # Офис 1M
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_1_x",
                        func_list=["функция_2", "функция_3"],
                        func_priority=["приоритет функция_2", "приоритет функция_3"],
                        office_numbers=3,
                        hours_points=2,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_1")
                        & (df_manager["Грейд"] == "Мидл"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )

                    # Офис 2M
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_2_x",
                        func_list=["функция_2", "функция_3"],
                        func_priority=["приоритет функция_2", "приоритет функция_3"],
                        office_numbers=2,
                        hours_points=2,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_2")
                        & (df_manager["Грейд"] == "Мидл"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )

                    # Офис 3M
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_3_x",
                        func_list=["функция_2", "функция_3"],
                        func_priority=["приоритет функция_2", "приоритет функция_3"],
                        office_numbers=1,
                        hours_points=2,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_3")
                        & (df_manager["Грейд"] == "Мидл"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )

                    # Офис 1D
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_1_x",
                        func_list=["функция_3"],
                        func_priority=["приоритет функция_3"],
                        office_numbers=3,
                        hours_points=1.5,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_1")
                        & (df_manager["Грейд"] == "Джун"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )

                    # Офис 2D
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_2_x",
                        func_list=["функция_3"],
                        func_priority=["приоритет функция_3"],
                        office_numbers=2,
                        hours_points=1.5,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_2")
                        & (df_manager["Грейд"] == "Джун"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )
                    # Офис 3D
                    vals_dicts = get_coordinate(
                        df=df_points1,
                        num_office="офис_3_x",
                        func_list=["функция_3"],
                        func_priority=["приоритет функция_3"],
                        office_numbers=1,
                        hours_points=1.5,
                    )
                    df_points1 = df_points1.drop(index=vals_dicts["idx"])
                    manager = df_manager.loc[
                        (df_manager["офис"] == "офис_3")
                        & (df_manager["Грейд"] == "Джун"),
                        "ФИО",
                    ].values[0]
                    df_manager = put_data(
                        df=df_manager,
                        manager=manager,
                        hours=vals_dicts["hours"],
                        lenth=vals_dicts["lenth"],
                        coordinate=vals_dicts["coordinate"],
                        task=vals_dicts["task"],
                        adress=vals_dicts["adress"],
                    )

                    st.write("### План задач менеджерам")

                    df_test = df_manager[
                        [
                            "ФИО",
                            "Адрес локации",
                            "Грейд",
                            "список времени",
                            "список растояние (км)",
                            "куда ехать адрес",
                            "задачи на точке",
                        ]
                    ]
                    new_data = []
                    Q = 1
                    for fullname, adresse, rank, time_list, durachion_list, get_point, tasks in df_test.values:
                        for time, durachion, point, task in zip(time_list, durachion_list, get_point, tasks):
                            new_data.append([fullname, adresse, rank, time, durachion, point, Q, task])
                            Q += 1
                        Q = 1    
                    df_final = pd.DataFrame(new_data, columns=[
                            "ФИО",
                            "Адрес локации",
                            "Грейд",
                            "Время на задачу",
                            "Расстояние (км)",
                            "Адес партнёра",
                            "Приоритет",
                            "Задача",
                        ])
                    gd1 = GridOptionsBuilder.from_dataframe(
                        df_final, columns_auto_size_mode=0
                    )
                    gd1.configure_pagination(
                        enabled=True,
                        paginationAutoPageSize=False,
                        paginationPageSize=10,
                    )
                    # for colname in df_final.columns:
                    #     gd1.configure_columns(colname, wrapText=True)
                    #     gd1.configure_columns(colname, autoHeight=True)
                    gd1.configure_grid_options(
                        stopEditingWhenCellsLoseFocus=True
                    )  # , rowHeight=80
                    gd1.configure_grid_options(localeText=AG_CRID_LOCALE_RU)
                    gd1.configure_default_column(editable=True, groupable=True)
                    gd1.configure_selection(
                        selection_mode="multiple", use_checkbox=True
                    )
                    gd1.configure_grid_options(onRowSelected=js, pre_selected_rows=[])
                    gridoptions = gd1.build()
                    grid_table1 = AgGrid(
                        df_final,
                        gridOptions=gridoptions,
                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        allow_unsafe_jscode=True,
                        theme="alpine",
                    )

        if selected2 == "Ручной ввод":
            df = pd.DataFrame(
                columns=[
                    "№ точки",
                    "Наименование города",
                    "Адрес",
                    "Карты и материалы доставлены?",
                    "Кол-во дней после выдачи последней карты",
                    "Кол-во одобренных заявок",
                    "Кол-во выданных карт",
                ]
            )
            col1, col2, col3 = st.columns(3)
            with col2:
                partner_param_form = st.form("partner_param_form")
                partner_param_form.write("Добавить критерии партнёра")
                partner = get_partner_list()
                partner["partner_param_options"] = (
                    partner["Номер точки"]
                    + ", "
                    + partner["Наименование города"]
                    + ", "
                    + partner["Адрес"]
                )
                partner = partner_param_form.selectbox(
                    label="Партнер",
                    options=partner["partner_param_options"],
                    placeholder="Введите партнёра ...",
                    index=None,
                    help="введите партнёра",
                    key="full_name",
                )
                delivered = partner_param_form.toggle(
                    label="Карты и материалы доставлены?",
                    help="карты и материалы доставлены?",
                    key="delivered",
                )
                num_days = partner_param_form.number_input(
                    label="Кол-во дней после выдачи последней карты",
                    min_value=0,
                    step=1,
                    help="введите кол-во дней после выдачи последней карты",
                    key="num_days",
                )
                num_applications = partner_param_form.number_input(
                    label="Кол-во одобренных заявок",
                    min_value=0,
                    step=1,
                    help="введите кол-во одобренных заявок",
                    key="num_applications",
                )
                num_cards = partner_param_form.number_input(
                    label="Кол-во выданных карт",
                    min_value=0,
                    step=1,
                    help="введите кол-во выданных карт",
                    key="num_cards",
                )
                submitted1 = partner_param_form.radio(
                    "Добавить/Очистить данные",
                    ["Добавить", "Очистить данные"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                submitted = partner_param_form.form_submit_button("сохранить")
            if submitted and submitted1 == "Добавить":
                df.loc[df.shape[0]] = [
                    partner,
                    partner,
                    partner,
                    delivered,
                    num_days,
                    num_applications,
                    num_cards,
                ]

                st.session_state.df = pd.concat([st.session_state.df, df])

                aggrid = plot_table(
                    st.session_state.df, key=random.randint(10, 20000000)
                )
            elif submitted and submitted1 == "Очистить данные":
                st.session_state.df = pd.DataFrame(
                    columns=[
                        "№ точки",
                        "Наименование города",
                        "Адрес",
                        "Карты и материалы доставлены?",
                        "Кол-во дней после выдачи последней карты",
                        "Кол-во одобренных заявок",
                        "Кол-во выданных карт",
                    ]
                )
            else:
                aggrid = plot_table(st.session_state.df, key=8)

        if selected2 == "Из базы данных":
            df = get_partner_param_list()
            aggrid = plot_change_table(df, key=9)

    if selected == "Аналитика":
        st.write("### Анализ выполнения плана задач менеджерами")
        st.write(
            '<iframe frameborder="0" src="https://datalens.yandex/cuc912b6qxye1" width="100%" height=1400></iframe>',
            unsafe_allow_html=True,
        )

    if selected == "Контакты":
        col1, col2, col3, col4 = st.columns((1, 1, 2, 1))
        col2.image(Image.open("images/ruslan.png"), width=200)
        col3.subheader("Руслан Латипов")
        col3.write(
            """
        #### Python developer 

        Зеленодольск, Татарстан"""
        )

        col3.write(
            """<p><img src="data:image/jpeg;base64,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" width="30" height="30" align="middle" /> 
        @rus_lat116</p>""",
            unsafe_allow_html=True,
        )

        col2.write("##")
        col3.write("##")

        col2.image(Image.open("images/yura.png"), width=200)
        col3.subheader("Юрий Дон")
        col3.write(
            """
        #### Data science 

        Краснодар, Краснодарский край"""
        )

        col3.write(
            """<p><img src="data:image/jpeg;base64,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" width="30" height="30" align="middle" /> 
        @Yuriy_Nikitich</p>""",
            unsafe_allow_html=True,
        )

        col2.write("##")
        col3.write("##")
        col3.write("##")

        col2.image(Image.open("images/tanya.png"), width=200)
        col3.subheader("Татьяна Моисеева")
        col3.write(
            """
        #### Data science 

        Москва, Московская область"""
        )

        col3.write(
            """<p><img src="data:image/jpeg;base64,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" width="30" height="30" align="middle" /> 
        @Estochka</p>""",
            unsafe_allow_html=True,
        )
