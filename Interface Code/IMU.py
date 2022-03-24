import board
import adafruit_bno055
i2c = board.I2C()
sensor = adafruit_bno055.BNO055(i2c)
sensor.acceleration #returns a 3-tuple of acceleration (gravity+linear) in m/second^2
sensor.linear_acceleration #returns a 3-tuple (x,y,z) of linear acceleration (acceleration-gravity) in m/sec^2
sensor.quaternion #returns a 4-tuple of calculated orientation as a rotation around a 3-d vector (x,y,z,rotation)
sensor.gravity #returns a 3-tuple (x,y,z) of gravity in microteslas
sensor.euler #returns a 3-tuple (x,y,z) of orientation in degrees
sensor.gyro #returns a 3-tuple of the yaw rate (0-2pi, clockwise) of angular velocity (xy,yz,xz)
sensor.magnetic #returns the strength of the local magnetic field in microteslas (x,y,z)
sensor.temperature #returns the local temperature in Celsius. Doesn’t work. Use the following code block:

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
            result = sensor.temperature
        if abs(result - last_val) == 128:
                return 0b00111111 & result
    last_val = result
    return result
temperature()

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

qv_mult(sensor.quaternion,sensor.gravity) # orientation with respect to gravity
qv_mult(sensor.quaternion,sensor.magnetic) #orientation with respect to magnetic north

