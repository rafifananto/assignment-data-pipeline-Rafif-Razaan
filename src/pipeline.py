import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
import warnings 
warnings.filterwarnings('ignore')

def load_data(filename):
    "Membaca dataset dari file CSV..."
    print("="*50)
    print("1. memuat dataset")
    print('='*50)
    try:
        data = pd.read_csv(filename)
        print (f'Dataset memuat dari {filename}')
        return data
    except Exception as e:
        print(f'gagal memuat {e}')
        return None

def inspect_dataset(data):
    "Melakukan inspeksi data..."
    print("="*50)
    print("2. Melakukan inspeksi data dari {filename}")
    print("*"*50)
    print("Tampilan 5 kolom pertama dari data")
    data.head(5)
    print("Menghitung jumlah bari dan kolom dataset :")
    jmlh_baris = len(data.index)
    jmlh_kolom = len(data.columns)
    print(f'Jumlah baris adalah {jmlh_baris} dan jumlah kolom adalah {jmlh_kolom}')
    print("Menghitung jumlah missing value dari setiap kolom")
    missing_value = data.info()
    print(missing_value)
    print("Jumlah duplicated value")
    duplicate_display=len(data.duplicated())
    print(f'Jumlah duplicated value sebesar {duplicate_display}')

def cleaning_columns(data):
    "Melakukan cleanning data"
    print("="*50)
    print("3. Melakukan cleanning pada dataframe")
    print("="*50)
    data_raw = data.copy()
    # Drop Duplicated value
    data_raw = data_raw.drop_duplicates()
    # Mengganti kolom num-f-doors jadi int
    num_doors_map = {"two":2, "four":4}
    data_raw['num-of-doors'] = data_raw['num-of-doors'].map(num_doors_map)
    # Ganti value pada "num-off-cylinder"
    num_cylinder_map = {"four":4, "six":6, "five":5, "three":3, "twelve":12, "two":2, "eight":8}
    data_raw['num-of-cylinders']=data_raw['num-of-cylinders'].map(num_cylinder_map)
    # Drop missing value setiap kolom
    data_raw = data_raw.dropna()
    # Ubah tipe data tanggal menjadi "datetime" dan pisahkan kolom bulan dan tahun
    data_raw['transaction_date']=pd.to_datetime(data_raw['transaction_date'], format ='mixed')
    data_raw['bulan'] = data_raw['transaction_date'].dt.month
    data_raw['year'] = data_raw['transaction_date'].dt.year
    data_raw.drop('transaction_date', axis=1, inplace = True)
    # Melakukan lowercase pada value kolom yang ada capitalize dan remove 
    data_raw['make']=data_raw['make'].str.lower()
    data_raw['make']=data_raw['make'].str.strip()
    data_raw['fuel-system']=data_raw['fuel-system'].str.lower()
    return data_raw

def data_transformation(data_raw):
    """Melakukan proses data transformation."""
    print("="*50)
    print("4. DATA TRANSFORMATION")
    print("="*50)
    # Ordinal Encoding
    ordinal_cols = ['horsepower-binned']
    ord_encoder = OrdinalEncoder(categories=[['Low', 'Medium', 'High']])
    data_raw[ordinal_cols] = ord_encoder.fit_transform(data_raw[ordinal_cols])
    # Onehoot encoding
    nominal_cols = ['make', 'aspiration', 'body-style', 'drive-wheels', 
                'engine-location', 'engine-type', 'fuel-system']
    data_raw = pd.get_dummies(data_raw, columns=nominal_cols, drop_first=True, dtype=int)
    # Minmax scalling
    numeric_cols = ['normalized-losses', 'wheel-base', 'length', 'width', 'height', 
                'curb-weight', 'engine-size', 'bore', 'stroke', 'compression-ratio', 
                'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'city-L/100km']
                
    scaler = MinMaxScaler()
    data_raw[numeric_cols] = scaler.fit_transform(data_raw[numeric_cols])

    return data_raw

def save_data(data_raw, output_filename="automobileEDA_processed.csv"):
    data_raw.to_csv(output_filename, index=False)
    print(f"Dataset berhasil disimpan ke: {output_filename}")

def pipelining_data(filename):
    data = load_data(filename)
    if data is not None:
        # Menjalankan fungsi inspeksi untuk melihat kondisi awal (muncul di terminal)
        inspect_dataset(data)
        
        # Sesuai urutan yang Anda minta:
        data_raw = cleaning_columns(data)
        data_raw = data_transformation(data_raw)
        save_data(data_raw, output_filename="automobileEDA_processed.csv")

if __name__ == "__main__":
    # Tentukan nama file yang mau diproses di sini
    # Pastikan file ini ada di dalam folder 'raw' di directory yang sama dengan script
    file_input = "raw/automobileEDA_dirty_training.csv"
    
    # Jalankan pipeline
    pipelining_data(file_input)