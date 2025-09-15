import magicbot
import rev
import wpilib
import wpilib.event
from phoenix6.configs import Slot0Configs

from components.chassis import ChassisComponent, SwerveConfig
from components.intake import Intake
from ids import DioChannel, SparkId
from utilities.game import is_red
from utilities.scalers import rescale_js


class MyRobot(magicbot.MagicRobot):
    # Controllers

    # Components
    chassis: ChassisComponent
    intake: Intake

    def createObjects(self) -> None:
        self.intake_motor = rev.SparkMax(
            SparkId.INTAKE_MOTOR, rev.SparkMax.MotorType.kBrushless
        )

        self.event_loop = wpilib.event.EventLoop()
        self.data_log = wpilib.DataLogManager.getLog()

        # Log driver station data
        wpilib.DriverStation.startDataLog(self.data_log)

        self.gamepad = wpilib.XboxController(0)

        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData(self.field)

        self.chassis_swerve_config = SwerveConfig(
            drive_ratio=(14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0),
            drive_gains=Slot0Configs()
            .with_k_p(1.0868)
            .with_k_i(0)
            .with_k_d(0)
            .with_k_s(0.15172)
            .with_k_v(2.8305)
            .with_k_a(0.082659),
            steer_ratio=(14 / 50) * (10 / 60),
            steer_gains=Slot0Configs()
            .with_k_p(30.234)
            .with_k_i(0)
            .with_k_d(0.62183)
            .with_k_s(0.1645),
            reverse_drive=False,
        )
        # metres between centre of left and right wheels
        self.chassis_track_width = 0.467
        # metres between centre of front and back wheels
        self.chassis_wheel_base = 0.467

        self.coast_button = wpilib.DigitalInput(DioChannel.SWERVE_COAST_SWITCH)
        self.coast_button_pressed_event = wpilib.event.BooleanEvent(
            self.event_loop, self.coast_button.get
        ).falling()

    def teleopInit(self) -> None:
        self.field.getObject("Intended start pos").setPoses([])
        self.chassis.set_coast_in_neutral(False)

    def teleopPeriodic(self) -> None:
        # Set max speed
        max_speed = 2.0  # m/s
        max_spin_rate = 1.0  # rad/s

        # Driving
        drive_x = -rescale_js(self.gamepad.getLeftY(), 0.05, 15) * max_speed
        drive_y = -rescale_js(self.gamepad.getLeftX(), 0.05, 15) * max_speed
        drive_z = (
            -rescale_js(self.gamepad.getRightX(), 0.1, exponential=20) * max_spin_rate
        )
        local_driving = self.gamepad.getRightBumperButton()

        if local_driving:
            self.chassis.drive_local(drive_x, drive_y, drive_z)
        else:
            if is_red():
                drive_x = -drive_x
                drive_y = -drive_y
            self.chassis.drive_field(drive_x, drive_y, drive_z)

        if self.gamepad.getAButton():
            self.intake.intake()
        if self.gamepad.getBButton():
            self.intake.stow()

    def testInit(self) -> None:
        self.chassis.set_coast_in_neutral(True)

    def testPeriodic(self) -> None:
        pass

    def disabledPeriodic(self) -> None:
        pass
