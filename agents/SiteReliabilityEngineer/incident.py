from core.task import Task
class Incident(Task):
     def __init__(self, description, app_id, deployment_id, id=None, severity=None,
                  raised_at=None, source=None):
          self.description=description
          self.app_id=app_id
          self.deployment_id=deployment_id
          self.id=id
          self.severity=severity
          self.raised_at=raised_at
          self.source=source


     @classmethod
     def from_dict(cls, data):
          return cls(
               description=data["description"],
               app_id=data["app_id"],
               deployment_id=data["deployment_id"],
               id=data.get("id"),
               severity=data.get("severity"),
               raised_at=data.get("raised_at"),
               source=data.get("source")
          )
     def to_string(self):
          return f"Id: {self.id}, Incident: {self.description} (App: {self.app_id}, Deployment: {self.deployment_id}), Severity: {self.severity}, raised at: {self.raised_at}, source: {self.source}"