from django.db import models

class Rule(models.Model):
    rule_string = models.TextField()  # Store the rule as a string
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
