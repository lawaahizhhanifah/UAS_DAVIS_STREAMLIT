import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Top Box Office IMDB :page_with_curl:', divider='grey')
# Menyisipkan baris kosong
st.markdown("<br>", unsafe_allow_html=True)

# Membaca data dari file CSV
df = pd.read_csv('C:\\Users\\ali.imran\\Downloads\\SEM 6\\DAVIS\\STREAMLIT_DAVIS\\imdb_combine.csv', delimiter=';')

# Menampilkan DataFrame dalam bentuk tabel
#st.write("Data IMDb Combined")
#st.dataframe(df)

#########################################
#COMPARISON
st.subheader("***Comparison***")

# Visualisasi dengan Plotly Express (bar chart)
fig = px.bar(df, x='Titles', y='Opening_Week_Rev', title="Opening Week Revenue Comparison",)
st.plotly_chart(fig, use_container_width=True)

#Penjelasan
st.markdown("""
<div style="text-align: justify">
            
Grafik batang ini membandingkan pendapatan minggu pertama dari berbagai film. Setiap batang mewakili satu film, dan tinggi batang menunjukkan pendapatan yang dihasilkan selama minggu pertama perilisan. Visualisasi ini membantu untuk mengidentifikasi dengan cepat film-film yang memiliki pendapatan minggu pertama lebih tinggi atau lebih rendah dibandingkan satu sama lain.

            
**Insight:**
  - Mengidentifikasi film-film teratas berdasarkan pendapatan minggu pertama.
  - Membandingkan kinerja pendapatan dari berbagai film dalam format visual.
  - Memahami distribusi dan rentang pendapatan minggu pertama di seluruh dataset.

Perbandingan ini berguna bagi pemangku kepentingan di industri film untuk menilai kesuksesan awal film-film setelah rilis dan merancang strategi pemasaran dan distribusi dengan tepat.

</div>
""", unsafe_allow_html=True)


####################################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#COMPOSITION
st.subheader("***Composition***")

# Menghapus baris yang memiliki nilai None pada kolom Gross_World
df_cleaned = df.dropna(subset=['Gross_World'])

# Mengonversi kolom Gross_World menjadi tipe numerik untuk pengurutan
df_cleaned['Gross_World'] = pd.to_numeric(df_cleaned['Gross_World'], errors='coerce')

# Menghapus baris dengan nilai NaN setelah konversi
df_cleaned = df_cleaned.dropna(subset=['Gross_World'])

# Mengurutkan berdasarkan kolom Gross_World dari besar ke kecil
df_sorted = df_cleaned.sort_values(by='Gross_World', ascending=False)

# Membuat Treemap menggunakan Plotly Express
fig = px.treemap(df_sorted, 
                 path=['Titles'], 
                 values='Gross_World',
                 color='Gross_World',
                 title="Treemap of Top Box Office Film IMDB",
                 hover_data=['Titles', 'Gross_World'],
                 width=800, height=600)

# Menampilkan Treemap menggunakan Streamlit
st.plotly_chart(fig)

#Penjelasan
st.markdown("""
<div style="text-align: justify">

Treemap ini memvisualisasikan film-film box office teratas di IMDB berdasarkan pendapatan Gross World mereka. Setiap persegi panjang mewakili sebuah film, dan ukurannya sesuai dengan pendapatan yang dihasilkannya secara global. Intensitas warna juga mencerminkan pendapatan, dengan warna yang lebih gelap menunjukkan pendapatan yang lebih tinggi.

**Insights:**
- Cepat mengidentifikasi film-film yang paling sukses berdasarkan pendapatan global.
- Membandingkan kontribusi pendapatan dari berbagai film secara visual.
- Memahami distribusi kesuksesan box office di seluruh dataset.

Visualisasi ini berguna untuk memahami kinerja keuangan film dan mengidentifikasi film blockbuster dalam dataset.

</div>
""", unsafe_allow_html=True)


####################################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#RELATIONSHIP
st.subheader("***Relationship***")

