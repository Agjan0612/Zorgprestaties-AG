import dash
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
from dash_bootstrap_templates import load_figure_template
import openpyxl as pxl
import gunicorn


pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

# # Winkeldochter analyse maken voor apotheken
#
# # Stap 1: Inlezen van de dataframes, toekennen kolommen, aanmaken periodes
#
# # assortiment dataframe inlezen
# assortiment_oosterhaar = pd.read_csv('assortiment_oosterhaar_test.txt')
# assortiment_musselpark = pd.read_csv('assortiment_musselpark_test.txt')
# assortiment_hanzeplein = pd.read_csv('assortiment_hanzeplein_test.txt')
#
#
# assortiment_kolommen = pd.read_excel('kolommen assortiment rapport.xlsx')
# columns_assortiment = assortiment_kolommen.columns
# assortiment_apotheek = assortiment_hanzeplein
# assortiment_apotheek.columns = columns_assortiment
# # voorraadwaarde kolom maken
#
# assortiment_apotheek['voorraadwaarde'] = (assortiment_apotheek['voorraadtotaal']/assortiment_apotheek['inkhvh']) * assortiment_apotheek['inkprijs']
#
#
#
# kolommen_receptverwerking = pd.read_excel('kolommen receptverwerking rapport.xlsx')
# columns_recept = kolommen_receptverwerking.columns
#
# hanzeplein_recept = pd.read_csv('receptverwerking_hanzeplein_test.txt')
# hanzeplein_recept.columns = columns_recept
# hanzeplein_recept['APOTHEEK'] = 'HANZEPLEIN'
# helpman_recept =pd.read_csv('receptverwerking_helpman_test.txt', encoding='latin-1')
# helpman_recept.columns = columns_recept
# helpman_recept['APOTHEEK'] = 'HELPMAN'
# musselpark_recept =pd.read_csv('receptverwerking_musselpark_test.txt')
# musselpark_recept.columns = columns_recept
# musselpark_recept['APOTHEEK'] = 'MUSSELPARK'
# oosterhaar_recept =pd.read_csv('receptverwerking_oosterhaar_test.txt')
# oosterhaar_recept.columns = columns_recept
# oosterhaar_recept['APOTHEEK'] = 'OOSTERHAAR'
# oosterpoort_recept =pd.read_csv('receptverwerking_oosterpoort_test.txt')
# oosterpoort_recept.columns = columns_recept
# oosterpoort_recept['APOTHEEK'] = 'OOSTERPOORT'
# wiljes_recept =pd.read_csv('receptverwerking_wiljes_test.txt', encoding='latin-1')
# wiljes_recept.columns = columns_recept
# wiljes_recept['APOTHEEK'] = 'WILJES'
#
#
# # bundel de recept dataframes
# recept = pd.concat([hanzeplein_recept, helpman_recept, musselpark_recept, oosterhaar_recept, oosterpoort_recept, wiljes_recept])
#
# # Voeg de maand kolom toe
#
# recept['ddDatumRecept'] = pd.to_datetime(recept['ddDatumRecept'])
# recept['Maand'] = recept['ddDatumRecept'].dt.month
#
# # Dataframe aanpassen en onnodige kolommen verwijderen
#
# Recept = recept[['ddDatumRecept', 'ReceptHerkomst', 'cf',
#        'ndReceptnummer', 'ndATKODE', 'sdEtiketNaam', 'ndAantal', 'sdMedewerkerCode',
#        'Uitgifte','APOTHEEK', 'Maand']]
#
#
#
# # Definieer de filters voor het dataframe
# CF_niet = (Recept['cf']!='J')
# LSP_niet = (Recept['sdMedewerkerCode']!='LSP')
# Dienstrecepten_niet = (Recept['ReceptHerkomst'] !='DIENST')
# Zorgregels_niet = (Recept['ReceptHerkomst']!='Z')
# Distributieregels_niet = (Recept['ReceptHerkomst']!='D')
# ZI_ongelijk_0 = (Recept['ndATKODE']!= 0)
#
#
# # Filter het dataframe
# Recept_f = Recept.loc[CF_niet & LSP_niet & Dienstrecepten_niet & Zorgregels_niet & Distributieregels_niet & ZI_ongelijk_0]
#
# #================ VANAF HIER BEGINT HET STUK VAN DE CALLBACK# ================================================================
#
# # stap 1: Filter de periode
#
# periode_begin = 7
# periode_eind = 10
#
# begin = (Recept_f['Maand']>=periode_begin)
# eind = (Recept_f['Maand']<=periode_eind)
#
# Recept_f_periode = Recept_f.loc[begin & eind]
#
# # Maak een aparte dataframe voor iedere apotheek met een telling van de verstrekkingen en het aantal eenheden dat is verstrekt (2 per apotheek = 12 totaal)
#
# # Hanzeplein verstrekkingen en eenheden verstrekt
#
# hanzeplein = (Recept_f_periode['APOTHEEK'] == 'HANZEPLEIN')
# helpman = (Recept_f_periode['APOTHEEK'] == 'HELPMAN')
# musselpark = (Recept_f_periode['APOTHEEK'] == 'MUSSELPARK')
# oosterhaar = (Recept_f_periode['APOTHEEK'] == 'OOSTERHAAR')
# oosterpoort = (Recept_f_periode['APOTHEEK'] == 'OOSTERPOORT')
# wiljes = (Recept_f_periode['APOTHEEK'] == 'WILJES')
#
# # stap 2: bereken de verstrekkingen en eenheden verstrekt voor iedere apotheek
#
# # Hanzeplein verstrekkingen en eenheden
# Recept_f_periode_hzp = Recept_f_periode.loc[hanzeplein]
# #verstrekkingen
# hzp_vs = Recept_f_periode_hzp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen hanzeplein').reset_index()
# #eenheden verstrekt
# hzp_eh = Recept_f_periode_hzp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt hanzeplein').reset_index()
#
#
# # Helpman verstrekkingen en eenheden
# Recept_f_periode_hlp = Recept_f_periode.loc[helpman]
# #verstrekkingen
# hlp_vs = Recept_f_periode_hlp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen helpman').reset_index()
# #eenheden verstrekt
# hlp_eh = Recept_f_periode_hlp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt helpman').reset_index()
#
#
# # Musselpark verstrekkingen en eenheden
# Recept_f_periode_mp = Recept_f_periode.loc[musselpark]
# #verstrekkingen
# mp_vs = Recept_f_periode_mp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen musselpark').reset_index()
# #eenheden verstrekt
# mp_eh = Recept_f_periode_mp.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt musselpark').reset_index()
#
#
# # Oosterhaar verstrekkingen en eenheden
# Recept_f_periode_oh = Recept_f_periode.loc[oosterhaar]
# #verstrekkingen
# oh_vs = Recept_f_periode_oh.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen oosterhaar').reset_index()
# #eenheden verstrekt
# oh_eh = Recept_f_periode_oh.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt oosterhaar').reset_index()
#
#
# # Oosterpoort verstrekkingen en eenheden
# Recept_f_periode_op = Recept_f_periode.loc[oosterpoort]
# #verstrekkingen
# op_vs = Recept_f_periode_op.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen oosterpoort').reset_index()
# #eenheden verstrekt
# op_eh = Recept_f_periode_op.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt oosterpoort').reset_index()
#
#
# # Wiljes verstrekkingen en eenheden
# Recept_f_periode_wil = Recept_f_periode.loc[wiljes]
# #verstrekkingen
# wil_vs = Recept_f_periode_wil.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndATKODE'].count().to_frame('verstrekkingen wiljes').reset_index()
# #eenheden verstrekt
# wil_eh = Recept_f_periode_wil.groupby(by=['ndATKODE', 'sdEtiketNaam'])['ndAantal'].sum().to_frame('eenheden verstrekt wiljes').reset_index()
#
# # stap 3 Merge de verstrekkingen en eenheden databases
#
# totaal_verstrekkingen_eenheden_verstrekt = hzp_eh.merge(hzp_vs[['ndATKODE', 'verstrekkingen hanzeplein']]).merge(hlp_eh[['ndATKODE', 'eenheden verstrekt helpman']]).merge(hlp_vs[['ndATKODE', 'verstrekkingen helpman']]).merge(mp_eh[['ndATKODE', 'eenheden verstrekt musselpark']]).merge(mp_vs[['ndATKODE', 'verstrekkingen musselpark']]).merge(oh_eh[['ndATKODE', 'eenheden verstrekt oosterhaar']]).merge(oh_vs[['ndATKODE', 'verstrekkingen oosterhaar']]).merge(op_eh[['ndATKODE', 'eenheden verstrekt oosterpoort']]).merge(op_vs[['ndATKODE', 'verstrekkingen oosterpoort']]).merge(wil_eh[['ndATKODE', 'eenheden verstrekt wiljes']]).merge(wil_vs[['ndATKODE', 'verstrekkingen wiljes']])
#
# # stap 4 Merge de verstrekkingen en eenheden aan het assortiments dataframe
#
# # maak het assortimentsdataframe gebruiksklaar
#
#
# assortiment_apotheek_1 = assortiment_apotheek[['produktgroep','zinummer', 'etiketnaam',
#        'inkhvh', 'eh', 'voorraadminimum', 'voorraadmaximum', 'locatie1',
#        'voorraadtotaal', 'inkprijs', 'voorraadwaarde']]
#
#
# # merge de boel maar
#
# merge = assortiment_apotheek.merge(totaal_verstrekkingen_eenheden_verstrekt,
#                                how='left',
#                                left_on='zinummer',
#                                right_on='ndATKODE',
#                                ).drop(columns=['ndATKODE', 'sdEtiketNaam'])
#
# merge = merge.replace(np.nan, 0)
#
# # zorg nu dat de doelapotheek (hanzeplein in dit scenario gefilterd wordt op 0 verstrekkingen in de meetperiode
#
# #filters hanzeplein
# nul_verstrekkingen_hanzeplein = (merge['verstrekkingen hanzeplein'] == 0)
# voorraadwaarde_apotheek_positief = (merge['voorraadtotaal']>=1)
#
# #filters andere apotheken
# helpman_verstrekkingen = (merge['verstrekkingen helpman']>=1)
# musselpark_verstrekkingen = (merge['verstrekkingen musselpark']>=1)
# oosterhaar_verstrekkingen = (merge['verstrekkingen oosterhaar']>=1)
# oosterpoort_verstrekkingen = (merge['verstrekkingen oosterpoort']>=1)
# wiljes_verstrekkingen = (merge['verstrekkingen wiljes']>=1)
#
# merge_1 = merge.loc[nul_verstrekkingen_hanzeplein & voorraadwaarde_apotheek_positief]
# merge_2 = merge_1.drop_duplicates(subset=['zinummer'], keep='first')
# merge_3 = merge_2.loc[helpman_verstrekkingen | musselpark_verstrekkingen | oosterhaar_verstrekkingen | oosterpoort_verstrekkingen | wiljes_verstrekkingen]
#
# merge_4 = merge_2.sort_values(by=['voorraadwaarde'], ascending=False)
#
# # filters op productgroepen
# geen_embalage = (merge_4['produktgroep']!='EM')
# geen_zorgactiviteit = (merge_4['produktgroep']!='ZI')
# geen_zorgactiviteit_niet_individueel = (merge_4['produktgroep']!='ZN')
#
# merge_5 = merge_4.loc[geen_embalage & geen_zorgactiviteit & geen_zorgactiviteit_niet_individueel]
#
# winkeldochters = merge_5[['produktgroep', 'zinummer', 'etiketnaam', 'inkhvh', 'eh', 'voorraadminimum', 'voorraadmaximum', 'locatie1',
#        'voorraadtotaal', 'inkprijs', 'voorraadwaarde','verstrekkingen hanzeplein', 'verstrekkingen helpman',
#         'verstrekkingen musselpark','verstrekkingen oosterhaar','verstrekkingen oosterpoort','verstrekkingen wiljes']]
#
# winkeldochters.to_excel('wd_hh.xlsx', index=False)
#
#
#
#
#
# # Stap 2:
#
# # Ontwerp de app
#
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# app.layout = dbc.Container([
#
#     dbc.Row([
#         html.H1('Winkeldochter analyse apotheek', style={'textAlign':'center'})
#     ]),
#     html.Br(),
#     html.Br(),
#
#     dbc.Row([html.H6('Selecteer de periode waarover je de winkeldochters wilt bepalen!', style={'textAlign':'center'})]),
#
#     html.Br(),
#     html.Br(),
#
#     dbc.Row([
#         dcc.RangeSlider(id='periode selectie',
#                         min=1,
#                         max=12,
#                         value=[1, 5],
#
#                         marks={1: 'Januari', 2: 'Februari', 3: 'Maart', 4: 'April', 5: 'Mei', 6: 'Juni',
#                                7: 'Juli', 8: 'Augustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'December'})
#     ]),
#
#     dbc.Row([
#         html.H6('Druk op de knop om de lijst met winkeldochters te downloaden in excel', style={'textAlign':'center'})
#     ]),
#
#     html.Br(),
#     html.Br(),
#
#     dbc.Row([
#         dbc.Col([]),
#         dbc.Col([
#             dbc.Button(id='winkeldochters',
#                        children='Download winkeldochters.xlsx',
#                        color='danger',
#                        class_name='me-1'),
#
#             dcc.Download(id='Download')
#         ]),
#         dbc.Col([]),
#
#     ]),
# ])
#
# # Callback
#
# if __name__ == '__main__':
#     app.run(debug=True)

