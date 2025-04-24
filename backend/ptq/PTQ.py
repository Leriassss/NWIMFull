import pandas as pd
import numpy as np
class PTQ:
    def __init__(self, p, etp, q, dates):
        self.p = p
        self.etp = etp
        self.q = q
        self.dates = dates

    def daily_qobs_mean(self):
        df = pd.DataFrame({
            "Date": pd.to_datetime(self.dates),
            "Q_obs": self.q
        })
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day


        daily_avg = df.groupby(["month", "day"])[["Q_obs"]].mean().reset_index()

        full_days = pd.date_range(start="2020-01-01", end="2020-12-31")
        full_days_df = pd.DataFrame({
                "month": full_days.month,
                "day": full_days.day
            })

        # Merge pour garantir 366 jours dans le résultat
        merged = full_days_df.merge(daily_avg, on=["month", "day"], how="left")
        idx_29_feb = merged[(merged["month"] == 2) & (merged["day"] == 29)].index

        if not idx_29_feb.empty:
            idx = idx_29_feb[0]
            # On récupère les valeurs du 28 février et du 1er mars
            val_before = merged.loc[idx - 1, "Q_obs"]
            val_after = merged.loc[idx + 1, "Q_obs"]
            # On remplace le NaN du 29 février par leur moyenne
            merged.loc[idx, "Q_obs"] = np.nanmean([val_before, val_after])

        return merged["Q_obs"]

    

    def get_qobs_mean(self, date_str):
        date = pd.to_datetime(date_str)

        prev_day = date - pd.Timedelta(days=1)

        jour_annee = prev_day.dayofyear
        return jour_annee
