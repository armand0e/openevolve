# target_code.py
def hello():
    print("Hello from target_code.py!")

# EVOLVE-BLOCK-START
def main_logic():
    # This is the part to be evolved
    return 1 + 1
# EVOLVE-BLOCK-END

if __name__ == '__main__':
    hello()
    print(f"Main logic returns: {main_logic()}")
