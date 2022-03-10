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
    print("\n1 - Show data for specified title")
    print("2 - Show streaming service for specified title")
    print("3 - Filter by age limit")
    print("4 - Filter by release year")
    print("5 - Filter by age limit and release year")
    print("6 - Filter shows by imdb rating")
    print("7 - Filter shows by rotten tomatoes rating")
    print("8 - List all Shows")
    print("9 - Show average rating per streaming service")
    print("10 - Show all shows per streaming service")
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
  print('-'*150)
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
    
def search_show_data(cursor):
    try:
      title = str(input("Title: "))
      query = ''' SELECT *
                  FROM shows
                  WHERE title LIKE '%{}%'
                  ORDER BY title asc;
              '''.format(title)
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
      print('-'*150)
      for show in result:
          show = list(show)[1:]
          show = [str(x) for x in show]
          print(print_schema.format(*show))
    except:
      print("Please enter a title as string")
      search_show_data(cursor)
    
def search_show(cursor):
  try:
    title = str(input("Title: "))
    query = ''' SELECT title, streaming_services.streaming_service as streaming_on
                FROM shows
                JOIN streams_on ON movie_ID = shows.ID
                JOIN streaming_services ON streaming_services.ID = streams_on.streaming_ID
                WHERE title LIKE '%{}%'
                ORDER BY title asc
            '''.format(title)
    cursor.execute(query)
    result = cursor.fetchall()
    print_schema = "{:<75}| {}  "
    print(print_schema.format(
              "Title",
              "Streaming on"
      ))
    for show in result:
      show = [str(x) for x in show]
      print(print_schema.format(*show))
  except:
    print("Please enter a title as string")
    search_show(cursor)

def average_rating(cursor):
    query = ''' SELECT streaming_service, ROUND(AVG(imdb),2), ROUND(AVG(rotten_tomatoes),2)
                FROM shows, streaming_services
                JOIN streams_on ON streaming_services.ID = streams_on.streaming_ID
                WHERE shows.ID = streams_on.movie_ID
                GROUP BY streaming_service
            '''
    cursor.execute(query)
    result = cursor.fetchall()
    print_schema = "{:<20}| {:<20}| {}  "
    print(print_schema.format(
              "Streaming Service",
              "Average Rating imdb",
              "Average Rating rotten tomatoes",
      ))
    for show in result:
      show = [str(x) for x in show]
      print(print_schema.format(*show))
      
def search_release_year(cursor):
  try:
    year = int(input("Release year: "))
    query = ''' SELECT *
                FROM shows
                WHERE year >= {}
                ORDER BY year asc;
            '''.format(year)
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
    print('-'*150)
    for show in result:
        show = list(show)[1:]
        show = [str(x) for x in show]
        print(print_schema.format(*show))
  except:
    print("Please enter a number as integer")
    search_release_year(cursor)

def search_age_limit(cursor):
  try:
    age = str(input("Age limit: "))
    query = ''' SELECT *
                FROM shows
                WHERE age = '{}+'
                ORDER BY title asc;
            '''.format(age)
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
    print('-'*150)
    for show in result:
        show = list(show)[1:]
        show = [str(x) for x in show]
        print(print_schema.format(*show))
  except:
    print("Please enter a number as integer")
    search_age_limit(cursor)
    
def search_age_year(cursor):
  try:
    age = str(input("Age limit: "))
    year = int(input("Release year: "))
    query = ''' SELECT *
                FROM shows
                WHERE age = '{}+' AND year >= {} 
                ORDER BY year asc;
            '''.format(age, year)
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
    print('-'*150)
    for show in result:
        show = list(show)[1:]
        show = [str(x) for x in show]
        print(print_schema.format(*show))
  except:
    print("Please enter a number as integer")
    search_age_year(cursor)
    
def choose_streaming_service(cursor):
    print("\n1 - Netflix.")
    print("2 - Hulu.")
    print("3 - Prime")
    print("4 - Disney")
    while True:
      try:
        number = int(input("Enter a number between 1 and 4: "))
        if 1 <= number <= 4:
              arr = ["Netflix", "Hulu", "Prime", "Disney"]
              query = ''' SELECT title, year, age, imdb, rotten_tomatoes, streaming_services.streaming_service as streaming_on
                          FROM shows
                          JOIN streams_on ON movie_ID = shows.ID
                          JOIN streaming_services ON streaming_services.ID = streams_on.streaming_ID
                          WHERE streaming_service = '{}'
                          ORDER BY streaming_on asc
            '''.format(arr[number-1])
              cursor.execute(query)
              result = cursor.fetchall()
              print_schema = "{:<75}| {:<20} | {:<10} | {:<10} | {:<10} | {} "
              print(print_schema.format(
                        "Title",
                        "Released (Year)",
                        "Age limit",
                        "imdb /10",
                        "rotten tomatoes /100",
                        "streaming on"
                ))
              print('-'*150)
              for show in result:
                print(print_schema.format(*show))
              break
        raise ValueError()
      except ValueError:
        print("Input must be an integer between 1 and 4.")
    


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
            search_show_data(cursor)
        elif option == 2:
            search_show(cursor)
        elif option == 3:
            search_age_limit(cursor)
        elif option == 4:
            search_release_year(cursor)
        elif option == 5:
            search_age_year(cursor)
        elif option == 6:
            search_imdb_rating(cursor)
        elif option == 7:
            search_tomatoe_rating(cursor)
        elif option == 8:
            list_all_shows(cursor)
        elif option == 9:
            average_rating(cursor)
        elif option == 10:
            choose_streaming_service(cursor)
        else:
            print("\nApplication closed!")
            exit(1)
        input("\nPress any key and enter to return to the menu... ")
        
