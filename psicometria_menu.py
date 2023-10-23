import funciones
RA = 287.055 # constante del gas para el aire  J/kg*K 
Tbs = 20
Rh  = 50
altitud = 0
programa = funciones.Funciones(Tbs,Rh,altitud)

print(f'1.Presión parcial de vapor a saturacion(Pvs):{programa.Pvs()} Pa\n')
print(f'2.Presión parcial de vapor(Pv):{programa.Pv()} Pa\n')
print(f'3.Razon de humedad(W):{programa.W()} Kg(vp)/Kg(as) \n')
print(f'4.Razon de humedad en condición de saturacion(Ws):{programa.Ws()}Kg(vp)/Kg(as)\n')
print(f'5.Grado de saturación(u):{programa.G_saturacion()} %\n')
print(f'6.Volumen específico del aire humedo(Veh):{programa.Veh(RA)} m^3/Kg\n')
print(f'7.Temperatura del punto de rocio(Tpr):{programa.Tpr()} °C\n')
print(f'8.Entalpía(h):{programa.entalpia()} J/kg(aire_seco)\n')
print(f'9.Temperatura del bulbo humedo:{programa.bulbo_humedo(iter=20)} °C\n')
  