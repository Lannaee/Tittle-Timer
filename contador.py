import tkinter as tk
from tkinter import ttk
import keyboard
import os
import sys

class Opcion:
    def __init__(self, nombre, tiempo, img_normal, img_opaco, tecla):
        self.nombre = nombre
        self.tiempo_max = tiempo
        self.tiempo_actual = tiempo
        self.activo = False
        self.tecla = tecla
        self.img_normal_path = img_normal
        self.img_opaco_path = img_opaco
        self.tk_imagen_normal = None
        self.tk_imagen_opaco = None

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de títulos Elsword")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # Ruta base para PyInstaller
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # --- Icono Tkinter ---
        icono_tk_path = os.path.join(self.base_path, "iconotk.ico")
        self.root.iconbitmap(icono_tk_path)

        # --- Fondo ---
        self.ruta_fondo = os.path.join(self.base_path, "Fondo1.png")
        self.fondo_img = None
        self.canvas = tk.Canvas(root, width=400, height=200, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        if os.path.exists(self.ruta_fondo):
            self.fondo_img = tk.PhotoImage(file=self.ruta_fondo)
            self.canvas.create_image(0,0, image=self.fondo_img, anchor="nw")
        else:
            print("No se encontró la imagen de fondo.")

        # --- Lista de títulos ---
        self.lista_titulos = [
            ("Protector elianod", 60, "Title_1470.png", "Title_1470_opaco.png"),
            ("Gruta", 30, "Title_1840.png", "Title_1840_opaco.png"),
            ("Flote", 25, "Title_2050.png", "Title_2050_opaco.png"),
            ("Bastión", 60, "Title_2160.png", "Title_2160_opaco.png"),
            ("Order", 30, "Title_2210.png", "Title_2210_opaco.png"),
            ("Concerto", 60, "title_2320.png", "title_2320_opaco.png"),
            ("Resurrección", 180, "Res.png", "Res_opaco.png"),
        ]

        # --- Teclas por slot ---
        teclas_slots = ["f1", "f2", "f3", "f4"]

        self.lista_opciones = [
            Opcion(*self.lista_titulos[i], teclas_slots[i]) for i in range(4)
        ]

        # --- GUI ---
        self.labels_nombre = []
        self.labels_imagen = []
        self.labels_tiempo = []

        for i in range(4):
            frame = tk.Frame(self.canvas, borderwidth=1, relief="groove", width=80)
            frame.place(x=5 + i*95, y=10, width=90, height=180)

            combo_nombre = ttk.Combobox(frame, values=[t[0] for t in self.lista_titulos],
                                        state="readonly", font=("Arial", 7, "bold"), width=10)
            combo_nombre.current(i)
            combo_nombre.pack(pady=1)
            combo_nombre.bind("<<ComboboxSelected>>", lambda e, col=i: self.cambiar_opcion_combo(col))

            lbl_imagen = tk.Label(frame)
            lbl_imagen.pack(pady=1)
            self.labels_imagen.append(lbl_imagen)
            self.mostrar_imagen(i, tamaño=(35,35))

            lbl_tiempo = tk.Label(frame, text=f"{self.lista_opciones[i].tiempo_max}s", font=("Arial", 8))
            lbl_tiempo.pack(pady=1)

            lbl_tecla = tk.Label(frame, text=f"[{self.lista_opciones[i].tecla.upper()}]", font=("Arial", 7, "italic"))
            lbl_tecla.pack(pady=1)

            self.labels_nombre.append(combo_nombre)
            self.labels_tiempo.append(lbl_tiempo)

            self.tick(i)

        # Hook teclado
        keyboard.hook(self.on_key_event)

    def on_key_event(self, event):
        if event.event_type == "down":
            for op in self.lista_opciones:
                if event.name == op.tecla:
                    op.tiempo_actual = op.tiempo_max
                    op.activo = True

    def mostrar_imagen(self, col, tamaño=(35,35)):
        op = self.lista_opciones[col]
        try:
            if op.tk_imagen_normal is None:
                img = tk.PhotoImage(file=os.path.join(self.base_path, op.img_normal_path)).subsample(max(1, int(64/tamaño[0])))
                op.tk_imagen_normal = img
            if op.tk_imagen_opaco is None:
                img = tk.PhotoImage(file=os.path.join(self.base_path, op.img_opaco_path)).subsample(max(1, int(64/tamaño[0])))
                op.tk_imagen_opaco = img

            if op.activo and op.tiempo_actual > 0:
                self.labels_imagen[col].config(image=op.tk_imagen_opaco)
            else:
                self.labels_imagen[col].config(image=op.tk_imagen_normal)
        except:
            self.labels_imagen[col].config(text="[IMAGEN]", image="")

    def cambiar_opcion_combo(self, col):
        nombre = self.labels_nombre[col].get()
        tecla_slot = self.lista_opciones[col].tecla
        for t in self.lista_titulos:
            if t[0] == nombre:
                self.lista_opciones[col] = Opcion(*t, tecla_slot)
                break
        op = self.lista_opciones[col]
        op.tiempo_actual = op.tiempo_max
        op.activo = False
        self.labels_tiempo[col].config(text=f"{op.tiempo_actual}s")
        self.mostrar_imagen(col)

    def tick(self, col):
        op = self.lista_opciones[col]
        if op.activo and op.tiempo_actual > 0:
            op.tiempo_actual -= 1
        self.labels_tiempo[col].config(text=f"{op.tiempo_actual}s")
        self.mostrar_imagen(col)
        self.root.after(1000, lambda: self.tick(col))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