#PROJECT Zorgprestaties in een dashboard


hanzeplein_zorg = pd.read_excel('hanzeplein_zorg.xlsx')
helpman_zorg = pd.read_excel('helpman_zorg.xlsx')
musselpark_zorg = pd.read_excel('musselpark_zorg.xlsx')
oosterhaar_zorg = pd.read_excel('oosterhaar_zorg.xlsx')
oosterpoort_zorg = pd.read_excel('oosterpoort_zorg.xlsx')
wiljes_zorg = pd.read_excel('wiljes_zorg.xlsx')

hanzeplein_zorg['apotheek'] = 'hanzeplein'
helpman_zorg['apotheek'] = 'helpman'
musselpark_zorg['apotheek'] = 'musselpark'
oosterhaar_zorg['apotheek'] = 'oosterhaar'
oosterpoort_zorg['apotheek'] = 'oosterpoort'
wiljes_zorg['apotheek'] = 'wiljes'

zorgprestaties = pd.concat([hanzeplein_zorg, helpman_zorg, musselpark_zorg, oosterhaar_zorg, oosterpoort_zorg, wiljes_zorg])

# maand en jaar kolom maken

zorgprestaties['maand'] = zorgprestaties['PrestatieDatum'].dt.month
zorgprestaties['jaar'] = zorgprestaties['PrestatieDatum'].dt.year

