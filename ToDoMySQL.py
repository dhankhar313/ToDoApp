import mysql.connector
import os

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.environ.get('mySQLPass')
)

cursor = dataBase.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS TODOApp')
cursor.execute('USE TODOApp')
listsTable = 'CREATE TABLE IF NOT EXISTS lists (title varchar(50),description varchar(400))'
tasksTable = "CREATE TABLE IF NOT EXISTS tasks (id int primary key auto_increment, hashtag varchar(50),description " \
             "varchar(400), status enum('0', '1')) "
cursor.execute(listsTable)
cursor.execute(tasksTable)


def createList():
    lName = input('Enter list name: ')
    print('Keep adding elements. Enter quit to quit.')
    while True:
        product = input(': ')
        if product == 'quit':
            break
        cursor.execute(f"INSERT INTO lists VALUES ('{lName}', '{product}');")
        dataBase.commit()
    print(f'List {lName} created Successfully!')


def showList():
    title = input('Enter title: ')
    cursor.execute(f"SELECT * FROM lists WHERE title='{title}';")
    printList(cursor.fetchall())


def showAllLists():
    cursor.execute(f"SELECT * FROM lists;")
    printList(cursor.fetchall())


def deleteList():
    title = input('Enter title for deletion: ')
    cursor.execute(f"DELETE FROM lists WHERE title='{title}';")
    print('List Deleted Successfully!')
    dataBase.commit()


def printList(data):
    lDict = {}
    for i in data:
        if lDict.get(i[0], 0) == 0:
            lDict[i[0]] = [i[-1]]
        else:
            lDict[i[0]].append(i[-1])
    for i, j in lDict.items():
        print(f'{i}: {j}')


def createTask():
    desc = input('Enter Description: ')
    flag = False
    for i in desc.split():
        if i.startswith('#'):
            hashtag = i
            flag = True
            cursor.execute(f"INSERT INTO tasks(hashtag, description, status) VALUES ('{hashtag}', '{desc}', '0');")
    if not flag:
        cursor.execute(f"INSERT INTO tasks(hashtag, description, status) VALUES ('Undefined', '{desc}', '0');")
    print('Task Created Successfully!')
    dataBase.commit()


def showTasks():
    cursor.execute(f"SELECT * FROM tasks;")
    printTasks(cursor.fetchall())


def markAsDone():
    cursor.execute('SELECT * FROM TASKS')
    printTasks(cursor.fetchall())
    choice = int(input('Enter id of task whose status you want to update: '))
    cursor.execute(f"UPDATE TASKS SET status='1' WHERE id={choice};")
    print('Task status updated successfully!')
    dataBase.commit()


def editTask():
    cursor.execute('SELECT * FROM TASKS')
    printTasks(cursor.fetchall())
    choice = int(input('Enter id of task which you want to update: '))
    desc = input('Enter updated description: ')
    cursor.execute(f"UPDATE TASKS SET description='{desc}' WHERE id={choice};")
    print('Task updated successfully!')
    dataBase.commit()


def deleteTask():
    cursor.execute('SELECT * FROM TASKS')
    printTasks(cursor.fetchall())
    choice = int(input('Enter id of task you want to delete: '))
    cursor.execute(f"DELETE FROM TASKS WHERE id='{choice}';")
    print('Task deleted successfully!')
    dataBase.commit()


def searchByHashtag():
    choice = input('Enter hashtag: ')
    cursor.execute(f"SELECT * FROM TASKS WHERE hashtag='{choice}';")
    printTasks(cursor.fetchall())
    dataBase.commit()


def printTasks(data):
    print('ID    Hashtag    Description      Status')
    for i in data:
        print(i)


if __name__ == '__main__':
    while True:
        choice = '''
        1. Create a List
        2. Show a List
        3. Show All Lists
        4. Delete A List
        5. Create A Task
        6. Show All Tasks
        7. Edit A Task
        8. Mark A Task as Done
        9. Delete A Task
        10. Search Tasks by Hashtags
        11. Quit'''
        print(choice)
        userInput = int(input('Enter choice: '))
        if userInput == 1:
            createList()
        elif userInput == 2:
            showList()
        elif userInput == 3:
            showAllLists()
        elif userInput == 4:
            deleteList()
        elif userInput == 5:
            createTask()
        elif userInput == 6:
            showTasks()
        elif userInput == 7:
            editTask()
        elif userInput == 8:
            markAsDone()
        elif userInput == 9:
            deleteTask()
        elif userInput == 10:
            searchByHashtag()
        elif userInput == 11:
            print('Program Terminated!')
            dataBase.close()
            break
