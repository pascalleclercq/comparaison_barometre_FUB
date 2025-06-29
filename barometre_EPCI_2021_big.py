import contextlib
from io import StringIO
from PIL import Image

import sys
import EPCI
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as pl
import numpy as np
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import matplotlib.cbook as cbook
from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    DrawingArea,
    HPacker,
    TextArea,
    VPacker,
)
from matplotlib.patches import Rectangle
from tqdm import tqdm


mpl.rcParams["text.color"] = "black"   # default lebel color

pl.ion() # Enable interactive mode

epci = EPCI.all[sys.argv[1]] #Find EPCI by id
    
gdf_communes_shp = gpd.read_file("data/communes-20220101-shp")

gdf_2021 = gpd.read_file("data/barometre2021.json")

gdf_2021.rename(columns={"geometry": "coords"}, inplace=True)
gdf_2021.rename(columns={"contributions": "contributions_2021"}, inplace=True)

gdf_communes = gdf_communes_shp.join(
    gdf_2021.set_index("insee").loc[:, ("contributions_2021", "coords")], on="insee", how="outer"
)

#gdf_communes["contributions_2021"] = gdf_communes["contributions_2021"].fillna(0)
gdf_communes["contributions_2021"] = gdf_communes["contributions_2021"].fillna(0)

NO_RESPONSE = (1.0, 0.98, 0.98)
AT_LEAST_ONE= (0.77, 0.18, 0.20)
QUALIFIED = (0.61, 0.87, 0.19)
BACKGROUNG = (1.0, 0.98, 0.98)
TITLE = "#000000"
SUB_TITLE = "mediumblue"
EDGE_COLOR = (0.0, 0.0, 0.0)

gdf_2021 = gdf_2021[gdf_2021["insee"].isin(epci.insee)]

qualifs_2021 = []

qualifs = pd.DataFrame(
#    columns=["qualifs_2021", "qualifs_2025", "diff"],
    columns=["qualifs_2021"],
    dtype=float,
#    index=dep_ids,
)

lon_min, lat_min, lon_max, lat_max = [-5, 40.7, 10, 51.5]
ratio_dep = (lat_max - lat_min) / (lon_max - lon_min)


dep_id = 59

is_epci = gdf_communes["insee"].isin(epci.insee)

gdf_dep = gdf_communes[is_epci]
    
lon_min, lat_min, lon_max, lat_max = gdf_dep.total_bounds
ratio_dep = (lat_max - lat_min) / (lon_max - lon_min)
fig, ax = pl.subplots(
    1, 1, constrained_layout=True, figsize=(11.7, 8.3)
)

fig.patch.set_facecolor(BACKGROUNG)

with contextlib.suppress(ValueError):
    gdf_dep[gdf_dep["contributions_2021"] == 0].plot(
        color=(NO_RESPONSE),
        ax=ax,
        edgecolor=(EDGE_COLOR),
    )
with contextlib.suppress(ValueError):
    gdf_dep[
        (gdf_dep["contributions_2021"] > 0) & (gdf_dep["contributions_2021"] < 50)
    ].plot(
        color=(AT_LEAST_ONE),
        ax=ax,
        edgecolor=(EDGE_COLOR),
    )
with contextlib.suppress(ValueError):
    gdf_dep[(gdf_dep["contributions_2021"] >= 50)].plot(
        color=(QUALIFIED),
        ax=ax,
        edgecolor=(EDGE_COLOR),
    )


qualif_2021 = len(gdf_dep[(gdf_dep["contributions_2021"] >= 50)])

sup_zero_2021 = len(gdf_dep[(gdf_dep["contributions_2021"] > 0)])

qualifs_2021.append(qualif_2021)

qualifs.loc[dep_id, 'qualifs_2021'] = qualif_2021


qualifees_2021 = gdf_dep[(gdf_dep["contributions_2021"] >= 50)] 

for idx, row in qualifees_2021.iterrows():
    if row['coords'] is not None:
        texte = row['nom']+"\n"+ str(int(row['contributions_2021']))
        ax.annotate(text=texte,xy=(row['coords'].x,row['coords'].y),horizontalalignment='center',
            verticalalignment='center', fontsize=9, color="mediumblue")

ax.set_title(
    f"Participation Baromètre Vélo : {epci.name}\n\n  2021",
    loc="center",
    fontdict={"fontsize": "22", "color": TITLE},
)

ax.set_axis_off()

box_text_reponses = TextArea(
    f"Communes : {epci.nbr_communes} ", textprops=dict(color=SUB_TITLE, size=16)
)


box_text_red = TextArea(
    f"   au moins une réponse : {sup_zero_2021} ",
    textprops=dict(color=SUB_TITLE, size=16),
)
box_draw_red = DrawingArea(20, 20, 0, 0)
rect = Rectangle((2, 2), width=16, height=16, angle=0, fc=(AT_LEAST_ONE))
box_draw_red.add_artist(rect)
box_red = HPacker(
    children=[ box_draw_red, box_text_red],
    align="center",
    pad=0,
    sep=0,
    mode="fixed",
)

box_text_green = TextArea(
    f"   qualifiées : {qualif_2021} ", textprops=dict(color=SUB_TITLE, size=16)
)
box_draw_green = DrawingArea(20, 20, 0, 0)
rect = Rectangle((2, 2), width=16, height=16, angle=0, fc=(QUALIFIED))
box_draw_green.add_artist(rect)
box_green = HPacker(
    children=[box_draw_green, box_text_green],
    align="center",
    pad=0,
    sep=0,
    mode="fixed",
)

box = VPacker(
    children=[box_text_reponses, box_green, box_red],
    align="left",
    pad=0,
    sep=4,
    mode="fixed",
)
anchored_box = AnchoredOffsetbox(
    loc="upper center",
    child=box,
    pad=0.0,
    frameon=False,
    bbox_to_anchor=(0.4, 0),
    bbox_transform=ax.transAxes,
    borderpad=0.0,
)
ax.add_artist(anchored_box)



pl.savefig(f"png/{epci.id}_2021.png", dpi=300)

#qualifs["diff"] = qualifs["qualifs_2025"] - qualifs["qualifs_2021"]
#try:
#    qualifs["relatif"] = qualifs["qualifs_2025"].divide(qualifs["qualifs_2021"])
#except ZeroDivisionError:
#    qualifs["relatif"] = np.nan
#qualifs.to_csv('outputs/commune_qualif.csv')


