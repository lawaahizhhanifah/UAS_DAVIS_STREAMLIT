import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import pymysql
import random

st.header('Penjualan Produk Adventure Works :page_with_curl:', divider='grey')
# Menyisipkan baris kosong
st.markdown("<br>", unsafe_allow_html=True)

#########################################
def create_connection():
    host = "kubela.id"
    port = 3307
    user = "davis2024irwan"
    password = "wh451n9m@ch1n3"
    database = "aw"
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Fungsi untuk menjalankan query dan mendapatkan data
def fetch_data(query):
    connection = create_connection()
    if connection is None:
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        connection.close()
        
# Membuat koneksi ke database
db_engine = create_engine("mysql+pymysql://davis2024irwan:wh451n9m%40ch1n3@kubela.id:3306/aw")

#########################################
#COMPARISON
st.subheader("***Comparison***")
#st.subheader("**1. Angka Penjualan Produk Berdasarkan Promosi (***Comparison***)**")

# Ambil data dari tabel dimpromotion
select_dimpromotion = "SELECT EnglishPromotionName, PromotionKey FROM dimpromotion"
promotion = pd.read_sql(select_dimpromotion, db_engine)

# Ambil data dari tabel factinternetsales
select_salesamount = "SELECT SalesAmount, PromotionKey FROM factinternetsales"
sales_amount = pd.read_sql(select_salesamount, db_engine)

# Gabungkan data dari kedua tabel berdasarkan PromotionKey
data = pd.merge(promotion, sales_amount, on='PromotionKey')

# Menghitung total penjualan per promosi
data_grouped = data.groupby('EnglishPromotionName')['SalesAmount'].sum().reset_index()

#st.markdown("**Angka Penjualan Produk Berdasarkan Promosi**")

# Menampilkan bar chart interaktif menggunakan Streamlit
#st.bar_chart(data_grouped.set_index('EnglishPromotionName')['SalesAmount'])

# Plotly Bar Chart
fig = px.bar(data_grouped, x='EnglishPromotionName', y='SalesAmount', title="Angka Penjualan Produk Berdasarkan Promosi",
             labels={'EnglishPromotionName': 'Promosi', 'SalesAmount': 'Penjualan'})

# Menampilkan plot di Streamlit dengan ukuran yang ditentukan
st.plotly_chart(fig)

#Penjelasan
st.markdown("""
<div style="text-align: justify">
            
Visualisasi ini menampilkan total penjualan produk berdasarkan promosi yang dilakukan. Setiap batang dalam diagram menunjukkan jumlah penjualan yang terkait dengan promosi tersebut. Terdapat 4 jenis promosi yaitu:
- **No Discount**
- **Touring-1000 Promotion**
- **Touring-3000 Promotion**
- **Volume Discount 11 to 14**

**Insights:**
- **Promosi Terbaik:** Identifikasi promosi yang menghasilkan penjualan tertinggi.
Dari 4 jenis promosi diatas, dapat diketahui bahwa jenis promosi **No Discount** memiliki **total penjualan tertinggi** sebesar **27.3 juta**.
- **Perbandingan Promosi:** Bandingkan kontribusi penjualan dari berbagai promosi secara visual.
Dari visualisasi di atas, dapat diketahui bahwa penjualan **tanpa adanya diskon memiliki kontribusi terbesar** dibanding promosi lainnya seperti Touring 1000 Promotion (tidak ada penjualan), Touring 3000 Promotion (tidak ada penjualan), dan Volume Discount 11 to 14 (2 juta).
- **Efektivitas Promosi:** Evaluasi efektivitas berbagai promosi berdasarkan penjualan yang dihasilkan.
Dapat dilihat dari visualisasi diatas bahwa dengan adanya promosi tersebut tidak berpengaruh besar terhadap peningkatan penjualan produk yang ditawarkan.

Visualisasi ini membantu dalam memahami performa penjualan produk berdasarkan promosi yang dilakukan, serta membantu dalam pengambilan keputusan untuk strategi promosi yang lebih efektif. Dengan demikian dapat disimpulkan bahwa tanpa adanya diskon penjualan perusahaan dapat meningkat. Namun, jika perusahaan ingin meningkatkan penjualannya dapat menerapkan promosi dengan potongan harga yang menarik pada produk-produk tertentu.  
            
</div>
""", unsafe_allow_html=True)


