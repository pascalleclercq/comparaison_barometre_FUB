import contextlib
import textwrap
import os
import sys
import EPCI
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as pl
#import matplotlib.image as mpimg
from matplotlib.patches import Patch



mpl.rcParams["text.color"] = "black"   # default lebel color
#mpl.rcParams["legend.loc"] = "upper right" 

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


NO_RESPONSE = (1.0, 0.98, 0.98)
AT_LEAST_ONE= (0, 0, 0, 0)
color_classe_Ap = "#2b7910"
color_classe_A = "#4b9833"
color_classe_B = "#79b52d"
color_classe_C = "#c8d227"
color_classe_D = "#feef30"
color_classe_E = "#fccb2c"
color_classe_F = "#f39939"
color_classe_G = "#e44b23"
BACKGROUNG = (1.0, 0.98, 0.98)
TITLE = "#000000"
SUB_TITLE = "mediumblue"
EDGE_COLOR = (0.0, 0.0, 0.0)

legend_loc='upper right'

cmap = pl.cm.colors.ListedColormap([color_classe_A, color_classe_B, color_classe_C, color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(11.7, 8.3))
if(epci.id=="MEL"):
    cmap = pl.cm.colors.ListedColormap([color_classe_B, color_classe_C, color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(11.7, 11.7))
if(epci.id=="CABBALR"):
    cmap = pl.cm.colors.ListedColormap([color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
if(epci.id=="CCPC"):
    cmap = pl.cm.colors.ListedColormap([color_classe_C, color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
if(epci.id=="CCFL"):
    cmap = pl.cm.colors.ListedColormap([color_classe_C, color_classe_D, color_classe_E, color_classe_F, AT_LEAST_ONE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(18.7, 8.3))
if(epci.id=="LITTORAL"):
    legend_loc='lower right'
    cmap = pl.cm.colors.ListedColormap([color_classe_A, color_classe_B, color_classe_C, color_classe_D, color_classe_E, color_classe_F, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(11.7, 13.7))
if(epci.id=="CALL"):
    cmap = pl.cm.colors.ListedColormap([color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(18.7, 11.7))
if(epci.id=="CCFI"):
    cmap = pl.cm.colors.ListedColormap([color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(17.7, 11.7))
if(epci.id=="CAPH"):
    cmap = pl.cm.colors.ListedColormap([color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(9, 10))
if(epci.id=="CAVM"):
    cmap = pl.cm.colors.ListedColormap([color_classe_D, color_classe_E, color_classe_F, color_classe_G, AT_LEAST_ONE, NO_RESPONSE])
    fig, ax = pl.subplots(1, 1, constrained_layout=True, figsize=(11.7, 13.7))


gdf = gdf[gdf["insee"].isin(epci.insee)]

is_epci = gdf_communes["insee"].isin(epci.insee)

gdf_dep = gdf_communes[is_epci]
    
pl.title(f"Baromètre vélo - {epci.name} 2025", fontdict={'size':20, 'fontweight':'bold'})

fig.patch.set_facecolor(BACKGROUNG)

with contextlib.suppress(ValueError):
    gdf_dep[gdf_dep["contributions"] == 0].plot(
        color=(NO_RESPONSE),
        ax=ax,
        edgecolor=(EDGE_COLOR),
#        legend=True,
        linewidth=0.1,
        label="Non participation"
    )
 

with contextlib.suppress(ValueError):
    gdf_dep.plot(
        column="classe",
        ax=ax,
        edgecolor=(EDGE_COLOR),
        cmap=cmap,
#        legend=True,
        linewidth=0.1
    )


# legend_elements = [Line2D([0], [0], marker='o', color='w', label='A', markerfacecolor=color_classe_A, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='B', markerfacecolor=color_classe_B, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='C', markerfacecolor=color_classe_C, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='D', markerfacecolor=color_classe_D, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='E', markerfacecolor=color_classe_E, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='F', markerfacecolor=color_classe_F, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='G', markerfacecolor=color_classe_G, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='Non classée', markerfacecolor=AT_LEAST_ONE, markersize=10, markeredgecolor='black',markeredgewidth=0.2),
#                    Line2D([0], [0], marker='o', color='w', label='Non participation', markerfacecolor=NO_RESPONSE, markersize=10, markeredgecolor='black',markeredgewidth=0.2)]

legend_elements = [
    Patch(facecolor=color_classe_Ap, edgecolor='black', linewidth=0.5, label='A+  ≥ 4.6'),
    Patch(facecolor=color_classe_A,  edgecolor='black', linewidth=0.5, label='A    ≥ 4.3 et < 4.6'),
    Patch(facecolor=color_classe_B,  edgecolor='black', linewidth=0.5, label='B    ≥ 3.9 et < 4.3'),
    Patch(facecolor=color_classe_C,  edgecolor='black', linewidth=0.5, label='C    ≥ 3.5 et < 3.9'),
    Patch(facecolor=color_classe_D,  edgecolor='black', linewidth=0.5, label='D    ≥ 3.1 et < 3.5'),
    Patch(facecolor=color_classe_E,  edgecolor='black', linewidth=0.5, label='E    ≥ 2.7 et < 3.1'),
    Patch(facecolor=color_classe_F,  edgecolor='black', linewidth=0.5, label='F    ≥ 2.3 et < 2.7'),
    Patch(facecolor=color_classe_G,  edgecolor='black', linewidth=0.5, label='G    < 2.3'),
    Patch(facecolor=NO_RESPONSE,     edgecolor='black', linewidth=0.5, label='Non participation'),
]
ax.legend(handles=legend_elements, loc=legend_loc, title="Classe", fontsize=8, title_fontsize=9)

au_moins_une = gdf_dep
for idx, row in au_moins_une.iterrows():
    if(((row['surf_ha'] > epci.surface_mini_for_label))):
        if row['coords'] is not None:
            texte = textwrap.shorten(text=row['nom'], width=18, placeholder="...")
            ax.annotate(text=texte,xy=(row['coords'].x,row['coords'].y),horizontalalignment='center',
             verticalalignment='center', fontsize=9, color="mediumblue")


ax.set_axis_off()



pl.show()

if not os.path.isdir(f"png/{epci.id}"):
    os.makedirs(f"png/{epci.id}")

pl.savefig(f"png/resultats/{epci.id}_2025.png", dpi=300)



