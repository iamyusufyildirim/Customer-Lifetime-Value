                                                     #######################################
                                                     # MÜŞTERİ YAŞAM BOYU DEĞERİ HESAPLAMA #
                                                     #######################################


#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    +                                                            UYGULAMA ÖNCESİ                                                           +
#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    +                                                                                                                                      +
#    +          Invoice StockCode                          Description  Quantity         InvoiceDate   Price  Customer ID         Country   +
#    +   0       489434     85048  15CM CHRISTMAS GLASS BALL 20 LIGHTS        12 2009-12-01 07:45:00 6.95000  13085.00000  United Kingdom   +
#    +   1       489434    79323P                   PINK CHERRY LIGHTS        12 2009-12-01 07:45:00 6.75000  13085.00000  United Kingdom   +
#    +   2       489434    79323W                  WHITE CHERRY LIGHTS        12 2009-12-01 07:45:00 6.75000  13085.00000  United Kingdom   +
#    +   3       489434     22041         RECORD FRAME 7" SINGLE SIZE         48 2009-12-01 07:45:00 2.10000  13085.00000  United Kingdom   +
#    +   4       489434     21232       STRAWBERRY CERAMIC TRINKET BOX        24 2009-12-01 07:45:00 1.25000  13085.00000  United Kingdom   +
#    +                                                                                                                                      +
#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    +                                                            UYGULAMA SONRASI                                                                          +
#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    +                                                                                                                                                      +
#    +          Customer ID  Total_Transaction  Total_Price  Average_Order_Value  Purchase_Frequency  Profit_Margin  Customer_Value          CLTV Segment   +
#    +    0     18102.00000                 89 349164.35000           3923.19494             0.02064    34916.43500        80.97503 8591666.19527       A   +
#    +    1     14646.00000                 78 248396.50000           3184.57051             0.01809    24839.65000        57.60587 4348190.36027       A   +
#    +    2     14156.00000                102 196566.74000           1927.12490             0.02365    19656.67400        45.58598 2722937.51052       A   +
#    +    3     14911.00000                205 152147.57000            742.18327             0.04754    15214.75700        35.28469 1631351.87152       A   +
#    +    4     13694.00000                 94 131443.19000           1398.33181             0.02180    13144.31900        30.48311 1217569.56993       A   +
#    +                                                                                                                                                      +
#    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


"""
# 1. Business Problem 
# 2. Data Understanding
# 3. Data Preparation
# 4. Preparation of CLTV Data Structere
# 5. Average Order Value = total_price / total_transaction
# 6. Purchase Frequency = total_transaction / total_number_of_customers
# 7. Repeat Rate & Churn Rate = Birden fazla kez alışveriş yapan müşteri sayısı / tüm müşteriler
# 8. Profit Margin = total_price * 0.10
# 9. Customer Value = average_order_value * purchase_frequency
# 10. Customer Lifetime Value = (customer_value / churn_rate) * profit_margin
# 11. Creation of Segments
"""


# -----------------------
# - 1. Business Problem -
# -----------------------
# Şirketimiz her bir müşterinin yaşam boyu değerini hesaplayarak bu bilgiler özelinde
# müşteri segmentasyonu oluşturup pazarlama stratejileri belirlemek istemektedir.


# -------------------------
# - 2. Data Understanding -
# -------------------------

# Gerekli kütüphane importları ve bazı görsel ayarlamalar
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.float_format", lambda x : "%.5f" % x)


# online_retail_II.xlsx veri setinin projeye dahil edilmesi
def load_dataset():
    data = pd.read_excel("data_sets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
    return data


df_ = load_dataset()
df = df_.copy()


def check_df(dataframe, head=10):
    """
    Veri setinin temel istatistiksel bilgilerini ve yapısal özellikleri
    hakkında bilgilendirme sağlar.


    Parameters
    ----------
    dataframe : dataframe
                Bilgisi istenilen veri seti

    head : int
           Kaç satır gözlem birimi istenildiği bilgisi

    """
    print("###################################")
    print(f"#### İlk {head} Gözlem Birimi ####")
    print("###################################")
    print(dataframe.head(head), "\n\n")

    print("###################################")
    print("###### Veri Seti Boyut Bilgisi ####")
    print("###################################")
    print(dataframe.shape, "\n\n")

    print("###################################")
    print("######## Değişken İsimleri ########")
    print("###################################")
    print(dataframe.columns, "\n\n")

    print("###################################")
    print("####### Eksik Değer Var mı? #######")
    print("###################################")
    print(dataframe.isnull().values.any(), "\n\n")

    print("###################################")
    print("##### Betimsel İstatistikler ######")
    print("###################################")
    print(dataframe.describe().T, "\n\n")

    print("###################################")
    print("### Veri Seti Hakkında Bilgiler ###")
    print("###################################")
    print(dataframe.info())

check_df(dataframe=df)


def missing_values_table(dataframe, na_name=False):
    """
        Veri setindeki eksik değerleri analiz eder
        ve ilgili değerleri tablo formatında ekrana
        bastırır.

        Parameters
        ----------
        dataframe : dataframe
                    Eksik değer analizi yapılacak olan veri seti.

        na_name : bool
                  Eksik değerlere sahip değişken isimlerini
                  liste formatında ekrana bastırır.
                  NOT: Varsayılan değeri False.

        Returns
        -------
        na_name : list
                  Eksik gözlem birimine sahip olan değişken isimlerinin listesi.

        """
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]
    missing_values = (dataframe[na_columns].isnull().sum()).sort_values(ascending=False)
    ratio = (dataframe[na_columns].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)
    table = pd.concat([missing_values, ratio], axis=1, keys=["Value", "%"])
    print(table)

    if na_name:
        return na_columns

