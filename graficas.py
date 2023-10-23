import numpy as np
import matplotlib.pyplot as plt
import  funciones
import pandas as pd



df_temperatura = pd.read_csv('datos_tbs&Rh.csv')


    # Cargar datos de razón de humedad desde el archivo CSV
df_razon_humedad = pd.read_csv('resultados_psicrometricos.csv')




def carta():
    # Crear matrices para HR constantes y rango de temperatura
    hr_constantes = np.arange(0, 101, 10)
    temperatura_rango = np.arange(0, 51, 2)


            # Calcular Ws para cada combinación y almacenar los resultados en una matriz
    resultados = np.zeros((len(hr_constantes), len(temperatura_rango)))
    for i, hr in enumerate(hr_constantes):

        for j, temp in enumerate(temperatura_rango):
            proff = funciones.Fpsicometricos(temp,hr,0)
            ws = proff.W()
            
            resultados[i, j] = ws * 1000  # Multiplicar por 1000 para convertir a g/kg

            # Gráfica de HR Constantes vs Temperatura
    for i, hr in enumerate(hr_constantes):
                if hr != 0:
                    plt.plot(temperatura_rango, resultados[i, :], label=f'HR={hr}% ')
        
                    idx_max_valor = np.argmax(resultados[i, :])
    
    # Obtén el valor máximo
                    max_valor = resultados[i, idx_max_valor]
    
    # Agregar etiqueta de porcentaje sobre la línea
                    plt.text(temperatura_rango[idx_max_valor], max_valor, f'{hr}%', fontsize=8, ha='center')
    
    plt.plot(df_temperatura['Temperatura del Aire (C)'],df_razon_humedad['Razon de humedad']*1000
    ,color='blue',label='tbs Vs W',marker='.',linestyle='')
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Razon de humedad (W) (g/kg de aire seco)")
    plt.title("Tabla Psicrometrica")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

carta()