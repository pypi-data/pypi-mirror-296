import pandas as pd
import numpy as np
import itertools
import csv
import re

def count_base_consecutive(sequence, n, m):
    """
    Count consecutive occurrences of bases in a sequence.
    
    Args:
    sequence (str): DNA sequence
    n (int): Minimum consecutive count
    m (int): Maximum consecutive count
    
    Returns:
    dict: Counts of consecutive bases
    """
    bases = "ATGC"
    counts = {}
    for base in bases:
        for i in range(n, m):
            key = f"{base}_consecutive_{i}chars"
            counts[key] = len([1 for match in re.finditer(f'{base}{{{i},}}', sequence)])
    return counts

def count_kmer_consecutive(sequence, k, n):
    """
    Count consecutive occurrences of k-mers in a sequence.
    
    Args:
    sequence (str): DNA sequence
    k (int): Length of k-mer
    n (int): Minimum consecutive count
    
    Returns:
    dict: Counts of consecutive k-mers
    """
    kmers = [''.join(p) for p in itertools.product("ATGC", repeat=k)]
    counts = {}
    for kmer in kmers:
        key = f"{k}bases_consecutive_{n}counts"
        counts[key] = len([1 for match in re.finditer(f'({kmer}){{{n},}}', sequence)])
    return counts

def count_rich_regions(sequence, window_size, threshold, step):
    """
    Count AT-rich and GC-rich regions in a sequence.
    
    Args:
    sequence (str): DNA sequence
    window_size (int): Size of the sliding window
    threshold (float): Threshold for rich regions
    step (int): Step size for sliding window
    
    Returns:
    dict: Counts of AT-rich and GC-rich regions
    """
    at_count = 0
    gc_count = 0
    for i in range(0, len(sequence) - window_size + 1, step):
        window = sequence[i:i+window_size]
        at_content = (window.count('A') + window.count('T')) / window_size
        gc_content = (window.count('G') + window.count('C')) / window_size
        if at_content >= threshold:
            at_count += 1
        if gc_content >= threshold:
            gc_count += 1
    return {"AT_richs": at_count, "GC_richs": gc_count}

def extract_features(sequence):
    """
    Extract features from a DNA sequence.
    
    Args:
    sequence (str): DNA sequence
    
    Returns:
    dict: Extracted features
    """
    features = {}
    
    # Basic info
    features['length'] = len(sequence)
    features['GC_rate'] = (sequence.count('G') + sequence.count('C')) / len(sequence)
    
    # Consecutive bases
    for base in 'ATGC':
        for i in range(6, 21):
            key = f"{base}_consecutive_{i}chars"
            features[key] = len(re.findall(f'{base}{{{i},}}', sequence))
    
    # Consecutive k-mers
    for k, n in [(2, 8), (3, 5), (4, 4)]:
        key = f"{k}bases_consecutive_{n}counts"
        kmers = [''.join(p) for p in itertools.product("ATGC", repeat=k)]
        features[key] = sum(len(re.findall(f'({kmer}){{{n},}}', sequence)) for kmer in kmers)
    
    # Rich regions
    at_count, gc_count = 0, 0
    window_size, threshold, step = 100, 0.8, 10
    for i in range(0, len(sequence) - window_size + 1, step):
        window = sequence[i:i+window_size]
        at_content = (window.count('A') + window.count('T')) / window_size
        gc_content = (window.count('G') + window.count('C')) / window_size
        if at_content >= threshold:
            at_count += 1
        if gc_content >= threshold:
            gc_count += 1
    features["AT_richs"] = at_count
    features["GC_richs"] = gc_count
    
    return features

def create_feature_file(input_csv, output_csv):
    """
    Create a feature file from input CSV containing plasmid sequences.
    
    Args:
    input_csv (str): Path to input CSV file
    output_csv (str): Path to output CSV file
    """
    df = pd.read_csv(input_csv)
    features = df.apply(lambda row: extract_features(row['sequence']), axis=1)
    features_df = pd.DataFrame(features.tolist(), index=df.index)
    features_df['plasmid_id'] = df['plasmid_id']
    features_df.to_csv(output_csv, index=False)