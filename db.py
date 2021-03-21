import sqlite3

users_db = sqlite3.connect('users.db')

def saving_users(table, users):
    users_db.executemany(f"""
        insert or ignore into {table} (
            id,
            username  
            ) 
            values(?, ?)
    """, users.items())
    users_db.commit()

def select_one_user_to_send(table):
    '''
    Выборка одного пользователя из таблицы для отправки сообщения

    :param table: Название таблицы
    :return:
    '''
    user_id = list(users_db.execute(
            f"""
            select id from {table} where send is Null limit 1;
            """
        )
    )[0][0]
    return user_id

def successfully_sent(table, user_id):
    '''
    Запись положительного результата в таблицу

    :param table: Название таблицы
    :param user_id: ID пользователя
    :return:
    '''
    users_db.execute(
        f"""
        update {table} set send = 'Done' where id = {user_id};
        """
    )
    users_db.commit()
    print(user_id, 'done')

def sending_error(table, user_id):
    '''
    Запись негативного результата в таблицу

    :param table: Название таблицы
    :param user_id: ID пользователя
    :return:
    '''
    users_db.execute(
        f"""
        update {table} set send = 'Ignore' where id = {user_id};
        """
    )
    users_db.commit()
    print(user_id, 'ignore')

def count_is_null(table):
    '''
    Определение колличества пользователей, кому еще не были отправлены сообщения

    :param table: Название таблицы
    :return:
    '''
    count = users_db.execute(f"select count(*) from {table} where send is Null;")
    print('Осталось:', count.fetchone()[0])