#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Librerías a utilizar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
from datetime import datetime,date,timedelta
import dateutil.relativedelta as relativedelta


# In[9]:


# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized') # Que nos inicialize chrome maximizado
options.add_argument('--disable-extensions') # Que nos deshabilite las extensiones

driver_path = 'C:\\Users\\LAGOJ\\Downloads\\chromedriver_win32\\chromedriver.exe'

driver = webdriver.Chrome(driver_path, chrome_options=options) #Inicializamos nuestro driver, el cual será el que controle cada uno de los pasos.


# In[10]:


# Inicializamos el navegador
driver.get('https://eltiempo.es')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button.didomi-components-button didomi-button didomi-dismiss-button didomi-components-button--color didomi-button-highlight highlight-button'.replace(' ', '.'))))\
    .click() #En este punto vamos a ir a buscar el botón de aceptar las cookies, añadiendo el enlace que nos proporciona el código html.

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'input#term')))\
    .send_keys('Barcelona') #En este punto escribimos Barcelona en el buscardor

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'i.icon.icon-search')))\
    .click() # Una vez añadido Barcelona en el buscador, pulsamos en el icono de la lupa.

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'i.icon.icon-sm.icon-city')))\
    .click() # Pulsamos en el icono de ciudad, que nos dará la información relativa a Barcelona

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[5]/div[1]/div[4]/div/main/section[4]/section/div/article/section/ul[1]/li[2]/h2/a')))\
    .click() # Pulsamos en la casilla de horas. Para ello debemos añadir el full Xpath del enlace.


# Por último, buscamos la tabla a descargar.
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[5]/div[1]/div[4]/div/section[4]/section/div[1]/ul')))




# In[258]:


# Guardamos nuestra tabla
texto_columnas = driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div[4]/div/section[4]/section/div[1]/ul')

# La transformamos a texto para poder trabajar con ella.
texto_columnas = texto_columnas.text

# Cerramos nuestro driver.
driver.quit()


# In[259]:


# Separamos nuestro texto cuando encuentra la palabra Mañana. Nos quedamos con los dos elementos y guardamos en dos variables.
tiempo_hoy_temp = texto_columnas.split('Mañana')[0].split('\n')[1:-1]
tiempo_mañana_temp = texto_columnas.split('Mañana')[1].split('\n')[1:-1]


# In[260]:


# Creamos la lista tiempo hoy añadiendo la información de tiempo_hoy_temp.
tiempo_hoy=[]
for i in tiempo_hoy_temp:
    tiempo_hoy.append(i)
         
# Recorremos la lista tiempo_hoy y eliminamos la información relativa a precipitación.
index = 0
lst_hoy = []
while index < len(tiempo_hoy) - 1:
    if tiempo_hoy[index] == 'Precipitaciones en mm.':
        index += 2
    else:
        lst_hoy.append(tiempo_hoy[index])
        index += 1


# In[261]:


# Hacemos lo mismo para tiempo_mañana.
tiempo_mañana=[]
for i in tiempo_mañana_temp:
    tiempo_mañana.append(i)

index2 = 0
lst_mañana = []
while index2 < len(tiempo_mañana) - 1:
    if tiempo_mañana[index2] == 'Precipitaciones en mm.':
        index2 += 2
    else:
        lst_mañana.append(tiempo_mañana[index2])
        index2 += 1


# In[262]:


# Eliminamos los String de nuestra lista.
lista_hoy_final=[]
for i in lst_hoy:
    if not re.match(r'^[a-zA-Z]', i):
            lista_hoy_final.append(i)
    
print(lista_hoy_final)

# ELiminamos también nuestros String y nos quedamos con la información de las 24 horas.
lista_mañana_final=[]
for i in lst_mañana:
    if not re.match(r'^[a-zA-Z]', i):
            lista_mañana_final.append(i)
            lista_mañana_final = lista_mañana_final[0:72]
    
print(lista_mañana_final)


# In[263]:


# Creamos nuestas listas con la información que nos interesa para posteriormente crear un dataframe.

horas = []
temp = []
v_viento = []

for i in range(0, len(lista_hoy_final), 3):
    horas.append(lista_hoy_final[i])
    temp.append(lista_hoy_final[i+1])
    v_viento.append(lista_hoy_final[i+2])

horas2 = []
temp2 = []
v_viento2 = []
for i in range(0, len(lista_mañana_final), 3):
    horas2.append(lista_mañana_final[i])
    temp2.append(lista_mañana_final[i+1])
    v_viento2.append(lista_mañana_final[i+2])


# In[264]:


# Creamos nuestros dos dataframes de hoy y mañana y los concatenamos.

df = pd.DataFrame({'Horas': horas, 'Temperatura': temp, 'V_viento(km_h)':v_viento})
df['Date'] = date.today()

df2= pd.DataFrame({'Horas': horas2, 'Temperatura': temp2, 'V_viento(km_h)':v_viento2})
df2['Date'] = date.today() + relativedelta.relativedelta(days=1)

Df_Final = pd.concat([df,df2], axis=0)

# Por último, eliminamos el simbolo de grados para que cuando hagamos el export no haya problemas.

Df_Final["Temperatura"] = Df_Final["Temperatura"].apply(lambda x: x.replace("°",""))

Df_Final


# In[253]:


# Hacemos el export de nuestra tabla.

Df_Final.to_csv('tiempo_hoy.csv', index=False)


# In[2]:


test = pd.read_csv('tiempo_hoy.csv')


# In[3]:


test.info()

