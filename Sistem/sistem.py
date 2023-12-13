import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

def dokumentasi():
    teks_bantuan = """
    Selamat datang di Sistem Evaluasi Kinerja Karyawan!

    Benefit:
    - Gaji: Mencerminkan gaji karyawan.
    - Masa Kerja: Mencerminkan pengalaman kerja karyawan.
    - Pencapaian: Mencerminkan pencapaian karyawan.

    Cost:
    - Usia: Mencerminkan usia karyawan.

    Cara Kerja Sistem:
    1. Masukkan bobot untuk setiap kriteria (jumlah bobot harus 1).
    2. Klik tombol 'Hitung' untuk mengevaluasi kinerja karyawan.
    3. Sistem menghitung nilai Simple Additive Weighting (SAW).
    4. Karyawan diurutkan berdasarkan nilai SAW yang dihitung.
    5. Peringkat dan informasi detail ditampilkan.

    Catatan: Pastikan file 'sistem.csv' tersedia dengan data yang diperlukan.
    
    Atribut kriteria terdiri dari benefit atau cost, dimana benefit artinya semakin besar nilainya semakin bagus, sedangkan cost semakin kecil nilainya semakin bagus.
    """

    messagebox.showinfo("Help", teks_bantuan)

def validate_weights(weights):
    total_weight = sum(weights)
    return total_weight == 1.0

def show_error_message(message):
    messagebox.showerror("Error", message)
    
def saw_normalization(matrix, criteria_weights, is_benefit_criteria):
    num_alternatives, num_criteria = matrix.shape
    normalized_matrix = np.zeros_like(matrix, dtype=float)

    for j in range(num_criteria):
        column = matrix[:, j]
        min_val = min(column)
        max_val = max(column)

        for i in range(num_alternatives):
            value = matrix[i, j]

            if is_benefit_criteria[j]:
                # Benefit criteria, use x / max(x)
                normalized_matrix[i, j] = value / max_val
            else:
                # Cost criteria, use min(x) / x
                normalized_matrix[i, j] = min_val / value

    weighted_matrix = normalized_matrix * criteria_weights
    scores = weighted_matrix.sum(axis=1)

    return scores

def on_calculate():
    try:
        # Read data from CSV file
        data = pd.read_csv("sistem.csv")

        # Extract the decision matrix from the DataFrame
        decision_matrix = data.values[:, 1:]  # Assuming the first column is not part of the decision matrix

        # Define criteria weights and benefit/cost criteria information
        criteria_weights = [float(entry.get()) for entry in weight_entries]
        is_benefit_criteria = [True, False, True, True]
        
        if not validate_weights(criteria_weights):
            raise ValueError("Total bobot harus 1.")

        # Perform SAW normalization
        scores = saw_normalization(decision_matrix, criteria_weights, is_benefit_criteria)

        # Tambahkan hasil SAW ke dalam DataFrame
        data['SAW'] = scores

        # Urutkan DataFrame berdasarkan nilai SAW
        ranked_data = data.sort_values(by='SAW', ascending=False)

        # Menampilkan hasil hitung
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for i, (name, value) in enumerate(zip(ranked_data.iloc[:, 0], scores), start=1):
            result_text.insert(tk.END, f"Rank-{i}: {name} \n")
        result_text.config(state=tk.DISABLED)

        # Menampilkan peringkat dalam tabel terpisah
        ranked_data_text.config(state=tk.NORMAL)
        ranked_data_text.delete(1.0, tk.END)
        ranked_data_text.insert(tk.END, ranked_data[['Nama', 'SAW']].to_string(index=False))
        ranked_data_text.config(state=tk.DISABLED)

    except ValueError as ve:
        show_error_message(f"Error: {str(ve)}")
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        ranked_data_text.config(state=tk.NORMAL)
        ranked_data_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
        result_text.config(state=tk.DISABLED)
        ranked_data_text.config(state=tk.DISABLED)
        show_error_message(f"Error: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Sistem Penentuan Evaluasi Kinerja Karyawan PT. Luwu Tongkonan dengan menggunakan Metode Simple Additive Weighting")

# Create GUI components
weight_labels = ["Bobot Gaji (Benefit)", "Bobot Usia (Cost)", "Bobot Masa Kerja (Benefit)", "Bobot Pencapaian (Benefit)"]
weight_entries = [tk.Entry(root) for _ in range(4)]

calculate_button = tk.Button(root, text="Hitung", command=on_calculate)

original_data_text = tk.Text(root, height=10, width=60)
result_text = tk.Text(root, height=10, width=60, state=tk.DISABLED, wrap=tk.WORD)
ranked_data_text = tk.Text(root, height=10, width=60, state=tk.DISABLED, wrap=tk.WORD)

# Add scrollbars
original_data_scroll = tk.Scrollbar(root, command=original_data_text.yview)
original_data_text.config(yscrollcommand=original_data_scroll.set)

result_scroll = tk.Scrollbar(root, command=result_text.yview)
result_text.config(yscrollcommand=result_scroll.set)

ranked_data_scroll = tk.Scrollbar(root, command=ranked_data_text.yview)
ranked_data_text.config(yscrollcommand=ranked_data_scroll.set)

# Layout GUI components
for i, label_text in enumerate(weight_labels):
    label = tk.Label(root, text=label_text)
    entry = weight_entries[i]

    label.grid(row=i, column=0, padx=10, pady=10)
    entry.grid(row=i, column=1, padx=10, pady=10)

calculate_button.grid(row=len(weight_labels), column=0, columnspan=2, pady=10)
original_data_text.grid(row=len(weight_labels) + 1, column=0, columnspan=2, padx=10, pady=10)
original_data_scroll.grid(row=len(weight_labels) + 1, column=2, sticky='ns')
result_text.grid(row=len(weight_labels) + 2, column=0, columnspan=2, padx=10, pady=10)
result_scroll.grid(row=len(weight_labels) + 2, column=2, sticky='ns')
ranked_data_text.grid(row=len(weight_labels) + 3, column=0, columnspan=2, padx=10, pady=10)
ranked_data_scroll.grid(row=len(weight_labels) + 3, column=2, sticky='ns')

# Buat tombol Bantuan
tombol_bantuan = tk.Button(root, text="Help", command=dokumentasi)
tombol_bantuan.grid(row=len(weight_labels) + 4, column=0, columnspan=2, pady=10)

# Load and display original data
try:
    original_data = pd.read_csv("sistem.csv")
    original_data_text.insert(tk.END, original_data.to_string(index=False))
except FileNotFoundError:
    original_data_text.insert(tk.END, "File not found")

# Start GUI event loop
root.mainloop()
