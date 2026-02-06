"""
============================================
PROJECT 2: PASSWORD GENERATOR & CHECKER
============================================
A Python GUI application that:
- Generates secure random passwords
- Checks password strength
- Copies password to clipboard
- Shows real-time strength feedback

HOW TO RUN:
1. Make sure you have Python installed (python.org)
2. Open terminal/command prompt
3. Navigate to this file's folder
4. Run: python password_generator.py

LIBRARIES NEEDED:
- tkinter (usually comes with Python)
- No additional installation needed!
============================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator & Checker")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#667eea"
        self.secondary_color = "#764ba2"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI elements"""
        
        # ========== TITLE ==========
        title_frame = tk.Frame(self.root, bg=self.primary_color)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🔐 Password Generator",
            font=("Arial", 24, "bold"),
            bg=self.primary_color,
            fg="white",
            pady=20
        )
        title_label.pack()
        
        # ========== MAIN CONTAINER ==========
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=30, pady=10)
        
        # ========== PASSWORD LENGTH ==========
        length_label = tk.Label(
            main_frame,
            text="Password Length:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color
        )
        length_label.grid(row=0, column=0, sticky="w", pady=10)
        
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(
            main_frame,
            from_=6,
            to=30,
            textvariable=self.length_var,
            font=("Arial", 12),
            width=10
        )
        self.length_spinbox.grid(row=0, column=1, sticky="w", pady=10, padx=10)
        
        # ========== OPTIONS CHECKBOXES ==========
        options_label = tk.Label(
            main_frame,
            text="Include:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color
        )
        options_label.grid(row=1, column=0, sticky="w", pady=10)
        
        # Checkboxes for character types
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            main_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var,
            font=("Arial", 10),
            bg=self.bg_color
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        
        tk.Checkbutton(
            main_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var,
            font=("Arial", 10),
            bg=self.bg_color
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
        
        tk.Checkbutton(
            main_frame,
            text="Digits (0-9)",
            variable=self.digits_var,
            font=("Arial", 10),
            bg=self.bg_color
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
        
        tk.Checkbutton(
            main_frame,
            text="Symbols (!@#$%^&*)",
            variable=self.symbols_var,
            font=("Arial", 10),
            bg=self.bg_color
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=2)
        
        # ========== GENERATE BUTTON ==========
        self.generate_btn = tk.Button(
            main_frame,
            text="🎲 Generate Password",
            font=("Arial", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            command=self.generate_password,
            cursor="hand2",
            relief="flat",
            pady=15
        )
        self.generate_btn.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")
        
        # ========== PASSWORD DISPLAY ==========
        self.password_text = tk.Text(
            main_frame,
            height=3,
            width=40,
            font=("Courier", 12),
            wrap="word",
            relief="solid",
            borderwidth=2
        )
        self.password_text.grid(row=7, column=0, columnspan=2, pady=10)
        
        # ========== COPY BUTTON ==========
        self.copy_btn = tk.Button(
            main_frame,
            text="📋 Copy to Clipboard",
            font=("Arial", 12),
            bg="#10b981",
            fg="white",
            command=self.copy_to_clipboard,
            cursor="hand2",
            relief="flat",
            pady=10
        )
        self.copy_btn.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")
        
        # ========== STRENGTH METER ==========
        strength_label = tk.Label(
            main_frame,
            text="Password Strength:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color
        )
        strength_label.grid(row=9, column=0, columnspan=2, pady=(20, 5))
        
        self.strength_bar = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate'
        )
        self.strength_bar.grid(row=10, column=0, columnspan=2, pady=5)
        
        self.strength_label = tk.Label(
            main_frame,
            text="Generate a password to check strength",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="gray"
        )
        self.strength_label.grid(row=11, column=0, columnspan=2, pady=5)
        
        # ========== CUSTOM PASSWORD CHECKER ==========
        separator = tk.Frame(main_frame, height=2, bg="gray")
        separator.grid(row=12, column=0, columnspan=2, pady=20, sticky="ew")
        
        check_label = tk.Label(
            main_frame,
            text="Check Your Own Password:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color
        )
        check_label.grid(row=13, column=0, columnspan=2, pady=10)
        
        self.check_entry = tk.Entry(
            main_frame,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        self.check_entry.grid(row=14, column=0, columnspan=2, pady=5)
        
        self.check_btn = tk.Button(
            main_frame,
            text="🔍 Check Strength",
            font=("Arial", 12),
            bg=self.secondary_color,
            fg="white",
            command=self.check_custom_password,
            cursor="hand2",
            relief="flat",
            pady=10
        )
        self.check_btn.grid(row=15, column=0, columnspan=2, pady=10, sticky="ew")
    
    def generate_password(self):
        """Generate a random password based on selected options"""
        
        # Get password length
        length = self.length_var.get()
        
        # Build character set based on checkboxes
        characters = ""
        
        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.lowercase_var.get():
            characters += string.ascii_lowercase
        if self.digits_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Check if at least one option is selected
        if not characters:
            messagebox.showwarning(
                "No Options Selected",
                "Please select at least one character type!"
            )
            return
        
        # Generate password
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # Display password
        self.password_text.delete(1.0, tk.END)
        self.password_text.insert(1.0, password)
        
        # Check and display strength
        self.check_password_strength(password)
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_text.get(1.0, tk.END).strip()
        
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first!")
    
    def check_password_strength(self, password):
        """Check the strength of a password"""
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            feedback.append("Consider using 12+ characters")
        else:
            score += 5
            feedback.append("Too short! Use at least 8 characters")
        
        # Uppercase check
        if re.search(r"[A-Z]", password):
            score += 20
        else:
            feedback.append("Add uppercase letters")
        
        # Lowercase check
        if re.search(r"[a-z]", password):
            score += 20
        else:
            feedback.append("Add lowercase letters")
        
        # Digit check
        if re.search(r"\d", password):
            score += 20
        else:
            feedback.append("Add numbers")
        
        # Symbol check
        if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
            score += 15
        else:
            feedback.append("Add symbols for extra security")
        
        # Update progress bar
        self.strength_bar['value'] = score
        
        # Update strength label
        if score >= 80:
            strength = "💪 Very Strong"
            color = "#10b981"
        elif score >= 60:
            strength = "😊 Strong"
            color = "#3b82f6"
        elif score >= 40:
            strength = "😐 Moderate"
            color = "#f59e0b"
        else:
            strength = "😟 Weak"
            color = "#ef4444"
        
        self.strength_label.config(text=strength, fg=color)
        
        # Show feedback if any
        if feedback:
            feedback_text = "Suggestions: " + ", ".join(feedback)
        else:
            feedback_text = "Excellent password! 🎉"
        
        return strength, feedback_text
    
    def check_custom_password(self):
        """Check strength of user's custom password"""
        password = self.check_entry.get()
        
        if not password:
            messagebox.showwarning("No Password", "Please enter a password to check!")
            return
        
        strength, feedback = self.check_password_strength(password)
        messagebox.showinfo("Password Strength", f"{strength}\n\n{feedback}")


# ========== MAIN PROGRAM ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
