print("Welcome user, please enter your numbers and lets proceed")
number_one = int(input("Please enter your first number: "))
number_two = int(input("Please enter your second number: "))
stored_operations = ["+","-","/","*"]
user_operation = input("Please select the operation you would like me to perform.. example '+,/,-,*': ")
if user_operation == stored_operations[0]:
    answer = number_one + number_two
    print("Answer:",answer)

elif user_operation ==stored_operations[1]: 
    answer = number_one - number_two
    print("Answer:",answer)

elif user_operation == stored_operations[2]:
    answer = number_one / number_two
    print(answer)

elif user_operation == stored_operations[3]:
    answer = number_one * number_two
    print("Answer:",answer)

