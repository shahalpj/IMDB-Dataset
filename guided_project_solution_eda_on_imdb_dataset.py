#first we need to mount data from the drive.

from google.colab import drive
drive.mount('/content/drive/')

"""# Data Exploration"""

#Import package
import pandas as pd
import numpy as np

path='/content/drive/MyDrive/AlmaBetter/Cohort Nilgiri/Module 1/Week 3/Day 2/dat/imdb_data.csv'
imdb_df = pd.read_csv(path)

imdb_df.head(2)

imdb_df.info()

print(imdb_df.columns)

"""##After reading all Qs. now subsetting out columns neceesary for answering the question in order to get proper insights

#### **keep all columns which are non null.
"""

columns_to_keep= ['budget', 'genres','original_language', 'original_title','cast', 'crew', 'revenue']

#find all the row indexes for which genres is not null
imdb_df.loc[~imdb_df['genres'].isna(),'genres']

type(imdb_df.loc[0,'cast'])

"""##Converting the string values to proper list and we are using it on columns --> cast crew genres
## Converting only non null string
"""

def convert_to_list(str):
  return eval(str)

#apply the above function only on non null values in genres column
imdb_df.loc[~imdb_df['genres'].isna(),'genres']= imdb_df.loc[~imdb_df['genres'].isna(),'genres'].apply(convert_to_list)

#apply the above function only on non null values in cast column
imdb_df.loc[~imdb_df['cast'].isna(),'cast']= imdb_df.loc[~imdb_df['cast'].isna(),'cast'].apply(convert_to_list)

#apply the above function only on non null values in crew column
imdb_df.loc[~imdb_df['crew'].isna(),'crew']= imdb_df.loc[~imdb_df['crew'].isna(),'crew'].apply(convert_to_list)

"""just keep in mind which column we have to use"""

#creating a copy of orginal df
imdb_df_new = imdb_df.copy()

imdb_df_new.head(2)

"""#Q1.Which movie made the highest profit? Who were its producer and director? Identify the actors in that film."""

#checking for sanity in budget columns (outliers,vague values etc)
imdb_df_new.describe()
#budget of a movie in general cannot be 0 hence replacing those value with 0

imdb_df_new[imdb_df_new['budget']==0].head(3)

imdb_df_new['budget'].median()

#Replace extremely low values of budget and revenue column with median values of budget, revenue
imdb_df_new.loc[imdb_df_new['budget']<1000,'budget']= imdb_df_new['budget'].median()

imdb_df_new.loc[imdb_df_new['revenue']<1000,'revenue']= imdb_df_new['revenue'].median()

imdb_df_new.describe() #now fine

imdb_df_new['genres'].isnull().sum()

#create profit and ROI column
imdb_df_new['profit'] = imdb_df_new['revenue'] - imdb_df_new['budget']
imdb_df_new['roi']= 100* (imdb_df_new['profit']/imdb_df_new['budget'])

imdb_df_new.head(2)

#maximum profit
imdb_df_new['profit'].max()

#find index or row which have the max profit using .idxmax()
#.idxmax()-->> returns the row number(index) for the max value of the column 
imdb_df_new['profit'].idxmax()

"""###The movie which made the highest profit is:"""

imdb_df_new.loc[imdb_df_new['profit'].idxmax(),'original_title']

max_profit_movie_df = imdb_df_new.iloc[imdb_df_new['profit'].idxmax()]

max_profit_movie_df.head()

max_profit_movie_df.loc['cast'][0]['name']

crew_list= max_profit_movie_df.loc['crew']
crew_list[0:3]

"""### Name of the director and producer of the movie which made highest profit are:"""

producer_list=[]
director_list=[]
for elem in crew_list:
  if elem['job']=='Producer':
    producer_list.append(elem['name'])
  if elem['job']=='Director':
    director_list.append(elem['name'])

print(f'PRODUCERS : {producer_list}')
print(f'DIRECTORS : {director_list}')

cast_list =max_profit_movie_df['cast']

cast_list[0:3]

"""###Actors in the Highest profit movie"""

actor_list=[]
for elem in cast_list:
  actor_list.append(elem['name'])

#actors
print(f'Actors of the movie are :')
actor_list

"""####Understanding the groupby function"""

#kn.groupby('Name')['No.'].mean()

#kn.groupby('Name').count()

"""#Q2.This data has information about movies made in different languages. Which language has the highest average ROI (return on investment)? """

#we already calculated roi above
 #df['roi'] = 100 * df['profit']/df['budget']

#Use groupby function on movie languages and ROI and finding mean
imdb_df_new.groupby('original_language')['roi'].mean().reset_index().sort_values(by='roi',ascending=False).head(3)

print('Language with highest average roi is')
imdb_df_new.groupby('original_language')['roi'].mean().reset_index().sort_values(by='roi',ascending=False).iloc[0,0]

"""#Q3.Find out the unique genres of movies in this dataset."""

#considering only those rows in genres column which have no null values
no_na_genres = imdb_df_new[~imdb_df_new['genres'].isna()]

len(no_na_genres)

no_na_genres.loc[0,'genres']

no_na_genres.loc[0,'genres'][0]

no_na_genres.loc[3,'genres']

