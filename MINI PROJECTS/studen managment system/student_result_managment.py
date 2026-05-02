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
        marks = int(input("Enter Student Marks :"))
        # Update dictnary
        student[name] = marks
        print(f"{name} : Successfullly adedd!")
 
#  View Student
    elif choice == "2":
        if not student :
            print("Student not found")
        else:
            for name , marks in student.items():
                print(name , ":" , marks )

    elif choice == "3":
        name = input("Enter a student name :")

        if name in student:
            marks = student[name]
            
            if marks >=40:
                print("Pass")
            else:
                print("Fail")
        else:
            print("Student not exixt")
    
    elif choice == '4':
        print("Exit")
        break
    else:
        print("INvalid choice")