# Deskripsi atau teks di bawah judul
st.write('Pilih variabel untuk scatter plot di sidebar di bawah ini:')

# Sidebar untuk memilih variabel x dan y
x_variable = st.selectbox('Variabel X', ['Budget', 'Opening_Week_Rev', 'Gross_Us'])
y_variable = st.selectbox('Variabel Y', ['Gross_World', 'Opening_Week_Rev', 'Gross_Us'])
# Filter data yang akan digunakan
data = df[[x_variable, y_variable]].dropna()

# Membuat scatter plot dengan Plotly Express
fig = px.scatter(data, x=x_variable, y=y_variable, 
                 title=f'Scatter Plot of {x_variable} vs {y_variable}',
                 labels={x_variable: x_variable, y_variable: y_variable})

# Menampilkan scatter plot menggunakan Streamlit
st.plotly_chart(fig)

#Penjelasan
st.markdown('''
<div style="text-align: justify">

Scatter Plot ini memvisualisasikan hubungan antara dua variabel yang dipilih dalam dataset film IMDB. 
Setiap titik dalam plot mewakili satu film, dengan sumbu X dan Y masing-masing mewakili variabel yang dipilih.
Ini membantu dalam mengeksplorasi korelasi atau pola antara variabel-variabel berikut:

- **Variabel X:** {x_variable}
- **Variabel Y:** {y_variable}

**Insights:**
- Scatter plot membantu untuk melihat sebaran data dan pola hubungan antara variabel-variabel tersebut.
- Titik-titik yang terkumpul di sekitar garis diagonal mungkin menunjukkan korelasi positif antara kedua variabel.
- Penyebaran titik yang lebih acak menunjukkan hubungan yang tidak terlalu jelas atau tidak ada hubungan antara variabel-variabel tersebut.

Visualisasi ini membantu pengguna untuk lebih memahami distribusi data dan hubungan antara variabel-variabel terpilih dalam dataset IMDB.

</div>
'''.format(x_variable=x_variable, y_variable=y_variable), unsafe_allow_html=True)


####################################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#DISTRIBUTION
st.subheader("***Distribution***")

# Mengubah tipe data kolom Opening_Week_Date menjadi datetime
df['Opening_Week_Date'] = pd.to_datetime(df['Opening_Week_Date'])

# Menambahkan kolom baru 'Year' untuk menyimpan tahun dari tanggal 'Opening_Week_Date'
df['Year'] = df['Opening_Week_Date'].dt.year

# Menghitung total Gross World per tahun
gross_world_per_year = df.groupby('Year')['Gross_World'].sum().reset_index()

# Membuat bar chart dengan Plotly Express
fig = px.bar(gross_world_per_year, x='Year', y='Gross_World',  title="Gross World Revenue per Year",
             labels={'Year': 'Year', 'Gross_World': 'Gross World Revenue'})

# Menampilkan bar chart menggunakan Streamlit
st.plotly_chart(fig)

#Penjelasan
st.markdown('''
<div style="text-align: justify;">
    Bar chart di atas memvisualisasikan pendapatan Gross World dari film-film dalam dataset IMDB per tahun. 
    Ini memberikan gambaran tentang bagaimana total pendapatan global dari film-film tersebut berubah dari tahun ke tahun.
    <br><br>
    <strong>Insights:</strong>
    <ul>
        <li><strong>Tahun Terbaik:</strong> Identifikasi tahun dengan pendapatan Gross World tertinggi.</li>
        <li><strong>Tren Pendapatan:</strong> Amati apakah pendapatan Gross World cenderung meningkat, menurun, atau stabil dari tahun ke tahun.</li>
        <li><strong>Perbandingan Tahunan:</strong> Bandingkan kontribusi pendapatan dari berbagai tahun secara visual.</li>
    </ul>
    <br>
    Visualisasi ini berguna untuk mendapatkan pemahaman tentang performa finansial tahunan film-film dalam dataset IMDB dan potensialnya untuk mengidentifikasi tahun-tahun yang paling sukses dari segi pendapatan global.
</div>
''', unsafe_allow_html=True)

