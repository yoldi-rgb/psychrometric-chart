import funciones
import pandas as pd
import PySimpleGUI as sg

# Constante
RA = 287.055  # Constante del gas para el aire J/kg*K

def datos(altitud, csv_file):
    # Tu función 'datos' existente
    df = pd.read_csv(csv_file)
       # Listas para almacenar resultados
    Pvs_list = []
    Pv_list = []
    W_list = []
    Ws_list = []
    G_saturacion_list = []
    Veh_list = []
    Tpr_list = []
    entalpia_list = []
    bulbo_humedo_list = []

    # Calcular las propiedades psicrométricas para cada fila de datos
    for index, row in df.iterrows():
        Tbs= row['Temperatura del Aire (C)']
        Rh = row['Humedad relativa (%)']
        
        programa = funciones.Fpsicometricos(Tbs, Rh, altitud)
        Pvs_list.append(programa.Pvs())
        Pv_list.append(programa.Pv())
        W_list.append(programa.W())
        Ws_list.append(programa.Ws())
        G_saturacion_list.append(programa.G_saturacion())
        Veh_list.append(programa.Veh(RA))
        Tpr_list.append(programa.Tpr())
        entalpia_list.append(programa.entalpia())
        bulbo_humedo_list.append(programa.bulbo_humedo(iter=20))
    
    # Resto del código para procesar los datos y generar resultados



layout = [
    [sg.Text("Seleccione un archivo CSV:"), sg.InputText(key="-FILE-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text("Altitud (en metros):"), sg.InputText(key="-ALTITUD-")],
    [sg.Button("Cargar y Calcular"), sg.Button("Salir")],
    [sg.Output(size=(60, 10))]
]

window = sg.Window("Calculadora Psicrométrica", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Salir":
        break
    elif event == "Cargar y Calcular":
        try:
            altitud = float(values["-ALTITUD-"])
            csv_file = values["-FILE-"]
            datos(altitud, csv_file)
        except ValueError:
            print("Ingrese una altitud válida.")

window.close()
