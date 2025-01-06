from dataBase.dataBaseConection import DataBase

with DataBase() as db:
    db.deleteUser("this_user_is_a_test_of_signup@apigateway.com")