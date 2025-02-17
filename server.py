import socket
import struct
import math
import cmath

def solve_linear(a, b):
    if a == 0:
        return "No solution" if b != 0 else "Infinite solutions"
    return [-b / a]

def solve_quadratic(a, b, c):
    if a == 0:
        return solve_linear(b, c)
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    else:
        return []
    return [root1, root2]


def solve_cubic(a, b, c, d):
    if a == 0:
        return solve_quadratic(b, c, d)
    
    # Приведение уравнения к виду x^3 + px + q = 0
    p = (3*a*c - b**2) / (3*a**2)
    q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27*a**3)
    
    # Дискриминант
    discriminant = (q**2 / 4) + (p**3 / 27)
    
    if discriminant > 0:
        # Один действительный корень и два комплексных
        u = (-q / 2 + cmath.sqrt(discriminant))**(1/3)
        v = (-q / 2 - cmath.sqrt(discriminant))**(1/3)
        
        x1 = u + v - b / (3*a)
        ans = [x1]
    elif discriminant == 0:
        # Все корни действительные и по крайней мере два из них равны
        u = (-q / 2)**(1/3) 
        
        x1 = 2*u - b / (3*a)
        x2 = x3 = -u - b / (3*a)
        ans = [x1, x2]
    else:
        # Все три корня действительные и различны
        r = (-p**3 / 27)**0.5
        theta = cmath.acos(-q / (2 * r))
        
        x1 = 2 * r**(1/3) * cmath.cos(theta / 3) - b / (3*a)
        x2 = 2 * r**(1/3) * cmath.cos((theta + 2*cmath.pi) / 3) - b / (3*a)
        x3 = 2 * r**(1/3) * cmath.cos((theta + 4*cmath.pi) / 3) - b / (3*a)
        ans = [x1, x2, x3]
    ans = list(set(ans))
    ans_ = []
    for z in ans:
        if type(z) == float:
            ans_.append(z)
        elif z.imag == 0:
            ans_.append(z.real)
    print(ans_)
    return ans_

def handle_client(client_socket):
    try:
        # Получаем тип уравнения
        equation_type_data = client_socket.recv(4)
        equation_type = struct.unpack('i', equation_type_data)[0]

        # Получаем коэффициенты
        if equation_type == 1:  # Линейное уравнение
            coefficients_data = client_socket.recv(8)
            a, b = struct.unpack('ff', coefficients_data)
            roots = solve_linear(a, b)
        elif equation_type == 2:  # Квадратное уравнение
            coefficients_data = client_socket.recv(12)
            a, b, c = struct.unpack('fff', coefficients_data)
            roots = solve_quadratic(a, b, c)
        elif equation_type == 3:  # Кубическое уравнение
            coefficients_data = client_socket.recv(16)
            a, b, c, d = struct.unpack('ffff', coefficients_data)
            roots = solve_cubic(a, b, c, d)

        # Отправляем корни обратно клиенту
        roots_data = struct.pack(f'{len(roots)}f', *[float(root) for root in roots])
        client_socket.sendall(struct.pack('i', len(roots)) + roots_data)

    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