# filter voor jaar
jaarfilter = zorgprestaties['jaar']>=2020

zorgprestaties_filter_jaar = zorgprestaties.loc[jaarfilter]


print(zorgprestaties_filter_jaar['jaar'].unique())



# filters maken voor welke prestaties je wel wilt zien (1) consulten (2) ontslagbegeleiding

consulten = (zorgprestaties_filter_jaar['PrestatieOmschrijving'] == 'Farmaceutisch consult bij zorgvraag patient')
ontslagbegeleiding = (zorgprestaties_filter_jaar['PrestatieOmschrijving'] == 'Farmaceutische begeleiding i.v.m. ontslag uit het ziekenhuis')
instructie_hulpmiddel = (zorgprestaties_filter_jaar['PrestatieOmschrijving'] == 'Instructie UR geneesmiddel gerelateerd hulpmiddel')

zorgprestaties_filter_jaar_filter = zorgprestaties_filter_jaar.loc[consulten | ontslagbegeleiding | instructie_hulpmiddel]

zorgprestaties_filter_jaar_filter = zorgprestaties_filter_jaar_filter.sort_values(by=['jaar'], ascending=True)



# ++++++++++++++++ APP Bewerking 1 apotheek voorbeeld +++++++++++++++++++

# filters voor jaar
jaar = (zorgprestaties_filter_jaar_filter['jaar']==2024)

