import tkinter as tk
from tkinter import font
import re

def check_password_strength(password):
    length_score = min(10, len(password))  # Max score for length is 10
    uppercase_score = 2 if any(c.isupper() for c in password) else 0
    digit_score = 2 if any(c.isdigit() for c in password) else 0
    symbol_score = 2 if any(c in "!@#$%^&*()" for c in password) else 0
    consecutive_sequence_score = -5 if re.search(r'(?:012345|12345|23456|34567|45678|56789|98765|87654|76543|65432|54321|43210)', password.lower()) else 0
    
    total_score = length_score + uppercase_score + digit_score + symbol_score + consecutive_sequence_score
    
    if total_score >= 12:
        return "Very Strong"
    elif total_score >= 8:
        return "Strong"
    elif total_score >= 6:
        return "Moderate"
    elif total_score >= 4:
        return "Weak"
    else:
        return "Very Weak"

def get_password_suggestions(password):
    suggestions = []
    
    if len(password) < 6:
        suggestions.append("Use a longer password")
        
    if not any(c.isupper() for c in password):
        suggestions.append("Include at least one uppercase letter")
        
    if not any(c.isdigit() for c in password):
        suggestions.append("Include at least one digit")
        
    if not any(c in "!@#$%^&*()" for c in password):
        suggestions.append("Include at least one special character")
        
    # Check for consecutive sequences (e.g., 12345, abcde)
    if re.search(r'012345|12345|23456|34567|45678|56789|98765|87654|76543|65432|54321|43210', password.lower()):
        suggestions.append("Avoid consecutive sequences")
        
    return suggestions

def update_strength_bar(password):
    strength = check_password_strength(password)
    if strength == "Very Strong":
        fill_color = "green"
        width = 200  # Set width to 200 for very strong passwords
    elif strength == "Strong":
        fill_color = "green"
        width = 150  # Set width to 150 for strong passwords
    elif strength == "Moderate":
        fill_color = "orange"
        width = 100  # Set width to 100 for moderate passwords
    else:
        fill_color = "red"
        width = 50  # Set width to 50 for weak passwords
    
    strength_canvas.delete("all")  # Clear the canvas
    strength_canvas.create_rectangle(0, 0, width, 20, fill=fill_color, outline="")

    # Calculate the middle of the bar
    middle_x = 200 / 2
    
    # Draw the strength text in the middle
    strength_canvas.create_text(middle_x, 10, text=strength, fill="black", font=("Helvetica", 10, "bold"))

def update_result_label():
    password = password_entry.get()
    strength = check_password_strength(password)
    suggestions = get_password_suggestions(password)
    
    suggestions_text = "\n".join(suggestions)
    bold_font = font.Font(result_label, result_label.cget("font"))
    bold_font.configure(weight="bold")

    result_label.config(text=f"Password strength: {strength}\nSuggestions:\n{suggestions_text}", font=bold_font)

    update_strength_bar(password)

    # Show the canvas when the result is updated
    strength_canvas.pack(pady=8)

    result_label.pack(pady=8)

# Function to update the password entry visibility based on the checkbutton state
def update_password_visibility(*args):
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Function to apply styling on hover
def on_enter(e):
    check_button['background'] = "#3498db"
    check_button['font'] = ("Helvetica", 12, "bold")

def on_leave(e):
    check_button['background'] = "skyblue"
    check_button['font'] = ("Helvetica", 12)

# Create the main application window
app = tk.Tk()
app.title("Password Strength Checker")

# Set the width and height of the window (change these values as needed)
window_width = 500
window_height = 450
app.geometry(f"{window_width}x{window_height}")

# Customize the application's appearance
app.configure(bg="#cfe2f3")

# Create a StringVar to hold the password value
password_var = tk.StringVar()

# Create a BooleanVar to track whether the password should be visible
show_password_var = tk.BooleanVar()
show_password_var.set(False)  # Default to not showing the password

title_label = tk.Label(app, text="Password Strength Checker", font=("Helvetica",18, "bold"), background="#cfe2f3", fg="blue")
title_label.pack(pady=10)

password_label = tk.Label(app, text="Enter Password:", font=("Helvetica", 14), background="#cfe2f3")
password_label.pack(pady=10)

password_entry = tk.Entry(app, show="*", font=("Helvetica", 12), width=20, background="white", highlightcolor="blue")
password_entry.pack(pady=5)

# Create a Frame for the password entry and show password checkbutton
password_frame = tk.Frame(app)
password_frame.pack(pady=8)

# Create the show password checkbutton
show_password_checkbutton = tk.Checkbutton(password_frame, text="Show Password",font=("Helvetica",10), variable=show_password_var,background="#cfe2f3")
show_password_checkbutton.pack(side="left")

# Attach the function to the checkbutton's state change event
show_password_var.trace("w", update_password_visibility)

check_button = tk.Button(app, text="Check Strength", font=("Helvetica", 12), command=update_result_label,
                         relief=tk.FLAT, borderwidth=2, background="lightblue")
check_button.pack(pady=10)

# Create a Canvas widget to display the strength bar
strength_canvas = tk.Canvas(app, width=200, height=20, bg="#ffffff")
strength_canvas.pack()

# Initially hide the canvas
strength_canvas.pack_forget()

result_label = tk.Label(app, text="", font=("Helvetica", 12), bg="#f2f2f2")
result_label.pack(pady=10)

result_label.pack_forget()

# Binding the hover functions to the button
check_button.bind("<Enter>", on_enter)
check_button.bind("<Leave>", on_leave)

# Start the main event loop
app.mainloop()
