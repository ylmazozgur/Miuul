################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


import pandas as pd
# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_csv("rar/persona.csv")
df.head()
df.info()
df.shape


# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()


# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()


# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

df.pivot_table(values="PRICE", index="COUNTRY", aggfunc="count") #pivot table kullanarak yazılışı



# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.pivot_table(values="PRICE", index="COUNTRY", aggfunc="sum")
#ya da
df.groupby("COUNTRY").agg({"PRICE":"sum"})




# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})


# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})




# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).head(3)

# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
#Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE",ascending=False)
agg_df


# GÖREV 4: Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.
agg_df.reset_index(inplace=True) #böyle yazmak yerine "agg_df = agg_df.reset_index()" şeklinde de yazılabilirdi
agg_df.head()



# GÖREV 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
# Aralıkları ‘0_18’, ‘19_23’, ’24_30’, ’31_40’, ’41_70’ şeklinde oluşturunuz.
_araliklar = [0, 18, 23, 30, 40, df["AGE"].max()]
_araliklar_isim = ["0_18", "19_23", "24_30", "31_40", "41_" + str(agg_df["AGE"].max())]

agg_df["age_cat"] = pd.cut(agg_df["AGE"], _araliklar, labels=_araliklar_isim)
agg_df.head()


# GÖREV 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız
#Yeni eklenecek değişkenin adı: customers_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir.

agg_df["customers_level_based"] = agg_df[["COUNTRY", "SOURCE", "SEX", "age_cat"]].agg(lambda x: '_'.join(x).upper(), axis=1)
agg_df.head()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"}) #Hedeflenen çıktı istediği için bunu yaptık.
agg_df.head()


# GÖREV 7: Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["segment"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head()
agg_df.groupby(["segment"]).agg({"PRICE":["mean", "max", "sum"]})


# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

agg_df[agg_df["customers_level_based"] == "TUR_ANDROID_FEMALE_31_40"] #bu kodu çalıştırınca KeyError: 'customer_level_based' hatası alırız. Bunun nedeni: customer'ın index de yer almasıdır. Sütun olarak almamasıdır. Normalde Görev 6 da bunun düzeltilmesi gerekiyordu ama hatayı şimdi yakaladım.

#Hatanın çözümü:
agg_df.reset_index(inplace=True)
agg_df.columns
agg_df[agg_df["customers_level_based"] == "TUR_ANDROID_FEMALE_31_40"] #kodumuz hatasız çalışıyor.

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
agg_df[agg_df["customers_level_based"] == "FRA_IOS_FEMALE_31_40"]



print(agg_df.keys())
print(agg_df.columns)












