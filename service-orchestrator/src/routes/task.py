from flask import Blueprint, request, redirect, url_for, session, render_template, flash
import requests
import os
task_blueprint = Blueprint('task', __name__)

from config import config

import pandas as pd
import logging
from services.task_service import TaskService
from objects.task import Task
from utils.utils import convert_to_title_case
from config import config

# create logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                    handlers=[logging.StreamHandler(), 
                              logging.FileHandler('app.log', mode='a')])

logger = logging.getLogger(__name__)

# base route
base_route = '/api/v1'

task_service = TaskService(base_url=config["TASK_URL"])

@task_blueprint.route(base_route + '/task-selection', methods=['GET', 'POST'])
def task_selection():
    if request.method == 'POST':
        selected_task = request.form.get('task')
        if selected_task:
            print(selected_task)
            # Store the selected task in the session
            session['selected_task'] = selected_task
            return redirect(base_route + '/configure-task')
    
    # Fetch tasks for selection
    tasks = task_service.get_tasks_list()  # Define this function as needed
    tasks_title_case = {convert_to_title_case(task): task for task in tasks}
    return render_template('task_selection.html', tasks=tasks_title_case)


@task_blueprint.route(base_route + '/configure-task')
def configure_task():
    selected_task = session.get('selected_task')
    if not selected_task:
        return redirect(url_for('task_selection'))

    task = Task(selected_task)
    task.load_data()
    task.generate_metrics_table()
    task.filter_common_metrics_and_sliders()

    if request.method == 'POST':
        slider_values = {metric: int(request.form.get(metric, 50)) for metric in task.sliders}
        
        try:
            pod_name, method = task.deploy_model(slider_values)
            if method:
                session["pod_method"] = method
            print(f"[DEMO] Deployed Pod ({pod_name})", flush=True)
            return redirect(url_for('monitor_task'))
        except Exception as e:
            return render_template('task_configured.html', task=selected_task, sliders=task.sliders, error=str(e))

    return render_template('task_configured.html', 
                           task=selected_task, 
                           sliders=task.sliders, 
                           slider_descriptions=task.get_slider_descriptions(), 
                           mapper=task.get_mapper())

@task_blueprint.route('/deploy', methods=['GET', 'POST'])
def deploy():
    task, sliders,  slider_descriptions, mapper = task_service.prepare_deploy_data()

    if not task:
        flash("No task selected. Please select a task first.", "warning")
        return redirect(url_for('select_task'))

    if request.method == 'POST':
        slider_values = {
            "Better_results": int(request.form.get("Better_results")),
            "Faster_results": int(request.form.get("Faster_results")),
            "Greener_AI": int(request.form.get("Greener_AI")),
            "Cost": int(request.form.get("Cost")),
        }

        success, message = task_service.deploy_model(task=task, slider_values=slider_values)

        if success:
            flash(f"Deployed Pod: {message}", "success")
            return redirect(url_for('monitor'))
        else:
            flash(f"Deployment failed. Error: {message}", "danger")

    return render_template('deploy.html', sliders=sliders, slider_descriptions=slider_descriptions, mapper=mapper)

#@app.route('/tasks', methods=['GET'])
#def get_tasks():
#    """
#    API endpoint to retrieve the list of tasks.
#    """
#    logger.info("Fetching tasks from API")
#    tasks = api_client.get_tasks_list()
#    if tasks:
#        logger.info(f"Tasks fetched successfully: {tasks}")
#        return jsonify({"tasks": tasks}), 200
#    logger.error("Failed to fetch tasks")
#    return jsonify({"error": "Failed to fetch tasks"}), 500
#
#@app.route('/algorithms', methods=['GET'])
#def get_algorithms():
#    """
#    API endpoint to retrieve algorithms for a given task.
#    """
#    task = request.args.get('task', 'interpolation')
#    logger.info(f"Fetching algorithms for task: {task}")
#    algorithms = api_client.get_algorithms_per_task(task=task)
#    if algorithms:
#        logger.info(f"Algorithms fetched successfully for task '{task}': {algorithms}")
#        return jsonify({"algorithms": algorithms}), 200
#    logger.error(f"Failed to fetch algorithms for task: {task}")
#    return jsonify({"error": f"Failed to fetch algorithms for task: {task}"}), 500
#
#@app.route('/metrics', methods=['GET'])
#def get_metrics():
#    """
#    API endpoint to retrieve metrics for a given algorithm.
#    """
#    algorithm = request.args.get('algorithm', 'ts_linear_interpolation')
#    logger.info(f"Fetching metrics for algorithm: {algorithm}")
#    metrics = api_client.get_metrics(algorithm=algorithm)
#    if metrics:
#        logger.info(f"Metrics fetched successfully for algorithm '{algorithm}': {metrics}")
#        return jsonify({"metrics": metrics}), 200
#    logger.error(f"Failed to fetch metrics for algorithm: {algorithm}")
#    return jsonify({"error": f"Failed to fetch metrics for algorithm: {algorithm}"}), 500
#
#@app.route('/constant-columns', methods=['POST'])
#def constant_columns():
#    """
#    API endpoint to find columns with a constant value in a DataFrame.
#    Expects a JSON with the DataFrame and constant value.
#    """
#    data = request.json
#    logger.info("Received request to find constant columns")
#    df = pd.DataFrame(data.get('data', {}))
#    constant = data.get('constant', 1)
#    constant_columns = columns_with_constant_value(df, constant=constant)
#    logger.info(f"Constant columns found: {constant_columns}")
#    return jsonify({"constant_columns": constant_columns}), 200
#
#@app.route('/non-null-columns', methods=['POST'])
#def non_null_columns():
#    """
#    API endpoint to get columns with non-null values in a DataFrame.
#    Expects a JSON with the DataFrame.
#    """
#    data = request.json
#    logger.info("Received request to find non-null columns")
#    df = pd.DataFrame(data.get('data', {}))
#    non_null_columns = get_non_null_columns(df)
#    logger.info(f"Non-null columns found: {non_null_columns}")
#    return jsonify({"non_null_columns": non_null_columns}), 200
#