na_cols = missing_values_table(dataframe=df, na_name=True)


# -----------------------
# - 3. Veriyi Hazırlama -
# -----------------------

# ataFrame'deki sayısal sütunların temel istatistiksel bilgilerine göz atalım.
df.describe().T


# Veri setinde eksik değerler mevcut. Veri setimiz daha ölçülebilir olsun,
# ölçülebilen değerler üzerinden gidelim isteğimizden dolayı
# veri setindeki eksik değerleri  temizliyoruz.
df.dropna(inplace=True)


# Invoice değişkeninde başında "C" olan ifadeler iadeleri temsil etmektedir.
# İadele olan işlemler veri setinin yapısını bozmaktadır.
# Bu sebeple iadele olan işlemleri veri setinin dışında bıraktık.
df = df[~df["Invoice"].str.contains("C", na=False)]


# Quantity ve Price değişkenlerindeki minimum değer 0'dan büyük olsun isteğimizi belirtiyoruz.
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]


# Bir üründen kaç adet alındığı bilgisi var, ürünün fiyat bilgisi var.
# Ancak o satın alma için ne kadar ödendiği bilgisi yok. Bir ürüne ödenen toplam değeri hesaplayalım.
df["Total_Price"] = df["Quantity"] * df["Price"]



# ---------------------------------------------
# - 4. Converting dataframe to CLTV dataframe -
# ---------------------------------------------

cltv = df.groupby("Customer ID").agg({"Invoice" : lambda invoice : invoice.nunique(),
                                      "Total_Price" : lambda total_price : total_price.sum()
                                      }).sort_values(by="Total_Price", ascending=False)

cltv.columns = ["Total_Transaction", "Total_Price"]

cltv.reset_index(inplace=True)


# ------------------------------------------------------------
# - 5. Average Order Value = total_price / total_transaction -
# ------------------------------------------------------------

# Ortalama Sipariş Değeri = Toplam Fiyat / Toplam İşlem
cltv["Average_Order_Value"] = cltv["Total_Price"] / cltv["Total_Transaction"]


# -------------------------------------------------------------------------
# - 6. Purchase Frequency = total_transaction / total_number_of_customers -
# -------------------------------------------------------------------------

# Satın Alım Sıklığı = Toplam İşlem / Toplam Müşteri Sayısı
cltv["Purchase_Frequency"] = cltv["Total_Transaction"] / cltv.shape[0]


# ----------------------------------------------------------------------------------------------------
# - # 7. Repeat Rate & Churn Rate = Birden fazla kez alışveriş yapan müşteri sayısı / tüm müşteriler -
# ----------------------------------------------------------------------------------------------------

# Müşteri Kaybetme Oranı = 1 — Birden Fazla Alışveriş Yapan Müşteri Oranı
repeat_rate = cltv[cltv["Total_Transaction"] > 1].shape[0] / cltv.shape[0]
churn_rate = 1 - repeat_rate

# -----------------------------------------
# - 8. Profit Margin = total_price * 0.10 -
# -----------------------------------------

# Kar Marjı = Toplam Fiyat * 0.10 (.10 değişkenlik gösterebilir)
cltv["Profit_Margin"] = cltv["Total_Price"] * 0.10


# ----------------------------------------------------------------
# - 9. Customer Value = average_order_value * purchase_frequency -
# ----------------------------------------------------------------

# Müşteri Değeri = Ortalama Sipariş Değeri * Satın Alma Sıklığı
cltv["Customer_Value"] = cltv["Average_Order_Value"] * cltv["Purchase_Frequency"]

# -------------------------------------------------------------------------------
# - 10. Customer Lifetime Value = (customer_value / churn_rate) * profit_margin -
# -------------------------------------------------------------------------------

# CLTV = (Müşteri Değeri / Müşteri Kaybetme Oranı) * Kar Marjı
cltv["CLTV"] = (cltv["Customer_Value"] / churn_rate) * cltv["Profit_Margin"]


# ----------------------------
# - 11. Creation of Segments -
# ----------------------------

cltv["Segment"] = pd.qcut(cltv["CLTV"], 4, labels=["D", "C", "B", "A"])



# CLTV Dataframe'inin Excel ortamına aktarılması:

df_and_cltv_data = df.merge(cltv, on="Customer ID")

df_and_cltv_data = pd.DataFrame(df.merge(cltv, on="Customer ID"))

df_and_cltv_data.to_excel("df_and_cltv_data.xlsx")

cltv[cltv["Customer ID"] == 14646.00000]
