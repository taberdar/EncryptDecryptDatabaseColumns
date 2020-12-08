import pandas as pd
from datetime import datetime
from datetime import date
from sqlalchemy import create_engine
import EncryptDecrypt

##############################################################################
# Read a database table into a data frame
# parameters:
#   database_location: The location of the file containing the database.
#   database_table: The name of the table in the database to create.
# returns: A data frame containing all the rows of the database table.
##############################################################################
def read_from_database(database_location, database_table):
  sqlite_engine = create_engine(database_location)
  query = 'select * from ' + database_table
  dataframe = pd.read_sql(sql = query, con = sqlite_engine)
  return(dataframe)
  
##############################################################################
# Save a dataframe to an SQLite database
# parameters:
#   pd_df: A pandas dataframe.
#   database_location: The location of the file containing the database.
#   database_table: The name of the table in the database to create.
# returns: Nothing.
##############################################################################
def save_to_database(pd_df, database_location, database_table, if_exists='replace'):
  sqlite_engine = create_engine(database_location)
  sqlite_connection = sqlite_engine.connect()
  pd_df.to_sql(database_table, sqlite_connection, if_exists=if_exists, index=False)
  sqlite_connection.close()

##############################################################################
# Encrypt a column of a dataframe
# parameters:
#   pd_df: A pandas dataframe.
#   column: A string containing the name of the column to encrypt. This column
#           must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not encrypt.
# returns: A pandas dataframe with the contents of the specified column
#          encrypted.
##############################################################################
def encrypt_column(pd_df, column, password):
  if password is not None:
    pd_df[column] = [EncryptDecrypt.strong_encrypt(password=password, plaintext=p) for p in pd_df[column]]
  return pd_df

##############################################################################
# Decrypt a column of a dataframe
# parameters:
#   pd_df: A pandas dataframe.
#   column: A string containing the name of the column to decrypt. This column
#           must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not decrypt.
# returns: A pandas dataframe with the contents of the specified column
#          decrypted.
##############################################################################
def decrypt_column(pd_df, column, password):
  if password is not None:
    pd_df[column] = [EncryptDecrypt.strong_decrypt(password=password, encrypted_text=c) for c in pd_df[column]]
  return pd_df

##############################################################################
# Encrypt multiple columns of a dataframe
# parameters:
#   pd_df: A pandas dataframe.
#   column: A list of the names of the columns to encrypt. 
#           These column must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not encrypt.
# returns: A pandas dataframe with the contents of the specified columns
#          encrypted.
##############################################################################
def encrypt_columns(pd_df, columns, password):
  for column in columns:
    en = encrypt_column(pd_df, column, password)
    pd_df[column] = en[column]
  return pd_df

##############################################################################
# Decrypt multiple columns of a dataframe
# parameters:
#   pd_df: A pandas dataframe.
#   columns: A list of the names of the columns to decrypt. These columns
#           must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not decrypt.
# returns: A pandas dataframe with the contents of the specified columns
#          decrypted.
##############################################################################
def decrypt_columns(pd_df, columns, password):
  for column in columns:
    de = decrypt_column(pd_df, column, password)
    pd_df[column] = de[column]
  return pd_df

##############################################################################
# Encrypt multiple columns of a database and save to the same database
# parameters:
#   database_location: The location of the file containing the database.
#   database_table: The name of the table in the database to create.
#   columns: A list of the names of the columns to encrypt. These columns
#           must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not decrypt.
# returns: Nothing
###############################################################################
def encrypt_columns_in_database(database_location, database_table, columns_to_encrypt, password):
  df = read_from_database(database_location, database_table)
  df = encrypt_columns(df, columns_to_encrypt, password)
  save_to_database(df, database_location, database_table, if_exists='replace')
  
##############################################################################
# Decrypt multiple columns of a database and save to the same database
# parameters:
#   database_location: The location of the file containing the database.
#   database_table: The name of the table in the database to create.
#   columns: A list of the names of the columns to decrypt. These columns
#           must be in the dataframe.
#   password: A string containing the password to use. Set this to None
#             to not decrypt.
# returns: Nothing
###############################################################################
def decrypt_columns_in_database(database_location, database_table, columns_to_decrypt, password):
  df = read_from_database(database_location, database_table)
  df = decrypt_columns(df, columns_to_decrypt, password)
  save_to_database(df, database_location, database_table, if_exists='replace')

