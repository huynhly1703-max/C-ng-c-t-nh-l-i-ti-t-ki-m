import streamlit as st
st.image("logo.jpg")
import pandas as pd

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================

so_tien = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_nhan_lai = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

loai_lai = st.radio(
    "🧮 Loại lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# ==============================
# TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0%.")
        st.stop()

    # Lãi suất năm -> lãi suất tháng
    lai_suat_thang = lai_suat / 100 / 12

    # Số kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = ky_han
        lai_suat_ky = lai_suat_thang
        ten_ky = "Tháng"

    elif hinh_thuc_nhan_lai == "Hàng quý":
        # Nếu kỳ hạn không chia hết cho 3,
        # phần tháng còn lại vẫn được tính theo tháng
        so_ky = ky_han // 3
        lai_suat_ky = lai_suat / 100 / 4
        ten_ky = "Quý"

    else:
        # Cuối kỳ
        so_ky = ky_han
        lai_suat_ky = lai_suat_thang
        ten_ky = "Kỳ"

    # =====================================
    # LÃI CUỐI KỲ
    # =====================================

    if hinh_thuc_nhan_lai == "Cuối kỳ":

        if loai_lai == "Lãi đơn":
            tien_lai = so_tien * (lai_suat / 100) * (ky_han / 12)
            tong_tien = so_tien + tien_lai

        else:
            # Lãi kép tính theo tháng
            tong_tien = so_tien * (1 + lai_suat_thang) ** ky_han
            tien_lai = tong_tien - so_tien

        # Tiền lãi định kỳ
        lai_dinh_ky = tien_lai

        st.subheader("📊 KẾT QUẢ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi",
                dinh_dang_tien(tien_lai)
            )

        with col2:
            st.metric(
                "🏦 Tổng tiền nhận được",
                dinh_dang_tien(tong_tien)
            )

        st.info(
            f"Tiền gốc ban đầu: **{dinh_dang_tien(so_tien)}**"
        )

    # =====================================
    # NHẬN LÃI HÀNG THÁNG / HÀNG QUÝ
    # =====================================

    else:

        # Danh sách dữ liệu từng kỳ
        bang_du_lieu = []

        tien_goc = so_tien
        tong_lai = 0

        if hinh_thuc_nhan_lai == "Hàng tháng":

            for ky in range(1, ky_han + 1):

                if loai_lai == "Lãi đơn":
                    # Lãi đơn: tiền gốc không thay đổi
                    tien_lai_ky = so_tien * lai_suat_thang
                    tien_goc_sau_ky = so_tien

                else:
                    # Lãi kép: lãi nhập vào gốc
                    tien_lai_ky = tien_goc * lai_suat_thang
                    tien_goc_sau_ky = tien_goc + tien_lai_ky
                    tien_goc = tien_goc_sau_ky

                tong_lai += tien_lai_ky

                bang_du_lieu.append({
                    "Kỳ": f"Tháng {ky}",
                    "Tiền gốc": tien_goc_sau_ky - tien_lai_ky
                    if loai_lai == "Lãi kép" else so_tien,
                    "Tiền lãi kỳ này": tien_lai_ky,
                    "Tổng lãi": tong_lai,
                    "Tổng tiền": tien_goc_sau_ky
                })

        else:
            # ==============================
            # NHẬN LÃI HÀNG QUÝ
            # ==============================

            so_quy = ky_han // 3

            for ky in range(1, so_quy + 1):

                if loai_lai == "Lãi đơn":
                    tien_lai_ky = so_tien * (lai_suat / 100 / 4)
                    tien_goc_sau_ky = so_tien

                else:
                    tien_lai_ky = tien_goc * (lai_suat / 100 / 4)
                    tien_goc_sau_ky = tien_goc + tien_lai_ky
                    tien_goc = tien_goc_sau_ky

                tong_lai += tien_lai_ky

                bang_du_lieu.append({
                    "Kỳ": f"Quý {ky}",
                    "Tiền gốc": tien_goc_sau_ky - tien_lai_ky
                    if loai_lai == "Lãi kép" else so_tien,
                    "Tiền lãi kỳ này": tien_lai_ky,
                    "Tổng lãi": tong_lai,
                    "Tổng tiền": tien_goc_sau_ky
                })

        # ==============================
        # KẾT QUẢ
        # ==============================

        if bang_du_lieu:

            tong_tien = bang_du_lieu[-1]["Tổng tiền"]

            st.subheader("📊 KẾT QUẢ")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "💰 Lãi kỳ đầu",
                    dinh_dang_tien(
                        bang_du_lieu[0]["Tiền lãi kỳ này"]
                    )
                )

            with col2:
                st.metric(
                    "📈 Tổng tiền lãi",
                    dinh_dang_tien(tong_lai)
                )

            with col3:
                st.metric(
                    "🏦 Tổng tiền",
                    dinh_dang_tien(tong_tien)
                )

            st.write("### 📋 Chi tiết tiền lãi từng kỳ")

            df = pd.DataFrame(bang_du_lieu)

            # Định dạng tiền
            df_hien_thi = df.copy()

            for cot in [
                "Tiền gốc",
                "Tiền lãi kỳ này",
                "Tổng lãi",
                "Tổng tiền"
            ]:
                df_hien_thi[cot] = df_hien_thi[cot].apply(
                    lambda x: f"{x:,.0f} VNĐ"
                )

            st.dataframe(
                df_hien_thi,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning(
                "Kỳ hạn phải từ 3 tháng trở lên nếu chọn nhận lãi hàng quý."
            )


# ==============================
# CÔNG THỨC
# ==============================

with st.expander("📚 Xem công thức tính"):

    st.markdown("""
### 1. Lãi đơn

**Tiền lãi:**

`Tiền lãi = Tiền gốc × Lãi suất năm × Số năm`

Trong đó:

`Số năm = Số tháng / 12`

---

### 2. Lãi kép

**Tổng tiền:**

`Tổng tiền = Tiền gốc × (1 + r)^n`

Trong đó:

- `r`: lãi suất của mỗi kỳ
- `n`: số kỳ tính lãi
- Tiền lãi = Tổng tiền − Tiền gốc

---

### 3. Lãi hàng tháng

Lãi suất tháng được tính:

`Lãi suất tháng = Lãi suất năm / 12`

---

### 4. Lãi hàng quý

Lãi suất quý được tính:

`Lãi suất quý = Lãi suất năm / 4`
""")

st.divider()

st.caption("💡 Công cụ tính toán mang tính tham khảo.")
