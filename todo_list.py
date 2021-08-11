from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

today = datetime.today()

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

print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
cmd = input()
while cmd != "0":
    if cmd == "1":
        # get all rows from the table.
        # all() method returns all rows from the table as a Python list
        rows = session.query(Table).all()
        # first_row = rows[0]  # In case rows list is not empty
        print(f"\nToday {today.day} {today.strftime('%b')}:")
        if rows:
            print("\n".join([(str(rows[i].id) + ". " + rows[i].task) for i in range(len(rows))]))
            # print()
        else:
            print("Nothing to do!")
    elif cmd == "2":
        week = [(today + timedelta(days=i)).date() for i in range(7)]
        days_week = [i.strftime('%A %d %B') for i in week]
        for i in range(len(week)):
            print(days_week[i])
            rows = session.query(Table).filter(Table.deadline == str(week[i])).all()
            if rows:
                # print(*rows)
                print("\n".join(((str(rows[i].id) + ". " + rows[i].task) for i in range(len(rows)))),
                      end="\n\n")
            else:
                print("Nothing to do!\n")
    elif cmd == "3":
        print("\nAll tasks:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            n = len(rows)
            print("\n".join([f"{i+1}. {rows[i].task}. {rows[i].deadline.day} "
                             f"{rows[i].deadline.strftime('%b')}" for i in range(n)]), end="\n\n")
        else:
            print("Nothing to do!")

    elif cmd == "4":
        print("\nEnter task")
        todo_task = input()
        print("Enter deadline")
        task_deadline = input()
        new_row = Table(task=todo_task,
                        deadline=datetime.strptime(task_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    else:
        print("Wrong command")
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
    cmd = input()

print("Bye!")
