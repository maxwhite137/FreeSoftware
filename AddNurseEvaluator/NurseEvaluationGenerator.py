######################################
#
#   Nurse Evaluation Generator
#
#   Created by: Max White, 10/24/2024
#
######################################

import openai
from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext, messagebox, StringVar
import pyperclip

# Set your OpenAI API key here
client = OpenAI(
    api_key = ''
)

# Function to generate evaluation using ChatGPT
def generate_evaluation():

    # Get input values from the GUI
    name = name_entry.get()
    role = role_var.get()
    rating = rating_entry.get()
    teammate_info = teammate_entry.get("1.0", tk.END).strip()
    patient_info = patient_entry.get("1.0", tk.END).strip()
    areas_of_growth_info = growth_entry.get("1.0", tk.END).strip()
    other_info = other_entry.get("1.0", tk.END).strip()

    # Define the prompt
    prompt = f"""
    I am writing an evaluation for a {role} named {name}. Here are some details:
    - Rating: {rating}/5
    - Teammate and coworker: {teammate_info}
    - Patient care: {patient_info}
    - Areas of Growth: {areas_of_growth_info}
    - Other characteristics: {other_info}
    
    Write a professional, 250-word evaluation with the following structure:
    1. A general summary paragraph.
    2. A paragraph on how well they work as a teammate and coworker.
    3. A paragraph on how well they take care of patients.
    4. A paragraph on their areas of growth.

    Some other things to note:
    * Do not refer to the person with their role name. This is just to give better context for the review
    """

    # Call OpenAI's ChatCompletion to generate the response
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",  # or use "gpt-4" if you have access gpt-4o-mini
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    # Get the evaluation text from the response
    evaluation = response.choices[0].message.content

    # Display the generated evaluation in the output box
    output_text.delete("1.0", tk.END)  # Clear previous output
    output_text.insert(tk.END, evaluation)

    # Update the word count for the output
    update_word_count()

# Function to copy output text to clipboard
def copy_to_clipboard():
    evaluation_text = output_text.get("1.0", tk.END).strip()
    pyperclip.copy(evaluation_text)
    messagebox.showinfo("Copied", "Evaluation copied to clipboard.")

# Function to save output text to a file named after the nurse
def save_to_file():
    nurse_name = name_entry.get().strip()
    evaluation_text = output_text.get("1.0", tk.END).strip()
    
    if not nurse_name:
        messagebox.showerror("Error", "Please enter a name to save the file.")
        return
    
    if evaluation_text:
        with open(f"{nurse_name}.txt", "w") as file:
            file.write(evaluation_text)
        messagebox.showinfo("Saved", f"Evaluation saved as {nurse_name}.txt")
    else:
        messagebox.showerror("Error", "No evaluation text to save.")

def clear_fields():
    name_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    role_var.set("Nurse")  # Reset role dropdown to default
    teammate_entry.delete("1.0", tk.END)
    patient_entry.delete("1.0", tk.END)
    growth_entry.delete("1.0", tk.END)
    other_entry.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)  # Clear the output box as well
    update_word_count() # Update the word count for generated response back to 0
    update_word_counts() # Update the word count of entries back to 0

def update_word_count():
    evaluation = output_text.get("1.0", tk.END).strip()
    word_count = len(evaluation.split()) if evaluation else 0
    word_count_label.config(text=f"Word Count: {word_count}")

# Function to update word counts for each input box
def update_word_counts():
    # Get the current text from each input box
    teammate_text = teammate_entry.get("1.0", tk.END).strip()
    patient_text = patient_entry.get("1.0", tk.END).strip()
    growth_text = growth_entry.get("1.0", tk.END).strip()
    other_text = other_entry.get("1.0", tk.END).strip()

    # Calculate the word counts
    teammate_count = len(teammate_text.split()) if teammate_text else 0
    patient_count = len(patient_text.split()) if patient_text else 0
    growth_count = len(growth_text.split()) if growth_text else 0
    other_count = len(other_text.split()) if other_text else 0

    # Update the labels with the counts
    teammate_count_label.config(text=f"Teammate Word Count: {teammate_count}")
    patient_count_label.config(text=f"Patient Word Count: {patient_count}")
    growth_count_label.config(text=f"Growth Word Count: {growth_count}")
    other_count_label.config(text=f"Other Word Count: {other_count}")

