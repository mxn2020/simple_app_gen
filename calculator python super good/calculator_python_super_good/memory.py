memory_storage = []

def store_number(number):
    memory_storage.append(number)

    
def recall_number(index):
    if index < len(memory_storage):
        return memory_storage[index]
    return 'Error: Index out of range'


def clear_memory():
    memory_storage.clear()
