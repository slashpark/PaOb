from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from page_monitor import PageMonitorService
from fastapi.middleware.cors import CORSMiddleware

monitor_service = PageMonitorService()
monitor_service.start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Page(BaseModel):
    page_name: str
    page_url: str
    element_to_monitor: str = None
    check_interval: int = 60

class NotifierConnector(BaseModel):
    connector_name: str
    connector_type: str
    connector_status: str
    connector_params: dict


#-----------PAGES---------------
@app.post("/pages/")
def add_page(page: Page):
    monitor_service.add_page_to_monitor(page.page_name, page.page_url, page.check_interval, page.element_to_monitor)
    return {"message": "Page added to monitoring service"}

@app.get("/pages/")
def list_pages():
    return monitor_service.get_all_pages()

@app.get("/pages/{page_id}")
def get_page(page_id: int):
    page = monitor_service.get_page(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@app.delete("/pages/{page_id}")
def delete_page(page_id: int):
    monitor_service.delete_page(page_id)
    return {"message": "Page deleted successfully"}

@app.put("/pages/{page_id}")
def update_page(page_id: int, page: Page):
    updated = monitor_service.update_page(page_id, page.page_url, page.page_name, page.check_interval)
    if not updated:
        raise HTTPException(status_code=404, detail="Page not found or update failed")
    return {"message": "Page updated successfully"}

@app.get("/pages/{page_id}/next_check")
def get_next_check(page_id: int):
    next_check_time = monitor_service.get_next_check_time(page_id)
    if not next_check_time:
        raise HTTPException(status_code=404, detail="Page not found or no job scheduled")
    return {"next_check": next_check_time.isoformat() if next_check_time else None}

#-----------------NOTIFIER---------------

@app.post("/notifiers/send_notification")
def send_notification(message: str):
    monitor_service.notifier.send_notification(message)
    return {"message": "Notification sent successfully"}

@app.get("/notifiers/connectors")
def get_connectors():
    return monitor_service.notifier.get_connectors()

@app.post("/notifiers/add_connector")
def add_connector(connector: NotifierConnector):
    success = monitor_service.notifier.add_connector(connector.connector_name, connector.connector_type, connector.connector_status, connector.connector_params)
    if not success:
        raise HTTPException(status_code=400, detail="Connector already exists")
    return {"message": "Connector added successfully"}

@app.delete("/notifiers/connectors/{connector_name}")
def remove_connector(connector_name: str):
    success = monitor_service.notifier.remove_connector(connector_name)
    if not success:
        raise HTTPException(status_code=404, detail="Connector not found")
    return {"message": "Connector removed successfully"}