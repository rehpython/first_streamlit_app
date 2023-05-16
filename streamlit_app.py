import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocardo Toast')
   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) 
      return(fruityvice_normalized)
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
   else:
      back_from_function  = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) 
except URLError as e :
   streamlit.error()
   
#streamlit.stop()


streamlit.header("The first Load list contains:")
#Snowflake Functions
def get_fruit_Load_list() :
   with my_cnx.cursor() as mycur:
      my_cur.execute("SELECT * FROM fruit_load_list")
      return my_cur.fetchall()
#Add a button to load the list     
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_Load_list()       
   streamlit.dataframe(my_data_rows)

# Allow user to enter data
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
      return "Thanks for adding :" + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding :', add_my_fruit)
if streamlit.button('Add Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)


