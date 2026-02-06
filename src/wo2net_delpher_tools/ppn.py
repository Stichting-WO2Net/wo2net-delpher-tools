def load_ppn_numbers_from_txt(file_path: str) -> list[str]:
    ppn_numbers = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            ppn_numbers.append(line)
    return ppn_numbers    