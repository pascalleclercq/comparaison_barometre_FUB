import contextlib
from io import StringIO
from PIL import Image
import os
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
mpl.rcParams["legend.loc"] = "upper right" 

pl.ion() # Enable interactive mode

epci = EPCI.all[sys.argv[1]] #Find EPCI by id
    
gdf_communes_shp = gpd.read_file("data/communes-20220101-shp")
gdf = gpd.read_file("data/sortie.json")

gdf.rename(columns={"geometry": "coords"}, inplace=True)

gdf_communes = gdf_communes_shp.join(
        gdf.set_index("insee").loc[:, ("contributions", "classe", "coords", "per_cent")], on="insee", how="outer"
    )

#gdf_communes["contributions"] = gdf_communes["contributions"].fillna(0)
gdf_communes["classe"] = gdf_communes["classe"].fillna("Non participation")

print(type(gdf_communes))
print(gdf_communes)

NO_RESPONSE = (1.0, 0.98, 0.98)
AT_LEAST_ONE= "#e9e9e9"
QUALIFIED = (0.61, 0.87, 0.19)
color_classe_Ap = "#00822C"
color_classe_A = "#4b9833"
color_classe_B = "#79b52e"
color_classe_C = "#c8d228"
color_classe_D = "#ffee31"
color_classe_E = "#fccb2d"
color_classe_F = "#f39939"
color_classe_G = "#e44b23"
BACKGROUNG = (1.0, 0.98, 0.98)
TITLE = "#000000"
SUB_TITLE = "mediumblue"
EDGE_COLOR = (0.0, 0.0, 0.0)

#NPDC
if(epci.id=="NPDC"):
    cmap = pl.cm.colors.ListedColormap([color_classe_A, color_classe_B, color_classe_C, color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
if(epci.id=="MEL"):
    cmap = pl.cm.colors.ListedColormap([color_classe_B, color_classe_C, color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
if(epci.id=="CABBALR"):
    cmap = pl.cm.colors.ListedColormap([color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])

gdf = gdf[gdf["insee"].isin(epci.insee)]


lon_min, lat_min, lon_max, lat_max = [-5, 40.7, 10, 51.5]
ratio_dep = (lat_max - lat_min) / (lon_max - lon_min)

is_epci = gdf_communes["insee"].isin(epci.insee)

gdf_dep = gdf_communes[is_epci]
    
lon_min, lat_min, lon_max, lat_max = gdf_dep.total_bounds
ratio_dep = (lat_max - lat_min) / (lon_max - lon_min)
fig, ax = pl.subplots(
    1, 1, constrained_layout=True, figsize=(11.7, 11.7)
)

print(fig)
print(ax)

fig.patch.set_facecolor(BACKGROUNG)

with contextlib.suppress(ValueError):
    gdf_dep[gdf_dep["contributions"] == 0].plot(
        color=(NO_RESPONSE),
        ax=ax,
        edgecolor=(EDGE_COLOR),
        legend=True,
        linewidth=0.1,
        label="Non participation"
    )
 

with contextlib.suppress(ValueError):
    gdf_dep.plot(
        column="classe",
        ax=ax,
        edgecolor=(EDGE_COLOR),
        cmap=cmap,
        legend=True,
        linewidth=0.1
    )

leg1 = ax.get_legend()
leg1.set_title(f"{epci.name}")
leg1.set_alignment("left")
#leg1.set_loc("upper right")
#leg1.set_label(["A", "B", "C", "D", "E", "F", "G", "NC", "Non participation"])

au_moins_une = gdf_dep

for idx, row in au_moins_une.iterrows():
    if(((row['surf_ha'] > epci.surface_mini_for_label))):
        texte = row['nom']
        ax.annotate(text=texte,xy=(row['coords'].x,row['coords'].y),horizontalalignment='center',
             verticalalignment='center', fontsize=6, color="mediumblue")


ax.set_axis_off()

#fig.tight_layout()

pl.show()

if not os.path.isdir(f"png/{epci.id}"):
    os.makedirs(f"png/{epci.id}")

pl.savefig(f"png/resultats/{epci.id}.png", dpi=300)



