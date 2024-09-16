# UI for apscheduler

```python
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from schedule_manager_ui import ScheduleManager

app = Flask(__name__)
scheduler  = BackgroundScheduler()
sm = ScheduleManager(app, scheduler)
```
