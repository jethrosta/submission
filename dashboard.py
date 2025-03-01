import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='whitegrid')

# Load datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Konversi bentuk tanggal dan jam
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
hour_df["hour"] = hour_df["hr"].astype(int)

# Sidebar filter dengan gambar LinkedIn
st.sidebar.image("https://media.licdn.com/dms/image/v2/D5603AQHiHaPeTHXFFw/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1725678161780?e=1746057600&v=beta&t=ca-lAeFCENwaJ7gPADDvr73qe3kry3IX-18eddSowsc")

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Waktu", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)

start_hour, end_hour = st.sidebar.slider(
    "Pilih Rentang Jam", 
    0, 23, (0, 23)
)

# Filter dataset berdasarkan masukan user
filtered_hour_df = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df["dteday"] <= pd.to_datetime(end_date)) &
    (hour_df["hour"] >= start_hour) &
    (hour_df["hour"] <= end_hour)
]

# ==============Judul Proyek==============
st.header('Tugas Proyek Analisis Bike-Sharing🚲')

# Jumlah pengguna
st.subheader("Jumlah Pengguna")
col1, col2 = st.columns(2)
user_counts = filtered_hour_df[["registered", "casual"]].sum()

# Registered vs Casual Users
with col1:
    st.metric("Registered Users", value=user_counts["registered"])

with col2:
    st.metric("Casual Users", value=user_counts["casual"])

# Pengaruh Cuaca pada Pengguna
# Mapping kategori weathersit
weather_mapping = {
    1: "Clear/Few clouds",
    2: "Mist + Cloudy",
    3: "Light Snow",
    4: "Very bad Weather"
}

# ==============Mengelompokkan data dan memetakan kategori cuaca==============
weather_counts = filtered_hour_df.groupby("weathersit")["cnt"].sum().reset_index()
weather_counts["weathersit"] = weather_counts["weathersit"].map(weather_mapping)

# Menampilkan grafik
st.subheader("Jumlah Pengguna berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots()
sns.barplot(data=weather_counts, x="weathersit", y="cnt", ax=ax)

# Menambahkan label pada sumbu x dan y
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)

# Menampilkan angka pada sumbu y sebagai integer
yticks = ax.get_yticks()
ax.set_yticklabels([int(y) for y in yticks])
st.pyplot(fig)

# ==============Efek Lingkungan terhadap Jumlah Pemakai Sepeda==============
# 3 Kolom terdiri dari Season - cnt; mnth - cnt; hr - cnt
st.subheader("Faktor lain yang mempengaruhi jumlah Pengguna")
# Mapping kategori musim (season)
season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

