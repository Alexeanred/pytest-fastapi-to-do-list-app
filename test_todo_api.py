import requests
import uuid
ENDPOINT = "https://todo.pixegami.io"

response = requests.get(ENDPOINT)

data = response.json()
print(data)

status_code = response.status_code
print(status_code)


def create_task(payload):
    return requests.put(ENDPOINT+ '/create-task', json=payload)
def get_task(task_id):
    return requests.get(ENDPOINT+ f'/get-task/{task_id}')
def update_task(payload):
    return requests.put(ENDPOINT+ '/update-task', json=payload)
def list_tasks(user_id):
    return requests.get(ENDPOINT+ f'/list-tasks/{user_id}')
def delete_tasks(task_id):
    return requests.delete(ENDPOINT+ f'/delete-task/{task_id}')
def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"

    print(f"Creating task for user {user_id} with content {content}")
    return {
    "content": content,
    "user_id": user_id,
   # "task_id": "1",
    "is_done": False
    }

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    # create task
    # get task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']

def test_can_update_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # update the task
    update_payload = {
    "content": "my new content",
    "is_done": True,
    "user_id": payload['user_id'],
    "task_id": task_id
    }
    update_task_response = update_task(update_payload)
    assert update_task_response.status_code == 200
    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == update_payload['content']
    assert get_task_data['is_done'] == update_payload['is_done']

def test_can_list_tasks():
    # create tasks
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    # list tasks
    user_id = payload["user_id"]
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()

    tasks = data['tasks']
    assert len(tasks) == n

def test_can_delete_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # delete a task
    delete_task_response = delete_tasks(task_id)
    assert delete_task_response.status_code == 200

    # Get the task, check that it's not found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
