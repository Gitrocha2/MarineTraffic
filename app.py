from tkinter import Tk, Label, Button, Menu, ttk, Frame


class TkGui:
    def __init__(self):
        self.master = Tk()
        self.master.title("Análise do Tráfego Marinho na Costa Brasileira")

    def geometry_definition(self):
        # App resolution fixed
        self.master.geometry("800x600")

    def create_menu(self):
        # Create Menu
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.greet)
        filemenu.add_command(label="Open", command=self.greet)
        filemenu.add_command(label="Save", command=self.greet)
        filemenu.add_command(label="Save as...", command=self.greet)
        filemenu.add_command(label="Close", command=self.greet)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.greet)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.greet)
        editmenu.add_command(label="Copy", command=self.greet)
        editmenu.add_command(label="Paste", command=self.greet)
        editmenu.add_command(label="Delete", command=self.greet)
        editmenu.add_command(label="Select All", command=self.greet)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.greet)
        helpmenu.add_command(label="About...", command=self.greet)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=menubar)

    def add_tabs(self):
        # Create a tab control that manages multiple tabs
        tabsystem = ttk.Notebook(self.master, padding=30)

        # Create new tabs using Frame widget
        tab1 = Frame(tabsystem)
        tabsystem.add(tab1, text='IMO')

        tab2 = Frame(tabsystem)
        tabsystem.add(tab2, text='FROTAS')

        tab3 = Frame(tabsystem)
        tabsystem.add(tab3, text='ANÁLISE')

        tabsystem.pack(expand=1, fill="both")

    def add_buttons(self):
        print('oi')

    def add_texts(self):
        self.label = Label(self.master, text="TK GUI!")
        self.label.pack()
        print('oi')

    def greet(self):
        print("Greetings!")

    def launch_app(self):
        self.geometry_definition()
        self.create_menu()
        self.add_tabs()
        self.add_texts()
        self.add_buttons()
        self.master.mainloop()


if __name__ == "__main__":
    tk_app = TkGui()
    tk_app.launch_app()
