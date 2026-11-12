
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="StayWise AI | World Hotels",
    page_icon="🌍",
    layout="wide"
)

# Демонстрационные направления: страна, город, базовая цена в тенге
DESTINATIONS = [
    ("Казахстан", "Алматы", 14000),
    ("Казахстан", "Астана", 15000),
    ("Турция", "Стамбул", 22000),
    ("Турция", "Анталья", 25000),
    ("ОАЭ", "Дубай", 45000),
    ("ОАЭ", "Абу-Даби", 38000),
    ("Япония", "Токио", 42000),
    ("Япония", "Осака", 35000),
    ("Южная Корея", "Сеул", 38000),
    ("Таиланд", "Бангкок", 18000),
    ("Таиланд", "Пхукет", 28000),
    ("Китай", "Пекин", 25000),
    ("Китай", "Шанхай", 32000),
    ("Индия", "Дели", 16000),
    ("Индия", "Мумбаи", 24000),
    ("Франция", "Париж", 55000),
    ("Италия", "Рим", 45000),
    ("Италия", "Милан", 50000),
    ("Германия", "Берлин", 42000),
    ("Германия", "Мюнхен", 48000),
    ("Испания", "Барселона", 40000),
    ("Испания", "Мадрид", 38000),
    ("Великобритания", "Лондон", 65000),
    ("Нидерланды", "Амстердам", 55000),
    ("Греция", "Афины", 35000),
    ("Швейцария", "Цюрих", 75000),
    ("США", "Нью-Йорк", 80000),
    ("США", "Лос-Анджелес", 70000),
    ("США", "Майами", 65000),
    ("Канада", "Торонто", 60000),
    ("Канада", "Ванкувер", 62000),
    ("Мексика", "Мехико", 30000),
    ("Бразилия", "Рио-де-Жанейро", 35000),
    ("Аргентина", "Буэнос-Айрес", 28000),
    ("Египет", "Каир", 22000),
    ("Египет", "Шарм-эш-Шейх", 30000),
    ("Марокко", "Марракеш", 28000),
    ("ЮАР", "Кейптаун", 40000),
    ("Австралия", "Сидней", 70000),
    ("Австралия", "Мельбурн", 65000),
    ("Новая Зеландия", "Окленд", 60000),
    ("Сингапур", "Сингапур", 55000),
    ("Малайзия", "Куала-Лумпур", 22000),
    ("Индонезия", "Бали", 26000),
    ("Вьетнам", "Хошимин", 18000),
    ("Грузия", "Тбилиси", 20000),
    ("Азербайджан", "Баку", 24000),
    ("Узбекистан", "Ташкент", 16000),
]

# Создание демонстрационных вариантов для каждого направления
HOTELS = []

for country, city, price in DESTINATIONS:
    HOTELS.append({
        "country": country,
        "city": city,
        "name": f"{city} Demo Hotel",
        "price": price,
        "rating": 9.2,
        "stars": 4
    })

    HOTELS.append({
        "country": country,
        "city": city,
        "name": f"{city} Budget Stay",
        "price": int(price * 0.7),
        "rating": 8.4,
        "stars": 3
    })

st.markdown("""
<style>
.stApp {
    background-color: #f3f6fb;
}
h1 {
    color: #173b67;
}
.hotel-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #dce4ef;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 StayWise AI")
st.subheader("International Hotel Search")
st.write("Умный помощник для поиска отелей по всему миру.")

st.info(
    "Учебный проект. Используются демонстрационные отели "
    "и условные цены в тенге. Реальное бронирование недоступно."
)

st.divider()
st.header("🔎 Поиск отелей")

countries = sorted(set(x[0] for x in DESTINATIONS))

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("🌎 Выберите страну", countries)

cities = sorted(
    set(x[1] for x in DESTINATIONS if x[0] == country)
)

with col2:
    city = st.selectbox("📍 Выберите город", cities)

col3, col4 = st.columns(2)

with col3:
    checkin = st.date_input(
        "Дата заезда",
        value=date.today() + timedelta(days=1)
    )

with col4:
    checkout = st.date_input(
        "Дата выезда",
        value=date.today() + timedelta(days=5)
    )

col5, col6 = st.columns(2)

with col5:
    budget = st.slider(
        "Максимальная цена за ночь (₸)",
        5000, 150000, 50000, 1000
    )

with col6:
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
            if h["country"] == country
            and h["city"] == city
            and h["price"] <= budget
            and h["rating"] >= min_rating
        ]

        if sort == "Сначала дешевле":
            results.sort(key=lambda h: h["price"])
        else:
            results.sort(key=lambda h: h["rating"], reverse=True)

        st.divider()
        st.header(f"🏨 Отели: {city}, {country}")

        st.write(f"Найдено вариантов: {len(results)}")
        st.write(f"Количество ночей: {nights}")

        if results:
            best = max(results, key=lambda h: h["rating"])

            st.success(
                f"🤖 AI-рекомендация: {best['name']}. "
                f"Рейтинг {best['rating']}/10. "
                "Выбран вариант с самым высоким рейтингом."
            )

            for h in results:
                total = h["price"] * nights

                st.markdown(f"""
                <div class="hotel-card">
                    <h3>🏨 {h['name']}</h3>
                    <p>🌍 {h['country']}, {h['city']}</p>
                    <p>⭐ Рейтинг: {h['rating']}/10</p>
                    <p>Категория: {h['stars']} звезды</p>
                    <h3>{h['price']:,} ₸ / ночь</h3>
                    <b>Итого за {nights} ночей: {total:,} ₸</b>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.warning(
                "Отели не найдены. Увеличьте бюджет "
                "или измените минимальный рейтинг."
            )

st.divider()

st.markdown("""
### ℹ️ О проекте
StayWise AI — учебное приложение для поиска и сравнения
демонстрационных вариантов размещения в разных странах мира.

**Технологии:** Python, Streamlit.
""")

st.caption("StayWise AI | Educational Project | 2026")
