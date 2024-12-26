# Save the index
def save_index(index):
    with open("current_index.txt", "w") as f:
        f.write(str(index))

# Load the index
def load_index():
    try:
        with open("current_index.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0  
