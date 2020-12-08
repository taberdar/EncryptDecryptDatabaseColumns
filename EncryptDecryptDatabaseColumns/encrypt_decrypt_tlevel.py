import EncryptDecryptDatabaseColumns

#EncryptDecryptDatabaseColumns.encrypt_columns_in_database('sqlite:///TLevel.db',  'Name', ['Name'], 'secret')
EncryptDecryptDatabaseColumns.decrypt_columns_in_database('sqlite:///TLevel.db',  'Name', ['Name'], 'secret')
