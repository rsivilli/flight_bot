import time


class Point3D:
    x: float
    y: float
    z: float


class BaseDynamics:
    """
    Intent is to eventually create a base dynamics class around a platform centric coordinate system.
    That said, creating a full dynamics model that includes pitch/yaw/roll and all the fun dynamics of a quad copter are going to take some work, so let's start with a base class that does lat/lon and alt
    TODO look up pyhton interface template. There's a flag for methods that we need
    """

    maxV: float
    current_pos: list[float]

    def get_latlong() -> tuple[float]:
        pass


class FlyStraight(BaseDynamics):
    heading: float

    def get_latlong() -> tuple[float]:
        pass
