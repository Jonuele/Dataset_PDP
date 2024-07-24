import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import matplotlib.pyplot as plt
import missingno as msno
import contextily as ctx


calendar=pd.read_csv(r"C:\Users\Usuario\Desktop\Proyecto - Prediccion de Precios\Get data\calendar.csv", header=0)
listings=pd.read_csv(r"C:\Users\Usuario\Desktop\Proyecto - Prediccion de Precios\Get data\listings (1).csv",header=0)
neighbourhoods=pd.read_csv(r"C:\Users\Usuario\Desktop\Proyecto - Prediccion de Precios\Get data\neighbourhoods.csv", header=0)
#reviews=pd.read_csv(r"C:\Users\Usuario\Desktop\Proyecto - Prediccion de Precios\Get data\reviews.csv",header=0)

### MANIPULACION Y LIMPIEZA DEL DATAFRAME ###
        # print(calendar.info())
        # print(calendar.shape)

                    # Data columns (total 7 columns):
                    #  #   Column          Dtype
                    # ---  ------          -----
                    #  0   listing_id      int64
                    #  1   date            object
                    #  2   available       object
                    #  3   price           object
                    #  4   adjusted_price  float64
                    #  5   minimum_nights  float64
                    #  6   maximum_nights  float64
                    # dtypes: float64(3), int64(1), object(3)
                    # memory usage: 721.9+ MB
                    # None
                    # (13517780, 7)

 ##En principio reordenamos los Dtype de cada columna###
 
calendar["date"]=pd.to_datetime(calendar['date'], format='%Y-%m-%d')
calendar['price']=calendar['price'].str.replace('$','').str.replace(',','').astype(float)

### 1. Manipulacion de Nulos ###

missing_nan = calendar[['listing_id', 'date', 'available', 'price', 'adjusted_price', 'minimum_nights', 'maximum_nights']].isna().sum()

        # **Valores nulos  

        # listing_id               0
        # date                     0
        # available                0
        # price                    0
        # adjusted_price    13517780
        # minimum_nights           3
        # maximum_nights           3

missing_zero=(calendar[['listing_id','date','available','price','adjusted_price','minimum_nights','maximum_nights']]==0).sum()

       # **Valores en cero
        # listing_id          0
        # date                0
        # available           0
        # price             730
        # adjusted_price      0
        # minimum_nights      0
        # maximum_nights      0


   #**Reemplazamos los valores nulos de las columnas 'minimum_nights','maximum_nights' por "0" ya que son datos que vamos a utilizar,
   #entendiendo que no hubo datos sobre esas 3 reservas.**###
calendar[['minimum_nights','maximum_nights']]=calendar[['minimum_nights','maximum_nights']].replace(np.nan,0)

     #**Valores en cero
        # listing_id          0
        # date                0
        # available           0
        # price             730
        # adjusted_price      0
        # minimum_nights      3
        # maximum_nights      3

#Por otro lado la columna 'adjusted_price' está completamente vacia, podemos eliminarla
calendar= calendar.drop(columns=['adjusted_price'])

#Con respecto a los Valores en Cero, despues del analisis vemos que se tratan de solo dos departamentos con precio 0 con fechas futuras.
#podemos eliminarlas para que no afecten a nuestro analisis

price_zero=calendar[calendar['price']==0]
price_zero=price_zero['listing_id'].unique()
    #print(price_zero)  
     
     #[16119052 43112374]
calendar=calendar[calendar['price'] != 0]


calendar['minimum_nights']=calendar['minimum_nights'].astype(int)
calendar['maximum_nights']=calendar['maximum_nights'].astype(int)

####RESULTADO FINAL DEL DATASET "CALENDAR.CSV"####
            #print(calendar.info())
            #print(calendar.shape)
            
                        #  #   Column          Dtype
                        # ---  ------          -----
                        #  0   listing_id      int64
                        #  1   date            datetime64[ns]
                        #  2   available       object
                        #  3   price           float64
                        #  4   minimum_nights  int32
                        #  5   maximum_nights  int32
                        
                        # (13517050, 6)




###Analisis "NEIGHBOURHOODS.CSV"

        # print(neighbourhoods.columns)
        # print(neighbourhoods.shape)
        # print(neighbourhoods.info())

                # Index(['neighbourhood_group', 'neighbourhood'], dtype='object')
                # (49, 2)
                
                # Data columns (total 2 columns):
                #  #   Column               Non-Null Count  Dtype
                # ---  ------               --------------  -----
                #  0   neighbourhood_group  0 non-null      float64
                #  1   neighbourhood        49 non-null     object
                # dtypes: float64(1), object(1)
                # memory usage: 916.0+ bytes





