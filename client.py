import socket
import struct

def get_equation_type():
    print("Choose the type of equation to solve:")
    print("1. Linear equation (ax + b = 0)")
    print("2. Quadratic equation (ax^2 + bx + c = 0)")
    print("3. Cubic equation (ax^3 + bx^2 + cx + d = 0)")
    choice = int(input("Enter your choice (1/2/3): "))
    return choice

def get_coefficients(equation_type):
    if equation_type == 1:
        a = float(input("Enter coefficient a: "))
        b = float(input("Enter coefficient b: "))
        return struct.pack('ff', a, b)
    elif equation_type == 2:
        a = float(input("Enter coefficient a: "))
        b = float(input("Enter coefficient b: "))
        c = float(input("Enter coefficient c: "))
        return struct.pack('fff', a, b, c)
    elif equation_type == 3:
        a = float(input("Enter coefficient a: "))
        b = float(input("Enter coefficient b: "))
        c = float(input("Enter coefficient c: "))
        d = float(input("Enter coefficient d: "))
        return struct.pack('ffff', a, b, c, d)

def main():
    server_ip = input("Enter the server IP address: ")
    
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, 9999))

            equation_type = get_equation_type()
    
            client_socket.sendall(struct.pack('i', equation_type))
        
            coefficients_data = get_coefficients(equation_type)
        
            client_socket.sendall(coefficients_data)

            num_roots_data = client_socket.recv(4)
            num_roots = struct.unpack('i', num_roots_data)[0]

            roots_data = client_socket.recv(num_roots * 4)
            roots = struct.unpack(f'{num_roots}f', roots_data)

            print("The roots of the equation are:", roots)

if __name__ == "__main__":
    main()