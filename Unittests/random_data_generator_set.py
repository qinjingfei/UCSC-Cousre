# Weikai Wu
# this is a script set file.
# scripts used to generate random data are integrated here
# may not runable any more since stubs and dummies are replaced by actual component
# just for record

import random, string

def randomstring(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

# insert random tasks
def random_tasks():
    for i in range(0,20):
        time = random.randint(1, 999)
        db.task.insert(
            user_email=random.choice(['12@34.com', '34@56.com', '56@78.com', '78@90.com']),
            task_content=randomstring(random.randint(1, 10)),
            category=random.choice(['p', 'np', 'n']),
            time_remained=time,
            time_total=time
        )
    return 'ok'


#insert random record
def random_record():
    for i in range(0,20):
        db.record.insert(
                       user_email=random.choice(['12@34.com', '34@56.com', '56@78.com', '78@90.com']),
                       record_content=randomstring(random.randint(1, 20))
                       )
    return 'ok'


# generate random percentile list
# i.e. sum of all entries is 1
def random_percentile_list(length):
    A = []
    for i in range(0,length):
        A.append(random.randint(1, 999))
    return [t / sum(A) for t in A]


def random_explode(length):
    A = []
    for i in range(0,length):
        A.append(random.choice([0.0,0.1]))
    return A


def random_label(length):
    A = []
    for i in range(0,length):
        A.append(randomstring(random.randint(1, 10)))
    return A


