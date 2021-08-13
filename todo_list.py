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


def today_tasks():
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if rows:
        return "\n".join([(str(i+1) + ". " + rows[i].task) for i in range(len(rows))])
    return "Nothing to do!"


def print_all_tasks(rows):
    if rows:
        n = len(rows)
        print("\n".join([f"{i+1}. {rows[i].task}. {rows[i].deadline.day} "
              f"{rows[i].deadline.strftime('%b')}" for i in range(n)]))
    else:
        print("Nothing to do!")


def week_tasks():
    week = [(today + timedelta(days=i)).date() for i in range(7)]
    days_week = [i.strftime('%A %d %B') for i in week]
    for i in range(len(week)):
        print(days_week[i])
        rows = session.query(Table).filter(Table.deadline == str(week[i])).all()
        if rows:
            print("\n".join(((str(rows[i].id) + ". " + rows[i].task) for i in range(len(rows)))), end="\n\n")
        else:
            print("Nothing to do!\n")


def missed_tasks():
    r = session.query(Table).filter(Table.deadline < today.date()).all()
    n = len(r)
    if r:
        for i in range(n):
            print(f"{i + 1}. {r[i].task}. {r[i].deadline.day} {r[i].deadline.strftime('%b')}")
    else:
        print("Nothing is missed!")


def main():
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n\
4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    cmd = input()
    while cmd != "0":
        if cmd == "1":
            print(f"\nToday {today.day} {today.strftime('%b')}:")
            print(today_tasks())

        elif cmd == "2":
            week_tasks()


        elif cmd == "3":
            rows = session.query(Table).order_by(Table.deadline).all()
            print("\nAll tasks:")
            print_all_tasks(rows)

        elif cmd == "4":
            print("\nMissed tasks:")
            missed_tasks()

        elif cmd == "5":
            print("\nEnter task")
            todo_task = input()
            print("Enter deadline")
            task_deadline = input()
            new_row = Table(task=todo_task,
                            deadline=datetime.strptime(task_deadline, '%Y-%m-%d').date())
            session.add(new_row)
            session.commit()
            print("The task has been added!")

        elif cmd == "6":
            rows = session.query(Table).order_by(Table.deadline).all()
            if rows:
                print("Choose the number of the task you want to delete:")
                print_all_tasks(rows)
                del_choice = int(input())
                specific_row = rows[del_choice-1]  # in case rows is not empty
                session.delete(specific_row)
                session.commit()
                print("Task has been deleted!")
            else:
                print("Nothing to delete")
        else:
            print("Wrong command")
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\
    \n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        cmd = input()


main()
print("\nBye!")
