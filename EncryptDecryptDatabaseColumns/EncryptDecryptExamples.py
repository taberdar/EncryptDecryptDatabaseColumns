import EncryptDecryptDatabaseColumns

EncryptDecryptDatabaseColumns.encrypt_columns_in_database('sqlite:///ps3.db',  'ps3', ['Name'], 'secret')
EncryptDecryptDatabaseColumns.decrypt_columns_in_database('sqlite:///ps3.db',  'ps3', ['Name'], 'secret')