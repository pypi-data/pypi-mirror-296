from SESAMI.run import calculation_bet
from SESAMI.predict import betml

calculation_bet(csv_file="ac_low.csv", columns=["Pressure","Loading"],
                   adsorbate="N2", p0=1e5, T=77,
                   R2_cutoff=0.9995, R2_min=0.998,
                   font_size=12, font_type="DejaVu Sans",
                   legend=True, dpi=600, save_fig=True)

betml("ac_low.csv")
