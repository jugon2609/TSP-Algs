#file_code_Alg_final
def load_file(self,file):
    coords = []
    with open(file) as f:
        for i in f:
            i = i.strip()
            a = i.split(',')
            x = i[0]
            y = i[1]
            coords.append((x,y))

def export_file(self,file):
    file = f"{file}_{round(self.total_score())}.txt"
    with open(file, 'w') as f:
        for i in self.route:
            f.write(f"{i[0]},{i[1]}")