import difflib

def check_plagiarism(file1_path: str, file2_path: str) -> float:
    try:
        with open(file1_path, 'r') as file1:
            content1 = file1.read()
        
        with open(file2_path, 'r') as file2:
            content2 = file2.read()

        tokens1 = content1.split()
        tokens2 = content2.split()

        similarity = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()
        return similarity * 100  # Return as percentage

    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0