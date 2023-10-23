import funciones
import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Constante
RA = 287.055  # Constante del gas para el aire J/kg*K

def datos(altitud, csv_file):
    # Tu función 'datos' existente
    df = pd.read_csv(csv_file)
    results = []

    # Calcular las propiedades psicrométricas para cada fila de datos
    for index, row in df.iterrows():
        Tbs = row['Temperatura del Aire (C)']
        Rh = row['Humedad relativa (%)']
        
        programa = funciones.Fpsicometricos(Tbs, Rh, altitud)
        Pvs = programa.Pvs()
        Pv = programa.Pv()
        W = programa.W()
        Ws = programa.Ws()
        G_saturacion = programa.G_saturacion()
        Veh = programa.Veh(RA)
        Tpr = programa.Tpr()
        entalpia = programa.entalpia()
        bulbo_humedo = programa.bulbo_humedo(iter=20)

        results.append([Tbs, Rh, Pvs, Pv, W, Ws, G_saturacion, Veh, Tpr, entalpia, bulbo_humedo])

    return results

def guardar_csv(results):
    if not results:
        sg.popup("No hay resultados para guardar.", title="Aviso")
        return

    save_file = sg.popup_get_file("Guardar CSV", save_as=True, file_types=(("CSV Files", "*.csv"),))
    if save_file:
        try:
            df = pd.DataFrame(results, columns=["Temperatura (C)", "Humedad Relativa (%)", "Pvs", "Pv", "W", "Ws", "Grado Saturación", "Veh", "Tpr", "Entalpía", "Bulbo Húmedo"])
            df.to_csv(save_file, index=False)
            sg.popup(f"Datos guardados en {save_file}", title="Éxito")
        except Exception as e:
            sg.popup_error(f"Error al guardar el archivo CSV:\n{str(e)}")

#def graficar(datos):
    if not datos:
        sg.popup("No hay datos para graficar.", title="Aviso")
        return

    plt.use("TkAgg")  # Usar el backend de Tkinter para matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Gráfico de Ejemplo")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.plot(datos)  # Reemplaza esto con tus datos y gráficos reales

    # Crear una figura de lienzo para Tkinter
    canvas = FigureCanvasTkAgg(fig, master=tab2_layout)

    # Obtener el widget de lienzo de la figura
    canvas_widget = canvas.get_tk_widget()

    # Limpiar cualquier widget de lienzo anterior si existe
    if canvas_widget.winfo_exists():
        canvas_widget.destroy()

    # Colocar el widget de lienzo en el diseño de la pestaña de gráficos
    canvas.get_tk_widget().pack()

def carta():
    df_temperatura = pd.read_csv('datos_tbs&Rh.csv')


    # Cargar datos de razón de humedad desde el archivo CSV
    df_razon_humedad = pd.read_csv('resultados_psicrometricos.csv')
    # Crear matrices para HR constantes y rango de temperatura
    hr_constantes = np.arange(0, 101, 10)
    temperatura_rango = np.arange(0, 51, 2)

    # Calcular Ws para cada combinación y almacenar los resultados en una matriz
    resultados = np.zeros((len(hr_constantes), len(temperatura_rango)))
    for i, hr in enumerate(hr_constantes):
        for j, temp in enumerate(temperatura_rango):
            proff = funciones.Fpsicometricos(temp, hr, 0)
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

    plt.plot(df_temperatura['Temperatura del Aire (C)'], df_razon_humedad['Razon de humedad']*1000
             , color='blue', label='tbs Vs W', marker='.', linestyle='')
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Razon de humedad (W) (g/kg de aire seco)")
    plt.title("Tabla Psicrometrica")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

sg.theme('LightBrown4')

# Contenido de la pestaña "Cálculos"
tab1_layout = [
    [sg.Text("Introduzca un archivo CSV con los datos de Tbs y Humedad Relativa")],
    [sg.Text("Seleccione un archivo CSV:"), sg.InputText(key="-FILE-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text("Altitud (en metros):"), sg.InputText(key="-ALTITUD-")],
    [sg.Button("Cargar y Calcular"), sg.Button("Guardar CSV"), sg.Button("Salir")],
    [sg.Table(values=[], headings=["Temperatura (C)", "Humedad Relativa (%)", "Pvs", "Pv", "W", "Ws", "Grado Saturación", "Veh", "Tpr", "Entalpía", "Bulbo Húmedo"], auto_size_columns=False, justification='right', num_rows=20, key='-TABLE-')],
]

# Contenido de la pestaña "Gráficas"
tab2_layout = [
    [sg.Button("Generar Carta Psicrométrica", key="-CARTA-")],
]

# Diseño de la ventana con pestañas
layout = [
    [sg.TabGroup([
        [sg.Tab("Cálculos", tab1_layout), sg.Tab("Gráficas", tab2_layout)]
    ])]
]

window = sg.Window("Calculadora Psicrométrica", layout)
results = []  # Inicializamos results fuera del bucle principal

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Salir":
        break
    elif event == "Cargar y Calcular":
        try:
            altitud = float(values["-ALTITUD-"])
            csv_file = values["-FILE-"]
            results = datos(altitud, csv_file)
            
            # Actualizar la tabla con los resultados
            window["-TABLE-"].update(values=results)
        except ValueError:
            sg.popup_error("Ingrese una altitud válida.")
    elif event == "Guardar CSV":
        if results:
            guardar_csv(results)
    elif event == "-CARTA-":
        carta()  # Llama a la función para generar la carta psicrométrica

window.close()  