#create a list of genres and using .iterrow() method to iterate over genres column 
# .iterrow() --->> same as enumerate() its compulsory to use it in case of DataFrame
gen_list=[]
for index,row in no_na_genres.iterrows():
  genre = no_na_genres.loc[index,'genres']
  for k in genre:
    gen_list.append(k['name'])
  
#unique list of genres are:
pd.DataFrame(set(gen_list),columns=['Unique Genres'])

"""#Q4.Make a table of all the producers and directors of each movie. Find the top 3 producers who have produced movies with the highest average RoI? """

#considering only those rows in crew column which have no null values
no_na_crew = imdb_df_new[~imdb_df_new['crew'].isna()]

no_na_crew.shape

#A simple function to extract list of all producers for a given movie_index
def create_producer_list(index):
  movie_index = no_na_crew.iloc[index]
  crew_list= movie_index.loc['crew']
  producer_list=[]
  for elem in crew_list:
     if elem['job']=='Producer':
        producer_list.append(elem['name'])
  return producer_list

create_producer_list(61)

#A simple function to extract names of all directors for a given movie_index
#each movie has only one director
def create_director(index):
  movie_index = no_na_crew.iloc[index]
  crew_list= movie_index.loc['crew']

  for elem in crew_list:
     if elem['job']=='Director':
        return elem['name']

create_director(61)

#create a empty DataFrame with required Column names in which we will append data later
Table = pd.DataFrame(columns=['Movie Title','Producers','Directors','ROI'])

"""####appending in Table Df and using Try Except block to bypass error because some values of the crew dictionaries contain float as value


"""

for index,row in no_na_crew.iterrows():
  
  try:
      Table = Table.append({'Movie Title':no_na_crew.loc[index,'original_title'],'Producers':create_producer_list(index),'Directors':create_director(index),'ROI':no_na_crew.loc[index,'roi']},ignore_index=True)
  except:
    continue

"""###Table containing columns of Movie Title,its Producers
###,Directors and ROI
"""

Table.head(10)

"""#Q5.Which actor has acted in the most number of movies? Deep dive into the movies, genres and profits corresponding to this actor. """

#considering only those rows in cast column which have no null values
no_na_cast = imdb_df_new[~imdb_df_new['cast'].isna()]

no_na_cast.loc[0,'cast'][0]['name']

actor_list=[]
for index,row in no_na_cast.iterrows():
  for iter in no_na_cast.loc[index,'cast']:
    if type(iter)== dict:
      actor= iter['name']
      actor_list.append(actor)

#create a  DataFrame with actor list 
Actor_Table = pd.DataFrame(actor_list,columns=['Name of Actor'])

Actor_Table.shape

Actor_Table.head()

#sorting the actors using groupby function
Actor_Table.value_counts().reset_index().head()

"""###Actors who have done maximum movies are:

"""

print('Samuel L. Jackson and Robert De Niro both have done 30 films')

profit1=[]
profit2=[]
movie1=[]
movie2=[]
for index,row in no_na_cast.iterrows():
  for iter in no_na_cast.loc[index,'cast']:
    if type(iter)== dict:
      actor= iter['name']
      if 'Robert De Niro' in actor:
        profit1.append(no_na_cast.loc[index,'profit'])
        movie1.append(no_na_cast.loc[index,'original_title'])
      

        

      if 'Samuel L. Jackson' in actor:
        profit2.append(no_na_cast.loc[index,'profit'])
        movie2.append(no_na_cast.loc[index,'original_title'])

#creating a loop to get the genres for Robert and Samuel
gener_r=[]
a=[]
for i in range(len(movie1)):
  for g in no_na_cast.loc[i,'genres']:
    a.append(g['name'])
    
  gener_r.append(a)
  a=[]

gener_s=[]
b=[]
for i in range(len(movie2)):
  for g in no_na_cast.loc[i,'genres']:
    b.append(g['name'])
    
  gener_s.append(b)
  b=[]

genr = np.array(gener_r)
gens = np.array(gener_s)

#creating sub dataframe for Robert.
mov1= pd.DataFrame(movie1,columns=['Movie Name'])
prof1=pd.DataFrame(profit1,columns=['Movie Profit'])
gen1= pd.DataFrame(genr.flatten(),columns=['Genres'])

Movies_by_Robert=pd.concat([mov1,gen1,prof1],axis=1)

"""##Movies by Robert De Niro"""

Movies_by_Robert.sort_values(by='Movie Profit',ascending=False).head()

#creating sub dataframe for Samuel
mov2= pd.DataFrame(movie2,columns=['Movie Name'])
prof2=pd.DataFrame(profit2,columns=['Movie Profit'])
gen2= pd.DataFrame(gens.flatten(),columns=['Genres'])

Movies_by_Samuel=pd.concat([mov1,gen1,prof1],axis=1)

"""###Movies by Samuel L jackson"""

Movies_by_Samuel.sort_values(by='Movie Profit',ascending=False).head()

g=[]
each_movie=[]
for i in range(5):
  b=no_na_genres.loc[i,'genres']
  for k in b:
    g.append(k['name'])
#     each_movie.append([g])
    
#   a=pd.DataFrame((each_movie))
#   each_movie=[]
# #a=pd.DataFrame([[g]])

