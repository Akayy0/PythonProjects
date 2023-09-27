import tkinter as tk
from tkinter import messagebox
import time
import threading

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro App")
        self.root.geometry("400x400")  # Definindo o tamanho inicial da janela

        self.root.option_add("*Font", "Poppins")  # Definindo a fonte Poppins para todos os elementos de texto

        # Variáveis para duração dos pomodoros e pausas
        self.pomodoro_duration = tk.StringVar()
        self.short_break_duration = tk.StringVar()
        self.long_break_duration = tk.StringVar()

        # Inicializa as variáveis com valores padrão
        self.pomodoro_duration.set("25")
        self.short_break_duration.set("5")
        self.long_break_duration.set("15")

        # Caixas de entrada com bordas arredondadas
        entry_style = {"borderwidth": 2, "relief": "groove", "font": ("Poppins", 12)}
        tk.Label(root, text="Duração Pomodoro (min):").pack()
        tk.Entry(root, textvariable=self.pomodoro_duration, **entry_style).pack()

        tk.Label(root, text="Duração Pausa Curta (min):").pack()
        tk.Entry(root, textvariable=self.short_break_duration, **entry_style).pack()

        tk.Label(root, text="Duração Pausa Longa (min):").pack()
        tk.Entry(root, textvariable=self.long_break_duration, **entry_style).pack()

        # Botões para iniciar, parar, resetar com bordas arredondadas e espaçamento
        button_style = {"borderwidth": 2, "relief": "groove", "font": ("Poppins", 12)}

        self.start_button = tk.Button(root, text="Iniciar Pomodoro", command=self.start_pomodoro, **button_style)
        self.stop_button = tk.Button(root, text="Parar", command=self.stop_pomodoro, state=tk.DISABLED, **button_style)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_pomodoro, state=tk.DISABLED, **button_style)
        self.completed_pomodoros = 0
        self.completed_pomodoros_label = tk.Label(root, text=f"Pomodoros Completos: {self.completed_pomodoros}", font=("Poppins", 12))
        self.completed_pomodoros_label.pack()

        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.reset_button.pack(pady=5)

        # Variáveis de controle do ciclo
        self.is_running = False
        self.remaining_time = 0
        self.current_duration = 0

        # Interface de relógio digital
        self.timer_label = tk.Label(root, text="", font=("Poppins", 48))
        self.timer_label.pack()

    def start_pomodoro(self):
        if not self.is_running:
            self.current_duration = int(self.pomodoro_duration.get()) * 60
            self.remaining_time = self.current_duration
            self.is_running = True
            self.update_timer()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
    
    def stop_pomodoro(self):
        if self.is_running:
            self.is_running = False
            self.root.after_cancel(self.timer_id)
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def reset_pomodoro(self):
        self.stop_pomodoro()
        self.remaining_time = 0
        self.root.title("Pomodoro App")
        self.timer_label.config(text="00:00")

    def update_timer(self):
        if self.is_running:
            minutes, seconds = divmod(self.remaining_time, 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            self.root.title(f"Pomodoro App - {timer_text}")
            self.timer_label.config(text=timer_text)
            
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.is_running = False
                self.root.title("Pomodoro App")
                self.timer_label.config(text="00:00")
                self.completed_pomodoros += 1
                self.completed_pomodoros_label.config(text=f"Pomodoros Completos: {self.completed_pomodoros}")
                self.show_notification()

    def show_notification(self):
        def flash():
            for _ in range(5):
                self.root.iconify()
                self.root.update()
                time.sleep(0.5)
                self.root.deiconify()
                self.root.update()
                time.sleep(0.5)

        notification_thread = threading.Thread(target=flash)
        notification_thread.start()
        messagebox.showinfo("Pomodoro Concluído", "Pomodoro concluído! Hora de uma pausa!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()