import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk

import pyperclip

AMBIGUOUS = set("0OIl1")
history = []


def build_charset(upper, lower, digits, symbols, exclude_ambiguous):
    pools = []
    if upper:
        pools.append(string.ascii_uppercase)
    if lower:
        pools.append(string.ascii_lowercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(string.punctuation)

    if exclude_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in pools]

    return pools


def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Invalid length", "Password length must be a whole number.")
        return

    if length < 8:
        messagebox.showerror("Invalid length", "Minimum password length is 8.")
        return

    pools = build_charset(
        upper_var.get(), lower_var.get(), digit_var.get(),
        symbol_var.get(), ambiguous_var.get()
    )

    if len(pools) < 2:
        messagebox.showerror("Character types", "Select at least two character types.")
        return

    if length < len(pools):
        messagebox.showerror("Length", "Length must be at least the number of selected character types.")
        return

    # Guarantee one character from every selected type, then fill the rest securely.
    password_chars = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    password_chars.extend(secrets.choice(alphabet) for _ in range(length - len(password_chars)))

    # Secure shuffle using secrets.choice rather than random.shuffle.
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    password = "".join(password_chars)
    password_var.set(password)

    strength = get_strength(length, len(pools))
    strength_var.set(f"Strength: {strength}")

    try:
        pyperclip.copy(password)
        clipboard_var.set("Copied to clipboard")
    except Exception:
        clipboard_var.set("Clipboard unavailable")

    history.insert(0, password)
    del history[5:]
    history_box.delete(0, tk.END)
    for item in history:
        history_box.insert(tk.END, item)


def get_strength(length, types):
    score = 0
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if types >= 3:
        score += 1
    if types == 4:
        score += 1

    if score <= 1:
        return "Weak"
    if score <= 2:
        return "Medium"
    return "Strong"


def copy_password():
    password = password_var.get()
    if not password:
        messagebox.showinfo("Clipboard", "Generate a password first.")
        return
    try:
        pyperclip.copy(password)
        clipboard_var.set("Copied to clipboard")
    except Exception as exc:
        clipboard_var.set("Clipboard unavailable")
        messagebox.showerror("Clipboard error", str(exc))


root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("600x600")
root.resizable(False, False)

main = ttk.Frame(root, padding=25)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Secure Password Generator", font=("Arial", 20, "bold")).pack(pady=(0, 15))

length_var = tk.StringVar(value="16")
password_var = tk.StringVar()
strength_var = tk.StringVar(value="Strength: -")
clipboard_var = tk.StringVar()

row = ttk.Frame(main)
row.pack(fill="x", pady=8)
ttk.Label(row, text="Length", width=18).pack(side="left")
ttk.Spinbox(row, from_=8, to=128, textvariable=length_var, width=10).pack(side="left")

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
ambiguous_var = tk.BooleanVar(value=False)

for text, variable in (
    ("Uppercase", upper_var),
    ("Lowercase", lower_var),
    ("Numbers", digit_var),
    ("Symbols", symbol_var),
    ("Exclude ambiguous 0/O/l/1", ambiguous_var),
):
    ttk.Checkbutton(main, text=text, variable=variable).pack(anchor="w", pady=3)

ttk.Button(main, text="Generate Password", command=generate_password).pack(pady=15)

ttk.Entry(main, textvariable=password_var, font=("Consolas", 14), justify="center").pack(fill="x", pady=5)
ttk.Label(main, textvariable=strength_var, font=("Arial", 12, "bold")).pack(pady=5)
ttk.Button(main, text="Copy to Clipboard", command=copy_password).pack(pady=5)
ttk.Label(main, textvariable=clipboard_var).pack()

ttk.Label(main, text="Last 5 passwords in this session", font=("Arial", 11, "bold")).pack(pady=(20, 5))
history_box = tk.Listbox(main, height=7)
history_box.pack(fill="both", expand=True)

ttk.Label(
    main,
    text="Passwords are kept only in memory during this session and are not written to disk.",
    wraplength=520,
).pack(pady=12)

root.mainloop()
