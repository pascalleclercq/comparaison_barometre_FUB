import contextlib
from io import StringIO
from PIL import Image
import textwrap 
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
    OffsetImage,
    AnnotationBbox,
    AnchoredOffsetbox,
    DrawingArea,
    HPacker,
    TextArea,
    VPacker,
)
from matplotlib.patches import Rectangle
from tqdm import tqdm


mpl.rcParams["text.color"] = "white"   # default lebel color

pl.ion() # Enable interactive mode

epci = EPCI.all[sys.argv[1]] #Find EPCI by id
    
gdf_communes_shp = gpd.read_file("data/communes-20220101-shp")
gdf_2025 = gpd.read_file("data/barometre2025.json")

gdf_2025.rename(columns={"geometry": "coords"}, inplace=True)
#gdf_2025.rename(columns={"contributions": "contributions_2025"}, inplace=True)

gdf_2021 = gpd.read_file("data/barometre2021.json")

gdf_2021.rename(columns={"geometry": "coords"}, inplace=True)
#gdf_2021.rename(columns={"contributions": "contributions_2021"}, inplace=True)

gdf_communes = gdf_communes_shp.join(
    gdf_2021.set_index("insee"), on="insee", how="outer"
)
gdf_communes = gdf_communes.join(
    gdf_2025.set_index("insee").loc[:, ("coords","contributions","population")], on="insee", how="outer", lsuffix="_2021"
)

#print(gdf_communes.columns)

gdf_communes["contributions_2021"] = gdf_communes["contributions_2021"].fillna(0)
gdf_communes["contributions_2025"] = gdf_communes["contributions"].fillna(0)


NO_RESPONSE = (1.0, 0.98, 0.98)
AT_LEAST_ONE= (0.77, 0.18, 0.20)
QUALIFIED = (0.61, 0.87, 0.19)
BACKGROUNG = (1.0, 0.98, 0.98)
TITLE = "#000000"
SUB_TITLE = "#3399FF"
EDGE_COLOR = (0.0, 0.0, 0.0)
#SNOW = (1.0, 0.98, 0.98)

# imgplot = pl.imshow(img)
# pl.show()

gdf_2025 = gdf_2025[gdf_2025["insee"].isin(epci.insee)]
gdf_2021 = gdf_2021[gdf_2021["insee"].isin(epci.insee)]


qualifs_2021= []
qualifs_2025 = []

