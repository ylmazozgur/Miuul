########################################
# List Comprehension Alıştırmalar
########################################

# Görev1: List Comprehension yapısı kullanarak car_crashes verisindeki numeric değişkenlerin isimlerini büyük harfe çeviriniz ve başına NUM ekleyiniz.
import seaborn as sns
df = sns.load_dataset("car_crashes")
df.info()

["NUM_"+col.upper() for col in df.columns if df[col].dtype in [int,float]] #Bizden istenen asıl cevap bu. Nümerik değişkenlerin isimlerini büyük harfe çeviren ve NUM_ ekleyen diyor.

["NUM_" + col.upper() if df[col].dtype != "O" else col.upper() for col in df.columns] #Bu cevap ise bize bütün değişkenlerin isimlirini büyük harfe çevirir ve nümerik değişkenlerin başına NUM_ ekler



# Görev2:  List Comprehension yapısı kullanarak car_crashes verisinde isminde "no" barındırmayan değişkenlerin isimlerinin sonuna "FLAG" yazınız.
[sutun+"_FLAG" if "no" not in sutun else sutun for sutun in df.columns] # "no" barındırmayan sütunların sonuna "_FLAG" ekledik

[col.upper() + "_FLAG" if "no" not in col else col.upper() for col in df.columns] #Hocanın cevabı




# Görev3: List Comprehension yapısı kullanarak aşağıda verilen değişken isimlerinden FARKLI olan değişkenlerin isimlerini seçiniz ve yeni bir dataframe oluşturunuz. 
# og_list = ["abbrev", "no_previous"]

# #    total  speeding  alcohol  not_distracted  ins_premium  ins_losses
# # 0 18.800     7.332    5.640          18.048      784.550     145.080
# # 1 18.100     7.421    4.525          16.290     1053.480     133.930
# # 2 18.600     6.510    5.208          15.624      899.470     110.350
# # 3 22.400     4.032    5.824          21.056      827.340     142.390
# # 4 12.000     4.200    3.360          10.920      878.410     165.630


og_list = ["abbrev", "no_previous"]
_new_col = [col for col in df.columns if col not in og_list] #"abbrev" ve "no_previous" sütunlarını içermeyen yeni bir liste oluştur.
_new_df = df[_new_col] # İçermeyecek olan sütunların listesini yeni bir dataframe değişkenine atıyoruz
_new_df

 


########################################
# Pandas Alıştırmalar
########################################

# Görev1: Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız.
import seaborn as sns
import pandas as pd

df = sns.load_dataset("titanic")
df.head()


# Görev2: Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz.
df["sex"].value_counts() #577 erkek, 314 kadın yolcu vardır.
df["sex"].value_counts().sum() #Toplam 891 yolcu vardır.



# Görev3: Her bir sutuna ait unique değerlerin sayısını bulunuz.
df.nunique()



# Görev4: pclass değişkeninin unique değerlerinin sayısını bulunuz.
df["pclass"].unique()


# Görev5: pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
df[["pclass","parch"]].nunique()



# Görev6: embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz ve tekrar kontrol ediniz.
df["embarked"].dtype
df.info()
df["embarked"] = df["embarked"].astype(dtype="category")
df["embarked"].dtype



# Görev7: embarked değeri C olanların tüm bilgelerini gösteriniz.
df[df["embarked"]=="C"]
df[df["embarked"]=="C"].head()



# Görev8: embarked değeri S olmayanların tüm bilgelerini gösteriniz.
df[df["embarked"]!="S"]

df[df["embarked"] != "S"]["embarked"].unique()

df[~(df["embarked"] == "S")]["embarked"].unique()



# Görev9: Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
df["sex"]=="female" & df["age"]<30 #ne olduklarını görmek amacıyla yazdım.

df[ (df["sex"] == "female") & (df["age"]<30) ] #Yaşı 30'dan küçük ve kadın olan yolcuların bilgileri



# Görev10: Fare’i 500’den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
df[ (df["fare"]>500) | (df["age"]>70) ]



# Görev11: Her bir değişkendeki boşdeğerlerin toplamını bulunuz.
df.isnull().sum()


# Görev12: who değişkenini dataframe’den çıkarınız.