# Membuat salinan dataframe agar tidak mengubah yang asli
comparison_df = filtered_hour_df.copy()
# Mapping kategori musim
comparison_df["season"] = comparison_df["season"].map(season_mapping)
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    # Grafik pertama: Season vs cnt
    sns.barplot(data=comparison_df.groupby("season")["cnt"].sum().reset_index(), 
            x="season", y="cnt", ax=ax, palette="Blues")
    ax.set_title("Jumlah Pengguna berdasarkan Musim", fontsize=50)
    yticks = ax.get_yticks()
    ax.set_yticklabels([int(y) for y in yticks])
    ax.set_xlabel("Musim", fontsize=35)
    ax.set_ylabel("Jumlah Pengguna", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    # Grafik kedua: Month vs jumlah pengguna
    sns.barplot(data=comparison_df.groupby("mnth")["cnt"].sum().reset_index(), 
                x="mnth", y="cnt", ax=ax, palette="Greens")
    ax.set_title("Jumlah Pengguna berdasarkan Bulan", fontsize=50)
    ax.set_xlabel("Bulan", fontsize=35)
    ax.set_ylabel("Jumlah Pengguna", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Menyiapkan untuk pengaruh jam terhadap jumlah pengguna
fig, ax = plt.subplots(figsize=(24, 10))
# Grafik ketiga: Hour vs jumlah pengguna
sns.barplot(data=comparison_df.groupby("hour")["cnt"].sum().reset_index(), 
            x="hour", y="cnt", ax=ax, palette="Oranges")
ax.set_title("Jumlah Pengguna berdasarkan Jam", fontsize=50)
ax.set_xlabel("Jam", fontsize=35)
ax.set_ylabel("Jumlah Pengguna", fontsize=30)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader("Pengaruh suhu lingkungan terhadap jumlah pengguna Sepeda")
# Konversi normalisasi temperatur ke derajat Celsius
filtered_hour_df["temp_celsius"] = filtered_hour_df["temp"] * 41

# Plot Scatter Plot dengan x-axis dalam Celsius
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_hour_df, x="temp_celsius", y="cnt", alpha=0.5, color="blue", ax=ax)
ax.set_title("Pengaruh Temperatur terhadap Jumlah Pengguna sepeda", fontsize=14)
ax.set_xlabel("Temperatur (°C)", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
st.pyplot(fig)
# Penambahan visualisasi regresi
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(data=filtered_hour_df, x="temp_celsius", y="cnt", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
ax.set_title("Pengaruh Temperatur terhadap Jumlah Pengguna dengan Regresi", fontsize=14)
ax.set_xlabel("Temperatur (°C)", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
st.pyplot(fig)

st.subheader("Karakteristik Pengguna Terdaftar vs Kasual")
# Karakter pengguna kasual vs terdaftar
hourly_summary = filtered_hour_df.groupby('hour')[['casual', 'registered']].sum().reset_index()
# Menentukan jam dengan jumlah pengguna tertinggi dan terendah
peak_casual_hour = hourly_summary.loc[hourly_summary['casual'].idxmax(), 'hour']
peak_registered_hour = hourly_summary.loc[hourly_summary['registered'].idxmax(), 'hour']
lowest_usage_hour = hourly_summary.loc[hourly_summary[['casual', 'registered']].sum(axis=1).idxmin(), 'hour']
# Membuat figure
fig, ax = plt.subplots(figsize=(12, 6))
# Plot pengguna casual dan registered
sns.lineplot(data=hourly_summary, x='hour', y='casual', label='Casual', marker='o', color='blue', ax=ax)
sns.lineplot(data=hourly_summary, x='hour', y='registered', label='Registered', marker='o', color='red', ax=ax)
# Tambahkan garis vertikal berdasarkan hasil perhitungan
ax.axvline(peak_casual_hour, linestyle='--', color='blue', label=f'Peak Casual: {peak_casual_hour}')
ax.axvline(peak_registered_hour, linestyle='--', color='red', label=f'Peak Registered: {peak_registered_hour}')
ax.axvline(lowest_usage_hour, linestyle='--', color='black', label=f'Lowest Usage: {lowest_usage_hour}')
# Label dan judul
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.set_title("Perbandingan Pengguna Casual dan Registered per Jam", fontsize=14)
ax.legend()
st.pyplot(fig)

# ==============RFM Analysis==============
st.subheader("Analisis RFM")
# Pastikan dataset yang digunakan adalah hasil filter
rfm_df = filtered_hour_df.groupby("instant").agg({
    "dteday": "max",  # Tanggal transaksi terakhir
    'cnt': ['count', 'sum']  # Frekuensi dan total transaksi
}).reset_index()
rfm_df.columns = ["instant", "last_rental", "frequency", "monetary"]
# Hitung recency berdasarkan rentang waktu filter
recent_date = filtered_hour_df["dteday"].max()
rfm_df["recency"] = (recent_date - rfm_df["last_rental"]).dt.days
rfm_df.drop("last_rental", axis=1, inplace=True)
# Menampilkan plot RFM
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(40, 15))
colors = ["#72BCD4"] * 5
sns.barplot(y="recency", x="instant", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="instant", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="instant", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)    
