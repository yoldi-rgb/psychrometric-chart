import math
import os 
import funciones 
def run():
    Tbs = float(input('Introduce la temperatura del bulbo seco(°C): '))
    Rh = float(input('Introduce la humedad relativa % : '))
    altitud = float(0) # metros
    Ra = 287.055 # constante del gas para el aire  J/kg*K 

    def Pvs(Tbs): #Presion de vapor a saturacion
        TbsKelvin = Tbs + 273.15
        if Tbs in range(-100,0):
            Presion_vapor = ((-5674535*10**3)/TbsKelvin)+(6.3925247)+(-0.00967784*TbsKelvin)+(0.0000006221569*(TbsKelvin**2))+(0.0000000020747825*(TbsKelvin**3))+(-0.00000000000094844024*(TbsKelvin**4))+(4.1635019*(math.log(TbsKelvin)))
            res1_Pvs = math.log(Presion_vapor)
            return res1_Pvs
        elif Tbs in range(1,200):
            Presion_vapor = ((-5.8002206*10**3)/TbsKelvin)+(1.3914993)+((-48.640239*10**-3)*(TbsKelvin))+((41.764768*10**-6)*(TbsKelvin**2))+((-14.452093*10**-9)*(TbsKelvin**3))+((6.5459673)*(math.log(TbsKelvin)))
            res2_Pvs = math.exp(Presion_vapor)
            return res2_Pvs
  
    def Pv(Rh): # presion de vapor 
        percentRH = Rh/100
        return  percentRH* Pvs(Tbs) 
    def p_atm(altitud):
        return (101.325*(1-(2.25577*10**-5)*altitud)**5.2559)*1000 # conversion de unidades 
    def W(): #razon de humedad 
        
        den = (p_atm(altitud)-Pv(Rh))
        res = (0.622)*Pv(Rh)/den
        return res
    def Ws(): # razon de humedad a saturacion *
        den = (p_atm(altitud)-Pvs(Tbs))
        res = (0.622)*Pvs(Tbs)/den
        return res
        
    def G_saturacion(): #grado de saturacion 
        return W()/Ws()*100
    
    def Ve(Ra,Tbs): # Volumen especifico
        TbsKelvin = Tbs + 273.15
        Res = ((Ra*TbsKelvin)/p_atm(altitud))*(1+1.6078*W())
        return Res
       
    def Veh(Ra,Tbs): #Volumen especifico del aire humedo
        TbsKelvin = Tbs + 273.15
        Res = (((Ra*TbsKelvin)/p_atm(altitud))*((1+1.6078*W())/(1+W())))
        return Res
    def Tpr(Tbs): # punto de rocio 
        if Tbs in range(-60,0):
            res1 =-60.450 + 7.0322*math.log(Pv(Rh))+0.3700*(math.log(Pv(Rh)))**2
            return res1
        elif Tbs in range(1,70):
            res2 = -35.957-1.8726*math.log(Pv(Rh))+1.1689*(math.log(Pv(Rh)))**2
            return res2
    def entalpia(Tbs): # entalpia especifica
        h = 1.006*Tbs + W()*(2501 + 1.805*Tbs)
        return h


    def bulbo_humedo(Tbs,Rh): # temperatura del bulbo humedo 
        tbh = (
        Tbs * math.atan(0.151977 * (Rh + 8.313659) ** 0.5) +
        math.atan(Tbs + Rh) - math.atan(Rh - 1.676331) +
        0.00391838 * (Rh ** 1.5) * math.atan(0.023101 * Rh) - 4.686035)
        return tbh
   
    os.system('cls')
    print('------------------------------------------------------------')
    print('---------------------------RESULTADOS-------------------')
    print(f'1.Presión parcial de vapor a saturacion(Pvs):{Pvs(Tbs)} Pa\n')
    print(f'2.Presión parcial de vapor(Pvs):{Pv(Rh)} Pa\n')
    print(f'3.Razon de humedad(W):{W()} Kg(vp)/Kg(as) \n')
    print(f'4.Razon de humedad en condición de saturacion(Ws):{Ws()}Kg(vp)/Kg(as)\n')
    print(f'5.Grado de saturación(u):{G_saturacion()} %\n')
    print(f'6.Volumen específico del aire humedo(Veh):{Veh(Ra,Tbs)} m^3/Kg\n')
    print(f'7.Temperatura del punto de rocio(Tpr):{Tpr(Tbs)} °C\n')
    print(f'8.Entalpía(h):{entalpia(Tbs)} J/kg(aire_seco)\n')
    print(f'9.Temperatura del bulbo humedo:{bulbo_humedo(Tbs,Rh)} °C\n')
  
 
if __name__== '__main__':
    run()

