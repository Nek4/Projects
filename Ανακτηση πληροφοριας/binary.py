# -*- coding: utf-8 -*-
"""
BTDIM2_ex1.py — Binary Term–Document Incidence Matrix + Boolean Query Support

Extension for Exercise 1:
- After building the Binary Term–Document Incidence Matrix,
  the program asks the user for a Boolean query.
- Supported query forms:
    term1 AND term2 AND ... AND termN
    term1 OR term2 OR ... OR termN
- Returns:
    * the query
    * the Document IDs
    * the filenames of matching documents
"""

import re
import time
import atexit
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


# =========================
# Total runtime timer
# =========================
__SCRIPT_START = time.perf_counter()

def __report_total_time() -> None:
    elapsed = time.perf_counter() - __SCRIPT_START
    h = int(elapsed // 3600)
    m = int((elapsed % 3600) // 60)
    s = elapsed % 60
    print(f"\n[TIMER] Total execution time: {h:02d}:{m:02d}:{s:06.3f} (HH:MM:SS.sss)")

atexit.register(__report_total_time)


# =========================
# Tokenization
# =========================
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:\'[A-Za-z0-9]+)?")

def tokenize_to_set(text: str) -> Set[str]:
    """Tokenize text -> set of unique lowercase terms (binary model)."""
    return {m.group(0).lower() for m in WORD_RE.finditer(text)}


# =========================
# Document structure
# =========================
@dataclass(frozen=True)
class Document:
    doc_id: int
    filename: str


# =========================
# One-pass build: term -> bitset
# =========================
def build_term_bitsets(folder: Path) -> Tuple[List[Document], Dict[str, int]]:
    """
    Reads *.txt in alphabetical order and builds:
      - docs: [Document(D1..)]
      - term_bits: term -> bitmask with bit j set if term appears in document j
                   (j=0 for D1, j=1 for D2, ...)
    """
    files = sorted([p for p in folder.glob("*.txt") if p.is_file()])
    if not files:
        raise ValueError(f"No .txt files found in: {folder}")

    docs: List[Document] = []
    term_bits: Dict[str, int] = {}

    for j, path in enumerate(files):  # j = 0..num_docs-1
        doc_id = j + 1
        docs.append(Document(doc_id=doc_id, filename=path.name))

        text = path.read_text(encoding="utf-8", errors="ignore")
        terms = tokenize_to_set(text)

        bit = 1 << j
        for t in terms:
            term_bits[t] = term_bits.get(t, 0) | bit

    return docs, term_bits


# =========================
# Printing (matrix + stats)
# =========================
def print_doc_mapping(docs: List[Document]) -> None:
    print("Document IDs:")
    for d in docs:
        print(f"  D{d.doc_id}: {d.filename}")
    print()

def print_matrix(docs: List[Document], vocab: List[str], term_bits: Dict[str, int]) -> None:
    num_docs = len(docs)
    doc_headers = [f"D{d.doc_id}" for d in docs]

    term_width = max(4, max((len(t) for t in vocab), default=4))
    col_width = max(2, max((len(h) for h in doc_headers), default=2)) + 1

    header = "TERM".ljust(term_width) + " | " + "".join(h.rjust(col_width) for h in doc_headers)
    print(header)
    print("-" * len(header))

    for term in vocab:
        mask = term_bits.get(term, 0)
        row_vals = "".join(("1" if (mask >> j) & 1 else "0").rjust(col_width) for j in range(num_docs))
        print(term.ljust(term_width) + " | " + row_vals)

def print_statistics(num_docs: int, vocab: List[str], term_bits: Dict[str, int]) -> None:
    num_terms = len(vocab)
    total_ones = sum(term_bits[t].bit_count() for t in vocab)
    total_cells = num_docs * num_terms
    total_zeros = total_cells - total_ones
    avg_docs_per_term = (total_ones / num_terms) if num_terms else 0.0

    print("\n" + "=" * 45)
    print("STATISTICS")
    print("=" * 45)
    print(f"Number of documents: {num_docs}")
    print(f"Number of unique terms found: {num_terms}")
    print(f"Average #documents per term: {avg_docs_per_term:.2f}")
    print(f"Total number of 1s in matrix: {total_ones}")
    print(f"Total number of 0s in matrix: {total_zeros}")


# =========================
# Query parsing / evaluation
# =========================
def parse_boolean_query(query: str) -> Tuple[str, List[str]]:
    """
    Accepts only:
      term1 AND term2 AND ... AND termN
      term1 OR term2 OR ... OR termN

    Returns:
      ("AND", [terms]) or ("OR", [terms])
    """
    query = query.strip()

    if " AND " in query and " OR " in query:
        raise ValueError("Mixed operators are not supported.")

    if " AND " in query:
        parts = [p.strip().lower() for p in query.split(" AND ")]
        operator = "AND"
    elif " OR " in query:
        parts = [p.strip().lower() for p in query.split(" OR ")]
        operator = "OR"
    else:
        raise ValueError("Query must contain only AND or only OR between terms.")

    if not parts or any(p == "" for p in parts):
        raise ValueError("Invalid query format.")

    return operator, parts


def evaluate_boolean_query(query: str, docs: List[Document], term_bits: Dict[str, int]) -> Tuple[List[int], List[str]]:
    """
    Evaluates a Boolean query using term bitsets.

    Returns:
      matching_doc_ids, matching_filenames
    """
    operator, terms = parse_boolean_query(query)
    num_docs = len(docs)

    if operator == "AND":
        # start with all bits = 1 for existing docs
        result_mask = (1 << num_docs) - 1
        for term in terms:
            result_mask &= term_bits.get(term, 0)

    elif operator == "OR":
        result_mask = 0
        for term in terms:
            result_mask |= term_bits.get(term, 0)

    else:
        raise ValueError("Unsupported operator.")

    matching_doc_ids = []
    matching_filenames = []

    for j, d in enumerate(docs):
        if (result_mask >> j) & 1:
            matching_doc_ids.append(d.doc_id)
            matching_filenames.append(d.filename)

    return matching_doc_ids, matching_filenames


def query_loop(docs: List[Document], term_bits: Dict[str, int]) -> None:
    """
    Keeps asking user for Boolean queries until 'exit'.
    """
    print("\nBoolean query mode")
    print("Supported forms:")
    print("  term1 AND term2 AND term3")
    print("  term1 OR term2 OR term3")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter query: ").strip()

        if query.lower() == "exit":
            print("Exiting query mode.")
            break

        try:
            doc_ids, filenames = evaluate_boolean_query(query, docs, term_bits)

            print("\n--- QUERY RESULT ---")
            print("Query:", query)
            print("Document IDs:", doc_ids)
            print("Filenames:", filenames)
            print("--------------------\n")

        except ValueError as e:
            print(f"Error: {e}\n")


# =========================
# Main
# =========================
def main() -> None:
    parser = argparse.ArgumentParser(description="Binary Term–Document Incidence Matrix (BTDIM2) + Exercise 1 queries.")
    parser.add_argument(
        "--folder",
        type=str,
        default=None,
        help="Folder that contains the .txt files. Default: the folder of this script."
    )
    parser.add_argument(
        "--no-matrix",
        action="store_true",
        help="Skip printing the full matrix."
    )
    args = parser.parse_args()

    folder = Path(args.folder) if args.folder else Path(__file__).resolve().parent

    t0 = time.perf_counter()
    docs, term_bits = build_term_bitsets(folder)
    t1 = time.perf_counter()

    vocab = sorted(term_bits.keys())
    t2 = time.perf_counter()

    print_doc_mapping(docs)

    if not args.no_matrix:
        print_matrix(docs, vocab, term_bits)
    t3 = time.perf_counter()

    print_statistics(len(docs), vocab, term_bits)
    t4 = time.perf_counter()

    print("\n[TIMER] Breakdown (seconds):")
    print(f"  read+tokenize+build bitsets: {t1 - t0:.6f}")
    print(f"  sort vocabulary:             {t2 - t1:.6f}")
    print(f"  print mapping+matrix:        {t3 - t2:.6f}")
    print(f"  stats:                       {t4 - t3:.6f}")

    # NEW: Query support for Exercise 1
    query_loop(docs, term_bits)


if __name__ == "__main__":
    main()