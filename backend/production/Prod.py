# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

class Production:
    def horton(prec,f_0,f_t,k):
        """
        Parameters
        ----------
        f_0 : initial soil infiltration capacity [mm/day]
        f_t : final soil infiltration capacity [mm/day]
        k : exponent parameter [1/day]
        prec : rainfall [mm]

        Returns
        -------
        ruissellement : Net rainfall [mm]

        """
        t = prec.index
        taux_infiltration = pd.Series(f_t + (f_0-f_t)*np.exp(-k*t))
        ruissellement = np.maximum(0, prec-taux_infiltration)
        return ruissellement 

    def phi(prec,c_r):
        """
        Parameters
        ----------
        c_r : Runoff coefficient
        prec : Rainfall [mm]

        Returns
        -------
        ruissellement : Net rainfall [mm]

        """
        prec_sorted = (prec.sort_values(ascending=False)).round(3)
        dt = prec.index
        lame_ruisselee = (c_r*prec.sum()).round(3)
        phis = []
        for i in dt:
            print(i)
            prec_iter_sum = prec_sorted[:(i+1)].sum()
            phi_index = (prec_iter_sum-lame_ruisselee)/(i+1)
            phis.append(phi_index)
            ruissellement = [0] if phi_index < 0 else np.maximum(0, prec-phi_index)
            ruissellement = pd.Series(ruissellement)
            final_data = []
            if(ruissellement.sum()).round(3) == lame_ruisselee and phi_index>0 :
                print("****************************************")
                print(phi_index)
                final_data.append({'phi' : phi_index, 'ruissellement' : ruissellement})
        return final_data

    def holtan(prec,f_0,f_t,k,storage_capacity):
        """
        Parameters
        ----------
        f_0 : initial soil infiltration capacity [mm/day]
        f_t : final soil infiltration capacity [mm/day]
        k : exponent parameter [1/day]
        storage_capacity : storage capacity
        prec : rainfall [mm]

        Returns
        -------
        ruissellement : Net rainfall [mm]
        """
        lame_cumulee_ruisselee = np.zeros(prec.count())
        infiltration = np.zeros(prec.count())
        for i in range(1,prec.count()):
            rapport = lame_cumulee_ruisselee[i-1]/storage_capacity
            infiltration[i-1] = 0 if rapport<1 else f_t + f_0*np.power((1-rapport),k)
            lame_cumulee_ruisselee[i] =infiltration[i-1]+lame_cumulee_ruisselee[i-1]
        return np.maximum(0, prec-infiltration)

    def philip(prec,S,K):
        """
        Parameters
        ----------
        S : Sorptivity 
        K : Hydraulic conductivity
        prec : rainfall [mm]
        
        Returns
        -------
        Net rainfall [mm]
        """
        infiltration_phillip = np.power(prec.index+1,-1/2)*S + K
        return np.maximum(0, prec-infiltration_phillip)


    def w_min(prec,runoff_coef):
        """
        Parameters
        ----------
        runoff_coef : Runoff coefficient [0;1]

        Returns
        -------
        ruissellement : Net rainfall [mm]
        """
        return prec*runoff_coef

    def scs(prec,curve_number):
        """
        Parameters :
        ----------
        - precipitation : Rainfall [mm]
        - CN : Curve Number

        Return :
        -------
        - net_runoff :  Net runoff  [mm]
        """

        s = (25400 / curve_number) - 254
        i_a = 0.2 * s  
        
        n = prec.count()
        rainfall_cumul = np.zeros(n)  
        runoff_cumul = np.zeros(n)
        net_runoff = np.zeros(n)
        
        for t in range(1, n):
            rainfall_cumul[t] = rainfall_cumul[t - 1] + prec[t]
            p = rainfall_cumul[t]
            if p > i_a:
                runoff_cumul[t] = ((p - i_a) ** 2) / (p - i_a + s)
            else:
                runoff_cumul[t] = 0
            
            net_runoff[t] = runoff_cumul[t] - runoff_cumul[t - 1]
        
        return net_runoff
    


    def green_ampt(prec,succion,d_theta,ks,H0):
        """
        Parameters
        ----------
        succion : 0.434 [%]
        d_theta : 8.89 [cm]
        ks : Hydraulic conductivity [cm/day]
        H0 : [%]

        Returns
        -------
        Net runoff [mm]
        """
        lame_cumulee_ruisselee = np.zeros(prec.count())
        infiltration = np.zeros(prec.count())
        for i in range(1,prec.count()):
            infiltration[i-1] = ks*(1+succion*d_theta/lame_cumulee_ruisselee[i-1])
            lame_cumulee_ruisselee[i] =infiltration[i-1]+lame_cumulee_ruisselee[i-1]
        infiltration_ga = np.maximum(0, H0-infiltration)
        return np.maximum(0, prec-infiltration_ga)