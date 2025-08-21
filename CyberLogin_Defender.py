import tkinter as tk
from tkinter import messagebox
import random, time
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ----------------- User Database -----------------
users = {"admin": "1234", "user1": "abcd"}

# ----------------- Log Storage -----------------
login_attempts = []

# ----------------- Functions -----------------
def attempt_login():
    username = username_entry.get()
    password = password_entry.get()
    ip = f"192.168.1.{random.randint(2,254)}"
    success = users.get(username) == password

    login_attempts.append({
        "username": username,
        "ip": ip,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "success": success
    })

    if success:
        messagebox.showinfo("Login Status", f"Welcome {username}!")
    else:
        messagebox.showerror("Login Status", "Login failed!")

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def show_analysis():
    if not login_attempts:
        messagebox.showinfo("Analysis", "No login attempts yet.")
        return

    df = pd.DataFrame(login_attempts)

    # Detect suspicious IPs
    suspicious_ips = df[df['success']==False]['ip'].value_counts()
    suspicious_ips = suspicious_ips[suspicious_ips > 2]

    analysis_text = "Suspicious IPs:\n"
    if suspicious_ips.empty:
        analysis_text += "None detected"
    else:
        analysis_text += "\n".join(suspicious_ips.index)

    messagebox.showinfo("Analysis Summary", analysis_text)

    # Create a graph
    fig, ax = plt.subplots(figsize=(6,4))
    df['success_str'] = df['success'].map({True:'Success', False:'Failed'})
    df.groupby(['ip','success_str']).size().unstack(fill_value=0).plot(kind='bar', ax=ax)
    ax.set_title("Login Attempts by IP")
    ax.set_ylabel("Attempts")
    plt.tight_layout()

    # Embed graph in Tkinter
    graph_window = tk.Toplevel(root)
    graph_window.title("Login Attempt Graph")
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ----------------- GUI -----------------
root = tk.Tk()
root.title("CyberLogin Defender")
root.geometry("400x300")
root.configure(bg="#1e1e2f")  # dark background

title = tk.Label(root, text="CyberLogin Defender", font=("Arial", 18, "bold"), fg="#ffffff", bg="#1e1e2f")
title.pack(pady=10)

username_label = tk.Label(root, text="Username:", fg="#ffffff", bg="#1e1e2f")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:", fg="#ffffff", bg="#1e1e2f")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=attempt_login, bg="#4caf50", fg="#ffffff", width=15)
login_button.pack(pady=10)

analysis_button = tk.Button(root, text="Show Analysis", command=show_analysis, bg="#2196f3", fg="#ffffff", width=15)
analysis_button.pack()

root.mainloop()

