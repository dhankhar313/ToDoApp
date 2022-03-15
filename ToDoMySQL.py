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
listsTable = "CREATE TABLE IF NOT EXISTS lists (title varchar(50),description varchar(400));"
tasksTable = "CREATE TABLE IF NOT EXISTS tasks (id int primary key auto_increment, description " \
             "varchar(400), status enum('0', '1'));"
hashtagTable = "CREATE TABLE IF NOT EXISTS hashtags (TaskID int, hashtag varchar(40), FOREIGN KEY (TaskID) REFERENCES" \
               " tasks(id));"
cursor.execute(listsTable)
cursor.execute(tasksTable)
cursor.execute(hashtagTable)


def createList():
    lName = input('Enter list name: ')
    titles = getLists()
    if lName in titles:
        print('List already present. All items will be appended to existing list!')
    print('Keep adding elements. Enter quit to quit.')
    while True:
        product = input(': ')
        if product == 'quit':
            break
        cursor.execute(f"INSERT INTO lists VALUES ('{lName}', '{product}');")
        dataBase.commit()
    print(f'List {lName} created/updated Successfully!')


def showList():
    titles = getLists()
    showListTitles()
    title = input('\nEnter title: ')
    if title not in titles:
        print('No such list found!')
    else:
        cursor.execute(f"SELECT * FROM lists WHERE title='{title}';")
        printList(cursor.fetchall())


def showAllLists():
    print('Lists in the database are: ')
    cursor.execute(f"SELECT * FROM lists;")
    printList(cursor.fetchall())


def deleteItemFromList():
    keys = getLists()
    showListTitles()
    title = input('\nEnter List title for deletion: ')
    if title not in keys:
        print('No such list found!')
    else:
        print(f'Elements in list {title} are: ')
        elements = showElements(title)
        print(elements)
        element = input('Enter element name to delete: ')
        if element not in elements:
            print('No such element found!')
        else:
            cursor.execute(f"DELETE FROM lists WHERE title='{title}' and description='{element}'")
            print('Element Deleted Successfully!')
            dataBase.commit()


def deleteList():
    showListTitles()
    keys = getLists()
    title = input('\nEnter title for deletion: ')
    if title not in keys:
        print('No such list found!')
    else:
        cursor.execute(f"DELETE FROM lists WHERE title='{title}';")
        print('List Deleted Successfully!')
        dataBase.commit()


def showElements(title):
    cursor.execute(f"SELECT * FROM lists WHERE title='{title}'")
    return [i[-1] for i in cursor.fetchall()]


def getLists():
    cursor.execute('SELECT DISTINCT(title) FROM lists;')
    keys = [i[0].replace(',', '') for i in cursor.fetchall()]
    return keys


def showListTitles():
    titles = getLists()
    print('Lists in the database are: ')
    print(titles)


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
    tags = getHashTags(desc)
    cursor.execute(f"INSERT INTO tasks(description, status) VALUES ('{desc}', '0');")
    insertHashtags(desc, tags)
    print('Task Created Successfully!')


def getHashTags(desc):
    tags = []
    for i in desc.split():
        if i.startswith('#'):
            tags.append(i)
    return tags


def insertHashtags(desc, tags):
    if len(tags) == 0:
        cursor.execute(f"INSERT INTO hashtags VALUES ((SELECT id FROM tasks where description='{desc}'),'Undefined')")
    elif len(tags) == 1:
        cursor.execute(f"INSERT INTO hashtags VALUES ((SELECT id FROM tasks where description='{desc}'),'{tags[0]}')")
    else:
        for i in tags:
            cursor.execute(f"INSERT INTO hashtags VALUES ((SELECT id FROM tasks where description='{desc}'),'{i}')")
    dataBase.commit()


def showAllTasks():
    print('Tasks in the database are:')
    cursor.execute(f"SELECT * FROM tasks;")
    printTasks(cursor.fetchall())


def editTask():
    showAllTasks()
    keys = getKeys()
    choice = int(input('Enter id of task which you want to update: '))
    if choice not in keys:
        print('ID not found in the database!')
    else:
        cursor.execute(f"DELETE FROM hashtags WHERE taskID='{choice}'")
        desc = input('Enter updated description: ')
        cursor.execute(f"UPDATE TASKS SET description='{desc}' WHERE id={choice};")
        tags = getHashTags(desc)
        print('Tags in updated description: ', tags)
        insertHashtags(desc, tags)
        print('Task updated successfully!')
        dataBase.commit()


def markAsDone():
    showAllTasks()
    keys = getKeys()
    choice = int(input('Enter id of task whose status you want to update: '))
    if choice not in keys:
        print('ID not found in the database!')
    else:
        cursor.execute(f"UPDATE TASKS SET status='1' WHERE id={choice};")
        print('Task status updated successfully!')
        dataBase.commit()


def deleteTask():
    showAllTasks()
    keys = getKeys()
    choice = int(input('Enter id of task you want to delete: '))
    if choice not in keys:
        print('ID not found in the database!')
    else:
        cursor.execute(f"DELETE FROM hashtags WHERE taskID='{choice}';")
        cursor.execute(f"DELETE FROM TASKS WHERE id='{choice}';")
        print('Task deleted successfully!')
        dataBase.commit()


def searchByHashtag():
    cursor.execute(f"SELECT DISTINCT(hashtag) FROM hashtags")
    tags = [i[0].replace(',', '') for i in cursor.fetchall()]
    print('Hashtags present in the database are: ')
    print(tags)
    choice = input('Enter hashtag: ')
    if choice not in tags:
        print('No such hashtag found in the database!')
    else:
        cursor.execute(f"SELECT id, description, status FROM tasks JOIN hashtags on tasks.id=hashtags.taskID "
                       f"WHERE hashtag='{choice}';")
        printTasks(cursor.fetchall())
        dataBase.commit()


def printTasks(data):
    print('ID    Description      Status')
    for i in data:
        print(i)


def getKeys():
    cursor.execute('SELECT id FROM tasks;')
    keys = [i[0] for i in cursor.fetchall()]
    return keys


if __name__ == '__main__':
    choice = '''
    1. Lists
    2. Tasks
    3. Quit'''
    while True:
        print(choice)
        subInput = int(input('Enter choice: '))
        if subInput == 1:
            choice1 = '''
            1. Create a List
            2. Show a List
            3. Show All Lists
            4. Delete specific item from list
            5. Delete A List
            6. Quit'''
            while True:
                print(choice1)
                userInput = int(input('Enter choice: '))
                if userInput == 1:
                    createList()
                elif userInput == 2:
                    showList()
                elif userInput == 3:
                    showAllLists()
                elif userInput == 4:
                    deleteItemFromList()
                elif userInput == 5:
                    deleteList()
                elif userInput == 6:
                    break
                else:
                    print('Invalid input!')
        elif subInput == 2:
            choice1 = '''
            1. Create A Task
            2. Show All Tasks
            3. Edit A Task
            4. Mark A Task as Done
            5. Delete A Task
            6. Search Tasks by Hashtags
            7. Quit'''
            while True:
                print(choice1)
                userInput = int(input('Enter choice: '))
                if userInput == 1:
                    createTask()
                elif userInput == 2:
                    showAllTasks()
                elif userInput == 3:
                    editTask()
                elif userInput == 4:
                    markAsDone()
                elif userInput == 5:
                    deleteTask()
                elif userInput == 6:
                    searchByHashtag()
                elif userInput == 7:
                    break
                else:
                    print('Invalid input!')
        elif subInput == 3:
            break
        else:
            print('Invalid input!')
    print('Program Terminated!')
    dataBase.close()
