import tkinter as tk
from tkinter import ttk, Button, messagebox, filedialog
import pandas as pd
from PIL import ImageTk, Image
from ttkthemes import ThemedTk
import pathlib
from Main.massops import imo_query, imolist_query
from threading import *
from tkinter.font import BOLD, Font
from pandasgui import show
from Main.analysis import metrics
#from Main.analysis import metrics
#import time as t
#import shutil
#from functools import partial


class TkGui:
    def __init__(self):
        self.master = ThemedTk(themebg=True)
        # self.master.overrideredirect(True)
        self.master.set_theme('equilux')
        self.style = ttk.Style(self.master)
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.wdpath = pathlib.Path().absolute()
        self.configpath = self.wdpath / 'config'
        self.app_image = ImageTk.PhotoImage(Image.open(self.configpath / 'oceanica-negative.png').resize((345, 228)))

        # title_bar = Frame(self.master, bg='grey', relief='raised', bd=0)
        # title_bar.pack(expand=1, fill=X)
        # title_bar.bind("<B1-Motion>", self.move_app)

        # title_label = Label(title_bar, text="MY APP!", bg="grey", fg="white")
        # title_label.pack(side=LEFT)
        # self.tabsystem = ttk.Notebook(self.master, padding=30)
        # self.imotab = Frame(self.tabsystem)
        # self.fleetstab = Frame(self.tabsystem)
        # self.analysistab = Frame(self.tabsystem)

    # ------- CONFIGURATION FUNCTIONS ---------------
    def move_app(self, e):
        self.master.geometry(f'+{e.x_root}+{e.y_root}')

    def create_tabs(self):
        # Create tabs to navigate in frontend
        self.tabsystem = ttk.Notebook(self.master, style='lefttab.TNotebook', padding=30)

        # ---- MAIN TAB
        self.maintab = tk.Frame(self.tabsystem, pady=20, padx=20)
        self.tabsystem.add(self.maintab, text='INÍCIO')
        self.maintab.columnconfigure(0, weight=1)
        self.maintab.columnconfigure(1, weight=6)
        self.maintab.columnconfigure(2, weight=1)

        # ---- IMO TAB
        self.imotab = tk.Frame(self.tabsystem, pady=20, padx=20)
        self.tabsystem.add(self.imotab, text='IMO')
        self.imotab.columnconfigure(0, weight=2)
        self.imotab.columnconfigure(1, weight=8)
        self.imotab.columnconfigure(2, weight=1)

        # ---- FLEETS TAB
        self.fleetstab = tk.Frame(self.tabsystem, pady=20, padx=20)
        self.tabsystem.add(self.fleetstab, text='FROTAS')

        # tab_2_label = tk.Label(self.fleetstab, image=self.app_image).grid(row=0,
        #
        #                                          column=self.grid_column_main)

        # ---- ANALYSIS TAB
        self.analysistab = tk.Frame(self.tabsystem, pady=20, padx=20)
        self.tabsystem.add(self.analysistab, text='RESUMO')
        # tab_3_label = tk.Label(self.analysistab, image=self.app_image).grid(row=0,
        #                                                                    column=self.grid_column_main)

        self.tabsystem.pack(expand=1, fill="both")

    def properties_definition(self):
        # App resolution fixed
        self.master.geometry("1080x720")
        self.master.title('TRÁFEGO MARINHO NA COSTA BRASILEIRA')
        self.master.iconbitmap(self.configpath / 'imotab.ico')
        self.grid_column_main = 1
        self.grid_row_main = 1

        # Font Style
        self.bold14 = Font(self.master, size=14, weight=BOLD)

    def create_menu(self):
        # Create Menu
        menubar = tk.Menu(self.master, background='black', fg='white')

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=lambda: self.greet('new'))
        filemenu.add_command(label="Save as...", command=self.greet)
        filemenu.add_command(label="Close", command=self.greet)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.greet)
        helpmenu.add_command(label="About...", command=self.greet)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)

    def add_buttons(self):

        button_search_ttc = Button(self.maintab, text='READ ME',
                                   command=self.action_search_imo)

        button_search_ttc.grid(row=5, column=1,
                               padx=1, pady=1)

        button_search_ppt = Button(self.maintab, text='SOBRE',
                                   command=self.action_search_imo)

        button_search_ppt.grid(row=6, column=1,
                               padx=1, pady=1)

        button_search_imo = Button(self.imotab, text='PROCURAR',
                                   command=self.action_search_imo)

        button_search_imo.grid(row=3,
                               column=self.grid_column_main,
                               padx=10, pady=15)


        button_search_fleets = Button(self.fleetstab, text='PROCURAR',
                                      command=self.action_search_fleet)

        button_search_fleets.grid(row=13, column=4,
                                  padx=10, pady=10)


        button_display_data = Button(self.analysistab, text='ANALISAR',
                                      command=self.action_display_dataframe_gui)

        button_display_data.grid(row=13, column=4,
                                  padx=10, pady=10)

    def add_inputs(self):
        # Create input fields to search IMO numbers etc

        # ------------ IMO TAB
        self.input_field_imo = tk.Entry(self.imotab)
        self.input_field_imo.grid(row=2,
                                  column=1,
                                  padx=10, pady=1)



        # ------------ FLEETS TAB
        # self.input_field_fleetname1 = tk.Entry(self.fleetstab)
        # self.input_field_fleetname1.grid(row=2, column=0,
        #                                 padx=1, pady=1)

        # self.input_field_fleetimo1 = tk.Entry(self.fleetstab)
        # self.input_field_fleetimo1.grid(row=2, column=2,
        #                                columnspan=2,
        #                                padx=1, pady=1)

        self.my_entry_names = []
        self.my_entry_imos = []

        for y in range(2, 12):
            name_entry = tk.Entry(self.fleetstab, width=20)
            name_entry.grid(row=y, column=1, padx=10, pady=10)
            self.my_entry_names.append(name_entry)

            fleets_entry = tk.Entry(self.fleetstab, width=50)
            fleets_entry.grid(row=y, column=4, padx=10, pady=10)
            self.my_entry_imos.append(fleets_entry)

        # ------------ ANALYSIS TAB

    def add_texts_images(self):

        # self.master.title("ANÁLISE DO TRÁFEGO MARINHO NA COSTA BRASILEIRA")

        self.label = tk.Label(self.master,
                              text="  TRANSPORTE MARÍTIMO")

        # --------------- MAIN TAB

        tab_0_image = tk.Label(self.maintab, image=self.app_image).grid(row=0,
                                                                        column=self.grid_column_main,
                                                                        padx=10, pady=60)

        tab_0_text = tk.Label(self.maintab,
                              text='ANÁLISE DO TRANSPORTE MARÍTIMO',
                              font=self.bold14).grid(row=1, column=self.grid_column_main,
                                                     padx=10, pady=0)

        # --------------- IMO TAB

        tab_1_image = tk.Label(self.imotab, image=self.app_image).grid(row=0,
                                                                       column=self.grid_column_main,
                                                                       padx=10, pady=60)

        tab_1_text = tk.Label(self.imotab, text='INSIRA O NÚMERO IMO').grid(row=1,
                                                                            column=self.grid_column_main,
                                                                            padx=10, pady=0)

        # --------------- Fleets Tab

        # tab_1_image = tk.Label(self.fleetstab, image=self.app_image).grid(row=0,
        #                                                               column=self.grid_column_main,
        #                                                               padx=10, pady=60)

        tab_2_text = tk.Label(self.fleetstab, text='NOME DA FROTA').grid(row=1, column=1,
                                                                         padx=100, pady=30)

        tab_3_text = tk.Label(self.fleetstab, text='NÚMEROS IMO').grid(row=1, column=4,
                                                                       padx=100, pady=30)

        # --------------- Analysis tab
        tab_1_text = tk.Label(self.analysistab, text='INSIRA O NÚMERO IMO').grid(row=1,
                                                                                 column=self.grid_column_main,
                                                                                 padx=10, pady=0)

        self.label.pack()

    # ------- METHODS AND FUNCTIONS ----------------
    def action_search_imo(self):

        user_value = self.input_field_imo.get()
        print('debug1')
        #try:
        user_int_value = int(user_value)
        print('debug2', isinstance(user_int_value, int), len(list(user_value)))
        if (isinstance(user_int_value, int) and (len(list(user_value)) >= 7)):
            tk.messagebox.showinfo('Processado iniciado',
                                   f'Por favor aguarde, as informações do navio {user_value} serão consultadas')
            print('USER VALUE', user_value)
            imo_query(user_int_value)
            tk.messagebox.showinfo('Consulta Finalizada',
                                   f'As informações do navio {user_value} foram obtidas')
        else:
            tk.messagebox.showinfo('Entrada inválida',
                                   'Erro - o código IMO deve conter apenas números e ter mais de 7 digitos')
        #except Exception as e:
        #    tk.messagebox.showinfo('Entrada inválida',
        #                           'Erro - o código IMO deve conter apenas números e ter mais de 7 digitos')

        self.input_field_imo.delete(0, 'end')

        # messagebox.askyesnocancel("Save file", "You have unsaved changes.\nDo you want to save before closing?")

        '''
        save = messagebox.askyesnocancel(
                "Save file",
                "You have unsaved changes.\nDo you want to save before closing?",
            )

            if save:
                self.save_file()
                if self.parent.title()[0] == "*":
                    self.wclose()
                else:
                    root.destroy()

            elif not save:
                root.destroy()
        else:
            root.destroy() 
        
        '''

    def action_search_fleet(self):

        self.result_my_entry_imos = []
        self.result_my_entry_names = []

        name_list = ''
        imo_list = ''

        for names, imos in zip(self.my_entry_names, self.my_entry_imos):
            name_list = name_list + str(names.get()) + ';'
            imo_list = imo_list + str(imos.get()) + ';'

        self.result_my_entry_names = [ele for ele in name_list.split(';') if ele.strip()]
        self.result_my_entry_imos = [ele for ele in imo_list.split(';') if ele.strip()]

        print(self.result_my_entry_names)
        print(self.result_my_entry_imos)

        print('debug1')

        user_values_list = [aimo.split(',') for aimo in self.result_my_entry_imos]

        fleets_lists = zip(user_values_list, self.result_my_entry_names)
        status_list = []
        for fleet, fleet_name in fleets_lists:
            for imo in fleet:
                print('checking', imo, 'from', fleet_name)
                try:
                    check = isinstance(int(imo), int)
                    if check:
                        print(check, imo)
                        status_list.append(True)
                except:
                    tk.messagebox.showinfo('Entrada inválida',
                                           f'Erro - o código IMO {imo} da frota {fleet_name} deve conter apenas números.')
                    print('try again',  imo)
                    status_list.append(False)

            print('all checks done', status_list)

        if all(status_list):
            print('ok  ok, starting query for')
            for fleet_number in range(len(self.result_my_entry_imos)):
                list_of_imos = self.result_my_entry_imos[fleet_number]
                fleet_name = self.result_my_entry_names[fleet_number]
                print(fleet_number, list_of_imos, fleet_name)
                imolist_query(nimo=fleet_number, name=fleet_name, amode='oil')   #NEED TO INPUT THE AMODE MODE VAR!!!

                # imolist_query(fleet)

        else:
            print('again')

        print('done')
        #self.input_field_imo.delete(0, 'end')

    def action_display_dataframe_gui(self):
        print('starting data analysis')

        csv_path = filedialog.askopenfilename(initialdir="./",
                                              title="Select a File",
                                              filetypes=(("Tabular files",
                                                          "*.csv*"),
                                                         ("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        print(csv_path)

        # df_cargas  = pd.DataFrame()

        try:
            df_viagens = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        except:
            df_viagens = pd.read_csv(csv_path, sep=';', encoding='latin-1')


        show(df_viagens)

    def greet(self, message):
        print(message)

    def threading(self, work):
        # Call work function
        t1 = Thread(target=work)
        t1.start()

    # ------- MAIN APP STARTUP ---------------------
    def launch_app(self):
        self.properties_definition()
        self.create_menu()
        self.create_tabs()
        self.add_texts_images()
        self.add_inputs()
        self.add_buttons()
        self.master.mainloop()


if __name__ == "__main__":
    # metrics.create_analysis_teu()
    tk_app = TkGui()
    tk_app.launch_app()