### MANIPULACION Y LIMPIEZA DEL DATAFRAME ###

            #print(listings.columns)
            #print(listings.info())
            #print(listings.shape)


                    # RangeIndex: 37035 entries, 0 to 37034
                    # Data columns (total 18 columns):
                    #  #   Column                          Non-Null Count  Dtype
                    # ---  ------                          --------------  -----
                    #  0   id                              37035 non-null  int64
                    #  1   name                            37035 non-null  object
                    #  2   host_id                         37035 non-null  int64
                    #  3   host_name                       37033 non-null  object
                    #  4   neighbourhood_group             0 non-null      float64
                    #  5   neighbourhood                   37035 non-null  object
                    #  6   latitude                        37035 non-null  float64
                    #  7   longitude                       37035 non-null  float64
                    #  8   room_type                       37035 non-null  object
                    #  9   price                           34005 non-null  float64
                    #  10  minimum_nights                  37035 non-null  int64
                    #  11  number_of_reviews               37035 non-null  int64
                    #  12  last_review                     29760 non-null  object
                    #  13  reviews_per_month               29760 non-null  float64
                    #  14  calculated_host_listings_count  37035 non-null  int64
                    #  15  availability_365                37035 non-null  int64
                    #  16  number_of_reviews_ltm           37035 non-null  int64
                    #  17  license                         430 non-null    object
                    # dtypes: float64(5), int64(7), object(6)
                    # memory usage: 5.1+ MB
                    # None
                    # (37035, 18)
                    
listings=listings.drop(columns=['neighbourhood_group','license'])                 
listings['last_review']=listings['last_review'].replace(np.nan,"")
listings['last_review']=pd.to_datetime(listings['last_review'], format='%Y-%m-%d')

listings['price']=listings['price'].fillna(0)
listings=listings[(listings['price'] != 0) | ((listings['price'] != 0) & (listings['host_id'] == 374872974))]
listings=listings[listings['neighbourhood'].isin(['Palermo','Belgrano','Recoleta','San Telmo','Areco','Balvanera','Villa Crespo','Saavedra'])]


# print(listings.info())
# print(listings.describe())
# print(listings.shape)

# msno.matrix(listings)
# plt.show()






###Grafico tipo de propiedades###

grafics_1=listings['room_type'].value_counts()
grafics_1=grafics_1.reset_index()
grafics_1.columns=['room_type','cantidad']
        #print(grafics_1)
                        #          room_type  cantidad
                        # 0  Entire home/apt     19837
                        # 1     Private room      1372
                        # 2      Shared room       113
                        # 3       Hotel room        51
                


# sns.barplot(data=grafics_1, x='room_type',y='cantidad')
# plt.xlabel('Tipo de propiedad')
# plt.ylabel('Cantidad')
# plt.title('Tipos de propiedades y cantidades')
#plt.show()

###Grafico: Distribucion de propiedades (barrios) ###

grafics_2=listings['neighbourhood'].value_counts()
grafics_2=grafics_2.reset_index()
grafics_2.columns=['neighbourhood','cantidad']
        #print(grafics_2)
                #   neighbourhood  cantidad
                # 0       Palermo     11167
                # 1      Recoleta      4867
                # 2      Belgrano      1803
                # 3  Villa Crespo      1187
                # 4     Balvanera      1180
                # 5     San Telmo       938
                # 6      Saavedra       231

# sns.barplot(data=grafics_2, x='neighbourhood',y='cantidad')
# plt.xlabel('Ubicacion')
# plt.ylabel('Cantidad')
# plt.title('Distribucion de propiedades por barrio en CABA')
# plt.show()

###Grafico minimo de noches ###

grafics_3 = listings.groupby('minimum_nights')['host_name'].count()
grafics_3=grafics_3.reset_index()
grafics_3.columns=['minimum_nights','host_name']

        #print(grafics_3)
                        #     minimum_nights  host_name
                        # 0                1       5712
                        # 1                2       5718
                        # 2                3       4807
                        # 3                4       1473
                        # 4                5       1079
                        # ..             ...        ...

# sns.scatterplot(data=grafics_3, x='minimum_nights', y='host_name')
# plt.xlabel('Noches minimas ofrecidas')
# plt.ylabel('Cantidad de Oferentes')
# plt.title('Dispercion de noches minimas requeridas y sus oferta')
# plt.show()


###Grafico de precio promedio por propiedad###

###Se puede observar un error en la evalucacion de los decimales en la columna "price",
# por lo tanto dividimos por 1000 para tener mas logica en la muestra, aunque de todas formas es algo a relevar y buscar la info correcta
# y de esta forma obtener correctamente outliers

grafics_4= listings[['id','host_name','neighbourhood','room_type','price']]
grafics_4['price_update']=listings['price']/1000
#print(grafics_4.describe())
                        #                  id         price  price_update
                        # count  2.137300e+04  2.137300e+04  21373.000000
                        # mean   6.563583e+17  7.278494e+04     72.784943
                        # std    4.511521e+17  1.068231e+06   1068.230730
                        # min    1.150800e+04  6.000000e+02      0.600000
                        # 25%    4.591259e+07  2.458400e+04     24.584000
                        # 50%    8.418504e+17  3.277900e+04     32.779000
                        # 75%    1.030297e+18  4.825800e+04     48.258000
                        # max    1.188644e+18  9.105257e+07  91052.574000
                        
# sns.boxplot(data=grafics_4, x='neighbourhood', y='price_update')
# plt.xlabel('Barrios')
# plt.ylabel('Precio')
# plt.title('Comparativa Barrio vs Precio por noche USD')
# plt.show()

###Grafico mapa de densidad por propiedad

#Podemos ajustar algunas propiedades que se escapan de la densidad del mapa, y de la zona de concentracion

grafics_5=listings[['latitude','longitude','neighbourhood','room_type']]

ax= sns.scatterplot(data=grafics_5, x='longitude',alpha=0.1, y='latitude')
plt.xlabel('longitud')
plt.ylabel('latitud')
plt.title('Concentracion de departamentos en CABA')

ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.CartoDB.Positron)
plt.show()
