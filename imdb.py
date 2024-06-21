import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Top Box Office IMDB :page_with_curl:', divider='grey')
# Menyisipkan baris kosong
st.markdown("<br>", unsafe_allow_html=True)

# Membaca data dari file CSV
df = pd.read_csv('imdb_combine.csv', delimiter=';')

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
            
Grafik batang ini membandingkan pendapatan minggu pertama dari berbagai film. Setiap batang mewakili satu film, dan tinggi batang menunjukkan pendapatan yang dihasilkan selama minggu pertama perilisan. Visualisasi ini membantu untuk mengidentifikasi dengan cepat film-film yang memiliki pendapatan minggu pertama lebih tinggi atau lebih rendah dibandingkan satu sama lain. Pada data film top box office IMDB, terdapat 10 film yang terdapat pada sumbu x dalam visualisasi di atas.
            
**Insight:**
  - Mengidentifikasi film-film teratas berdasarkan pendapatan minggu pertama.
  Inside Out 2 memiliki pendapatan tertinggi untuk perilisan film pada minggu pertama yaitu sebesar 154 juta. Hal tersebut dikarenakan banyak anak remaja yang menonton film Inside Out 1 pada masa kecilnya sehingga ingin melanjutkan menonton untuk season 2 nya yang dianggap relate. 
  - Memahami distribusi dan rentang pendapatan minggu pertama di seluruh dataset.
  Dari 10 film top box office di IMDB, dapat diketahui bahwa rentang pendapatannya antara 7 juta hingga 154 juta. Film dengan pendapatan minggu pertama terendah yaitu The Watchers sebesar 7 juta dan The Strangers: Chapter 1 merupakan pendapatan minggu pertama paling rendah kedua yaitu sebesar 11.8 juta dimana hanya berbeda 4 juta untuk kedua film tersebut. 

Perbandingan ini berguna bagi pemangku kepentingan di industri film untuk menilai kesuksesan awal film-film setelah rilis dan merancang strategi pemasaran dan distribusi dengan tepat. Untuk meningkatkan pendapatan minggu pertama, film-film lain dapat meramaikan promosi dengan membuat sebuah pop up store sehingga penonton dapat tertarik untuk menontonnya seperti yang dilakukan oleh film Inside Out 2.

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
Berdasarkan nilai Gross World yang didapatkan oleh masing-masing film, diketahui bahwa film The Lord of the Rings: The Fellowship of the Ring memiliki Gross World tertinggi sebesar 887 juta. Hal tersebut menunjukkan tetap banyak yang menonton film tersebut walaupun film tersebut dirilis pada tahun 2001. 
- Memahami distribusi kesuksesan box office di seluruh dataset.
Film The Lord of the Rings: The Fellowship of the Ring memiliki peran penting dalam menyukseskan dunia industri perfilman karena memiliki nilai Gross Worls tertinggi. Dengan begitu, 

Visualisasi ini berguna untuk memahami kinerja keuangan film dan mengidentifikasi film blockbuster (film yang sangat sukses secara komersial) dalam dataset. Film-film tersebut dapat dinilai sangat sukses karena dilihat berdasarkan Gross World yang merupakan pendapatan kotor dari seluruh dunia.  

</div>
""", unsafe_allow_html=True)


####################################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#RELATIONSHIP
st.subheader("***Relationship***")

# Deskripsi atau teks di bawah judul
#st.write('Pilih variabel untuk scatter plot di sidebar di bawah ini:')

# Sidebar untuk memilih variabel x dan y
#x_variable = st.selectbox('Variabel X', ['Budget', 'Opening_Week_Rev', 'Gross_Us'])
#y_variable = st.selectbox('Variabel Y', ['Gross_World', 'Opening_Week_Rev', 'Gross_Us'])
# Filter data yang akan digunakan
#data = df[[x_variable, y_variable]].dropna()

# Membuat scatter plot dengan Plotly Express
#fig = px.scatter(data, x=x_variable, y=y_variable, 
                 #title=f'Scatter Plot of {x_variable} vs {y_variable}',
                 #labels={x_variable: x_variable, y_variable: y_variable})

# Menampilkan scatter plot menggunakan Streamlit
#st.plotly_chart(fig)

# Plot scatter plot dengan Plotly
fig = px.scatter(data, x='Gross_US', y='Gross_World', title="Hubungan Gross_US Dengan Gross_World",
                 labels={'Gross_US': 'Gross US', 'Gross_World': 'Gross World'})
st.plotly_chart(fig)

#Penjelasan
st.markdown('''
<div style="text-align: justify">

Scatter Plot ini memvisualisasikan hubungan antara dua variabel yang dipilih dalam dataset film IMDB. 
Setiap titik dalam plot mewakili satu film, dengan sumbu X dan Y masing-masing mewakili variabel yang dipilih (Gross US dan Gross World).
Ini membantu dalam mengeksplorasi korelasi atau pola antara variabel-variabel tersebut:

- **Variabel X:** {x_variable}
- **Variabel Y:** {y_variable}

**Insights:**
- Scatter plot membantu untuk melihat sebaran data dan pola hubungan antara variabel-variabel tersebut.
Berdasarkan Scatter Plot diatas, dapat diketahui bahwa **kedua variabel tersebut (Gross US dan Gross World) berhubungan namun lemah karena arah korelasi membentuk garis linear dan cukup tersebar.

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
    Dimana batang sebelah kanan menunjukkan tahun 2001 dan sebelah kiri tahun 2024.
    <br><br>
    <strong>Insights:</strong>
    <ul>
        <li><strong>Tahun Terbaik:</strong> Identifikasi tahun dengan pendapatan Gross World tertinggi.</li>
        Tahun 2024 (diagram batang sebelah kanan) memiliki pendapatan Gross World tertinggi dengan nilai yang ditunjukkan sebesar 1.66 B. Hal tersebut dikarenakan total seluruh Gross World dari film yang dirilis pada tahun 2024. Begitu juga dengan diagram batang sebelah kanan (2001).
        <li><strong>Tren Pendapatan:</strong> Amati apakah pendapatan Gross World cenderung meningkat, menurun, atau stabil dari tahun ke tahun.</li>
        Untuk film yang dirilis pada tahun 2001 dan 2024 memiliki peningkatan pada pendapatan Gross World-nya. Peningkatan dapat dikatakan cukup signifikan karena memiliki perbandingan jumlah yang cukup besar.
        <li><strong>Perbandingan Tahunan:</strong> Bandingkan kontribusi pendapatan dari berbagai tahun secara visual.</li>
        Untuk top box office, film pada tahun 2001 memiliki kontribusi pendapatan yang paling sedikit (887 juta) dikarenakan hanya film The Lord of the Rings: The Fellowship of the Ring yang masuk ke top box office. Konribusi paling besar yaitu dari film yang dirilis pada tahun 2024 (film selain The Lord of the Rings: The Fellowship of the Ring)
    </ul>
    <br>
    Visualisasi ini berguna untuk mendapatkan pemahaman tentang performa finansial tahunan film-film dalam dataset IMDB dan potensialnya untuk mengidentifikasi tahun-tahun yang paling sukses dari segi pendapatan global.
</div>
''', unsafe_allow_html=True)

