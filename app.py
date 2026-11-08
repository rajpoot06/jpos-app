import streamlit as st
import pandas as pd

st.set_page_config(page_title="J POS GOLDEN EDITION", layout="centered")
st.title("✨ J POS GOLDEN EDITION")

if "login" not in st.session_state:
    st.session_state.login = False
if "products" not in st.session_state:
    st.session_state.products = []
if "sales" not in st.session_state:
    st.session_state.sales = []

st.info("Machine ID: 421AA90E")

if not st.session_state.login:
    key = st.text_input("License Key لکھیں (DEMO لکھیں 7 دن کے لیے)")
    if st.button("Login"):
        if key.strip().upper() == "DEMO":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("غلط Key ہے، DEMO لکھیں")
    st.stop()

st.success("Welcome! J POS چل رہا ہے")
menu = st.selectbox("کیا کرنا ہے؟", ["Dashboard", "نیا مال شامل کریں", "سیل کریں", "بل دیکھیں"])

if menu == "Dashboard":
    total_sale = sum([s['Total'] for s in st.session_state.sales])
    st.metric("کل سیل", f"Rs. {total_sale}")
    st.metric("کل آئٹم", len(st.session_state.products))
    st.metric("کل بل", len(st.session_state.sales))

elif menu == "نیا مال شامل کریں":
    name = st.text_input("آئٹم کا نام")
    price = st.number_input("قیمت", min_value=0)
    qty = st.number_input("تعداد", min_value=1)
    if st.button("Save کریں"):
        st.session_state.products.append({"Name": name, "Price": price, "Qty": qty})
        st.success(f"{name} شامل ہو گیا")

elif menu == "سیل کریں":
    if not st.session_state.products:
        st.warning("پہلے مال شامل کریں")
    else:
        names = [p['Name'] for p in st.session_state.products]
        sel = st.selectbox("آئٹم چنیں", names)
        q = st.number_input("کتنے چاہیے", min_value=1)
        prod = [p for p in st.session_state.products if p['Name']==sel][0]
        total = prod['Price'] * q
        st.write(f"Total: Rs. {total}")
        if st.button("بل بنائیں"):
            st.session_state.sales.append({"Item": sel, "Qty": q, "Total": total})
            st.success("بل بن گیا!")

elif menu == "بل دیکھیں":
    if st.session_state.sales:
        st.table(pd.DataFrame(st.session_state.sales))
    else:
        st.write("ابھی کوئی سیل نہیں")