# Create the main window
window = tk.Tk()
window.title("Evaluation Generator")

# Name
name_label = tk.Label(window, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(window, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Role Dropdown
role_var = StringVar(window)
role_var.set("Nurse")  # Default role
role_label = tk.Label(window, text="Role:")
role_label.grid(row=1, column=0, padx=10, pady=5)
role_dropdown = tk.OptionMenu(window, role_var, "Nurse", "MA", "Tech")
role_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Rating
rating_label = tk.Label(window, text="Overall Rating (1-5):")
rating_label.grid(row=2, column=0, padx=10, pady=5)
rating_entry = tk.Entry(window, width=40)
rating_entry.grid(row=2, column=1, padx=10, pady=5)

# Teammate and Coworker Info
teammate_label = tk.Label(window, text="Teammate and Coworker Information:")
teammate_label.grid(row=3, column=0, padx=10, pady=5)
teammate_entry = scrolledtext.ScrolledText(window, width=40, height=4)
teammate_entry.grid(row=3, column=1, padx=10, pady=5)

# Patient Care Info
patient_label = tk.Label(window, text="Patient Care Information:")
patient_label.grid(row=4, column=0, padx=10, pady=5)
patient_entry = scrolledtext.ScrolledText(window, width=40, height=4)
patient_entry.grid(row=4, column=1, padx=10, pady=5)

# Areas of Growth Info
growth_entry = tk.Label(window, text="Areas of Growth:")
growth_entry.grid(row=5, column=0, padx=10, pady=5)
growth_entry = scrolledtext.ScrolledText(window, width=40, height=4)
growth_entry.grid(row=5, column=1, padx=10, pady=5)

# Other Characteristics
other_label = tk.Label(window, text="Other Characteristics:")
other_label.grid(row=6, column=0, padx=10, pady=5)
other_entry = scrolledtext.ScrolledText(window, width=40, height=4)
other_entry.grid(row=6, column=1, padx=10, pady=5)

# Button to generate evaluation
generate_button = tk.Button(window, text="Generate Evaluation", command=generate_evaluation)
generate_button.grid(row=7, column=0, columnspan=4, pady=10)

# Output box for the generated evaluation
output_label = tk.Label(window, text="Generated Evaluation:")
output_label.grid(row=8, column=0, padx=10, pady=5)
output_text = scrolledtext.ScrolledText(window, width=80, height=10, wrap="word")
output_text.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

# Word Count Label
word_count_label = tk.Label(window, text="Word Count: 0")
word_count_label.grid(row=8, column=2, columnspan=2, padx=10, pady=5)

# Button to copy output
copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=10, column=0, pady=10)

# Button to save output to file
save_button = tk.Button(window, text="Save to File", command=save_to_file)
save_button.grid(row=10, column=1, pady=10)

# Clear Fields Button
clear_button = tk.Button(window, text="Clear All Fields", command=clear_fields)
clear_button.grid(row=10, column=2, pady=10, padx=10)

# Word count for each text input box
# Teammate Word Count Label
teammate_count_label = tk.Label(window, text="Teammate Word Count: 0")
teammate_count_label.grid(row=3, column=2, padx=10, pady=5)

# Patient Word Count Label
patient_count_label = tk.Label(window, text="Patient Word Count: 0")
patient_count_label.grid(row=4, column=2, padx=10, pady=5)

# Growth Word Count Label
growth_count_label = tk.Label(window, text="Growth Word Count: 0")
growth_count_label.grid(row=5, column=2, padx=10, pady=5)

# Other Word Count Label
other_count_label = tk.Label(window, text="Other Word Count: 0")
other_count_label.grid(row=6, column=2, padx=10, pady=5)

# Bind the text change events
teammate_entry.bind("<KeyRelease>", lambda e: update_word_counts())
patient_entry.bind("<KeyRelease>", lambda e: update_word_counts())
growth_entry.bind("<KeyRelease>", lambda e: update_word_counts())
other_entry.bind("<KeyRelease>", lambda e: update_word_counts())

# Start the GUI loop
window.mainloop()