#########################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#COMPOSITION
st.subheader("***Composition***")
# Ambil data dari tabel dimgeography
select_dimgeography = "SELECT EnglishCountryRegionName, SalesTerritoryKey FROM dimgeography" 
territory = pd.read_sql(select_dimgeography, db_engine)

# Ambil data dari tabel factinternetsales
select_salesamount = "SELECT SalesAmount, SalesTerritoryKey FROM factinternetsales"  
sales_amount = pd.read_sql(select_salesamount, db_engine)

# Gabungkan data dari kedua tabel berdasarkan SalesTerritoryKey
data = pd.merge(territory, sales_amount, on='SalesTerritoryKey')

# Mengelompokkan data berdasarkan Negara dan menghitung total penjualan untuk setiap kota
data_grouped = data.groupby('EnglishCountryRegionName')['SalesAmount'].sum().reset_index()

# Menghitung total penjualan keseluruhan
total_sales = data_grouped['SalesAmount'].sum()

# Menghitung proporsi penjualan untuk setiap kota
data_grouped['SalesPercentage'] = data_grouped['SalesAmount'] / total_sales * 100

# Plot diagram donat dengan Plotly
fig = px.pie(data_grouped, values='SalesPercentage', names='EnglishCountryRegionName',
             hover_data=['SalesAmount'], title="Proporsi Penjualan Produk Berdasarkan Wilayah Negara Penjualan", labels={'SalesPercentage': 'Persentase Penjualan'})
st.plotly_chart(fig)

#Penjelasan
st.markdown("""
<div style="text-align: justify">
            
***Pie chart*** ini menampilkan proporsi penjualan produk berdasarkan wilayah negara penjualan dalam dataset penjualan online. Setiap bagian dalam diagram donat mewakili persentase penjualan yang dihasilkan oleh setiap negara. Diagram atas menunjukkan bahwa penjualan produk tersebar di beberapa wilayah negara yaitu:
- United States
- Australia
- Germany
- United Kingdom
- Canada
- France

**Insights:**
- **Kontribusi Negara:** Identifikasi negara-negara yang menyumbang pendapatan penjualan terbesar.
Dari 6 negara, dapat diketahui bahwa **United States** memiliki peran penting dalam peningkatan penjualan produk dikarenakan **memiliki kontribusi paling besar** (sebesar **50,7%** dengan **total penjualan** sekitar **1 miliar**) walaupun negara lain menghasilkan penjualan produk yang rendah.
- **Pembandingan Wilayah:** Bandingkan proporsi penjualan antar negara secara visual.
Dari diagram di atas, diketahui bahwa negara **France** memiliki **proporsi paling sedikit** dibandingkan negara lainnya sebesar **6.25%**. Sedangkan **Australia** menghasilkan **total penjualan terbesar kedua** yaitu sebesar **362 juta (17.8%)**.
- **Distribusi Penjualan:** Memahami sebaran geografis penjualan produk dan kontribusi masing-masing wilayah terhadap total penjualan.
Dapat diketahui bahwa produk yang ditawarkan **banyak dibutuhkan di negara United States** dikarenakan banyak peminat olahraga sepeda di negara tersebut.

Visualisasi ini bermanfaat untuk analisis geografis penjualan, segmentasi pasar berdasarkan wilayah, dan untuk mendapatkan wawasan tentang performa penjualan berdasarkan negara penjualan. Dengan demikian perusahaan dapat memfokuskan penjualan di negara United States dan Australia karena negara memiliki pendapatan penjualan tertinggi. Namun, tidak menutup kemungkinan perusahaan juga gencar dalam mempromosikan produknya di negara lain.
            
</div>
""", unsafe_allow_html=True)


#########################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#RELATIONSHIP
st.subheader("***Relationship***")
# Ambil data dari tabel factinternetsales
select_data = "SELECT UnitPrice, OrderQuantity  FROM factinternetsales" 
data = pd.read_sql(select_data, db_engine)

# Plot scatter plot dengan Plotly
fig = px.scatter(data, x='UnitPrice', y='OrderQuantity', title="Hubungan Harga Produk Dengan Jumlah Pesanan",
                 labels={'UnitPrice': 'Harga Produk', 'OrderQuantity': 'Jumlah Pesanan'})
