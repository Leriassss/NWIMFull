# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:49:50 2025

@author: HP
"""

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from contracts.Bundle import DataSimulation, RoutingContract

from scipy.optimize import least_squares

from scipy.signal import deconvolve

from routing.Routing import Routing
from routing.models.DPFTModel import DPFTModel

class DPFT(Routing):

    def __init__(self, kwargs: RoutingContract):
        #Initialisation
        self.kwargs = kwargs
        self.dH = 0

        self.dpftModel =  DPFTModel(*self.kwargs)



    def deconvolution_least_squares(self,qobs_minus_qbase, pn):
        def residuals(H):
            return np.convolve(H, pn, mode='full')[:len(qobs_minus_qbase)] - qobs_minus_qbase
        
        # Estimation initiale de H
        H0 = np.zeros(len(pn))
        
        # Résolution par moindres carrés
        res = least_squares(residuals, H0)
        return res.x
    
    def calage(self, datas: DataSimulation):
        production = datas["p"]
        interm_hun = []

        # Éviter les zéros dans les précipitations pour la déconvolution
        pn_non_zero = np.where(production == 0, 1e-10, production)

        # Déconvolution pour obtenir la fonction de transfert H(t)
        qobs_minus_qbase = datas["qobs"]
        H, _ =  self.deconvolution_least_squares(qobs_minus_qbase, pn_non_zero)

        # Calcul de la différence première de la fonction de transfert
        self.dH = np.diff(H)
        print(deconvolve(qobs_minus_qbase, pn_non_zero))
        time_base = self.dpftModel.time_base
        seq_hun = np.arange(0, len(self.dH), time_base)
        hun_time_base = []

        for k in seq_hun:
            production_seq = production[k:k + time_base]
            dH_seq = self.dH[k:k + time_base]
            if production_seq.sum() > 0:
                hun_k = np.array(dH_seq / (production_seq.sum()))
            else:
                hun_k = np.zeros_like(dH_seq)
            interm_hun.append(pd.Series(hun_k.copy()))
            hun_time_base.append(pd.Series(np.convolve(production_seq, hun_k))[:len(production_seq)])

        self.hun = pd.concat(interm_hun).reset_index(drop=True)
        q_sim_direct = pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
        return np.maximum(0, q_sim_direct + datas["qbase"])


    def validation(self, datas: DataSimulation):
        hun_ = self.dH.copy()
        production = datas["pn"]
        time_base = self.dpftModel.time_base
        seq_hun = np.arange(0,len(production),time_base)
        hun_time_base = []        
        for k in seq_hun:
            production_seq = production[k:k+time_base]
            hun_seq = hun_[k:k+time_base]
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:time_base])
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
        return np.maximum(0, q_sim_direct + datas["qbase"])

    @staticmethod
    def help():
        """
        Affiche une description de la méthode DPFT et de son fonctionnement.
        """
        description = """
        Méthode DPFT (Différence de la Première Fonction de Transfert) :
        
        La méthode DPFT est utilisée pour simuler et modéliser les débits dans un système hydrologique
        ou hydraulique. Elle repose sur l'idée que la fonction de transfert permet de relier une entrée
        (par exemple, un flux entrant ou une précipitation) à une sortie (par exemple, un débit en aval) """
        
        print(description)

"""
    def validation(self,production):
        time_base = self.data_model.time_base
        seq_hun = np.arange(0,self.hun.count(),time_base)
        hun_time_base = []

        for k in seq_hun:
            production_seq = production[k:k+time_base]
            hun_seq = self.hun[k:k+time_base]
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:len(production_seq)])
        return pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]
"""