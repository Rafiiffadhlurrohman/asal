import os
import streamlit as st
import pandas as pd

def load_data(filename):
    if os.path.exists(filename):
        data = pd.read_excel(filename)
    else:
        data = pd.DataFrame(columns=["Nama", "Ukuran", "Jumlah"])
    return data

def save_data(data, filename):
    data.to_excel(filename, index=False)

def add_stock(data, name, size, quantity):
    if ((data["Nama"] == name) & (data["Ukuran"] == size)).any():
        data.loc[(data["Nama"] == name) & (data["Ukuran"] == size), "Jumlah"] += quantity
    else:
        new_row = pd.DataFrame({"Nama": [name], "Ukuran": [size], "Jumlah": [quantity]})
        data = pd.concat([data, new_row], ignore_index=True)
    return data

def subtract_stock(data, name, size, quantity):
    if ((data["Nama"] == name) & (data["Ukuran"] == size)).any():
        current_quantity = data.loc[(data["Nama"] == name) & (data["Ukuran"] == size), "Jumlah"].values[0]
        new_quantity = current_quantity - quantity
        if new_quantity < 0:
            st.error("Stok tidak mencukupi!")
        else:
            data.loc[(data["Nama"] == name) & (data["Ukuran"] == size), "Jumlah"] = new_quantity
    else:
        st.error("Produk tidak ditemukan!")
    return data

# Streamlit app
def main():
    st.title(":blue[KONVEKSI DAVA]")

    filename = 'data_stok_konveksi.xlsx'
    data = load_data(filename)

    menu = ["Tambah Stok", "Kurangi Stok", "Lihat Stok"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Tambah Stok":
        st.subheader("Tambah Stok")
        name = st.text_input("Nama Produk")
        size = st.selectbox("Ukuran", ["S", "M", "L", "XL", "XXL"])
        quantity = st.number_input("Jumlah", min_value=0, step=1)
        if st.button("Tambah"):
            if name and size and quantity > 0:
                data = add_stock(data, name, size, int(quantity))
                save_data(data, filename)
                st.success("Stok berhasil ditambahkan!")
            else:
                st.error("Silakan masukkan semua data dengan benar!")

    elif choice == "Kurangi Stok":
        st.subheader("Kurangi Stok")
        name = st.text_input("Nama Produk")
        size = st.selectbox("Ukuran", ["S", "M", "L", "XL", "XXL"])
        quantity = st.number_input("Jumlah", min_value=0, step=1)
        if st.button("Kurangi"):
            if name and size and quantity > 0:
                data = subtract_stock(data, name, size, int(quantity))
                save_data(data, filename)
                st.success("Stok berhasil dikurangi!")
            else:
                st.error("Silakan masukkan semua data dengan benar!")

    elif choice == "Lihat Stok":
        st.subheader("Data Stok")
        st.dataframe(data)

if __name__ == "__main__":
    main()
