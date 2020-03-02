while True:
    depth = input("Enter depth(minimum 1 and maximum 7):")
    try:
        depth = int(depth)
    except ValueError:
        print("Please enter a number")
    if depth > 0 and depth <= 7:
        break
    else:
        print("Please enter a number that is minimum 1 and maximum 7")
