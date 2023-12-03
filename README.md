# Rebalancing Bike Sharing System Dashboard
Revisa la presentación del proyecto en el archivo

    presentacion_del_proyecto.html

## Contexto
El servicio de MiBici, es un servicio de transporte público basado en una red de bicicletas compartidas en el Área Metropolitana de Guadalajara
<p align="center">
<img src="media/mapa.png" alt="BID" width="500" height="250"/>
</p>

<p align="center">
  <em> Elaboración Propia con datos de MiBici. </em>
</p>

Este proyecto fue realizado utilizando datos abiertos del servicio de [MiBici](https://www.mibici.net/)

## Metodología

<div style="text-align: center;">

### Dramatización
#### Estación 49 C. Robles Gil / Av. Vallarta

<img src="media/drama.png" alt="BID"/>
</div>


### Demanda positva
<div style="text-align: center;">

<img src="media/dema1.png" alt="BID" width="500" height="250"/>

</div>

### Demanda negativa
<div style="text-align: center;">

<img src="media/dema1.png" alt="BID" width="500" height="250"/>

</div>

### Propuesta de horarios de rebalanceo
<div style="text-align: center;">

<img src="media/dema3.png" alt="BID" width="500" height="250"/>

</div>

<div style="text-align: center;">

<img src="media/dema4.png" alt="BID" width="500" height="250"/>

</div>

## Algoritmo de rebalanceo


<img src="media/dema5.png" alt="BID" width="250" height="300"/>

[0 , 0 , 1 , 4,  5,  1,  3,  7]


<img src="media/dema6.png" alt="BID" width="250" height="300"/>

[0, 0, 1, 2, 1, 8, 2, 6]


Hacemos la diferencia de demanda positiva y demanda negativa para sacar la "demanda total":

[0 , 0 , 1 , 4,  5,  1,  3,  7] - [0 , 0 , 1 , 2 , 1 , 8 , 2 , 6] = [0, 0, 0, 2, 4, -7, 1, 1]


### [0, 0, 0, 2, 4, -7, 1, 1]


### Se realiza para todos los periodos
<div style="text-align: center;">
<img src="media/periodos.png" alt="BID"/>
</div>

## Predicción de demanda por estación
### Random Forest (Árboles de regresión)

Extracción de características:

  * Mes
  * Día
  * Hora

Con información de 2020 a 2022 para predecir 2023


<img src="media/arbol.png" alt="BID" width="380" height="250"/>

## Comparación de Resultados

<div style="text-align: center;">

<img src="media/resultados1.png" alt="BID" width="600" height="250"/>


</div>

<div style="text-align: center;">

<img src="media/resultados2.png" alt="BID" width="600" height="250"/>

</div>

## Prototipo de software

<p align="center">
<img src="images/mibiciapp.gif" alt="gifapp">
</p>

## Instalación

### Paso 0)

Clona este repositorio

### Paso 1)

Para instalar las bibliotecas necesarias para ejecutar la aplicación, debemos escribir lo siguiente en la terminal:

    pip install -r requirements.txt

O

    pip3 install -r requirements.txt

### Paso 2)
Ejecute el archivo app.py desde el directorio donde se ha clonado el repositorio

    streamlit run app.py
