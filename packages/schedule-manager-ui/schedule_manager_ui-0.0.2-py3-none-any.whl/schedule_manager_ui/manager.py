from datetime import datetime
from flask import Flask, render_template_string, redirect, send_from_directory
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.job import Job
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_REMOVED, JobEvent

import os.path

class ScheduleManager():              
    def __init__(self, app: Flask, scheduler: BaseScheduler, home_path: str = '/schedule-manager-ui'):
        self.app: Flask = app
        self.scheduler: BaseScheduler = scheduler
        self.HOME_PATH: str = home_path
        self.last_execution_store: dict[str, datetime] = {}
        self.__init_endpoints()
        self.__init_event_listeners()
    
    def __init_endpoints(self):
        file_path = os.path.abspath(os.path.dirname(__file__))
        def find_in_store(job_id):
            return self.last_execution_store.get(job_id, None)
        
        @self.app.route(self.HOME_PATH + '/files/<path:filename>')
        def schedulemanager_ui_serve_files(filename):
            return send_from_directory(os.path.join(file_path, 'templates'), filename)

        @self.app.route(self.HOME_PATH)
        def schedulemanager_ui_index():
            jobs = self.scheduler.get_jobs()
            jobs.sort(key=lambda x: x.id)
            with open(os.path.join(file_path, 'templates/index.html')) as file:
                scheduler_template = file.read()
            return render_template_string(scheduler_template, jobs=jobs, find_in_store=find_in_store)

        @self.app.route(self.HOME_PATH + '/toggle/<job_id>', methods=['POST'])
        def schedulemanager_ui_toggle_job(job_id):
            job: Job = self.scheduler.get_job(job_id)
            if job.next_run_time is None:
                job.resume()
            else:
                job.pause()
            return redirect(ScheduleManager.HOME_PATH)

    def __init_event_listeners(self):
        def job_listener(event: JobEvent):
            if event.code == EVENT_JOB_REMOVED:
                self.last_execution_store.pop(event.job_id)
            elif event.code == EVENT_JOB_EXECUTED:
                self.last_execution_store.update({event.job_id: datetime.now()})
                
        self.scheduler.add_listener(job_listener, 
                                    EVENT_JOB_EXECUTED | EVENT_JOB_REMOVED)
