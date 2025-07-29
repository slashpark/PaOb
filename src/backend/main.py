from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from page_monitor import PageMonitorService

monitor_service = PageMonitorService()
monitor_service.start()

app = FastAPI()

class Page(BaseModel):
    name: str
    url: str
    element: str = None
    interval: int = 60

@app.post("/pages/")
def add_page(page: Page):
    monitor_service.add_page_to_monitor(page.name, page.url, page.interval, page.element)
    monitor_service.start()
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
    updated = monitor_service.update_page(page_id, page.url, page.name, page.interval)
    if not updated:
        raise HTTPException(status_code=404, detail="Page not found or update failed")
    return {"message": "Page updated successfully"}