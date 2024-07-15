import hashlib
import json
from time import time, ctime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block(previous_hash='0')
        self.chain.append(genesis_block)

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'data': self.current_data,
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash_block(block)
        self.current_data = []
        return Block(**block)

    def hash_block(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_data(self, data):
        timestamped_data = {
            "transaction": data,
            "timestamp": ctime()
        }
        self.current_data.append(timestamped_data)

    def mine_block(self):
        if not self.chain:
            raise ValueError('Genesis block not found.')
        last_block = self.chain[-1]
        new_block = self.create_block(last_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            previous_block = self.chain[i - 1]

            if block.previous_hash != previous_block.hash:
                return False

            if block.hash != self.hash_block(block.__dict__):
                return False

        return True

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {ctime(block.timestamp)}")
            print(f"Data: {json.dumps(block.data, indent=4)}")
            print(f"Hash: {block.hash}")
            print("-" * 30)

def main():
    blockchain = Blockchain()
    
    while True:
        print("\n1. Add transaction")
        print("2. Mine block")
        print("3. Display blockchain")
        print("4. Check validity")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            transaction = input("Enter the transaction data: ")
            blockchain.add_data(transaction)
        elif choice == '2':
            blockchain.mine_block()
            print("Block mined successfully!")
        elif choice == '3':
            blockchain.display_chain()
        elif choice == '4':
            is_valid = blockchain.is_chain_valid()
            print(f"Is blockchain valid? {is_valid}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
