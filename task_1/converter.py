class Converter:
    def __init__(self):
        self.step_length = 0.075
        self.step_kalories = 0.05

    def convert_to_km(self, steps):
        return steps * self.step_length

    def convert_steps_to_kilokalories(self, steps):
        return steps * self.step_kalories

