import pandas as pd
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
        
        return daily_avg["Q_obs"]
    
    def get_qobs_mean(self, date_str):
        date = pd.to_datetime(date_str)

        prev_day = date - pd.Timedelta(days=1)

        jour_annee = prev_day.dayofyear
        return jour_annee