import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Car Resale Price Prediction", page_icon="🚗", layout="wide")

# --- Centered Title ---
st.markdown(
    "<h1 style='text-align: center; color: black;'>Car Resale Price Prediction 🚗</h1>",
    unsafe_allow_html=True
)

# --- Load data ---
cars_df = pd.read_csv("cars24-car-price.csv")

# --- Load model ---
with open("car_pred_model", "rb") as f:
    model = pickle.load(f)

# --- Encoding dictionary ---
encode_dict = {
    "fuel_type": {'Diesel': 1, 'Petrol': 2, 'CNG': 3, 'LPG': 4, 'Electric': 5},
    "seller_type": {'Dealer': 1, 'Individual': 2, 'Trustmark Dealer': 3},
    "transmission_type": {'Manual': 1, 'Automatic': 2},
}

# --- Layout: Left column (images + author) and right column (UI) ---
left_col, right_col = st.columns([1, 2])

# --- LEFT SIDE: Two stacked images + Author info ---
with left_col:
    st.image(
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d",
        caption="Luxury Car",
        use_container_width=True
    )
    st.image(
        "https://images.unsplash.com/photo-1502877338535-766e1452684a",
        caption="Sports Car",
        use_container_width=True
    )

    # Author info card
    st.markdown(
        """
        <div style='margin-top: 15px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; background-color: #f8f8f8; text-align: center;'>
            <strong>Author:</strong> Srinivas Devarapalli<br>
            <strong>Email:</strong> itsmedevarapalli@gmail.com
        </div>
        """,
        unsafe_allow_html=True
    )

# --- RIGHT SIDE: Table + Form ---
with right_col:
    st.dataframe(cars_df.head())

    st.markdown("### Enter Car Details")

    years = sorted(cars_df["year"].dropna().unique().tolist())
    seller_types = list(encode_dict["seller_type"].keys())
    fuel_types = list(encode_dict["fuel_type"].keys())
    trans_types = list(encode_dict["transmission_type"].keys())
    seats_opts = sorted(cars_df["seats"].dropna().unique().tolist())

    km_min, km_max = int(cars_df["km_driven"].min()), int(cars_df["km_driven"].max())
    mil_min, mil_max = float(cars_df["mileage"].min()), float(cars_df["mileage"].max())
    eng_min, eng_max = int(cars_df["engine"].min()), int(cars_df["engine"].max())
    pwr_min, pwr_max = float(cars_df["max_power"].min()), float(cars_df["max_power"].max())

    with st.form("price_form"):
        c1, c2, c3 = st.columns(3)
        year = c1.selectbox("Year", years)
        seller_type = c2.selectbox("Seller Type", seller_types)
        km_driven = c3.number_input("Kilometers Driven", min_value=km_min, max_value=km_max, step=1000)

        c4, c5, c6 = st.columns(3)
        fuel_type = c4.selectbox("Fuel Type", fuel_types)
        transmission_type = c5.selectbox("Transmission Type", trans_types)
        mileage = c6.slider("Mileage (km/l)", min_value=float(round(mil_min, 2)), max_value=float(round(mil_max, 2)))

        c7, c8, c9 = st.columns(3)
        engine = c7.slider("Engine (CC)", min_value=eng_min, max_value=eng_max, step=50)
        max_power = c8.slider("Max Power (bhp)", min_value=float(round(pwr_min, 2)), max_value=float(round(pwr_max, 2)))
        seats = c9.selectbox("Seats", seats_opts)

        submitted = st.form_submit_button("Get Price")

    if submitted:
        enc_seller = encode_dict["seller_type"][seller_type]
        enc_fuel = encode_dict["fuel_type"][fuel_type]
        enc_trans = encode_dict["transmission_type"][transmission_type]

        X = [[
            float(year),
            float(enc_seller),
            float(km_driven),
            float(enc_fuel),
            float(enc_trans),
            float(mileage),
            float(engine),
            float(max_power),
            float(seats),
        ]]

        price_lakhs = model.predict(X)[0]
        st.subheader(f"Estimated Price: **{round(price_lakhs, 2)}L INR**")
