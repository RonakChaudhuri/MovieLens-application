# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self,movie,title,year): #constructor
    self._Movie_ID = movie
    self._Title = title
    self._Release_Year = year

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self,movie,title,year,reviews,rating): #constructor
    self._Movie_ID = movie
    self._Title = title
    self._Release_Year = year
    self._Reviews = reviews
    self._Rating = rating

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Reviews

  @property
  def Avg_Rating(self):
    return self._Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self,movie,title,date,runtime,language,budget,revenue,reviews,rating,tagline,genres,companies): #constructor
    self._Movie_ID = movie
    self._Title = title
    self._Release_Date = date
    self._Runtime = runtime
    self._Language = language
    self._Budget = budget
    self._Revenue = revenue
    self._Reviews = reviews
    self._Rating = rating
    self._Tagline = tagline
    self._Genres = genres
    self._Product_Companies = companies

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Reviews

  @property
  def Avg_Rating(self):
    return self._Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Product_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  sql = """select count(*) from Movies"""
  row = datatier.select_one_row(dbConn, sql)
  total = row[0]
  if row is None:
    return -1
  return total;


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = """select count(*) from Ratings"""
  row = datatier.select_one_row(dbConn, sql)
  total = row[0]
  if row is None:
    return -1
  return total;


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by movie id; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """select Movie_ID,Title,strftime('%Y', Release_Date) 
           from Movies
           where Title like ?
           order by Movie_ID"""
  rows = datatier.select_n_rows(dbConn,sql,[pattern])
  if rows is None:
    return []
  #creates list
  mlist = []
  for row in rows:
    elem = Movie(row[0],row[1],row[2]);
    mlist.append(elem)

  return mlist
##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  sql = """select Movies.Movie_ID,Title,date(Release_Date),Runtime,
           Original_Language,Budget,Revenue,count(Rating),avg(Rating),
           Tagline from Movies
           left join Ratings on Movies.Movie_ID = Ratings.Movie_ID
           left join Movie_Taglines on 
           Movies.Movie_ID = Movie_Taglines.Movie_ID
           where Movies.Movie_ID = ?
           group by Movies.Movie_ID"""
  row = datatier.select_one_row(dbConn,sql,[movie_id])
  if not row:
    return None
  #genres sql statment
  sql = """select Genre_Name from Genres
           join Movie_Genres on 
           Genres.Genre_ID = Movie_Genres.Genre_ID
           where Movie_ID = ?
           order by Genre_Name"""
  g = datatier.select_n_rows(dbConn,sql,[movie_id])
  genres = []
  for x in g:
    genres.append(x[0])
  #companies sql statement
  sql = """select Company_Name from Companies
           join Movie_Production_Companies on 
           Companies.Company_ID = 
           Movie_Production_Companies.Company_ID
           where Movie_ID = ?
           Order by Company_Name"""
  c = datatier.select_n_rows(dbConn,sql,[movie_id])
  companies = []
  for x in c:
    companies.append(x[0])
  #Checks to see if Avg or tagline is null
  if not row[8] and not row[9]:
    md = MovieDetails(row[0],row[1],row[2],row[3],row[4],row[5],row[6],
                      row[7],0.0,"",genres,companies)
    return md
  if not row[8]:
    md = MovieDetails(row[0],row[1],row[2],row[3],row[4],row[5],row[6],
                      row[7],0.0,row[9],genres,companies)
    return md
  if not row[9]:
    md = MovieDetails(row[0],row[1],row[2],row[3],row[4],row[5],row[6],
                      row[7],row[8],"",genres,companies)
    return md
  md = MovieDetails(row[0],row[1],row[2],row[3],row[4],row[5],row[6],
                      row[7],row[8],row[9],genres,companies)
  return md
##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  sql = """select Movies.Movie_ID,Title,strftime('%Y', Release_Date),
           count(Rating),avg(Rating) from Movies
           join Ratings on Movies.Movie_ID = Ratings.Movie_ID
           group by Movies.Movie_ID
           having count(Rating) >= ?
           order by avg(Rating) desc
           limit ?"""

  rows = datatier.select_n_rows(dbConn,sql,[min_num_reviews,N])
  if rows is None:
    return []
  #create list
  mlist = []
  for row in rows:
    elem = MovieRating(row[0],row[1],row[2],row[3],row[4]);
    mlist.append(elem)

  return mlist
##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  #Check if it exists
  sql = """select Movie_ID from Movies
           where Movie_ID = ?"""
  row = datatier.select_one_row(dbConn, sql,[movie_id])
  if not row:
    return 0
  
  sql = """Insert into Ratings(Movie_ID, Rating)
           Values(?,?)"""

  modified = datatier.perform_action(dbConn,sql,[movie_id,rating])
  if(modified):
    return 1
  else:
    return 0
##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  #Check if movie_id exists
  sql = """select Movie_ID from Movies
           where Movie_ID = ?"""
  row = datatier.select_one_row(dbConn, sql,[movie_id])
  if not row:
    return 0
  #Insert
  sql = """select Movie_ID from Movie_Taglines
           where Movie_ID = ?"""
  row = datatier.select_one_row(dbConn, sql,[movie_id])
  if not row:
    sql = """Insert into Movie_Taglines(Movie_ID, Tagline)
           Values(?,?)"""
    modified = datatier.perform_action(dbConn,sql,[movie_id,tagline])
  #Update
  else:
    sql = """Update Movie_Taglines
            Set Tagline = ?
            where Movie_ID = ?"""
    modified = datatier.perform_action(dbConn,sql,[tagline,movie_id])
  if(modified):
    return 1
  else:
    return 0