st.plotly_chart(fig)

#Penjelasan
st.markdown("""
<div style="text-align: justify">
            
Scatter plot ini mengilustrasikan hubungan antara harga produk dengan jumlah pesanan dalam dataset penjualan online. Setiap titik dalam plot mewakili satu transaksi, dengan sumbu X dan Y masing-masing menunjukkan harga produk dan jumlah pesanan yang dilakukan.

**Insights:**
- **Korelasi Produk dan Pesanan:** Scatter plot membantu untuk melihat apakah ada hubungan atau pola antara harga produk dan jumlah pesanan.
Posisi titik-titik yang berkelompok atau tersebar dapat mengindikasikan korelasi antara dua variabel ini. Berdasarkan Scatter Plot diatas, dapat diketahui bahwa **kedua variabel tersebut (harga produk dan jumlah pesanan) tidak berhubungan karena arah korelasi lurus mendatar**.
            
</div>
""", unsafe_allow_html=True)

# Pisahkan data ke dalam dua kolom yang sesuai
#unit_price = data['UnitPrice']
#sales_amount = data['SalesAmount']

# Plot scatter plot dengan Streamlit
#st.scatter_chart(data)


#########################################
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
#DISTRIBUTION
st.subheader("***Distribution***")
# Query SQL untuk mengambil data sales amount dari tabel factinternetsales dan melakukan group by berdasarkan bulan
query_sales_by_month = """
    SELECT MONTH(OrderDateKey) AS Month, SUM(SalesAmount) AS TotalSales
    FROM factinternetsales
    GROUP BY Month;
"""

# Baca data dari database ke dalam DataFrame
sales_data = pd.read_sql(query_sales_by_month, db_engine)

# Plot bar chart dengan Plotly
fig = px.bar(sales_data, x='Month', y='TotalSales', title="Perkembangan Penjualan Tiap Bulan",
             labels={'Month': 'Bulan', 'TotalSales': 'Total Penjualan'})

st.plotly_chart(fig)

#Penjelasan
st.markdown("""
<div style="text-align: justify">
            
Grafik batang di atas menampilkan perkembangan penjualan tiap bulan berdasarkan data faktual dari tabel penjualan online. Setiap batang dalam diagram mewakili total penjualan yang dicapai pada bulan yang sesuai.

**Insights:**
- **Bulan Terbaik:** Identifikasi bulan dengan total penjualan tertinggi.
Diagram di atas menunjukkan bahwa terdapat 10 bulan untuk visualisasikan total penjualan tiap bulannya. **Total penjualan tertinggi** terjadi pada **bulan ke-10** dan **terendah** pada **bulan ke-5** dengan total penjualanya masing-masing yaitu sebesar **1.6** juta dan **467 ribu**.
- **Tren Penjualan:** Amati apakah terdapat tren peningkatan, penurunan, atau stabilitas penjualan dari bulan ke bulan.
Dari data total penjualan tiap bulannya, dapat diketahui bahwa **total penjualan** bergerak secara **stagnan** dari waktu ke waktu dimana **data bergerak meningkat di satu waktu** kemudian **turun lagi**. **Total penjualan** mengalami **kenaikan petamam kalinya** pada **bulan ke-3 (767 ribu)** kemudian turun pada **bulan ke-5 (467 ribu)** lalu mengalami **kenaikan lagi** pada **bulan ke-10 (1.6 juta)**.

Visualisasi ini membantu dalam memahami pola penjualan bulanan, mengidentifikasi bulan-bulan dengan performa penjualan yang baik, serta untuk merencanakan strategi pemasaran dan operasional berdasarkan tren penjualan. Dengan demikian, dapat disimpulkan bahwa dari bulan ke bulan, **performa penjualan Adventure Works cukup baik** dikarenakan **tidak adanya penurunan** total penjualan produk **secara signifikan**. Selain itu, untuk tahun kedepannya perusahaan juga dapat **mempromosikan produk baru dan menawarkan berbagai promosi yang menarik para pelanggan** sekitar **akhir tahun (bulan ke-8 hingga ke-10)**.
            
</div>
""", unsafe_allow_html=True)

#st.line_chart(sales_data.set_index('Month'))

