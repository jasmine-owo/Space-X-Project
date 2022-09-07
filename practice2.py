prompt = "What is your age?"
prompt +="\nquit if you want to quit\n"

status = True
total_cost = 0
try:
    while status:
        age = input(prompt)
        age = int(age)
        if age < 3:
            print("yout ticket is free")
            total_cost += 0
        elif age >= 3 and age < 12:
            print("the ticket is $10")
            total_cost += 10
        else:
            print("the ticket is $15")
            total_cost += 15
except ValueError:
    status = False
    print(f"total cost is {total_cost}")