#apotheek = (zorgprestaties_filter_jaar_filter['apotheek']=='musselpark')

zp = zorgprestaties_filter_jaar_filter.loc[jaar]

# maak de tabel voor de grafiek

wiljes = zp.groupby(by=['apotheek','PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal declaraties').reset_index()

print(wiljes.head(20))

Wiljes = px.bar(wiljes,
       x='PrestatieOmschrijving',
       y='aantal declaraties',
       color='apotheek',
                barmode='group',
                text_auto=True,
                title='AG Overzicht zorgprestaties 2024')

#Wiljes.show()

# app maken

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Layout
app.layout = dbc.Container([

    dbc.Row([
        html.H1('ZORGPRESTATIES APOTHEKERSGROEP GRONINGEN 2024')
    ]),    # Titel

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='jaar selectie', options=zorgprestaties_filter_jaar_filter['jaar'].unique(), value=zorgprestaties_filter_jaar_filter['jaar'].max())
        ], width=3),
        dbc.Col([]),
        dbc.Col([]),
    ]),    # Controls

    dbc.Row([
        dcc.Graph(id='overzicht prestaties AG')
    ]),    # Overzicht grafiek
    dbc.Row([dcc.Graph(id='hanzeplein')]),
    dbc.Row([dcc.Graph(id='oosterpoort')]),
    dbc.Row([dcc.Graph(id='helpman')]),
    dbc.Row([dcc.Graph(id='wiljes')]),
    dbc.Row([dcc.Graph(id='oosterhaar')]),
    dbc.Row([dcc.Graph(id='musselpark')]),





])

