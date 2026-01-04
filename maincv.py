import tkinter as tk
from deep_translator import GoogleTranslator
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from paddleocr import PaddleOCR
import pyperclip # For the Copy button

# --- English OCR Model Ko Pehle Hi Load Kar Lete Hain ---
print("Loading English OCR model... Please wait.")
# Model ab hamesha English hi rahega
ocr_model = PaddleOCR(lang='en') 
print("Model loaded successfully!")

# --- Global Variables ---
file_path = ""

# --- Functions ---

def select_image():
    """Lets the user select an image and shows a preview."""
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        pil_image = Image.open(file_path)
        pil_image.thumbnail((550, 500)) 
        tk_image = ImageTk.PhotoImage(pil_image)
        image_label.config(image=tk_image, text="")
        image_label.image = tk_image
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Image loaded. Click 'Extract Text' to perform OCR.")

def perform_ocr():
    """Performs OCR on the selected image."""
    if file_path:
        try:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Processing... Please wait.")
            window.update_idletasks()

            result = ocr_model.predict(file_path)
            
            extracted_lines = []
            
            if result and isinstance(result, list) and len(result) > 0:
                first_result_item = result[0] 
                if first_result_item and isinstance(first_result_item, dict) and 'rec_texts' in first_result_item:
                    extracted_lines = first_result_item['rec_texts']
            
            extracted_text = "\n".join(extracted_lines)
            
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, extracted_text if extracted_text else "No text found.")
        
        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"An error occurred: {e}")
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please select an image first.")

def translate_text():
    """Translates the text in the box to the selected language."""
    original_text = result_text.get("1.0", tk.END)
    target_language_name = selected_trans_lang.get()

    if not original_text.strip():
        return
        
    if not target_language_name:
        return

    translate_languages = {'Hindi': 'hi', 'Marathi': 'mr'}
    target_lang_code = translate_languages[target_language_name]

    try:
        translated_text = GoogleTranslator(source='en', target=target_lang_code).translate(original_text)
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", translated_text)
    except Exception as e:
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", f"Translation Error: {e}")

def save_text():
    """Saves the text to a .txt file."""
    text_to_save = result_text.get(1.0, tk.END)
    if text_to_save.strip():
        file_path_save = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path_save:
            with open(file_path_save, "w", encoding="utf-8") as file:
                file.write(text_to_save)

def copy_text():
    """Copies the text to the clipboard."""
    text_to_copy = result_text.get(1.0, tk.END)
    if text_to_copy.strip():
        pyperclip.copy(text_to_copy)

# --- GUI Setup ---
window = tk.Tk()
window.title("Image Text Translator") # Title bhi update kar diya
window.geometry("900x750")
window.config(bg="#f0f0f0")

main_frame = ttk.Frame(window, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

image_label = ttk.Label(main_frame, text="Please select an English image to view here", background="#ffffff", borderwidth=2, relief="solid", anchor="center")
image_label.pack(pady=10, fill="both", expand=True)

# === OCR Language selection wala frame HATA DIYA GAYA HAI ===

# Action buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=15)
select_btn = ttk.Button(button_frame, text="Select Image", command=select_image)
select_btn.pack(side=tk.LEFT, padx=15, ipady=5)
ocr_btn = ttk.Button(button_frame, text="Extract English Text", command=perform_ocr)
ocr_btn.pack(side=tk.LEFT, padx=15, ipady=5)
save_btn = ttk.Button(button_frame, text="Save Text", command=save_text)
save_btn.pack(side=tk.LEFT, padx=15, ipady=5)
copy_btn = ttk.Button(button_frame, text="Copy Text", command=copy_text)
copy_btn.pack(side=tk.LEFT, padx=15, ipady=5)

# Translation widgets
translate_frame = ttk.Frame(main_frame)
translate_frame.pack(pady=10)
translate_label = ttk.Label(translate_frame, text="Translate English Text to:")
translate_label.pack(side=tk.LEFT, padx=5)
translate_languages = {'Hindi': 'hi', 'Marathi': 'mr'}
selected_trans_lang = tk.StringVar()
trans_lang_combobox = ttk.Combobox(translate_frame, textvariable=selected_trans_lang, state="readonly")
trans_lang_combobox['values'] = list(translate_languages.keys())
trans_lang_combobox.current(0)
trans_lang_combobox.pack(side=tk.LEFT, padx=5)
translate_btn = ttk.Button(translate_frame, text="Translate", command=translate_text)
translate_btn.pack(side=tk.LEFT, padx=10, ipady=5)

# Result text box
result_text = tk.Text(main_frame, height=10, width=80, wrap=tk.WORD, font=("Segoe UI", 11), relief="solid", bd=2)
result_text.pack(pady=10, fill="both", expand=True)

# --- Start Application ---
window.mainloop()