RA = 287.055 # constante del gas para el aire  J/kg*K 
import math
class Fpsicometricos:

    def __init__(self,Tbs,Rh,altitud):
        self.Tbs = Tbs
        self.Rh  = Rh
        self.altitud = altitud

    #1   
    def Pvs(self): #Presion de vapor a saturacion
        TbsKelvin = self.Tbs + 273.15
        if -100 <= self.Tbs < 0:
            Presion_vapor = ((-5674535*10**3)/TbsKelvin)+(6.3925247)+(-0.00967784*TbsKelvin)+(0.0000006221569*(TbsKelvin**2))+(0.0000000020747825*(TbsKelvin**3))+(-0.00000000000094844024*(TbsKelvin**4))+(4.1635019*(math.log(TbsKelvin)))
            res1_Pvs = math.log(Presion_vapor)
            return res1_Pvs
        elif 0 <= self.Tbs < 200:
            Presion_vapor = ((-5.8002206*10**3)/TbsKelvin)+(1.3914993)+((-48.640239*10**-3)*(TbsKelvin))+((41.764768*10**-6)*(TbsKelvin**2))+((-14.452093*10**-9)*(TbsKelvin**3))+((6.5459673)*(math.log(TbsKelvin)))
            res2_Pvs = math.exp(Presion_vapor)
            return res2_Pvs
    
    #2
    def Pv(self): # presion de vapor 
        percentRH = self.Rh/100
        Pvs = self.Pvs()
        return  percentRH * Pvs
    #3
    def p_atm(self):
        return (101.325*(1-(2.25577*10**-5)*self.altitud)**5.2559)*1000 # conversion de unidades 
    #4
    def W(self): #razon de humedad 
        
        den = (self.p_atm()-self.Pv())
        res = (0.622)*self.Pv()/den
        return res
    #5
    def Ws(self): # razon de humedad a saturacion *
        den = (self.p_atm()-self.Pvs())
        res = (0.622)*self.Pvs()/den
        return res
    #6
    def G_saturacion(self): #grado de saturacion 
        return self.W()/ self.Ws()*100

    #7
       
    def Veh(self,RA): #Volumen especifico del aire humedo
        TbsKelvin = self.Tbs + 273.15
        Res = (((RA*TbsKelvin)/self.p_atm())*((1+1.6078*self.W())/(1+self.W())))
        return Res
    #8    
    def Tpr(self): # punto de rocio 
        if -60 <= self.Tbs < 0:
            res1 =-60.450 + 7.0322*math.log(self.Pv())+0.3700*(math.log(self.Pv()))**2
            return res1
        elif 1<= self.Tbs < 70:
            res2 = -35.957-1.8726*math.log(self.Pv())+1.1689*(math.log(self.Pv()))**2
            return res2
    #9        
    def entalpia(self): # entalpia especifica
        h = 1.006*self.Tbs + self.W()*(2501 + 1.805*self.Tbs)
        return h

    #10
    def bulbo_humedo(self,iter): # temperatura del bulbo humedo 
        Tpr = self.Tbs -1
        x0 = Tpr
        tolerancia = 0.00001
        i = 0
    
        while i < iter:
            X = x0 + 273.15
        
            if self.Tbs>0 and self.Tbs<200:
                Pvsa = self.Pvs()

                h_x = Pvsa * (-(-5.8002206e+3 / X ** 2) + (-48.640239e-3)
                        + (2 * 41.764768e-6 * X) + (3 * -14.452093e-9 * X ** 2)
                        + (6.5459673 / X))
            
            elif self.Tbs <0 and self.Tbs  >-200:
                Pvsa = self.Pvs() 

                h_x=Pvsa*(-(-5.6745359e+3/X**2)+(-9.677843e-3)
                +(2*0.6221570e-6*X)+(3*2.0747825e-9*X**2)
                +(4*-0.94844024e-12*X**3)+(4.1635019/X))

            wsa = 0.62198 * (Pvsa / (self.p_atm() - Pvsa))

            g_x = 0.62198 * ((self.p_atm() * h_x) / ((self.p_atm() - Pvsa) ** 2))

            fx = (((2501 - 2.381 * x0) * wsa - 1.006 * (self.Tbs - x0)) / (2501 + 1.805 * 20 - 4.186 * x0)) - self.W()

            f_x = ((((2501 - 2.381 * x0) * g_x + wsa * (-2.381) + 1.006)
                    / ((2501 + 1.805 * self.Tbs) - 4.186 * x0))
                - ((((2501 - 2.381 * x0) * wsa + 1.006 + (-1.006 * self.Tbs)) * (-4.186)) /
                    ((2501 + 1.805 * self.Tbs) - 4.186 * x0) ** 2))

            X1 = x0 - (fx / f_x)

            error = (X1 - x0) / x0

            #print(f"iteracion: ", i)
            #print(f'aproximacion: ', X1)
            #print(f'error: ', error)

            i = i + 1

            x0 = X1

            if abs(error) > tolerancia:
                break
        return X1    
        

