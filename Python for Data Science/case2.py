import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



# Amacım sadece pandas kullanmak değil, aynı zamanda sql sorgularıda yazmak.


# Soru 1: miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_excel("rar/miuul_gezinomi.xlsx")

df.info() #veri seti hakkındaki kısa bilgi
df.shape # 9 sütun ve yaklaşık 60k satırdan oluşuyor 
"""df.shape
Select count(*)
from sheet1
"""

df.head()
"""df.head()
Select * 
from [veritabanı] # sheet1 diyeceğim.
limit 5
"""


# Soru 2: Kaç unique şehir vardır? Frekansları nedir?
df["SaleCityName"].nunique()
"""df["SaleCityName"].nunique()
Select count(distinct SaleCityName)
from sheet1
"""

df["SaleCityName"].value_counts()
"""df["SaleCityName"].value_counts()
Select SaleCityName, count(*) as count1
from sheet1
group by SaleCityName
order by count1 desc
"""



# Soru 3: Kaç unique Concept vardır?
df["ConceptName"].nunique()

# Soru 4: Hangi Concept'dan kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()


# Soru 5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})
"""df.groupby("SaleCityName").agg({"Price": "sum"})
select SaleCityName, sum(Price)
from sheet1
group by SaleCityName
"""

# Soru 6: Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"})

# Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})

# Soru 8: Conceptlere  göre PRICE ortalamaları nedir?
df.groupby(by=["ConceptName"]).agg({"Price": "mean"})

# Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
df.groupby(["ConceptName", "SaleCityName"]).agg({"Price": "mean"})
df.groupby(by=["ConceptName", "SaleCityName"]).agg({"Price": "mean"})
"""df.groupby(["ConceptName", "SaleCityName"]).agg({"Price": "mean"})
select ConceptName, SaleCityName, avg(Price)
from sheet1
group by ConceptName, SaleCityName
"""


df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"})






# Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
#SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
#Aralıkları ikna edici şekilde oluşturunuz. Örneğin: ‘0_7’, ‘7_30’, ‘30_90’, ‘90_max’ aralıklarını kullanabilirsiniz.
#Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz.
_araliklar = [-1,7,30,90, df["SaleCheckInDayDiff"].max()]
_aralikar_isim = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]
df["Cat_SaleCheckInDayDiff"] = pd.cut(df["SaleCheckInDayDiff"], _araliklar, labels=_aralikar_isim)

 
df.info()
#df.head(50).to_excel("Cat_SaleCheckInDayDiff.xlsx", index=False) #excel oluşturuyor.



# Görev 3:  COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
# Şehir-Concept-EB Score(benim değişkenim olanı yazacağız), Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz?

# Şehir, Konsept, ve Cat_saleCheckInDayDiff e göre ortalama ücret ve frekansı
df.groupby(["SaleCityName","ConceptName","Cat_SaleCheckInDayDiff"]).agg({"Price": ["mean", "count"]})

# Şehir-Concept- Sezon e göre ortalama ücret ve frekansı
df.groupby(["ConceptName", "Seasons", "SaleCityName"]).agg({"Price": ["mean", "count"]})
df["Seasons"].value_counts()

# Şehir-Concept-CInDay e göre ortalama ücret ve frekansı
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})




# Görev 4:  City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Elde ettiğiniz çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price",ascending=False)
agg_df.head(5)
"""agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price",ascending=False)
SELECT SaleCityName, ConceptName, Seasons, avg(Price)
FROM gezinomi
GROUP by ConceptName, SaleCityName, Seasons
order by avg(Price) DESC
"""





# GÖREV 5: Indekste yer alan isimleri değişken ismine çeviriniz.
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
agg_df.reset_index(inplace=True)
agg_df.head()




# GÖREV 6: Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
#Yeni eklenecek değişkenin adı: sales_level_based
#Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.
agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x : '_'.join(x).upper(), axis=1)



# GÖREV 7: Personaları segmentlere ayırınız.
# Yeni personaları PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["Segment"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"]) #kodun açıklaması olarak şunu yazabilirim.
#pd.qcut(..., 4) -> Seçilen sütunun ya da verinin değerlerini 4 eşit parçaya bölmesi anlamına gelir. 3 yazarsak 3 eşit parçaya böler. Labels kısmı ise küçük büyüğe doğru ilerleyen şekilde isimlendirme yapılır.
agg_df.head(15)
agg_df.groupby("Segment").agg({"Price": ["mean", "max", "sum"]})



# GÖREV 8: Oluşan son df'i price değişkenine göre sıralayınız.
#Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
agg_df.sort_values(by="Price")

new_customer = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[ agg_df["sales_level_based"] == new_customer ]









