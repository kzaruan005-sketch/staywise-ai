
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="StayWise AI",
    page_icon="🏨",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
h1 {
    color: #173b67;
}
.hotel {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e0e6ef;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

HOTELS = [
    {"name": "Grand Almaty Hotel", "price": 18000,
     "rating": 9.2, "stars": 4, "city": "Алматы",
     "description": "Комфортабельный отель в центре города."},
    {"name": "Mountain View Hotel", "price": 15000,
     "rating": 9.5, "stars": 4, "city": "Алматы",
     "description": "Красивый вид на горы и уютные номера."},
    {"name": "Budget Stay", "price": 8500,
     "rating": 8.1, "stars": 2, "city": "Алматы",
     "description": "Недорогой вариант для путешественников."},
    {"name": "Astana Comfort", "price": 12000,
     "rating": 8.7, "stars": 3, "city": "Астана",
     "description": "Удобное расположение и комфортные номера."},
    {"name": "Capital Luxury", "price": 25000,
     "rating": 9.6, "stars": 5, "city": "Астана",
     "description": "Премиальный отель с высоким уровнем сервиса."}
]

st.title("🏨 StayWise AI")
st.subheader("Умный помощник для поиска отелей")
st.write("Найдите подходящий отель по городу, бюджету и рейтингу.")

st.divider()

st.header("🔎 Поиск отелей")

col1, col2, col3 = st.columns(3)

with col1:
    city = st.selectbox("Город", ["Алматы", "Астана"])

with col2:
    checkin = st.date_input("Дата заезда", value=date(2026, 12, 1))

with col3:
    checkout = st.date_input("Дата выезда", value=date(2026, 12, 5))

col4, col5 = st.columns(2)

with col4:
    budget = st.slider("Максимальная цена за ночь (₸)",
                       5000, 50000, 20000, 1000)

with col5:
    min_rating = st.slider("Минимальный рейтинг",
                           0.0, 10.0, 8.0, 0.1)

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
            hotel for hotel in HOTELS
            if hotel["city"] == city
            and hotel["price"] <= budget
            and hotel["rating"] >= min_rating
        ]

        if sort == "Сначала дешевле":
            results.sort(key=lambda x: x["price"])
        else:
            results.sort(key=lambda x: x["rating"], reverse=True)

        st.divider()
        st.header("🏨 Результаты поиска")

        st.info(f"Найдено вариантов: {len(results)} | Ночей: {nights}")

        if results:
            best = max(results, key=lambda x: x["rating"])

            st.success(
                f"🤖 AI-рекомендация: {best['name']} — "
                f"рейтинг {best['rating']}/10. "
                "Это самый высокооценённый вариант среди найденных."
            )

            for hotel in results:
                total = hotel["price"] * nights

                st.markdown(f"""
                <div class="hotel">
                    <h3>🏨 {hotel['name']}</h3>
                    <p>{hotel['description']}</p>
                    <p>⭐ Рейтинг: {hotel['rating']}/10</p>
                    <p>Категория: {hotel['stars']} звезды</p>
                    <h3>{hotel['price']:,} ₸ / ночь</h3>
                    <b>Стоимость за {nights} ночей: {total:,} ₸</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Подходящие отели не найдены. Измените фильтры.")

st.divider()

st.caption(
    "StayWise AI | Учебный проект. "
    "Отели и цены демонстрационные, бронирование не осуществляется."
)
