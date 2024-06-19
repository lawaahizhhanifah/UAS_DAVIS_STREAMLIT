import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.header('Penjualan Produk Adventure Works :page_with_curl:', divider='grey')
# Menyisipkan baris kosong
st.markdown("<br>", unsafe_allow_html=True)

#########################################
# Membuat koneksi ke database
db_engine = create_engine('mysql+mysqlconnector://root:@localhost:3307/davis_adventureworks')

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
            
Visualisasi ini menampilkan total penjualan produk berdasarkan promosi yang dilakukan. Setiap batang dalam diagram menunjukkan jumlah penjualan yang terkait dengan promosi tersebut.

**Insights:**
- **Promosi Terbaik:** Identifikasi promosi yang menghasilkan penjualan tertinggi.
- **Perbandingan Promosi:** Bandingkan kontribusi penjualan dari berbagai promosi secara visual.
- **Efektivitas Promosi:** Evaluasi efektivitas berbagai promosi berdasarkan penjualan yang dihasilkan.

Visualisasi ini membantu dalam memahami performa penjualan produk berdasarkan promosi yang dilakukan, serta membantu dalam pengambilan keputusan untuk strategi promosi yang lebih efektif.
            
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
            
***Pie chart*** ini menampilkan proporsi penjualan produk berdasarkan wilayah negara penjualan dalam dataset penjualan online. Setiap bagian dalam diagram donat mewakili persentase penjualan yang dihasilkan oleh setiap negara.

**Insights:**
- **Kontribusi Negara:** Identifikasi negara-negara yang menyumbang pendapatan penjualan terbesar.
- **Pembandingan Wilayah:** Bandingkan proporsi penjualan antar negara secara visual.
- **Distribusi Penjualan:** Memahami sebaran geografis penjualan produk dan kontribusi masing-masing wilayah terhadap total penjualan.

Visualisasi ini bermanfaat untuk analisis geografis penjualan, segmentasi pasar berdasarkan wilayah, dan untuk mendapatkan wawasan tentang performa penjualan berdasarkan negara penjualan.
            
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
- **Korelasi Produk dan Pesanan:** Scatter plot membantu untuk melihat apakah ada hubungan atau pola antara harga produk dan jumlah pesanan. Posisi titik-titik yang berkelompok atau tersebar dapat mengindikasikan korelasi antara dua variabel ini.
- **Outliers:** Identifikasi transaksi yang mungkin menjadi outlier, seperti produk dengan harga tinggi namun pesanannya rendah atau sebaliknya.
- **Segmentasi Produk:** Scatter plot juga dapat digunakan untuk memvisualisasikan pola atau cluster berdasarkan harga produk dan jumlah pesanan, membantu dalam segmentasi produk.

Visualisasi ini berguna untuk analisis penjualan dan strategi ***pricing*** dalam bisnis ***e-commerce***, serta untuk mendapatkan wawasan tentang preferensi pelanggan terhadap harga produk.
            
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
- **Tren Penjualan:** Amati apakah terdapat tren peningkatan, penurunan, atau stabilitas penjualan dari bulan ke bulan.
- **Perbandingan Bulanan:** Bandingkan kinerja penjualan antar bulan secara visual.

Visualisasi ini membantu dalam memahami pola penjualan bulanan, mengidentifikasi bulan-bulan dengan performa penjualan yang baik, serta untuk merencanakan strategi pemasaran dan operasional berdasarkan tren penjualan.
            
</div>
""", unsafe_allow_html=True)

#st.line_chart(sales_data.set_index('Month'))