qualifs = pd.DataFrame(
    columns=["qualifs_2021", "qualifs_2025", "diff"],
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
# fig, ax = pl.subplots(
#     1, 2, constrained_layout=True, figsize=(10, 10 * ratio_dep + 2)
# )

#fig = pl.figure(figsize=(10, ))
#print(ratio_dep)

#fig = pl.figure(figsize=(10, 10 * ratio_dep + 4))
fig = pl.figure(figsize=(15, 6 ), dpi=300, edgecolor =QUALIFIED, frameon=True)
#fig.set_layout_engine(layout='tight')
ax1 = pl.subplot2grid((35, 60), (18, 26), rowspan=6, colspan=4)  #logo
ax2 = pl.subplot2grid((35, 60), (1, 0),  rowspan=34, colspan=26) #2021
ax3 = pl.subplot2grid((35, 60), (1, 34), rowspan=34, colspan=26) #2024
ax4 = pl.subplot2grid((35, 60), (0, 0),   colspan=60)             #barre de titre

ax1.set_axis_off()
ax2.set_axis_off()
ax3.set_axis_off()
ax4.set_axis_off()


#chargement du logo
im = pl.imread('data/308482403_384298630581290_89844181439031233_n.jpg')
ax1.imshow(im)
ax1.tick_params(labeltop=False, labelbottom=False, labelleft=False)
ax1.set_anchor('S')


fig.patch.set_facecolor(BACKGROUNG)

with contextlib.suppress(ValueError):
    gdf_dep[gdf_dep["contributions_2021"] == 0].plot(
        color=(NO_RESPONSE),
        ax=ax2,
        edgecolor=(EDGE_COLOR),
    )
with contextlib.suppress(ValueError):
    gdf_dep[
        (gdf_dep["contributions_2021"] > 0) & (gdf_dep["contributions_2021"] < 50)
    ].plot(
        color=(AT_LEAST_ONE),
        ax=ax2,
        edgecolor=(EDGE_COLOR),
        alpha=0.75
    )
with contextlib.suppress(ValueError):
    gdf_dep[(gdf_dep["contributions_2021"] >= 50)].plot(
        color=(QUALIFIED),
        ax=ax2,
        edgecolor=(EDGE_COLOR),
        alpha=0.75
    )

with contextlib.suppress(ValueError):
    gdf_dep[gdf_dep["contributions_2025"] == 0].plot(
        color=(NO_RESPONSE),
        ax=ax3,
        edgecolor=(EDGE_COLOR),
    )
with contextlib.suppress(ValueError):
    gdf_dep[
        (( gdf_dep["contributions_2025"] < 50) & (gdf_dep["population"] > 5000)) | ((gdf_dep["contributions_2025"] < 30) & (gdf_dep["population"] <= 5000))
    ].plot(
        color=(AT_LEAST_ONE),
        ax=ax3,
        edgecolor=(EDGE_COLOR),
        alpha=0.75
    )
with contextlib.suppress(ValueError):
    gdf_dep[(( gdf_dep["contributions_2025"] >= 50) & (gdf_dep["population"] > 5000)) | ((gdf_dep["contributions_2025"] >= 30) & (gdf_dep["population"] <= 5000))].plot(
        color=(QUALIFIED),
        ax=ax3,
        edgecolor=(EDGE_COLOR),
        alpha=0.75
    )
    
#print(gdf_dep.columns)    
#print(gdf_dep)

au_moins_une_2021= gdf_dep[gdf_dep["contributions_2021"] > 0].copy()
for idx, row in au_moins_une_2021.iterrows():
    if(((row['surf_ha'] > epci.surface_mini_for_label))):
        text = textwrap.shorten(text=row['nom'], width=18, placeholder="...")
        ax2.annotate(text, xy=(row['coords_2021'].x,row['coords_2021'].y),horizontalalignment='center',
            verticalalignment='center', fontsize=5, color="mediumblue") 

au_moins_une_2025= gdf_dep[gdf_dep["contributions_2025"] > 0].copy()
for idx, row in au_moins_une_2025.iterrows():
    if((row['surf_ha'] > epci.surface_mini_for_label)):
        text = textwrap.shorten(text=row['nom'], width=18,  placeholder="...")
        ax3.annotate(text,xy=(row['coords'].x,row['coords'].y),horizontalalignment='center',
            verticalalignment='center', fontsize=5, color="mediumblue")

qualif_2021 = len(gdf_dep[(gdf_dep["contributions_2021"] >= 50)])
qualif_2025 = len(gdf_dep[(( gdf_dep["contributions_2025"] >= 50) & (gdf_dep["population"] > 5000)) | ((gdf_dep["contributions_2025"] >= 30) & (gdf_dep["population"] <= 5000))])
sup_zero_2021 = len(gdf_dep[(gdf_dep["contributions_2021"] > 0)])
sup_zero_2025 = len(gdf_dep[(gdf_dep["contributions_2025"] > 0)])

qualifs_2021.append(qualif_2021)
qualifs_2025.append(qualif_2025)

qualifs.loc[dep_id, 'qualifs_2021'] = qualif_2021
qualifs.loc[dep_id, 'qualifs_2025'] = qualif_2025
qualifs.loc[dep_id, 'diff'] = qualif_2025 - qualif_2021

ax4.set_title(
        f"Participation au Barometre Vélo:\n{epci.name}"
        ,
        loc="center",
        fontdict={"fontsize": "20", "color": TITLE},
)
ax2.set_title("2021", loc="center", fontdict={"fontsize": "20", "color": TITLE})
ax3.set_title("2025", loc="center", fontdict={"fontsize": "20", "color": TITLE})
#ax1.set_axis_off()

#imagebox = OffsetImage(im, zoom = 0.10)

#ab = AnnotationBbox(imagebox, (1, 0), xycoords='axes fraction', box_alignment=(1.1, 1), frameon = False)


box_text_reponses = TextArea(
    f"Communes : {len(epci.insee)} ", textprops=dict(color=SUB_TITLE, size=12)
)
box_text_red = TextArea(
    f"   au moins une réponse : {sup_zero_2021} ",
    textprops=dict(color=SUB_TITLE, size=12),
)
box_draw_red = DrawingArea(16, 16, 0, 0)
rect = Rectangle((2, 2), width=16, height=16, angle=0, fc=(AT_LEAST_ONE))
box_draw_red.add_artist(rect)
box_red = HPacker(
    children=[box_draw_red, box_text_red],
    align="center",
    pad=0,
    sep=0,
    mode="fixed",
)

box_text_green = TextArea(
    f"   qualifiées : {qualif_2021} ", textprops=dict(color=SUB_TITLE, size=12)
)
box_draw_green = DrawingArea(16, 16, 0, 0)
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
    bbox_transform=ax2.transAxes,
    borderpad=0.0,
)
ax2.add_artist(anchored_box)

box_text_reponses = TextArea(
    f"Communes : {len(epci.insee)} ", textprops=dict(color=SUB_TITLE, size=12)
)

box_text_commune = TextArea(
    f"Communes : ", textprops=dict(color=SUB_TITLE, size=12)
)

box_text_red = TextArea(
    f"   au moins une réponse : {sup_zero_2025} ",
    textprops=dict(color=SUB_TITLE, size=12),
)
box_draw_red = DrawingArea(16, 16, 0, 0)
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
    f"   qualifiées : {qualif_2025} ", textprops=dict(color=SUB_TITLE, size=12)
)
box_draw_green = DrawingArea(16, 16, 0, 0)
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
    bbox_transform=ax3.transAxes,
    borderpad=0.0,
)
ax3.add_artist(anchored_box)
print(epci.id)
pl.savefig(f"png/{epci.id}.png", dpi=300, pad_inches=0.1, bbox_inches='tight')

#qualifs["diff"] = qualifs["qualifs_2025"] - qualifs["qualifs_2021"]
#try:
#    qualifs["relatif"] = qualifs["qualifs_2025"].divide(qualifs["qualifs_2021"])
#except ZeroDivisionError:
#    qualifs["relatif"] = np.nan
#qualifs.to_csv('outputs/commune_qualif.csv')


