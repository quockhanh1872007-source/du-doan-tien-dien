
import streamlit as st
import pandas as pd
import re

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# =========================
# GIAO DIỆN
# =========================
st.set_page_config(
    page_title="Dự đoán tiền điện",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ App dự đoán tiền điện")
st.write("Nhập thông tin để dự đoán tiền điện mỗi tháng")

# =========================
# ĐỌC FILE EXCEL
# =========================
data = pd.read_csv("/content/tien_dien.csv")

# Xóa khoảng trắng dư
data.columns = data.columns.str.strip()

# =========================
# TÁCH CỘT QUẠT
# =========================
def tach_quat(text):

    text = str(text)

    numbers = re.findall(r'\d+', text)

    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])

    elif len(numbers) == 1:
        return int(numbers[0]), 0

    return 0, 0


data[["Số quạt", "Số giờ quạt"]] = data[
    "Số quạt máy và thời gian sử dụng 1 ngày?"
].apply(
    lambda x: pd.Series(tach_quat(x))
)

# =========================
# ĐỔI TỦ LẠNH
# =========================
data["Số tủ lạnh"] = data[
    "Phòng có tủ lạnh không?"
].map({
    "Có": 1,
    "Không": 0
})

# =========================
# MÃ HÓA LOẠI NHÀ
# =========================
le_loai_nha = LabelEncoder()

data["Loại nhà"] = le_loai_nha.fit_transform(
    data["Loại nhà"].astype(str)
)

# =========================
# INPUT - OUTPUT
# =========================
X = data[
    [
        "Số người",
        "Số máy lạnh",
        "Số quạt",
        "Số giờ quạt",
        "Số tủ lạnh",
        "Số giờ bật máy lạnh",
        "Diện tích",
        "Loại nhà"
    ]
]

y = data[
    "Tiền điện trung bình 1 tháng là bao nhiêu vnd?"
]

# =========================
# TRAIN MODEL
# =========================
model = RandomForestRegressor(
    random_state=42
)

model.fit(X, y)

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Nhập thông tin")

so_nguoi = st.number_input(
    "Số người",
    min_value=1,
    max_value=20,
    value=2
)

so_may_lanh = st.number_input(
    "Số máy lạnh",
    min_value=0,
    max_value=10,
    value=1
)

so_quat = st.number_input(
    "Số quạt",
    min_value=0,
    max_value=20,
    value=2
)

gio_quat = st.slider(
    "Số giờ sử dụng quạt/ngày",
    0,
    24,
    8
)

co_tu_lanh = st.radio(
    "Có tủ lạnh không?",
    ["Không", "Có"]
)

gio_may_lanh = st.slider(
    "Số giờ bật máy lạnh/ngày",
    0,
    24,
    5
)

dien_tich = st.number_input(
    "Diện tích phòng",
    min_value=5,
    max_value=500,
    value=20
)

loai_nha_text = st.selectbox(
    "Loại nhà",
    list(le_loai_nha.classes_)
)

# =========================
# DỰ ĐOÁN
# =========================
if st.button("🔍 Dự đoán tiền điện"):

    so_tu_lanh = 1 if co_tu_lanh == "Có" else 0

    loai_nha_ma = le_loai_nha.transform(
        [loai_nha_text]
    )[0]

    input_data = pd.DataFrame(
        [[
            so_nguoi,
            so_may_lanh,
            so_quat,
            gio_quat,
            so_tu_lanh,
            gio_may_lanh,
            dien_tich,
            loai_nha_ma
        ]],
        columns=X.columns
    )

    ket_qua = model.predict(input_data)[0]

    st.success(
        f"💰 Tiền điện dự đoán: {ket_qua:,.0f} VNĐ/tháng"
    )

    st.info(
        "Kết quả chỉ mang tính tham khảo"
    )
