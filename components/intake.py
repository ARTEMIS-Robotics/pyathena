import rev


class Intake:
    intake_motor: rev.SparkMax

    INTAKE_SETPOINT = 2.18  # rad
    NEUTRAL_SETPOINT = 0.0

    def __init__(self):
        self.setpoint = self.NEUTRAL_SETPOINT  # radians

    def intake(self):
        self.setpoint = self.INTAKE_SETPOINT

    def stow(self):
        self.setpoint = self.NEUTRAL_SETPOINT

    def execute(self):
        self.intake_motor.set(self.setpoint)