df.drop("who",axis=1) #inplace = 1 dersek silinmiş olarak veriye devam ederiz.
df


# Görev13: deck değikenindeki boş değerleri deck değişkenin en çok tekrar eden değeri (mode) ile doldurunuz
df["deck"].mode() #en çok tekrar eden değerin indeksi ve değerin kendisini gösterir.
df["deck"].mode()[0] #en çok tekrar eden değeri gösterdik.
df["deck"].fillna(df["deck"].mode()[0], inplace=True) # en çok tekrar eden değeri veri setinde kalıcı olarak ekledik
df["deck"] = df["deck"].fillna(df["deck"].mode()[0])
df["deck"].isnull().values.any() #boş NA değer var mı diye kontrol ettik.


# Görev14: age değikenindeki boşdeğerleri age değişkenin medyanı ile doldurunuz.
df["age"].median()
df["age"].fillna(df["age"].median(), inplace=True) #Bunu yazdığımızda hatamsı gibi bir şey alabiliriz. Doğru yazım şöyle olacaktır.
df["age"] = df["age"].fillna(df["age"].median())
df["age"].isnull().values.any()


# Görev15: survived değişkeninin pclass ve cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz

df.groupby(["pclass","sex"]).agg({"survived": ["sum", "count", "mean"]})
# Anlatılmak istenen, her pclass'ın cinsiyete göre hayatta kalma durumlarını sum, count ve mean değerlerine göre hesapla. 1.class için: 94 kadından 91'i hayatta kalmış yani %96'sı hayatta kalmış demek.


# Görev16: 30 yaşın altında olanlar 1, 30’a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazın. Yazdığınız fonksiyonu kullanarak titanik veri setinde age_flag adında bir değişken oluşturunuz oluşturunuz. (apply ve lambda yapılarını kullanınız)

age_flag = df["age"].apply(lambda x:1 if x<30 else 0)
#fonksiyon tanımlarsak..
def age(age):
    if age<30:
        return 1
    else:
        return 0
age_flag = df["age"].apply(lambda x: age(x))







# Görev 17: Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
df = sns.load_dataset("tips")
df.head()



# Görev 18: Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
df.groupby("time").agg({"total_bill": ["sum", "min", "max", "mean"]})



# Görev 19:  Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz
df.groupby(["day", "time"]).agg({"total_bill": ["sum", "min", "mean", "max"]})




# Görev 20:  Lunch zamanına ve kadın müşterilere ait total_bill ve tip  değerlerinin day’e göre toplamını, min, max ve ortalamasını bulunuz.
df["time"]=="Lunch"

df [(df["time"] == "Lunch") & (df["sex"] == "Female") ].groupby("day").agg({"total_bill": ["sum", "min", "mean", "max"],
                                                                            "tip": ["sum", "min", "mean", "max"]})
df.head()
df["day"].nunique()



# Görev 21: size’i 3’ten küçük, total_bill’i 10’dan büyük olan siparişlerin ortalaması nedir? (loc kullanınız).
df.loc[(df["size"] < 3) & (df["total_bill"] > 10) , "total_bill"].mean()



# Görev 22:  total_bill_tip_sum adında yeni bir değişken oluşturunuz. Her bir müşterinin ödediği totalbill ve tip in toplamını versin.
df["total_bill"], df["tip"]

df["total_bill_tip_sum"] = df["total_bill"] + df["tip"] #sorunun cevabı.
total_bill_tip_sum = df["total_bill"] + df["tip"] #sorunun cevabı.

df.groupby(df["sex"]).agg({"total_bill": "sum", "tip": "sum"})



# Görev 23:  total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe’e atayınız
total_bill_tip_sum.sort_values()[0:30]

_df_total_bill_tip_sum = df.sort_values("total_bill_tip_sum", ascending=False)[:30] #22.soruda df["total_bill_tip_sum"] içine aldığımız için bu şekilde yazabiliyoruz. Eğer dataframe içine almamış olsaydık, alttaki gibi yazacaktık.
_df_total_bill_tip_sum = total_bill_tip_sum.sort_values(ascending=False)[:30] 

_df_total_bill_tip_sum.shape







