class Incident:
     def __init__(self, description, app_id, deployment_id):
          self.description=description
          self.app_id=app_id
          self.deployment_id=deployment_id
     def print(self):
          print("the app id is ",self.app_id, " the deployment id is ", self.deployment_id," and the issue is:", self.description)