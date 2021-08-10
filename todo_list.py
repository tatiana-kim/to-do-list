from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

# access the database and store data
Session = sessionmaker(bind=engine)
session = Session()

print("\n1) Today's tasks\n2) Add task\n0) Exit")
cmd = input()
while cmd != "0":
    if cmd == "1":
        # get all rows from the table.
        # all() method returns all rows from the table as a Python list
        rows = session.query(Table).all()
        # first_row = rows[0]  # In case rows list is not empty
        print("\nToday:")
        if rows:
            print("\n".join([(str(rows[i].id) + ". " + rows[i].task) for i in range(len(rows))]))
            # print()
        else:
            print("Nothing to do!")
    elif cmd == "2":
        print("\nEnter task")
        # create a row in our table
        todo_task = input()
        new_row = Table(task=todo_task)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    else:
        print("Wrong command")
    print("\n1) Today's tasks\n2) Add task\n0) Exit")
    cmd = input()
