# handle input from user.
from unicodedata import decimal


def handle_input(choise):
    try:
        return str(input("Enter name of {} and press enter : ".format(choise)))
    except:
        print("\nPlease enter a {} as string!".format(choise))
        handle_input(choise)


# Print out the menu list     
def print_menu():
    print("\n1 - List all Shows.")
    print("2 - Filter shows by imdb rating.")
    print("3 - Filter shows by rotten tomatoes rating.")
    # print("4 - Show disered climate for given species.")
    # print("5 - Show average lifespan for all species classification.")
    print("0 - Exit")
    
def list_all_shows(cursor):
  query = ''' SELECT *
              FROM shows
              ORDER BY title ASC
          '''
  cursor.execute(query)
  result = cursor.fetchall()
  print_schema = "{:<75}| {:<20} | {:<10} | {:<10} | {} "
  print(print_schema.format(
            "Title",
            "Released (Year)",
            "Age limit",
            "imdb /10",
            "rotten tomatoes /100"
    ))
  print('-'*80)
  for show in result:
      show = list(show)[1:]
      show = [str(x) for x in show]
      print(print_schema.format(*show))
      
def search_imdb_rating(cursor):
  try:
    rating = float(input("Rating > "))
    query = ''' SELECT title, imdb
                FROM shows
                WHERE imdb > {}
                ORDER BY imdb asc
            '''.format(rating)
    cursor.execute(query)
    result = cursor.fetchall()
    print_schema = "{:<75}| {}  "
    print(print_schema.format(
              "Title",
              "imdb /10"
      ))
    for show in result:
      show = [str(x) for x in show]
      print(print_schema.format(*show))
  except:
    print("Please enter a number as decimal with . separator")
    search_imdb_rating(cursor)

def search_tomatoe_rating(cursor):
  try:
    rating = int(input("Rating > "))
    query = ''' SELECT title, rotten_tomatoes
                FROM shows
                WHERE rotten_tomatoes > {}
                ORDER BY rotten_tomatoes asc
            '''.format(rating)
    cursor.execute(query)
    result = cursor.fetchall()
    print_schema = "{:<75}| {}  "
    print(print_schema.format(
              "Title",
              "Rotten Tomatoes /100"
      ))
    for show in result:
      show = [str(x) for x in show]
      print(print_schema.format(*show))
  except:
    print("Please enter a number as integer")
    search_tomatoe_rating(cursor)

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
            list_all_shows(cursor)
        elif option == 2:
            search_imdb_rating(cursor)
        elif option == 3:
            search_tomatoe_rating(cursor)
        # elif option == 4:
        #     desired_climate(cursor)
        # elif option == 5:
        #     average_lifespan(cursor)
        else:
            print("\nApplication closed!")
            exit(1)
        input("\nPress any key and enter to return to the menu... ")
        