# callback functie
@callback(
    Output('overzicht prestaties AG', 'figure'),
     Output('hanzeplein', 'figure'),
     Output('oosterpoort', 'figure'),
     Output('helpman', 'figure'),
     Output('wiljes', 'figure'),
     Output('oosterhaar', 'figure'),
     Output('musselpark', 'figure'),
    Input('jaar selectie', 'value')

)

def overzicht_zorgprestaties(jaar):


    periode = zorgprestaties_filter_jaar_filter['jaar']==jaar

    zp = zorgprestaties_filter_jaar_filter.loc[periode]

    # filters voor apotheken
    hanzeplein = zp['apotheek'] == 'hanzeplein'
    oosterpoort = zp['apotheek'] == 'oosterpoort'
    helpman = zp['apotheek'] == 'helpman'
    wiljes = zp['apotheek'] == 'wiljes'
    oosterhaar = zp['apotheek'] == 'oosterhaar'
    musselpark = zp['apotheek'] == 'musselpark'

    # maak de tabel voor het overzicht

    overzicht = zp.groupby(by=['apotheek', 'PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal prestaties AG').reset_index()

    totaal = px.bar(overzicht,
                    x='PrestatieOmschrijving',
                    y='aantal prestaties AG',
                    color='apotheek',
                    barmode='group',
                    text_auto=True,
                    title='OVERZICHT ZORGPRESTATIES AG')

    # HANZEPLEIN
    hanzeplein_data = zp.loc[hanzeplein]

    hanzeplein_data_grafiek = hanzeplein_data.groupby(by=['maand', 'PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    hanzeplein_grafiek = px.bar(hanzeplein_data_grafiek,
                                x='maand',
                                y='aantal prestaties',
                                color='PrestatieOmschrijving',
                                barmode='group',
                                text_auto='True',
                                title='HANZEPLEIN')

    # OOSTERPOORT
    oosterpoort_data = zp.loc[oosterpoort]

    oosterpoort_data_grafiek = oosterpoort_data.groupby(by=['maand', 'PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    oosterpoort_grafiek = px.bar(oosterpoort_data_grafiek,
                                x='maand',
                                y='aantal prestaties',
                                color='PrestatieOmschrijving',
                                barmode='group',
                                text_auto='True',
                                title='OOSTERPOORT')

    # HELPMAN
    helpman_data = zp.loc[helpman]

    helpman_data_grafiek = helpman_data.groupby(by=['maand', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    helpman_grafiek = px.bar(helpman_data_grafiek,
                                 x='maand',
                                 y='aantal prestaties',
                                 color='PrestatieOmschrijving',
                                 barmode='group',
                                 text_auto='True',
                                 title='HELPMAN')

    # WILJES
    wiljes_data = zp.loc[wiljes]

    wiljes_data_grafiek = wiljes_data.groupby(by=['maand', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    wiljes_grafiek = px.bar(wiljes_data_grafiek,
                             x='maand',
                             y='aantal prestaties',
                             color='PrestatieOmschrijving',
                             barmode='group',
                             text_auto='True',
                             title='WILJES')


    # OOSTERHAAR
    oosterhaar_data = zp.loc[oosterhaar]

    oosterhaar_data_grafiek = oosterhaar_data.groupby(by=['maand', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    oosterhaar_grafiek = px.bar(oosterhaar_data_grafiek,
                            x='maand',
                            y='aantal prestaties',
                            color='PrestatieOmschrijving',
                            barmode='group',
                            text_auto='True',
                            title='OOSTERHAAR')

    # MUSSELPARK
    musselpark_data = zp.loc[musselpark]

    musselpark_data_grafiek = musselpark_data.groupby(by=['maand', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal prestaties').reset_index()

    musselpark_grafiek = px.bar(musselpark_data_grafiek,
                                x='maand',
                                y='aantal prestaties',
                                color='PrestatieOmschrijving',
                                barmode='group',
                                text_auto='True',
                                title='MUSSELPARK')








    return totaal, hanzeplein_grafiek, oosterpoort_grafiek, helpman_grafiek, wiljes_grafiek, oosterhaar_grafiek, musselpark_grafiek

if __name__ == '__main__':
    app.run(debug=True)










