class K:
    def __init__(self):
        self.k = 5
    
    def get_k(self):
        return self.k

a = K()

b = a.k

a.k = 6

print(b)