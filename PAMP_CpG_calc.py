#! /usr/bin/python3

import argparse


def parse_seq_file(fname):
    """Convert input file into single string.

    Args:
        fname (str): file name of input sequence string

    Returns:
        str: sequence string
    """
    with open(fname, 'r') as handle:
        return ''.join([s.strip('\n') for s in handle]).lower()


def calculate_rf_values(seq):
    """Prints calculated RF1, RF2, RF3, and NRF3 values for rAAV assuming hg38.

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
    print("CpG: %s" % str(cpg_t))
    print("RF1: %s" % str(round(rf1, 3)))
    print("RF2: %s" % str(round(rf2, 3)))
    print("RF3: %s" % str(round(rf3, 3)))
    print("NRF3: %s" % str(round(nrf3, 3)))


def main():
    """PAMP CpG calculator based on work by Wright, JF (2020).
    """    
    ref_url = "Wright JF. Quantification of CpG Motifs in rAAV Genomes: " + \
    "Avoiding the Toll. Mol Ther. 2020;28(8):1756-1758. " + \
    "doi:10.1016/j.ymthe.2020.07.006"
    parser = argparse.ArgumentParser(
        description="PAMP CpG calculator. For more details, see: %s" % ref_url
    )
    parser.add_argument(
        'seqfile', metavar='SEQUENCE_FILE',
        help='sequence of interest'
    )
    args = parser.parse_args()
    seq = parse_seq_file(args.seqfile)
    calculate_rf_values(seq)


if __name__ == "__main__":
    main()
