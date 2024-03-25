import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import functools
import time

# thêm ma trận kề
Matrix = np.array([[0,1,1,1,0],[1,0,1,1,1],[1,1,0,1,0],[1,1,1,0,1],[0,1,0,1,0]])
G = nx.Graph(Matrix) # Xây dựng bản đồ với ma trận kề
color_list = ['y','c','g','b'] # danh sách các màu viết kí tự alphabet
max_color_num = 4 # Giá trị tối đa được phép cho màu
num = len(Matrix) # số đỉnh


class ColorProblem(object):
    '''
    Tìm kiếm chiến lược + Quay lui
    '''
    def __init__(self):
        self.path = []
        self.visited = set()
        self.color = 'w' * num
        self.colored_num = 0
        self.ok = False

        for i in range(num):
            if self.color[i] != 'w':
                self.colored_num += 1

    def ktra_trangthai(self):
        '''
        Xác định xem trạng thái hiện tại có hợp pháp không?
        '''

        for vi in range(num):
            for vj in range(num):
                if vi != vj and Matrix[vi][vj] and self.color[vi] != 'w' and self.color[vi] == self.color[vj]:
                    return False
        return True

    def ktra_dinh(self,color_s:str):   
        '''
        xác định xem một đỉnh có hợp pháp hay không
        '''
        for vi in range(num):
            for vj in range(num):
                if vi != vj and Matrix[vi][vj] and color_s[vi] != 'w' and color_s[vi] == color_s[vj]:
                    return False
        return True


    def get_next(self):
        '''
        Lấy phương pháp tô màu, [i, j] có nghĩa là tô nút i bằng màu j
        '''
        next = []
        for i in range(num):
            if self.color[i] != 'w':
                continue
            for j in range(max_color_num):
                next_state = self.color
                temp = list(next_state)
                temp[i] = color_list[j]
                next_state = ''.join(temp)
                if next_state in self.visited or not self.ktra_dinh(next_state):
                    continue
                next.append((i,j))

        
        def cmp(x,y):
            '''
           Chức năng so sánh, chiến lược so sánh của nó như sau:
           1.Phạm vi giá trị nhỏ nhất được ưu tiên
           2.Những chiếc có cùng dải kích thước, chiếc có độ lớn nhất được ưu tiên hơn
            '''
            set_x = set() # Lưu trữ màu của các điểm liền kề, phạm vi màu nhỏ hơn đối với màu
            set_y = set()
            for i in range(num):
                if Matrix[x[0]][i] == 0:
                    continue
                if self.color[i] == 'w':
                    continue
                set_x.add(self.color[i])
            for i in range(num):
                if Matrix[y[0]][i] == 0:
                    continue
                if self.color[i] == 'w':
                    continue
                set_y.add(self.color[i])
            if len(set_x) > len(set_y): # Phạm vi giá trị nhỏ được ưu tiên
                return 1
            if len(set_x) < len(set_y): 
                return -1
            if G.degree(x[0]) > G.degree(y[0]): # mức độ heuristic
                return 1
            if G.degree(x[0]) < G.degree(y[0]):
                return -1
            return 0

        # Sắp xếp danh sách các chiến lược có thể để tô màu theo các chiến lược trên
        next.sort(key=functools.cmp_to_key(cmp),reverse=True)

        if len(next):
            return next[0]
        return None

    def chuyen_dinh(self):
        '''
        Sơn để chuyển sang trạng thái tiếp theo
        '''

        next = self.get_next()
        if next == None:
            return False
        next_state = list(self.color)
        next_state[next[0]] = color_list[next[1]]
        self.color = ''.join(next_state)
        self.path.append(next)
        self.visited.add(self.color)
        self.colored_num+=1
        self.display()

        if not self.ktra_trangthai():
            return False
        if self.colored_num == num:
            self.ok = True
        return True

    def quay_lui(self):
        '''
        quay ngược lại
        '''
        back = self.path.pop()
        self.colored_num -= 1
        temp = list(self.color)
        temp[back[0]] = 'w'
        self.color = ''.join(temp)
        self.display()

    def start_color(self):
        '''
        bắt đầu tô màu
        '''
        if self.chuyen_dinh() == False:
            return
        while self.color != 'w' * num and self.ok == False:
            if not self.chuyen_dinh():
                self.quay_lui()
            if self.ok:
                self.display()
                print(self.color)
                return
        print("Không có giải pháp hợp lý!")

    def display(self):
        plt.clf()
        nx.draw_shell(G, with_labels=True, node_color=list(self.color))  
        plt.pause(0.02)


if __name__ == '__main__': 
    plt.figure()
    plt.ion()
    p = ColorProblem()
    p.start_color()
    plt.ioff()
    plt.show()
