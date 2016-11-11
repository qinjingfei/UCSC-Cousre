def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


@auth.requires_signature()
def add_task():
    # request.vars is the object sent from local server (default_index.js)
    name = request.vars.task_content
    cate = request.vars.task_category
    time = request.vars.task_time

    if auth.user_id: # if logged in
        # add to database
        t_id = db.task.insert(
            task_content=name,
            category=cate,
            time_used=0,
            time_total=float(time)
        )
        # has to return a dictionary
        # so that you can call data.id, data.name, data.cate, and data.time in local server (default_index.js)
        return response.json(dict(id=t_id, name=name, cate=cate, time=time))
    return 'failed'


def get_data():
    logged_in = True
    has_more = False
    tasklist = []
    current_usr_email = auth.user.email if auth.user_id else None
    if auth.user_id:
        start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
        end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
        rows = db(db.task.user_email == auth.user.email).select(db.task.ALL, orderby=~db.task.created_on, limitby=(start_idx, end_idx + 1))
        for i, r in enumerate(rows):
            if i < end_idx - start_idx:
                if auth.user.email == r.user_email:
                    t = dict(
                        id=r.id,
                        name=r.task_content,
                        cate=r.category,
                        time=r.time_total - r.time_used
                    )
                    tasklist.append(t)
            else:
                has_more = True
                break
    else:
        logged_in = False
    return response.json(dict(
        logged_in=logged_in,
        has_more=has_more,
        tasklist=tasklist,
        current_usr_email=current_usr_email
    ))

@auth.requires_signature()
def del_task():
    if auth.user_id:
        db(db.task.id == request.vars.task_id).delete()
        return 'ok'
    return 'failure'