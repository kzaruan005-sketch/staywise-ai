
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="StayWise AI Kazakhstan",
    page_icon="🏨",
    layout="wide"
)

HOTELS = [
    ("Alatau Comfort", "Алматы", 14000, 9.1, 3),
    ("Mountain City", "Алматы", 18000, 9.5, 4),
    ("Green Park", "Алматы", 10000, 8.4, 3),
    ("Capital Comfort", "Астана", 15000, 9.0, 3),
    ("Astana Grand", "Астана", 23000, 9.6, 5),
    ("City Light", "Астана", 11000, 8.5, 2),
    ("Shymkent Plaza", "Шымкент", 16000, 9.2, 4),
    ("Southern Stay", "Шымкент", 9000, 8.3, 2),
    ("Caspian View", "Актау", 19000, 9.3, 4),
    ("Sea Comfort", "Актау", 12000, 8.6, 3),
    ("Atyrau Residence", "Атырау", 17000, 9.0, 4),
    ("River Hotel", "Атырау", 10000, 8.2, 2),
    ("Karaganda Central", "Караганда", 12000, 8.8, 3),
    ("Saryarka Hotel", "Караганда", 9000, 8.3, 2),
    ("Turkestan Palace", "Туркестан", 18000, 9.4, 4),
    ("Silk Road Stay", "Туркестан", 11000, 8.7, 3),
    ("Taraz Comfort", "Тараз", 9500, 8.5, 3),
    ("Ancient City Hotel", "Тараз", 13000, 8.9, 3),
    ("Pavlodar City", "Павлодар", 10500, 8.6, 3),
    ("Irtysh Hotel", "Павлодар", 14500, 9.0, 4),
    ("Kostanay Inn", "Костанай", 10000, 8.4, 2),
    ("Northern Comfort", "Костанай", 13500, 8.9, 3),
    ("Altai View", "Өскемен", 16000, 9.2, 4),
    ("East Kazakhstan Stay", "Өскемен", 11000, 8.5, 3),
    ("Semey City Hotel", "Семей", 9500, 8.3, 2),
    ("Irtysh Comfort", "Семей", 12500, 8.8, 3),
    ("Kyzylorda Hotel", "Кызылорда", 10000, 8.4, 3),
    ("Aral Comfort", "Кызылорда", 13000, 8.9, 3),
    ("Ural Residence", "Уральск", 11500, 8.7, 3),
    ("West City Hotel", "Уральск", 14500, 9.0, 4),
    ("Kokshetau Park", "Кокшетау", 14000, 9.1, 3),
    ("Burabay Stay", "Кокшетау", 18000, 9.4, 4),
    ("Taldykorgan Hotel", "Талдыкорган", 9500, 8.5, 2),
    ("Jetisu Comfort", "Талдыкорган", 12500, 8.9, 3),
]

st.markdown("""
<style>
.stApp {background-color: #f4f7fb;}
h1 {color: #173b67;}
.hotel {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e0e6ef;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏨 StayWise AI")
st.subheader("Умный поиск отелей по всему Казахстану")
st.write("Выбирайте город, бюджет и рейтинг, чтобы найти подходящий вариант.")

st.info("Учебная версия: используются демонстрационные отели и цены.")

cities = sorted(set(h[1] for h in HOTELS))

st.header("🔎 Поиск отелей")

col1, col2, col3 = st.columns(3)

with col1:
    city = st.selectbox("Выберите город", cities)

with col2:
    checkin = st.date_input(
        "Дата заезда",
        value=date.today() + timedelta(days=1)
    )

with col3:
    checkout = st.date_input(
        "Дата выезда",
        value=date.today() + timedelta(days=5)
    )

col4, col5 = st.columns(2)

with col4:
    budget = st.slider(
        "Максимальная цена за ночь (₸)",
        5000, 50000, 20000, 1000
    )

with col5:
    min_rating = st.slider(
        "Минимальный рейтинг",
        0.0, 10.0, 8.0, 0.1
    )

sort = st.selectbox(
    "Сортировка",
    ["Сначала дешевле", "Сначала высокий рейтинг"]
)

if st.button("🔍 Найти отели", use_container_width=True):

    if checkout <= checkin:
        st.error("Дата выезда должна быть позже даты заезда.")
    else:
        nights = (checkout - checkin).days

        results = [
            h for h in HOTELS
            if h[1] == city
            and h[2] <= budget
            and h[3] >= min_rating
        ]

        if sort == "Сначала дешевле":
            results.sort(key=lambda h: h[2])
        else:
            results.sort(key=lambda h: h[3], reverse=True)

        st.divider()
        st.header(f"🏨 Отели города {city}")
        st.write(f"Найдено вариантов: {len(results)}")
        st.write(f"Количество ночей: {nights}")

        if results:
            best = max(results, key=lambda h: h[3])

            st.success(
                f"🤖 AI-рекомендация: {best[0]}. "
                f"Рейтинг {best[3]}/10. "
                "Это вариант с самым высоким рейтингом среди найденных."
            )

            for h in results:
                total = h[2] * nights

                st.markdown(f"""
                <div class="hotel">
                    <h3>🏨 {h[0]}</h3>
                    <p>📍 Город: {h[1]}</p>
                    <p>⭐ Рейтинг: {h[3]}/10</p>
                    <p>Категория: {h[4]} звезды</p>
                    <h3>{h[2]:,} ₸ за ночь</h3>
                    <b>Итого за {nights} ночей: {total:,} ₸</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Отели не найдены. Измените параметры поиска.")

st.divider()
st.caption(
    "StayWise AI | Учебный проект | "
    "Демонстрационные данные, не реальные предложения для бронирования."
)
