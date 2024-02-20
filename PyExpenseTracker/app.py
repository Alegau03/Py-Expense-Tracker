import flet as ft
from flet import *
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

class AppState:
    current_page = "home"

# FUNZIONE PRINCIPALE
def main(page: ft.Page):
    
    # IMPOSTAZIONI PRINCIPALI DELL APP
    current_day = datetime.today()

    page.title = "Finanz APP v1.1.4"
    page.theme_mode = "dark"
    page.scroll="ALWAYS"
   


    # gestisce il tema in tuta l'app
    def toggle_theme(e):
        if page.theme_mode == "dark":
            page.theme_mode = "light"
           
        else:
            page.theme_mode = "dark"
        page.update()



    # funzione per navigare tra le pagine
    def navigate_to(page_name):
        AppState.current_page = page_name
        render_page()



    # schermata home (completa)
    def home_page():

            ############### FUNZIONI SCHERMATA HOME######################
     
        # FUNZIONI SPESA
        #apre l'alert dialog spesa
        def aggiungi_spesa(e):
             open_dlg_modal(e)

        #chiude l'alert dialog spesa
        def close_dlg(e):
            dlg_modal.open = False
            dlg_modal.actions[0].value = ""
            dlg_modal.actions[2].value = ""
            dlg_modal.actions[3].value = ""
            page.update()

        #apre l'alert dialog spesa
        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        #prende i dati dall'alertdialog e inseriesce in spesa.csv, poi aggiorna il resto
        def conferma_spesa(e):
            importo = dlg_modal.actions[0].value
            nome_conto = str(dlg_modal.actions[2].value).lower()
            categoria = str(dlg_modal.actions[3].value).lower()
            categoria = categoria.replace(" ", "")
            data_corrente = change_date(e)

            if not importo.isdigit():
                return

            if importo == "" or importo == " ":
                importo = 0
            
            # Chiamata alla funzione per aggiornare il saldo del conto
            conto_trovato = aggiorna_saldo_conto_spesa(nome_conto, importo)

            # Chiudi la finestra solo se il conto è stato trovato e aggiornato
            if conto_trovato:
                with open('assets/spese.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([importo, data_corrente,nome_conto, categoria])
                dlg_modal.actions[0].value = ""
                dlg_modal.actions[2].value = ""
                dlg_modal.actions[3].value = ""
                aggiorna_spesa_totale()
                aggiorna_budget_rimanente()
                aggiorna_spesa_mensile()
                close_dlg(e)
            else:
                dlg_modal.actions[1].value = "Conto NON trovato"
                page.update()

        #ggiorna la spesa totale
        def aggiorna_spesa_mensile():
            spesa=spesa_totale_mese_corrente("assets/spese.csv")
            spesaTot_mese.value=f"Spesa Mensile: {spesa} €"
            page.update()

        def aggiorna_spesa_totale():
            spesa = calcola_spesa_totale()
            spesaTot.value = f"Spesa Totale: {spesa} €"
            page.update()

        #calcola la spesa totale
        def calcola_spesa_totale():
            totale = 0
            with open('assets/spese.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:  # Assicurati che la riga contenga almeno un elemento
                        totale += float(row[0])
            return totale

        #azzera la spesa totale
        def azzera_entrata_totale(e):
            with open('assets/entrate.csv', 'w', newline='') as file:
                pass
            aggiorna_budget_rimanente()
            aggiorna_entrata_totale()

        # FUNZIONI CONTO

        def aggiungi_conto(e):
            open_dlg_modal_conto(e)

        def open_dlg_modal_conto(e):
            page.dialog = dlg_modal_conto
            dlg_modal_conto.open = True
            page.update()

        def close_dlg_conto(e):
            dlg_modal_conto.open = False
            dlg_modal_conto.actions[0].value=""
            dlg_modal_conto.actions[1].value=""
            page.update()

        def conferma_conto(e):
            nome_conto = str(dlg_modal_conto.actions[0].value)
            nome_conto= nome_conto.lower()
            saldo_iniziale = dlg_modal_conto.actions[1].value 
            data = datetime.today().strftime("%Y-%m-%d")
            if not saldo_iniziale.isdigit():
                return
            if saldo_iniziale == "" or saldo_iniziale == " ":
                importo = 0
            with open('assets/conti.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nome_conto, data,saldo_iniziale])
            dlg_modal_entrata.actions[0].value = ""
            dlg_modal_entrata.actions[1].value = ""
            aggiorna_entrata(nome_conto,saldo_iniziale,data)
            close_dlg_conto(e)
            aggiorna_entrata_totale()
            aggiorna_budget_rimanente()
        
        #questa funzione viene chiamata quando creo un nuovo conto e inseriesce nello storico delle entrate una nuova entrata corrispondende alla creazione del conto
        def aggiorna_entrata(nome_conto,saldo_iniziale,data):
            with open('assets/entrate.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([saldo_iniziale, data,nome_conto])

        def aggiorna_saldo_conto_spesa(nome_conto, importo):
            # Leggi il file "conti.csv" e cerca il conto
            with open('assets/conti.csv', 'r', encoding="latin1") as conti_file:
                conti_reader = csv.reader(conti_file)
                conti = list(conti_reader)

            conto_trovato = False

            # Cerca il conto nel file
            for i, row in enumerate(conti):
                if row and row[0].lower() == nome_conto.lower():
                    # Aggiorna il saldo del conto sottraendo l'importo
                    conti[i][2] = str(float(conti[i][2]) - float(importo))
                    conto_trovato = True

            # Se il conto non è stato trovato, ritorna False
            if not conto_trovato:
                return False

            # Scrivi i dati aggiornati nel file "conti.csv"
            with open('assets/conti.csv', 'w', newline='', encoding="latin1") as conti_file:
                conti_writer = csv.writer(conti_file)
                conti_writer.writerows(conti)

            return True

        def aggiorna_saldo_conto(nome_conto, importo):
            # Leggi il file "conti.csv" e cerca il conto
            with open('assets/conti.csv', 'r', encoding="latin1") as conti_file:
                conti_reader = csv.reader(conti_file)
                conti = list(conti_reader)

            conto_trovato = False

            # Cerca il conto nel file
            for i, row in enumerate(conti):
                if row and row[0].lower() == nome_conto.lower():
                    # Aggiorna il saldo del conto
                    conti[i][2] = str(float(conti[i][2]) + float(importo))
                    conto_trovato = True

            # Se il conto non è stato trovato, crea una nuova riga
            if not conto_trovato:
                data_creazione = datetime.today().strftime("%Y-%m-%d")
                nuova_riga = [nome_conto, data_creazione, importo]
                conti.append(nuova_riga)

            # Scrivi i dati aggiornati o la nuova riga nel file "conti.csv"
            with open('assets/conti.csv', 'w', newline='', encoding="latin1") as conti_file:
                conti_writer = csv.writer(conti_file)
                conti_writer.writerows(conti)      

        # FUNZIONI ENTRATA
        def entrata(e):
            open_dlg_modal_entrata(e)

        def conferma_entrata(e):
            importo = dlg_modal_entrata.actions[0].value
            nome_conto = str(dlg_modal_entrata.actions[2].value)
            nome_conto=nome_conto.lower()
            data_corrente = change_date(e)

            if not importo.isdigit():
                return
            if importo == "" or importo == " ":
                importo = 0
            with open('assets/entrate.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([importo, data_corrente,nome_conto])
            dlg_modal_entrata.actions[0].value = ""
            dlg_modal_entrata.actions[2].value =""
            aggiorna_saldo_conto(nome_conto, importo)
            aggiorna_entrata_totale()
            aggiorna_entrata_mensile()
            aggiorna_budget_rimanente()
            close_dlg_entrata(e)

        def calcola_entrata_totale():
            totale = 0
            with open('assets/entrate.csv', 'r',encoding="latin1") as file:
                reader = csv.reader(file)
                for row in reader:
                    totale += float(row[0])
            return totale

        def aggiorna_entrata_totale():
            entrata = calcola_entrata_totale()
            entrataTot.value = f"Entrate Totali: {entrata} €"
            page.update()

        def aggiorna_entrata_mensile():
            entrata=entrate_totali_mese_corrente("assets/entrate.csv")
            entrataTot_mese.value= f"Entrate Mensili: {entrata} €"
            page.update()
        
        def close_dlg_entrata(e):
            dlg_modal_entrata.open = False
            dlg_modal_entrata.actions[0].value = ""
            dlg_modal_entrata.actions[2].value =""
            page.update()
        
       
        def open_dlg_modal_entrata(e):
            page.dialog = dlg_modal_entrata
            dlg_modal_entrata.open = True
            page.update()

        def calcola_budget_rimanente():
            spese = float(calcola_spesa_totale())
            budget = float(calcola_entrata_totale())
            rimanente = budget-spese
            return rimanente
        
        def aggiorna_budget_rimanente():
            rimanente = calcola_budget_rimanente()
            bugetRimanente.value = f"Totale Conti: {rimanente}"
            page.update()
            salva_budget_rimanente()

        def salva_budget_rimanente():
            rimanente = calcola_budget_rimanente()
            data_corrente = change_date(None)
            with open('assets/budget_rimanente.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([rimanente, data_corrente])

        def change_date(e):
            if date_picker.value!=None:
                current_day= (date_picker.value).strftime("%Y-%m-%d")
                
            else:
                current_day= datetime.today().strftime("%Y-%m-%d")
            return current_day

        def leggi_conti(file_path):
                lista_conti = []
                try:
                    with open(file_path, 'r', encoding="latin1") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            # Ignora le righe vuote o incomplete
                            if len(row) >= 3:
                                nome_conto = row[0].strip()
                                saldo = float(row[2])
                                tupla_conto = (nome_conto, saldo)
                                lista_conti.append(tupla_conto)
                except FileNotFoundError:
                    print(f"Il file {file_path} non è stato trovato.")
                except Exception as e:
                    print(f"Errore durante la lettura del file {file_path}: {e}")
                return lista_conti
        
        def spesa_totale_mese_corrente(file_path):
            # Ottieni la data corrente
            oggi = datetime.now()
            mese_corrente = oggi.month
            anno_corrente = oggi.year

            spesa_totale = 0

            with open(file_path, 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if row:  # Assicurati che la riga non sia vuota
                        importo, data_spesa, conto, categoria = row

                        # Converte la data dal formato stringa ad oggetto datetime
                        data_spesa = datetime.strptime(data_spesa, '%Y-%m-%d')

                        # Verifica se la data appartiene al mese corrente
                        if data_spesa.month == mese_corrente and data_spesa.year == anno_corrente:
                            spesa_totale += float(importo)

            return float(spesa_totale)

        def entrate_totali_mese_corrente(file_path):
            # Ottieni la data corrente
            oggi = datetime.now()
            mese_corrente = oggi.month
            anno_corrente = oggi.year

            entrate_totali = 0

            with open(file_path, 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if row:  # Assicurati che la riga non sia vuota
                        importo, data_entrata, conto = row

                        # Converte la data dal formato stringa ad oggetto datetime
                        data_entrata = datetime.strptime(data_entrata, '%Y-%m-%d')

                        # Verifica se la data appartiene al mese corrente
                        if data_entrata.month == mese_corrente and data_entrata.year == anno_corrente:
                            entrate_totali += float(importo)

            return entrate_totali

#########################àSTRUTTURA PAGINA###############################
        page.clean()
       
        conti = leggi_conti("assets/conti.csv")
        nomi_conti=[tupla[0] for tupla in conti]
        conto_dropdown=ft.Dropdown(width=150,alignment=ft.alignment.center)
        for nome in nomi_conti:
            
            conto_dropdown.options.append(ft.dropdown.Option(nome))
            
        # ALERT DIALOG PER SPESA
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Aggiungi Spesa"),
            content=ft.Text("Aggiungi Spesa"),
            actions=[
                ft.TextField(label="Spesa in euro"),
                ft.Container(content=ft.Text("Conto: "),alignment=ft.alignment.center_left),
                conto_dropdown,
                ft.TextField(label="Categoria"),
                ft.IconButton(icon="CALENDAR_MONTH",on_click=lambda _: date_picker.pick_date()),
                ft.Row([ft.TextButton("Conferma", on_click=conferma_spesa), ft.TextButton("Esci", on_click=close_dlg)])
                
            ],

        )
        date_picker = ft.DatePicker(
            on_change=change_date,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )

        page.overlay.append(date_picker)
        
        # ALERT DIALOG PER ENTRATA
        dlg_modal_entrata = ft.AlertDialog(
            modal=True,
            title=ft.Text("Aggiungi Entrata"),
            content=ft.Text("Aggiungi Entrata"),
            actions=[
                ft.TextField(label="Entrata in euro"),
                ft.Container(content=ft.Text("Conto:"),alignment=ft.alignment.center_left),
                conto_dropdown,
                ft.IconButton(icon="CALENDAR_MONTH",on_click=lambda _: date_picker.pick_date()),
                ft.TextButton("Conferma", on_click=conferma_entrata),
                ft.TextButton("Esci", on_click=close_dlg_entrata),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        #ALERT DIALOG PER NUOVO CONTO
        dlg_modal_conto= ft.AlertDialog(
            modal=True,
            title=ft.Text("Aggiungi Conto"),
            content=ft.Text("Aggiungi Conto"),
            actions=[
                ft.TextField(label="Nome Conto"),
                ft.TextField(label="Saldo Iniziale, sarà aggiunto al tuo saldo totale."),
                ft.TextButton("Conferma", on_click=conferma_conto),
                ft.TextButton("Esci", on_click=close_dlg_conto),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        ############PAGINA###############################
        #budget rimanente
        rimanente = calcola_budget_rimanente()
        stringaBudgetRimanente = f"Totale Conti: {rimanente} €"
        bugetRimanente = ft.Text(stringaBudgetRimanente,weight="bold",font_family="Arial",size=30)
        page.add(ft.Container(content=ft.Text("Benvenuto in FinanzApp",weight="bold",size=30,font_family="Arial"),alignment=ft.alignment.bottom_center))
        
        page.add(
                ft.Container(
                content=ft.Card(bugetRimanente,width=350),alignment=ft.alignment.top_center,border_radius=10,height=100
                    
                )
            
        )
        EffettuaMovimenti=ft.Card(
            content=ft.Container(
                content=ft.Column(
                        [
                        ft.Container(content=ft.Text("Effettua Movimenti",weight="bold",font_family="Arial",size=25),padding=7),
                        ft.Row(
                             [ft.FilledButton(text="Aggiungi Spesa", on_click=aggiungi_spesa,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )),
                              ft.FilledButton(text="Aggiungi Entrata", on_click=entrata,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        ))], 
                       )]),width=400,padding=7,margin=5,border_radius=10,height=130))
        #pulsanti per spese ed entrata
        

        GestioneConti=ft.Card(
                content=ft.Container(
                content=ft.Column(
                        [
                        ft.Container(content=ft.Text("Gestisci i Conti",weight="bold",font_family="Arial",size=25),padding=7),
                        ft.Row(
                             [ft.FilledButton(text="Aggiungi Conto", on_click=aggiungi_conto,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )),
                     ft.FilledButton(text="Gestisci Conti", on_click=lambda e: navigate_to("conti"),style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )),
                    
                    ])]),width=400,padding=7,margin=5,border_radius=10,height=130))

        page.add(ft.Row([EffettuaMovimenti,GestioneConti]))

        #container spesaTot

        page.add(ft.Container(content=ft.Text("Ecco alcuni dati sui tuoi conti:",weight="bold",font_family="Arial",size=20),padding=10))


        
        spesa = float(calcola_spesa_totale())
        stringaTot = f"Spesa Totale: {spesa} €"
        spesaTot=ft.Text(stringaTot)
        entrata = calcola_entrata_totale()
        stringaE = f"Entrate Totali: {entrata} €"
        entrataTot= ft.Text(stringaE)

        containerSpesaTot=(ft.Container(
            content=spesaTot,
            bgcolor=ft.colors.BLUE_GREY,padding=7,margin=5,border_radius=5,width=200

        ))
        totale_mese_corrente = spesa_totale_mese_corrente("assets/spese.csv")
        stringaTot_mese = f"Spesa Mensile: {totale_mese_corrente} €"
        spesaTot_mese=ft.Text(stringaTot_mese)
        containerSpesaMese=(ft.Container(
            content=spesaTot_mese,
            bgcolor=ft.colors.BLUE_GREY,padding=7,margin=5,border_radius=5,width=200

        ))
        #container Entrate Tot
        containerEntrataTot=(ft.Container(
            content=entrataTot,
            bgcolor=ft.colors.BLUE_GREY,border_radius=5,padding=7,margin=5,width=200

        ))
        
        totale_entrate_mese_corrente = entrate_totali_mese_corrente("assets/entrate.csv")
        stringaEntrataTot_mese = f"Entrate Mensili: {totale_entrate_mese_corrente} €"
        entrataTot_mese=ft.Text(stringaEntrataTot_mese)

        containerEntrataTot_mese=(ft.Container(
            content=entrataTot_mese,
            bgcolor=ft.colors.BLUE_GREY,padding=7,margin=5,border_radius=5,width=200

        ))

        rowTot=ft.Row([containerSpesaTot,containerEntrataTot])
        rowMensili= ft.Row([containerSpesaMese,containerEntrataTot_mese])
        page.add(rowTot)
        page.add(rowMensili)

        
       
        #page.add(ft.ElevatedButton(text="Azzera Entrate", on_click=azzera_entrata_totale))

    #schermata grafici (completa)
    def altro_page():
        
        #3 FUNZIONI DEI GRAFICI
        def crea_grafico_torta(file_csv, output_file, data_inizio, data_fine):
            # Carica il file CSV in un DataFrame senza intestazioni
            df = pd.read_csv(file_csv, header=None, names=['importo', 'data','conto', 'categoria'])
            df = df[(df['data'] >= data_inizio) & (df['data'] <= data_fine)]
            # Raggruppa i dati per categoria e calcola la somma degli importi per ogni categoria
            gruppo_categoria = df.groupby('categoria')['importo'].sum()

            # Crea il grafico a torta
            plt.figure(figsize=(8, 8))
            plt.pie(gruppo_categoria, labels=gruppo_categoria.index, autopct='%1.1f%%', startangle=140)

            # Aggiungi la legenda
            plt.legend(title='Categorie', bbox_to_anchor=(1, 0.5), loc="center left")

            # Aggiungi il titolo
            plt.title('Spese per Categoria')

            # Salva il grafico come un file .jpg di dimensioni 200x200
            plt.savefig(output_file, dpi=100, bbox_inches='tight', pad_inches=0.1)

        def crea_grafico_andamento_patrimonio(output_file, data_inizio, data_fine):
            # Carica il file CSV del budget rimanente
            df_budget = pd.read_csv('assets/budget_rimanente.csv', header=None, names=['rimanente', 'data'])

            # Converte la colonna 'data' in formato datetime
            df_budget['data'] = pd.to_datetime(df_budget['data'])

            # Filtra i dati tra le date selezionate
            df_budget = df_budget[(df_budget['data'] >= data_inizio) & (df_budget['data'] <= data_fine)]

            # Ordina il DataFrame in base alla colonna 'data'
            df_budget = df_budget.sort_values('data')

            # Crea il grafico di andamento del patrimonio
            plt.figure(figsize=(8, 8))
            plt.plot(df_budget['data'], df_budget['rimanente'], marker='o', linestyle='-', color='b')

            # Aggiungi titoli e etichette
            plt.title('Andamento del Patrimonio')
            plt.xlabel('Data')
            plt.ylabel('Budget Rimanente')

            # Personalizza le etichette sull'asse x
            plt.xticks(rotation=45, ha='right')

            # Salva il grafico come un file .jpg di dimensioni 200x200
            plt.savefig(output_file, dpi=100, bbox_inches='tight', pad_inches=0.1)
        
        def crea_istogramma(file_spese, file_entrate, anno_corrente):
            # Carica i dati dai file CSV senza riga di intestazione
            spese = pd.read_csv(file_spese, header=None, names=['soldi spesi', 'data', 'conto','categoria'])
            entrate = pd.read_csv(file_entrate, header=None, names=['soldi entrati', 'data','conto'])

            # Estrai il mese e l'anno dalla data e crea una colonna 'Mese' nel dataframe
            spese['Mese'] = pd.to_datetime(spese['data']).dt.strftime('%Y-%m').str.slice(5)
            entrate['Mese'] = pd.to_datetime(entrate['data']).dt.strftime('%Y-%m').str.slice(5)

            # Ordina i dataframe in base alla data
            spese = spese.sort_values(by='data')
            entrate = entrate.sort_values(by='data')

            # Raggruppa per mese e calcola la somma delle spese ed entrate
            spese_mensili = spese.groupby('Mese')['soldi spesi'].sum()
            entrate_mensili = entrate.groupby('Mese')['soldi entrati'].sum()

            # Crea un dataframe unificato per spese ed entrate
            dati_mensili = pd.DataFrame({'Spese': spese_mensili, 'Entrate': entrate_mensili}, index=spese_mensili.index)

            # Riempie i mesi senza dati con zeri
            mesi_totali = [str(i).zfill(2) for i in range(1, 13)]
            dati_mensili = dati_mensili.reindex(mesi_totali, fill_value=0)

            # Crea l'istogramma con le barre accanto
            larghezza_barre = 0.35  # Ridotto l'ampiezza delle barre per accomodare lo spazio tra di esse
            indici = range(1, 13)
            barre_spese = plt.bar(indici, dati_mensili['Spese'], width=larghezza_barre, color='red', label='Spese')
            barre_entrate = plt.bar([x + larghezza_barre for x in indici], dati_mensili['Entrate'], width=larghezza_barre, color='green', label='Entrate')

            # Imposta il layout
            plt.xlabel('Mese')
            plt.ylabel('Ammontare')
            plt.title(f'Istogramma Spese ed Entrate - Anno {anno_corrente}')
            plt.xticks([x + larghezza_barre / 2 for x in indici], mesi_totali)  # Posiziona le etichette al centro delle coppie di barre
            plt.legend()

            # Aggiungi etichette sopra le barre
            for i, (spese, entrate) in enumerate(zip(dati_mensili['Spese'], dati_mensili['Entrate'])):
                if not pd.isna(spese) and not pd.isna(entrate):
                    plt.text(i + 1, max(spese, entrate) + 10, f"{int(spese)}\n{int(entrate)}", ha='center', va='bottom')

            # Salva l'immagine come .jpg
            plt.savefig(f'images/istogramma_{anno_corrente}.jpg', dpi=100, pad_inches=0.1, bbox_inches="tight")
            plt.clf()
            plt.close()
        page.clean()

        def prima_data(e):
             prima_data= (date_picker_prima.value).strftime("%Y-%m-%d")
             stringaprima=str(prima_data)
             testo_prima.value=f"Prima data: {stringaprima}"
             page.update()
        
        def seconda_data(e):
             seconda_data= (date_picker_seconda.value).strftime("%Y-%m-%d")
             stringaseconda = str(seconda_data)
             testo_seconda.value=f"Seconda data: {stringaseconda}"
             page.update()

        def crea_grafici(e):
            # Verifica se le date sono state selezionate
            
            anno_corrente = datetime.now().year
            crea_istogramma("assets/spese.csv","assets/entrate.csv",anno_corrente)
            if date_picker_prima.value is not None and date_picker_seconda.value is not None:
                # Chiamate le funzioni di creazione dei grafici con le date selezionate
               
                crea_grafico_torta('assets/spese.csv', 'images/grafico_spesa.jpg', date_picker_prima.value.strftime("%Y-%m-%d"), date_picker_seconda.value.strftime("%Y-%m-%d"))
                crea_grafico_andamento_patrimonio('images/grafico_patrimonio.jpg', date_picker_prima.value.strftime("%Y-%m-%d"), date_picker_seconda.value.strftime("%Y-%m-%d"))
              
                image1=ft.Image(src="images/grafico_spesa.jpg",width=300,height=300)
                image2= ft.Image(src="images/grafico_patrimonio.jpg", width=300,height=300)
                image3=ft.Image(src=f"images/istogramma_{anno_corrente}.jpg", width=300,height=300)
                
                page.add(ft.Column([
                    ft.Container(ft.Text("Ecco i tuoi grafici",weight="bold",font_family="Georgia"),margin=5,
                    padding=5,
                    alignment=ft.alignment.center,),
                    ft.Container(
                    content=image1,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=250,
                    height=250,
                    border_radius=10),
                    ft.Text("Questo grafico mostra in cosa hai speso i tuoi soldi",font_family="sans-serif"),
                
                    ft.Container(
                    content=image2,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=250,
                    height=250,
                    border_radius=10),
                    ft.Text("Questo grafico mostra l'andamento del tuo patrimonio",font_family="sans-serif"),

                    ft.Container(
                    content=image3,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=250,
                    height=250,
                    border_radius=10),
                    ft.Text("Questo grafico mostra le spese e le entrate mese per mese durante l'anno",font_family="sans-serif"),])
                )
                page.update()
            else:
                ft.Text("Seleziona entrambe le date prima di creare i grafici.")
            

        page.add(ft.Container(content=ft.Text("Grafici",weight="bold",size=30,font_family="Arial"),alignment=ft.alignment.bottom_center))
        page.add(ft.Text("In questa pagina puoi creare dei grafici per capire come vanno le tue finanze personali.",size=20,font_family="Arial"))
        page.add(ft.Text("Seleziona le due date di intervallo:",size=20,weight="bold"))

        # PRIMO DATEPICKER
        date_picker_prima= ft.DatePicker(
            help_text="Prima data",
            on_change=prima_data,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )
        page.overlay.append(date_picker_prima)

        date_button_prima = ft.IconButton("CALENDAR_MONTH",on_click=lambda _: date_picker_prima.pick_date())
        stringa1=f"Prima data: "
        testo_prima=ft.Text(stringa1)
        page.add(ft.Row([date_button_prima,testo_prima]))
        #SECONDO DATEPICKER
        date_picker_seconda= ft.DatePicker(
            help_text="Seconda data",
            on_change=seconda_data,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )
        page.overlay.append(date_picker_seconda)
       
        stringa2=f"Seconda data: "
        testo_seconda= ft.Text(stringa2)
        date_button_seconda = ft.IconButton("CALENDAR_MONTH",on_click=lambda _: date_picker_seconda.pick_date())
        page.add(ft.Row([date_button_seconda,testo_seconda]))

        crea_grafici_button = ft.FilledButton("Crea Grafici", on_click=crea_grafici,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        ))
        page.add(crea_grafici_button)

    #schermata gestione conti (completa)
    def conti_page():
            page.clean()    
            
            # FUNZIONI PAGINA CONTI
            def leggi_conti(file_path):
                lista_conti = []
                try:
                    with open(file_path, 'r', encoding="latin1") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            # Ignora le righe vuote o incomplete
                            if len(row) >= 3:
                                nome_conto = row[0].strip()
                                saldo = float(row[2])
                                tupla_conto = (nome_conto, saldo)
                                lista_conti.append(tupla_conto)
                except FileNotFoundError:
                    print(f"Il file {file_path} non è stato trovato.")
                except Exception as e:
                    print(f"Errore durante la lettura del file {file_path}: {e}")
                return lista_conti
            
            #funzione che crea la colonna dei conti totali
            def colonna(conti):
                items=[]
                for tupla_conto in conti:
            
                    nome_conto,saldo=tupla_conto
                    nome_conto=nome_conto.upper()

                    temprow=ft.Container(content=ft.Row([ft.Container(content=ft.Text(nome_conto,weight="bold",font_family="Verdana"),alignment=ft.alignment.center_left,width=130),
                                                        ft.Container(content=ft.Text(f"{saldo} €"),alignment=ft.alignment.center_left,width=60),
                                                        ]))
                    items.append(ft.Container(content=temprow,margin=2))
                   
                return items
        
            def open_modifica_dialog(e):
                page.dialog = modifica_dialog
                modifica_dialog.open = True
                page.update()

            def open_elimina_dialog(e):
                page.dialog = elimina_dialog
                elimina_dialog.open = True
                page.update()

            def close_dlg_elimina(e):
                elimina_dialog.open = False
                elimina_dialog.actions[0].value=""
                page.update()

            def close_dlg_modifica(e):
                modifica_dialog.open = False
                modifica_dialog.actions[0].value = ""
                modifica_dialog.actions[1].value = ""
                modifica_dialog.actions[2].value = ""
                page.update()
            def modifica_conto(e):
                conto_selezionato = modifica_dialog.actions[0].value

                nuovo_nome = modifica_dialog.actions[1].value.lower()
                if nuovo_nome == "" or nuovo_nome == " " or nuovo_nome == None:
                    nuovo_nome = conto_selezionato
                
                nuovo_saldo = modifica_dialog.actions[2].value
                if nuovo_saldo == "" or nuovo_saldo == " " or nuovo_saldo == None:
                    pass
                else:
                    

                    # Leggi i conti dal file
                    file_path_conti = 'assets/conti.csv'
                    lista_conti = leggi_conti(file_path_conti)

                    # Cerca il conto da modificare
                    conto_da_modificare = None
                    for i, (nome_conto, saldo) in enumerate(lista_conti):
                        if nome_conto.lower() == conto_selezionato.lower():
                            conto_da_modificare = i
                            break

                    if conto_da_modificare is not None:
                        # Salva il saldo precedente
                        saldo_precedente = float(lista_conti[conto_da_modificare][1])

                        # Modifica il nome del conto e il saldo
                        lista_conti[conto_da_modificare] = (nuovo_nome, float(nuovo_saldo))

                        # Modifica il saldo nel file "conti.csv"
                        with open(file_path_conti, 'w', newline='', encoding='latin1') as conti_file:
                            conti_writer = csv.writer(conti_file)
                            for nome_conto, saldo in lista_conti:
                                conti_writer.writerow([nome_conto, datetime.now().strftime("%Y-%m-%d"), saldo])

                        # Modifica il saldo nei file "spese.csv" o "entrate.csv"
                        nuovo_saldo = float(nuovo_saldo)

                        if saldo_precedente > nuovo_saldo:
                            # Calcola la differenza
                            differenza_saldo = saldo_precedente - nuovo_saldo

                            # Aggiungi una spesa al file "spese.csv"
                            file_path_spese = 'assets/spese.csv'
                            with open(file_path_spese, 'a', newline='', encoding='latin1') as spese_file:
                                spese_writer = csv.writer(spese_file)
                                spese_writer.writerow([differenza_saldo, datetime.now().strftime("%Y-%m-%d"), nuovo_nome, "ModificaConto"])
                        elif saldo_precedente < nuovo_saldo:
                            # Calcola la differenza
                            differenza_saldo = nuovo_saldo - saldo_precedente

                            # Aggiungi un'entrata al file "entrate.csv"
                            file_path_entrate = 'assets/entrate.csv'
                            with open(file_path_entrate, 'a', newline='', encoding='latin1') as entrate_file:
                                entrate_writer = csv.writer(entrate_file)
                                entrate_writer.writerow([differenza_saldo, datetime.now().strftime("%Y-%m-%d"), nuovo_nome])

                    # Alla fine chiudo la finestra
                    close_dlg_modifica(e)

                    # Resetto l'alert dialog
                    modifica_dialog.actions[0].value = ""
                    modifica_dialog.actions[1].value = ""
                    modifica_dialog.actions[2].value = ""
              
            def elimina_conto(e):
                conto_da_eliminare = str(elimina_dialog.actions[0].value).lower()

                # Leggi i conti dal file
                file_path_conti = 'assets/conti.csv'
                lista_conti = leggi_conti(file_path_conti)

                # Cerca il conto da eliminare
                conto_da_eliminare_saldo = None
                for i, (nome_conto, saldo) in enumerate(lista_conti):
                    if nome_conto.lower() == conto_da_eliminare:
                        conto_da_eliminare_saldo = float(saldo)
                        del lista_conti[i]  # Elimina la tupla dalla lista
                        break

                if conto_da_eliminare_saldo is not None:
                    # Modifica il saldo nel file "conti.csv"
                    with open(file_path_conti, 'w', newline='', encoding='latin1') as conti_file:
                        conti_writer = csv.writer(conti_file)
                        for nome_conto, saldo in lista_conti:
                            conti_writer.writerow([nome_conto, datetime.now().strftime("%Y-%m-%d"), saldo])

                    # Aggiungi una spesa al file "spese.csv"
                    file_path_spese = 'assets/spese.csv'
                    with open(file_path_spese, 'a', newline='', encoding='latin1') as spese_file:
                        spese_writer = csv.writer(spese_file)
                        spese_writer.writerow([conto_da_eliminare_saldo, datetime.now().strftime("%Y-%m-%d"), conto_da_eliminare, "contoEliminato"])

                # Alla fine chiudo la finestra
                close_dlg_elimina(e)

                # Resetto l'alert dialog
                elimina_dialog.actions[0].value = ""


 
            # PAGINA CONTI  
            conti = leggi_conti('assets/conti.csv')
            page.add(ft.Container(content=ft.Text("Gestione Conti",weight="bold",size=30,font_family="Arial"),alignment=ft.alignment.bottom_center))
            page.add(ft.Text("In questa pagina puoi modificare o eliminare i tuoi conti",size=20,font_family="Arial"))
            col = ft.Column(controls=colonna(conti))
            colonna1=ft.Column([
                
                ft.Container(
                    content=ft.Text("Ecco i tuoi conti",size=25,font_family="serif"),alignment=ft.alignment.center_left,padding=7),
                ft.Card(
                    content=ft.Container(
                    content=col,width=250,padding=7,border_radius=5,margin=5)),
                ft.Text("Operazioni disponibili sui conti: ",size=20),
                ft.Container(content=ft.Row([ft.FilledButton(text="Modifica",on_click=open_modifica_dialog,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.ORANGE_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )),
                        ft.FilledButton(text="Elimina",on_click=open_elimina_dialog,style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.RED_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        ))]),alignment=ft.alignment.center,margin=10,border_radius=7)
                ])
            
            nomi_conti=[tupla[0] for tupla in conti]
            conto_dropdown=ft.Dropdown(width=150,alignment=ft.alignment.center)
            for nome in nomi_conti:
                
                conto_dropdown.options.append(ft.dropdown.Option(nome))
                
            
            

            modifica_dialog=ft.AlertDialog(
                modal=True,
                title=ft.Text("Modifica Conto"),
                actions=[
                    conto_dropdown,
                    ft.TextField(label="Cambia il nome del conto"),
                    ft.TextField(label="Cambia Saldo"),
                    ft.TextButton("Conferma",on_click=modifica_conto),
                    ft.TextButton("Esci",on_click=close_dlg_modifica)
                ], actions_alignment=ft.MainAxisAlignment.END,
                )

            elimina_dialog=ft.AlertDialog(
                modal=True,
                title=ft.Text("Elimina Conto"),
                actions=[
                    conto_dropdown,
                    ft.Text("ATTENZIONE L'ELIMINAZIONE E' DEFINITIVA",weight="bold",color="red"),
                    ft.TextButton("Conferma",on_click=elimina_conto),
                    ft.TextButton("Esci",on_click=close_dlg_elimina)
                ], actions_alignment=ft.MainAxisAlignment.END,
                )

        #chiude l'alert dialog spesa
        

            page.add(colonna1)
            page.update()

    #schermata impostazioni (completa)
    def impostazioni_page():
        page.clean()  


        def azzera_spesa_totale(e):
            with open('assets/spese.csv', 'w', newline='') as file:
                pass
            close_dlg_azzera(e)

        def formatta_applicazione(e):
            with open('assets/spese.csv', 'w', newline='') as file:
                pass
            with open('assets/entrate.csv', 'w', newline='') as file:
                pass
            with open('assets/conti.csv', 'w', newline='') as file:
                pass
            with open('assets/budget_rimanente.csv', 'w', newline='') as file:
                pass
            close_dlg_formatta(e)

        def open_conferma_azzeramento(e):
            page.dialog = elimina_dialog
            elimina_dialog.open = True
            page.update()

        def close_dlg_azzera(e):
                elimina_dialog.open = False
                page.update()

        def open_conferma_fromatta(e):
            page.dialog= formatta_dialog
            formatta_dialog.open = True
            page.update()

        def close_dlg_formatta(e):
                formatta_dialog.open = False
                page.update()

        elimina_dialog=ft.AlertDialog(
                modal=True,
                title=ft.Text("AZZERA SPESE"),
                actions=[
                    ft.Text("ATTENZIONE L'ELIMINAZIONE E' IRREVERSIBILE",weight="bold",color="red"),
                    ft.TextButton("Conferma",on_click=azzera_spesa_totale),
                    ft.TextButton("Esci",on_click=close_dlg_azzera)
                ], actions_alignment=ft.MainAxisAlignment.END,
                )
        formatta_dialog=ft.AlertDialog(
                modal=True,
                title=ft.Text("FORMATTA APPLICAZIONE"),
                actions=[
                    
                    ft.Text("ATTENZIONE L'ELIMINAZIONE E' IRREVERSIBILE",weight="bold",color="red"),
                    ft.TextButton("Conferma",on_click=formatta_applicazione),
                    ft.TextButton("Esci",on_click=close_dlg_formatta)
                ], actions_alignment=ft.MainAxisAlignment.END,
                )

        page.add(ft.Container(content=ft.Text("Impostazioni",weight="bold",size=30,font_family="Arial"),alignment=ft.alignment.bottom_center))
        page.add(ft.Text("In questa pagina puoi gestire le impostazioni dell'applicazione.",size=20,font_family="Arial"))
        page.add(ft.Container(content=ft.Text("ATTENZIONE, TUTTE LE MODIFICHE FATTE SONO IRREVERSIBILI. ",weight="bold",size=20,color=ft.colors.RED,font_family="Arial"),alignment=ft.alignment.bottom_center,padding=7))
        page.add(ft.Text("Clicca il pulsante sottostante per azzerare tutte le spese.",size=20))
        #inizio bottone azzera spese
        page.add(ft.FilledButton(text="Azzera Spese",on_click=open_conferma_azzeramento,
                        style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.RED_ACCENT_700,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )))
        #fine bottone azzera spese        
        
        page.add(ft.Text("Clicca il pulsante sottostante per azzerare tutta l'applicazione: spese, entrate, conti, budget totale.",size=20))
        page.add(ft.FilledButton(text="Azzera Applicazione",on_click=open_conferma_fromatta,
                        style=ButtonStyle(
                                        color={
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                                                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK,},
                                        bgcolor=ft.colors.RED_900,
                                        elevation={"pressed": 0, "": 1},
                                        animation_duration=500,
                                        shape={
                                            ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),},
                        )))
        
        testo=ft.Text("""Grazie per aver scaricato la mia applicazione FinanzApp! \nSe riscontri problemi di qualsiasi tipo oppure hai delle migliorie da proporre contattami senza problemi! \nCONTATTI: \n- alessandro.gautieri@gmail.com \n- github.com/alegau03
                      """)
        containerTesto=ft.Container(content=testo,alignment=ft.alignment.bottom_left,margin=10,padding=10)
       # page.add(containerTesto)

    ######## RENDER ALLE PAGINE ############
    def render_page():
        if AppState.current_page == "home":
            home_page()
        elif AppState.current_page == "altro":
            altro_page()
        elif AppState.current_page=="conti":
            conti_page()
        elif AppState.current_page=="impostazioni":
            impostazioni_page()
    
    # INSTESTAZIONE CON PULSANTI
    page.appbar = ft.AppBar(
        
        title=ft.Text("FinanzApp", color=ft.colors.ORANGE_ACCENT_700, size=25, weight=ft.FontWeight.W_900,font_family="Arial"),
        center_title=True,
        bgcolor='#394145',
        actions=[
            ft.IconButton(icon="brightness_4", on_click=toggle_theme),
            ft.IconButton(icon="home", on_click=lambda e: navigate_to("home")),
            ft.IconButton(icon="SHOW_CHART", on_click=lambda e: navigate_to("altro")),
            ft.IconButton(icon="MANAGE_ACCOUNTS",on_click= lambda e: navigate_to("conti")),
            ft.IconButton(icon="SETTINGS",on_click= lambda e: navigate_to("impostazioni"))
        ])
    
    
  

    # Inizializza la pagina alla home
    render_page()

ft.app(target=main)