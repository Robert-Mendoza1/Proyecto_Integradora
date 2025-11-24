import tkinter as tk
from database import Database
from auth.login_view import LoginView
from auth.login_controller import LoginController

def run_app():
    root = tk.Tk()
    root.geometry('400x500')
    db = Database()  # edit database connection inside class if needed
    view = LoginView(root)
    controller = LoginController(view, db)
    root.mainloop()

if __name__ == '__main__':
    run_app()
