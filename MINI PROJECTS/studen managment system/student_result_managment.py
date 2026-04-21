student = {}

while True:
    print("\n ------STUDENT MANAGER APP------")
    print("1: Add Student")
    print("2: View Student")
    print("3:Check Result")
    print("4:Exit")


    choice = input("Enter Your Choice!")

    if choice == '1':
        name = input("Enter Student Name :")
        marks = input("Enter Student Marks :")
        # Update dictnary
        student[name] : marks
        print(f"{name}Successfullly adedd!")
 
#  View Student