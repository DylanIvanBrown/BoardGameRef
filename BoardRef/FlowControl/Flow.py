from abc import ABC, abstractmethod


class Flow(ABC):
    def __init__(self):
        self.child_flows = []
    @abstractmethod
    def flow(self):
        pass

    def add_child_flow(self, child_flow):
        self.child_flows.append(child_flow)

    def pass_message_to_child_flows(self, message):
        for child_flow in self.child_flows:
            child_flow.flow(message)