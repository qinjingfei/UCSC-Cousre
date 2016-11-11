# data table

import datetime

db.define_table('task',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('task_content', 'string'),
                Field('category', 'string'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('time_used', 'float'),
                Field('time_total', 'float')
                )
