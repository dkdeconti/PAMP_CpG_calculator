#! /usr/bin/python

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()

sequence = tk.StringVar()

root.title("PAMP CpG calculator")
root.geometry('400x200+50+50')


def calculate_rf_values(seq):
    """Calculates RF1, RF2, RF3, and NRF3 values for rAAV assuming hg38.

    Args:
        seq (str): input sequence for calculation
    """    
    # nt = total length of sequence
    # cpg_t = total CpG in sequence
    # cpg_meneg = estimated fraction of CpG dinucleotides unmethylated
    #       experimentally determined for viruses and rAAV
    #       see: Toth, R. et al. Viruses. (2019)
    # rf3_hg = hg38 calcualted RF3 value for normalized RF3
    #       see: Wright, JF, Mol Therapy (2020)
    # s4 = known immune stimulatory motifs
    # i4 = known immune inhibitory motifs
    #   See references used in Write, JF, Mol Therapy (2020).
    nt = len(seq)
    cpg_t = seq.count('cg')
    cpg_meneg = 0.95
    rf3_hg = 0.191
    s4 = ["acgt", "tcgt", "ccgt"]
    i4 = ["gcgg", "ccgc", "gcgc"]
    # Calculate the RF values
    rf1 = (cpg_t / float(nt)) * 100
    rf2 = cpg_meneg * rf1
    cpg_s4 = sum(seq.count(s) for s in s4)
    cpg_i4 = sum(seq.count(s) for s in i4)
    rf3 = ((cpg_t + cpg_s4 - (2 * cpg_i4)))/float(nt) * cpg_meneg * 100
    nrf3 = rf3 / float(rf3_hg)
    return (rf1, rf2, rf3, nrf3)


def submit_clicked():
    results = calculate_rf_values(
        ''.join(
            sequence.get().split('\n')
        ).lower()
    )
    rf1, rf2, rf3, nrf3 = [
        str(round(f, 3))
        for f in results
    ]
    msg = "RF1: %s\nRF2: %s\nRF3: %s\nNRF3: %s" % (rf1, rf2, rf3, nrf3)
    showinfo(
        title="Results",
        message=msg
    )

input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10, fill='x', expand=True)

input_label = ttk.Label(input_frame, text="Input sequence:")
input_label.pack(fill='x', expand=True)

input_entry = ttk.Entry(input_frame, textvariable=sequence)
input_entry.pack(fill='x', expand=True)
input_entry.focus()

# submission button
submit_button = ttk.Button(input_frame, text="Run", command=submit_clicked)
submit_button.pack(fill='x', expand=True, pady=10)

root.mainloop()