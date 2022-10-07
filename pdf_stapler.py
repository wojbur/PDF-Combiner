from email.charset import add_alias
from importlib.resources import path
import tkinter as tk
import tkinter.filedialog as fd
import PyPDF2
from pathlib import Path

window = tk.Tk()
window.iconbitmap(Path('Icons', 'stapler.ico'))
window.title('PDF Stapler')
window.resizable(0, 0)

class PdfStapler:
    def __init__(self, main):
        self.file_list = []

        self.frame1 = tk.Frame(main, width=80, borderwidth=5)
        self.frame2 = tk.Frame(main, width=80, borderwidth=5)
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)

        self.add_button_image = tk.PhotoImage(file=Path('Icons', 'browse.png'))
        self.add_files_button = tk.Button(self.frame2, image=self.add_button_image, command=self.add_files, width=25, height=25, borderwidth=2)
        self.add_files_button.grid(row=0, column=0, padx=2, pady=2)

        self.remove_button_image = tk.PhotoImage(file=Path('Icons', 'remove.png'))
        self.remove_file_button = tk.Button(self.frame2, image=self.remove_button_image, command=self.remove_file, width=25, height=25, borderwidth=2)
        self.remove_file_button.grid(row=1, column=0, padx=2, pady=2)

        self.up_button_image = tk.PhotoImage(file=Path('Icons', 'up.png'))
        self.up_button = tk.Button(self.frame2, image=self.up_button_image, command=self.move_up, width=25, height=25, borderwidth=2)
        self.up_button.grid(row=2, column=0, padx=2, pady=2)

        self.down_button_image = tk.PhotoImage(file=Path('Icons', 'down.png'))
        self.down_button = tk.Button(self.frame2, image=self.down_button_image, command=self.move_down, width=25, height=25, borderwidth=2)
        self.down_button.grid(row=3, column=0, padx=2, pady=2)

        self.save_button_image = tk.PhotoImage(file=Path('Icons', 'save.png'))
        self.save_button = tk.Button(self.frame2, image=self.save_button_image, command=self.staple_save, width=25, height=25, borderwidth=2)
        self.save_button.grid(row=4, column=0, padx=2, pady=2)

        self.files_listbox = tk.Listbox(self.frame1, width=40, height=20, selectmode=tk.SINGLE)
        self.files_listbox.grid(row=0, column=1)

        self.scrollbar = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.scrollbar.grid(row=0, column=0, sticky=tk.NS)

        self.files_listbox.config(yscrollcommand=self.scrollbar)

    def add_files(self):
        root = tk.Tk()
        root.withdraw()
        self.selected_files = fd.askopenfilenames(parent=root, title='select files', filetypes=[('PDF', '.pdf')])
        root.destroy()
        for filepath in self.selected_files:
            self.file_list.append((filepath, Path(filepath).name))
        # self.file_list = [(filepath, Path(filepath).name) for filepath in self.selected_files]
        self.populate_listbox(self.files_listbox, self.file_list)
    
    def remove_file(self):
        if self.files_listbox.curselection():
            pos = self.files_listbox.curselection()[0]
            self.file_list.pop(pos)
            self.files_listbox.delete(pos)
            self.files_listbox.selection_set(pos)
    
    def move_up(self):
        if self.files_listbox.curselection():
            pos = self.files_listbox.curselection()[0]
            if pos == 0:
                return
            text = self.files_listbox.get(pos)
            self.files_listbox.delete(pos)
            self.files_listbox.insert(pos-1, text)
            self.file_list.insert(pos-1, self.file_list.pop(pos))
            self.files_listbox.selection_set(pos-1)

    def move_down(self):
        if self.files_listbox.curselection():
            pos = self.files_listbox.curselection()[0]
            if pos+1 >= len(self.file_list):
                return
            text = self.files_listbox.get(pos)
            self.files_listbox.delete(pos)
            self.files_listbox.insert(pos+1, text)
            self.file_list.insert(pos+1, self.file_list.pop(pos))
            self.files_listbox.selection_set(pos+1)
    
    def get_save_dir(self):
        root = tk.Tk()
        root.withdraw()
        output_dir = fd.asksaveasfilename(defaultextension=".pdf", filetypes=[('PDF', '.pdf')])
        root.destroy()
        return output_dir
    
    def staple_save(self):
        if len(self.file_list) == 0:
            return
        output_dir = self.get_save_dir()
        merger = PyPDF2.PdfFileMerger()
        for file in self.file_list:
            merger.append(file[0])
        merger.write(output_dir)
        
    
    def populate_listbox(self, lstbox, files):
        self.files_listbox.delete(0, tk.END)
        for file in files:
            lstbox.insert(tk.END, file[1])

stapler = PdfStapler(window)
window.mainloop()