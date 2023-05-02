import objecttier
import sqlite3

#dbConn = sqlite3.connect('MovieLens.db')
#objecttier.get_movie_details(dbConn, 604)

###############################
# Command One Function:
# Given a connection to a database
# Asks for movie name, outputs the movie ID, title, and year of release
# Also outputs number of movies found, will not output if more than
# 100 movies are found
def command_1(dbConn):
  #command_1
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")
  print()
  mlist = objecttier.get_movies(dbConn,name)
  print("# of movies found:", len(mlist))
  print()
  #No return if movie list > 100
  if(len(mlist)>100):
    print("There are too many movies to display, please narrow your search and try again...")
    return

  for m in mlist:
    print(m.Movie_ID, ":", m.Title, f"({m.Release_Year})")

###############################
# Command Two Function:
# Given a connection to a database
# Takes a movie ID and outputs detailed movie information about the
# movie
def command_2(dbConn):
  #command_2
  print()
  id = input("Enter movie id: ")
  md = objecttier.get_movie_details(dbConn,id)
  print()
  if not md:
    print("No such movie...")
    return
  print(md.Movie_ID, ":", md.Title)
  print(" Release Date:", md.Release_Date)
  print(" Runtime:", md.Runtime, "(mins)")
  print(" Orig Language:", md.Original_Language)
  print(" Budget:", f"${md.Budget:,}", "(USD)")
  print(" Revenue:", f"${md.Revenue:,}","(USD)")
  print(" Num reviews:", md.Num_Reviews)
  print(" Avg rating:", f"{md.Avg_Rating:.2f}", "(0..10)")
  print(" Genres:",end=" ")
  for g in md.Genres:
    print(g,end=", ")
  print()
  print(" Production companies:",end=" ")
  for p in md.Production_Companies:
    print(p,end=", ")
  print()
  print(" Tagline:", md.Tagline)
    

###############################
# Command Three Function: 
# Given a connection to a database
# Asks for num and min num reviews and outputs list of movie
# ratings
def command_3(dbConn):
  #command_3
  print()
  n = input("N? ")
  #valid input check
  if int(n) < 1:
    print("Please enter a positive value for N...")
    return
  min = input("min number of reviews? ")
  if int(min) < 1:
    print("Please enter a positive value for min number of reviews...")
    return
  mrlist = objecttier.get_top_N_movies(dbConn,int(n),int(min))
  print()
  #loop through movie ratings list
  for mr in mrlist:
    print(mr.Movie_ID, ":", mr.Title, f"({mr.Release_Year}),", "avg rating =", f"{mr.Avg_Rating:.2f}", f"({mr.Num_Reviews} reviews)")
  

  

################################
# Command Four Function:
# Given a connection to a database
# Inserts a movie and rating into the database
def command_4(dbConn):
  #command_4
  print()
  rating = input("Enter rating (0..10): ")
  if int(rating) < 0 or int(rating) > 10:
    print("Invalid rating...")
    return
  id = input("Enter movie id: ")
  print()
  modified = objecttier.add_review(dbConn,int(id),int(rating))
  #Check to see if movie exists
  if(modified):
    print("Review successfully inserted")
  else:
    print("No such movie...")
    
  

################################
# Command Five Function:
# Given a connection to a database 
# updates or inserts new tagline for movie
def command_5(dbConn):
  #command_5
  print()
  tagline = input("tagline? ")
  id = input("movie id? ")
  print()
  modified = objecttier.set_tagline(dbConn,int(id),tagline)
  #Check to see if movie exists
  if(modified):
    print("Tagline successfully set")
  else:
    print("No such movie...")

##################################################################  
#
# print_stats
#
# Given a connection to the MovieLens database, outputs basic stats.
#
def print_stats(dbConn):
    print("General stats:")
    print(" # of movies:", f"{objecttier.num_movies(dbConn):,}")
    print(" # of reviews:", f"{objecttier.num_reviews(dbConn):,}")
##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')
print()
dbConn = sqlite3.connect('MovieLens.db')

print_stats(dbConn)
print()
dbCursor = dbConn.cursor()
command = input("\nPlease enter a command (1-5, x to exit): ")

while command != "x":
  if command == "1":
    command_1(dbConn)
    command = input("\nPlease enter a command (1-5, x to exit): ")
  elif command == "2":
    command_2(dbConn)
    command = input("\nPlease enter a command (1-5, x to exit): ")
  elif command == "3":
    command_3(dbConn)
    command = input("\nPlease enter a command (1-5, x to exit): ")
  elif command == "4":
    command_4(dbConn)
    command = input("\nPlease enter a command (1-5, x to exit): ")
  elif command == "5":
    command_5(dbConn)
    command = input("\nPlease enter a command (1-5, x to exit): ")
  else:
    print("**Error, unknown command, try again...\n")
    command = input("\nPlease enter a command (1-5, x to exit): ")



