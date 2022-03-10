# handle input from user.
def handle_input(choise):
    try:
        return str(input("Enter name of {} and press enter : ".format(choise)))
    except:
        print("\nPlease enter a {} as string!".format(choise))
        handle_input(choise)


# Print out the menu list     
def print_menu():
    print("\n1 - List all planets by name.")
    print("2 - List planet details by name.")
    print("3 - List species with height greater than a given number.")
    print("4 - Show disered climate for given species.")
    print("5 - Show average lifespan for all species classification.")
    print("0 - Exit")


# handle the menu selections
def handle_menu(cursor):
    while True:
        print_menu()
        option = ""
        try:
            option = int(input("\nEnter choice: "))
        except:
            print("\nInvalid input!")
        if option == 1:
            list_all_planets(cursor)
        elif option == 2:
            search_specified_planet(cursor)
        elif option == 3:
            filter_species_by_height(cursor)
        elif option == 4:
            desired_climate(cursor)
        elif option == 5:
            average_lifespan(cursor)
        else:
            print("\nApplication closed!")
            exit(1)
        input("\nPress any key and enter to return to the menu... ")
        
