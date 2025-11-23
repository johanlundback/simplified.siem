from analysis.rules import RuleBruteforce, RulePortscan, RuleSQLi
from database.models import saveEvent
import datetime

class Analysis:
    def __init__(self):
        self.rules = [
            RuleSQLi(),
            RulePortscan(),
            RuleBruteforce()
        ]

    def handle_log_line(self, log_line):
        for rule in self.rules:
            incident = rule.process(log_line)
            if incident:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                saveEvent(timestamp, incident["message"], incident["risk"])
                print("Incident found & saved:", incident)
