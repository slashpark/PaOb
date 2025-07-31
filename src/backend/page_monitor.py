import time
import requests
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from hashlib import sha256
from db import DatabaseManager
from bs4 import BeautifulSoup

class PageMonitorService:
    def __init__(self, max_workers=10):
        self.db_manager = DatabaseManager()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.scheduler = BackgroundScheduler()
        self.scheduled_futures = {}

    def perform_check(self, page_id, url, element_to_monitor):
        print(f"[{datetime.now()}] PERFORMING CHECK for ID {page_id} on {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            new_status = "ok"
            self.db_manager.update_page_status(page_id, new_status)
        except requests.RequestException as e:
            print(f"[{datetime.now()}] ERROR accessing {url}: {e}")
            new_status = "error"
            self.db_manager.update_page_status(page_id, new_status)
            return

        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        page_content = body.get_text(separator="\n", strip=True) if body else ""
        hashed_content = sha256(page_content.encode()).hexdigest()
        last_content = self.db_manager.get_hashed_content(page_id)

        if last_content != hashed_content:
            print(f"[{datetime.now()}] CONTENT CHANGED for ID {page_id}. Updating DB...")
            self.db_manager.update_page_content(page_id, hashed_content)
            # TODO: send notification
        else:
            print(f"[{datetime.now()}] CONTENT UNCHANGED for ID {page_id}. No update needed.")

    def submit_check_to_pool(self, page_id, url, element):
        future = self.executor.submit(self.perform_check, page_id, url, element)
        self.scheduled_futures[page_id] = future

    def add_page_to_monitor(self, name, url, interval, element=None):
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            body = soup.body
            page_content = body.get_text(separator="\n", strip=True) if body else ""
            hashed_content = sha256(page_content.encode()).hexdigest()
            page_id = self.db_manager.add_page_to_monitor(name, url, element, interval, hashed_content)

            self.scheduler.add_job(
                self.submit_check_to_pool,
                'interval',
                seconds=interval,
                args=[page_id, url, None],
                id=f"job_{page_id}"
            )
        except requests.RequestException as e:
            print(f"[{datetime.now()}] ERROR accessing {url}. Page not added")

    def start(self):
        pages = self.db_manager.get_all_pages_to_monitor()

        for page in pages:
            interval_seconds = page['check_interval']
            print(f"Scheduling task for ID {page['id']} every {interval_seconds} seconds.")
            self.scheduler.add_job(
                self.submit_check_to_pool,
                'interval',
                seconds=interval_seconds,
                args=[page['id'], page['page_url'], page['element_to_monitor']],
                id=f"job_{page['id']}"
            )

        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
        self.executor.shutdown()

    def get_all_pages(self):
        return self.db_manager.get_all_pages_to_monitor()

    def get_page(self, page_id):
        return self.db_manager.get_page_by_id(page_id)
    
    def delete_page(self, page_id):
        self.db_manager.delete_page(page_id)
        self.scheduler.remove_job(f"job_{page_id}")
        self.scheduled_futures[page_id].cancel()
        del self.scheduled_futures[page_id]
    
    def update_page(self, page_id, new_url, new_name, new_interval):
        try:
            response = requests.get(new_url).text
            soup = BeautifulSoup(response, "html.parser")
            body = soup.body
            page_content = body.get_text(separator="\n", strip=True) if body else ""
            hashed_content = sha256(page_content.encode()).hexdigest()
            self.db_manager.update_page(page_id, new_name, new_url, new_interval)

            self.scheduler.remove_job(f"job_{page_id}")
            self.scheduler.add_job(
                self.submit_check_to_pool,
                'interval',
                seconds=new_interval,
                args=[page_id, new_url, None],
                id=f"job_{page_id}"
            )

            #print all the jobs in the scheduler
            print("Current jobs in the scheduler:")
            for job in self.scheduler.get_jobs():
                print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}, Interval: {job.trigger.interval}")

            print(self.scheduled_futures)
                    
            return True
        except requests.RequestException:
            print(f"[{datetime.now()}] ERROR accessing {url}. Page not modified")
            return False

    def get_next_check_time(self, page_id):
        job = self.scheduler.get_job(f"job_{page_id}")
        if job:
            return job.next_run_time
        else:
            print(f"No job found for page ID {page_id}.")
            return None      

