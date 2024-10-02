import streamlit as st
import os
from utils.apis import get_tasks_list
from utils.string_utils import convert_to_title_case
from streamlit import switch_page

# Set page configuration
st.set_page_config(page_title="Demo TALON", page_icon="🔒")

def task_selection():
    """
    Display task selection UI and handle task selection.
    """
    st.title("Select Task")

    print("[DEMO] Retrieving tasks...", flush=True)
    tasks = get_tasks_list()
    tasks_title_case = {convert_to_title_case(task): task for task in tasks}

    selected_task_title = st.selectbox("Choose which task you want to perform", list(tasks_title_case.keys()))

    if st.button("Configure Task"):
        selected_task = tasks_title_case[selected_task_title]
        start_task(selected_task)

def start_task(selected_task):
    """
    Start the selected task.
    """
    os.environ['selected_task'] = selected_task
    print("[DEMO] Selected task: {}".format(selected_task), flush=True)
    switch_page("pages/deploy_task.py")

# Main app
def main():
    task_selection()

if __name__ == "__main__":
    main()
