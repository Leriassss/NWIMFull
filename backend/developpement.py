# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 22:32:30 2025

@author: HP
"""

def nash(nash_k,nash_n,production,time_base=5):
    """
    Parameters
    ----------
    nash_k : Storage coefficient
    nash_n : Number of storage
    production : Net rainfall [mm]

    Returns
    -------
    HUC : Discharge values computed by the Nash's conceptuel hydrogramm method
            [mm/day]
    """
    #gamma = np.math.factorial(nash_n - 1)
    seq_hun_nash =  np.arange(0,production.count(),time_base)
    hun_time_base = []
    for k in seq_hun_nash:
        t = np.arange(k,k+time_base)
        q =pd.Series( (1/(nash_k*gamma(nash_n)))*np.power(t/nash_k,nash_n-1)*np.exp(-t/nash_k))
        hun_k = np.where(q==np.inf,0,q)
        hun_time_base.append(pd.Series(np.convolve(production[k:k+time_base],hun_k))[:len(t)])
    return pd.concat(hun_time_base).reset_index(drop=True)    


def unit_hydrogramm(production,q_obs,dt=1,time_base=5): 
    """
    Parameters
    ----------
    q_obs : Runoff observed [mm/j]
    production : Net rainfall [mm]
    time_base : Observed travel time of the peak flow through the section [day]
    Returns
    -------
    Discharge values computed by the unit hydrogramm method
    """
    seq_hun = np.arange(0,q_obs.count(),time_base)
    hun_time_base = []
    excedent_hun = np.zeros(time_base)
    i = 0
    for k in seq_hun:
        production_seq = production[k:k+time_base]
        q_obs_seq = q_obs[k:k+time_base]
        hun_intermediaire = q_obs_seq/(production_seq.sum())
        hun_k = np.where(hun_intermediaire==np.inf,0,hun_intermediaire)
        hun_time_base.append(pd.Series(np.convolve(production_seq,hun_k))[:len(production_seq)])
        i += 1
    return pd.concat(hun_time_base).reset_index(drop=True)

def unit(production,q_obs,dt=1,time_base=5): 
    """
    Parameters
    ----------
    q_obs : Runoff observed [mm/j]
    production : Net rainfall [mm]
    time_base : Observed travel time of the peak flow through the section [day]
    Returns
    -------
    Discharge values computed by the unit hydrogramm method
    """
    seq_hun = np.arange(0,q_obs.count(),time_base)
    hun_time_base = []
    excedent_hun = pd.Series(np.zeros(time_base))

    for k in seq_hun:
        production_seq = production[k:k+time_base]
        q_obs_seq = q_obs[k:k+time_base]
        if production_seq.sum()>0:
            hun_k = q_obs_seq/(production_seq.sum())
        else:
            hun_k = np.zeros_like(q_obs_seq)
        convolution = pd.Series(np.convolve(production_seq,hun_k))
        time_base_convolution = convolution[:len(production_seq)]+excedent_hun.copy()
        excedent_hun[:len(production_seq)-1] = convolution[len(production_seq):]
        hun_time_base.append(time_base_convolution)
    return pd.concat(hun_time_base).reset_index(drop=True)[:len(production)]


def unit(production,q_obs,dt): 
    """
    Parameters
    ----------
    q_obs : Runoff observed [mm/j]
    production : Net rainfall [mm]
    Returns
    -------
    Discharge values computed by the unit hydrogramm method
    """
    hun = q_obs/(production.sum())
    return pd.Series(np.convolve(production,hun))[:len(production)]*dt

def nash_hydrogramm(nash_k,nash_n,production):
    """
    Parameters
    ----------
    nash_k : Storage coefficient
    nash_n : Number of storage
    production : Net rainfall [mm]

    Returns
    -------
    HUC : Discharge values computed by the Nash's conceptuel hydrogramm method
            [mm/day]
    """
    #gamma = np.math.factorial(nash_n - 1)
    t =  np.arange(0,production.count())
    q =pd.Series( (1/(nash_k*gamma(nash_n)))*np.power(t/nash_k,nash_n-1)*np.exp(-t/nash_k))
    HUC = pd.Series(np.convolve(production,q))[:len(t)]
    return HUC





sampler = qmc.LatinHypercube(d=2)
sample = sampler.random(n=5)
sample
qmc.discrepancy(sample)
l_bounds = [0, 2]
u_bounds = [10, 5]
qmc.scale(sample, l_bounds, u_bounds)
sampler = qmc.LatinHypercube(d=2)
sample = sampler.random(n=5)
qmc.discrepancy(sample)
sampler = qmc.LatinHypercube(d=2, optimization="random-cd")
sample = sampler.random(n=5)
qmc.discrepancy(sample)

sampler = qmc.LatinHypercube(d=2, strength=2)
sample = sampler.random(n=9)
qmc.discrepancy(sample)


# Exemple d'utilisation
data = pd.DataFrame({
    'Date': pd.date_range(start='2022-01-01', end='2022-12-31', freq='D'),
    'Tmax': np.random.uniform(25, 35, 365),
    'Tmin': np.random.uniform(15, 25, 365),
    'RHmax': np.random.uniform(70, 90, 365),
    'RHmin': np.random.uniform(30, 50, 365),
    'u2': np.random.uniform(1, 3, 365)
})

constants = {
    'Elev': 100,  # Altitude en mètres
    'lambda': 2.45  # Chaleur latente de vaporisation (MJ/kg)
}


# Exemple de données
julian_days = np.arange(1, 367)  # Jours julian (1 à 366 pour une année)
temperatures = np.random.uniform(10, 30, size=366)  # Températures journalières aléatoires en °C
latitude = 45  # Latitude en degrés

# Calcul de l'évapotranspiration annuelle
et_annuelle = annual_evapotranspiration_oudin(julian_days, temperatures, latitude, lat_unit="deg")
print(f"Évapotranspiration annuelle : {et_annuelle:.2f} mm")
