"""
CoMPAS Navlib - Attitude Estimation

This module provides functions to estimate the attitude of a vehicle using different algorithms and sensors.

Functions:
    so3_integrator: Integrate the orientation of a frame using the exponential coordinate representation of rotations.
    so3_integrator_fast: Integrate the orientation of a frame using the exponential coordinate representation of rotations.
    ahrs_raw_rp: Compute the pitch and roll angles from raw accelerometer measurements.
    ahrs_raw_hdg: Compute the heading angle from raw magnetic field measurements.
    ahrs_raw_rph: Compute the roll, pitch, and heading angles from raw accelerometer and magnetic field measurements.
    ahrs_complementary_filter: Estimate the attitude of a vehicle using a complementary filter.
    ahrs_mahony_filter: Estimate the attitude of a vehicle using the Mahony filter.
    ahrs_hua_mahony_filter: Estimate the attitude of a vehicle using the Hua-Mahony filter.

Authors: Sebastián Rodríguez-Martínez and Giancarlo Troni
Contact: srodriguez@mbari.org
Last update: 2024-09-15
"""

__all__ = [
    "so3_integrator",
    "ahrs_raw_rp",
    "ahrs_raw_hdg",
    "ahrs_raw_rph",
    "ahrs_complementary_filter",
    "ahrs_mahony_filter",
    "ahrs_hua_mahony_filter",
]

from typing import List, Union

import numpy as np
import scipy

from navlib.math import (
    difference,
    norm,
    normalize,
    rot2rph,
    rph2rot,
    saturate,
    vec_to_so3,
)


def so3_integrator(
    Rold: Union[np.ndarray, List[float]],
    Rdot: Union[np.ndarray, List[float]],
    dt: float,
) -> np.ndarray:
    """
    so3_integrator integrates the final orientation R from a frame
    that was initially coincident with Rold followed a rotation described
    by Rdot by a time dt. This computation is based in the exponential
    coordinate representation of rotations.

    The Rodrigues' formula states that R = exp(skew(w)*dt). If we define
    the world frame w and the vehicle frame v, we have a initiall pose R_{wv}
    that we will denote as Rold. If we know the rotation w in the frame v and
    then the skew-symmetric matrix [w] we can compute Rdot as: R_dot = Rold @ [w]
    and equivalentlly: [w] = Rold.T @ Rdot, both inputs of the function. Then:

                Rnew = Rold @ exp((Rold.T @ Rdot) * dt)

    Source: Modern Robotics - Chapter 3.2.3 Exponential Coordinate Representation
    of Rotation (Linch & Park, 2017)

    Note: scipy.linalg.expm compute the matrix exponential using Pade approximation

    Args:
        Rold (Union[np.ndarray, List[float]]): Initial Rotation Matrix
        Rdot (Union[np.ndarray, List[float]]): Rotation Derivative computed from
            angular velocity skew-symmetric matrix
        dt (float): Time step between frames

    Returns:
        Rnew (Union[np.ndarray, List[float]]): New frame rotation matrix

    Raises:
        ValueError: If Rold or Rdot are not numpy arrays or lists
        ValueError: If Rold or Rdot are not 3x3 matrices
    """
    # Convert to numpy arrays
    if isinstance(Rold, list):
        Rold = np.array(Rold)
    if isinstance(Rdot, list):
        Rdot = np.array(Rdot)

    # Check inputs
    if not isinstance(Rold, np.ndarray):
        raise TypeError("Rold must be a numpy array or list")
    if not isinstance(Rdot, np.ndarray):
        raise TypeError("Rdot must be a numpy array or list")
    if not isinstance(dt, (float, int)):
        raise TypeError("dt must be a float or integer")
    dt = float(dt)
    if dt <= 0:
        raise ValueError("dt must be a positive value")

    # Check if Rold and Rdot are 3x3 matrices
    if Rold.shape != (3, 3):
        raise ValueError("Rold must be a 3x3 matrix")
    if Rdot.shape != (3, 3):
        raise ValueError("Rdot must be a 3x3 matrix")

    # Convert to numpy array
    Rold = np.asanyarray(Rold)
    Rdot = np.asanyarray(Rdot)

    # Check if Rold and Rdot are 3x3 matrices
    if Rold.shape != (3, 3):
        raise ValueError("Rold must be a 3x3 matrix")
    if Rdot.shape != (3, 3):
        raise ValueError("Rdot must be a 3x3 matrix")

    return np.dot(Rold, scipy.linalg.expm(np.dot(Rold.T, Rdot) * dt))


def ahrs_raw_rp(acceleration: Union[np.ndarray, List[float]]) -> np.ndarray:
    """
    ahrs_raw_rp computes pitch and roll from raw accelerometer measurements.

    The computations is based in the following formulas:
    * roll  = np.arctan2(-ay, -az)
    * pitch = np.arctan2(ax, np.sqrt(ay^2 + az^2))

    Args:
        acc (Union[np.ndarray, List[float]]): Accelerometer raw data in three
        dimensions.

    Returns:
        np.ndarray: Roll and pitch angles in radians

    Raises:
        ValueError: If acceleration is not a numpy array or list
    """
    # Convert to numpy array
    if isinstance(acceleration, list):
        acceleration = np.array(acceleration)

    # Check inputs
    if not isinstance(acceleration, np.ndarray):
        raise TypeError("Acceleration must be a numpy array or list")
    if acceleration.ndim != 2 or (
        acceleration.shape[0] != 3 and acceleration.shape[1] != 3
    ):
        raise ValueError("Acceleration must be a 3xN or Nx3 numpy array")

    # Check if acceleration is a 3xN or Nx3 matrix
    if acceleration.shape[0] == 3 and acceleration.shape[1] != 3:
        acceleration = acceleration.T

    # Normalize Accelerations
    acc = normalize(acceleration)

    # Calculating Roll and Pitch (base on gravity vector)
    roll = np.arctan2(-acc[:, 1], -acc[:, 2]).reshape(-1, 1)
    pitch = np.arctan2(acc[:, 0], np.sqrt(acc[:, 1] ** 2 + acc[:, 2] ** 2)).reshape(
        -1, 1
    )

    return np.concatenate([roll, pitch], axis=1)


def ahrs_raw_hdg(
    magnetic_field: Union[np.ndarray, List[float]],
    rph: Union[np.ndarray, List[float]] = None,
) -> np.ndarray:
    """
    raw_hdg computes the heading from magnetic field measurements and rph data.

    If rph is a parameter, the using roll and pitch the corresponding rotation
    matrices are computed and the magnetic field measuremnts are transformated
    to measurements in the xy plane. With the planar magnetic field measuremnts,
    the heading is computed as: heading = np.arcant2(-my, mx)

    Args:
        magnetic_field (Union[np.ndarray, List[float]]): Magnetic field raw data
        rph (Union[np.ndarray, List[float]], optional): Roll, pitch and heading data

    Returns:
        np.ndarray: Heading angle in radians

    Raises:
        ValueError: If mag_field is not a numpy array or list
        ValueError: If rph is not a numpy array or list
    """
    # Convert to numpy array
    if isinstance(magnetic_field, list):
        magnetic_field = np.array(magnetic_field)
    if rph is not None and isinstance(rph, list):
        rph = np.array(rph)
    # Check inputs
    if not isinstance(magnetic_field, np.ndarray):
        raise TypeError("mag_field must be a numpy array or list")
    if rph is not None and not isinstance(rph, np.ndarray):
        raise TypeError("rph must be a numpy array or list")
    # Check shape
    if magnetic_field.ndim != 2 or (
        magnetic_field.shape[0] != 3 and magnetic_field.shape[1] != 3
    ):
        raise ValueError("mag_field must be a 3xN or Nx3 numpy array")
    if rph is not None and (rph.ndim != 2 or (rph.shape[0] != 3 and rph.shape[1] != 3)):
        raise ValueError("rph must be a 3xN or Nx3 numpy array")

    # Check if mag_field and rph are 3xN or Nx3 matrices
    if magnetic_field.shape[0] == 3 and magnetic_field.shape[1] != 3:
        magnetic_field = magnetic_field.T
    if rph is not None and rph.shape[0] == 3 and rph.shape[1] != 3:
        rph = rph.T

    # Flatten Magnetic Field if the RPH is provided
    if rph is not None:
        rot_mat_flat = np.apply_along_axis(
            rph2rot, 1, np.concatenate([rph[:, [0, 1]], rph[:, [2]] * 0], axis=1)
        )
        mf = np.einsum(
            "ijk->ikj", rot_mat_flat @ magnetic_field.reshape(-1, 3, 1)
        ).squeeze()
    else:
        mf = magnetic_field

    # Calculate HDG
    heading = np.arctan2(-mf[:, 1], mf[:, 0]).reshape(-1, 1)

    return heading


def ahrs_raw_rph(
    magnetic_field: Union[np.ndarray, List[float]],
    accelerometer: Union[np.ndarray, List[float]],
) -> np.ndarray:
    """
    ahrs_raw_rph computes the roll, pitch and heading from magnetic field
    measurements and accelerometer raw data.

    The computations is based in the following formulas:
    * roll  = np.arctan2(-ay, -az)
    * pitch = np.arctan2(ax, np.sqrt(ay^2 + az^2))
    * heading = np.arctan2(-my, mx)

    Args:
        magnetic_field (Union[np.ndarray, List[float]]): Magnetic field raw data
        accelerometer (Union[np.ndarray, List[float]]): Accelerometer raw data

    Returns:
        np.ndarray: Roll, pitch and heading angles in radians
    """
    # Roll and Pitch
    roll_pitch = ahrs_raw_rp(accelerometer)

    # Heading
    heading = ahrs_raw_hdg(
        magnetic_field, np.concatenate([roll_pitch, roll_pitch[:, [0]] * 0], axis=1)
    )

    # RPH
    rph = np.concatenate([roll_pitch, heading], axis=1)

    return rph


def ahrs_complementary_filter(
    angular_rate: Union[np.ndarray, List[float]],
    acceleration: Union[np.ndarray, List[float]],
    time: Union[np.ndarray, List[float]],
    magnetic_field: Union[np.ndarray, List[float]] = None,
    gain: Union[float, int] = 0.9,
    initial_heading: Union[float, int] = 0.0,
) -> np.ndarray:
    """
    Estimates the attitude of a vehicle using a complementary filter. The filter fuses accelerometer and gyroscope,
    and optionally magnetometer data to estimate the roll, pitch, and heading angles.

    Args:
        angular_rate (Union[np.ndarray, List[float]]): Angular rate measurements (gyroscope data) in rad/s.
            Should be a 3xN or Nx3 array where N is the number of samples.
        acceleration (Union[np.ndarray, List[float]]): Acceleration measurements in m/s^2.
            Should be a 3xN or Nx3 array where N is the number of samples.
        time (Union[np.ndarray, List[float]]): Time vector in seconds. Should be a 1D array of length N.
        magnetic_field (Union[np.ndarray, List[float]], optional): Magnetic field measurements in microteslas.
            Should be a 3xN or Nx3 array where N is the number of samples. Defaults to None.
        gain (Union[float, int], optional): Gain for the complementary filter. Should be between 0 and 1.
            Defaults to 0.9.
        initial_heading (Union[float, int], optional): Initial heading in radians. Defaults to 0.0.

    Returns:
        np.ndarray: Estimated roll, pitch, and heading (yaw) angles in radians. The output is an Nx3 array where
        N is the number of samples.

    Raises:
        TypeError: If any of the inputs are not of the expected type.
        ValueError: If any of the inputs do not have the expected dimensions.
    """
    # Convert lists to numpy arrays if necessary
    if isinstance(acceleration, list):
        acceleration = np.array(acceleration)
    if isinstance(angular_rate, list):
        angular_rate = np.array(angular_rate)
    if isinstance(time, list):
        time = np.array(time)
    if magnetic_field is not None and isinstance(magnetic_field, list):
        magnetic_field = np.array(magnetic_field)

    # Validate inputs
    if not isinstance(acceleration, np.ndarray):
        raise TypeError("The acceleration must be a numpy array or a list.")
    if not isinstance(angular_rate, np.ndarray):
        raise TypeError("The angular rate must be a numpy array or a list.")
    if not isinstance(time, np.ndarray):
        raise TypeError("The time must be a numpy array or a list.")
    if magnetic_field is not None and not isinstance(magnetic_field, np.ndarray):
        raise TypeError("The magnetic field must be a numpy array or a list.")

    # Validate dimensions
    if acceleration.ndim != 2 or (
        acceleration.shape[0] != 3 and acceleration.shape[1] != 3
    ):
        raise ValueError("The acceleration must be a 3xN or Nx3 numpy array.")
    if angular_rate.ndim != 2 or (
        angular_rate.shape[0] != 3 and angular_rate.shape[1] != 3
    ):
        raise ValueError("The angular rate must be a 3xN or Nx3 numpy array.")
    if magnetic_field is not None:
        if magnetic_field.ndim != 2 or (
            magnetic_field.shape[0] != 3 and magnetic_field.shape[1] != 3
        ):
            raise ValueError("The magnetic field must be a 3xN or Nx3 numpy array.")

    # Ensure time is a 1D array
    time = time.squeeze()
    if time.ndim >= 2:
        raise ValueError("The time must be a (n, ), (n, 1) or (1, n) numpy array.")

    # Force Nx3 shape for acceleration, angular_rate, and magnetic_field
    if acceleration.shape[0] == 3 and acceleration.shape[1] != 3:
        acceleration = acceleration.T
    if angular_rate.shape[0] == 3 and angular_rate.shape[1] != 3:
        angular_rate = angular_rate.T
    if (
        magnetic_field is not None
        and magnetic_field.shape[0] == 3
        and magnetic_field.shape[1] != 3
    ):
        magnetic_field = magnetic_field.T

    # Validate initial_heading and gain
    if not isinstance(initial_heading, (float, int)):
        raise TypeError("The initial heading must be a float or integer.")
    initial_heading = float(initial_heading)
    if not isinstance(gain, (float, int)):
        raise TypeError("The gain must be a float or integer.")
    if gain < 0 or gain > 1:
        raise ValueError("The gain must be between 0 and 1.")
    gain = float(gain)

    # Compute the attitude from accelerometer and magnetic field, if available
    if magnetic_field is None:
        rph = np.zeros_like(acceleration)
        rph[:, :2] = ahrs_raw_rp(acceleration)
    else:
        rph = ahrs_raw_rph(magnetic_field, acceleration)

    # Time step vector
    dt = difference(time).reshape(-1, 1)

    # Complementary Filter
    estimated_rph = rph.copy()
    for ix in range(1, angular_rate.shape[0]):
        # Measurements
        w = angular_rate[ix, :]
        dt = time[ix] - time[ix - 1]

        # Integrate the angular rate
        if magnetic_field is None:
            # Estimate only using IMU, i.e., accelerometer and gyroscope
            estimated_rph[ix, :2] = (
                estimated_rph[ix - 1, :2] + w[:2] * dt
            ) * gain + rph[ix, :2] * (1 - gain)
            estimated_rph[ix, 2] = estimated_rph[ix - 1, 2] + w[2] * dt
        else:
            # Estimate using IMU and magnetometer
            estimated_rph[ix] = (estimated_rph[ix - 1] + w * dt) * gain + rph[ix] * (
                1 - gain
            )
            estimated_rph[ix, 2] += initial_heading

    return estimated_rph


def ahrs_mahony_filter(
    angular_rate: Union[np.ndarray, List[float]],
    acceleration: Union[np.ndarray, List[float]],
    time: Union[np.ndarray, List[float]],
    magnetic_field: Union[np.ndarray, List[float]] = None,
    reference_magnetic_field: Union[np.ndarray, List[float]] = None,
    rph0: Union[np.ndarray, List[float]] = None,
    k1: Union[float, int] = 50.0,
    k2: Union[float, int] = 1.0,
    kp: Union[float, int] = 1.0,
    ki: Union[float, int] = 0.3,
) -> np.ndarray:
    """
    Estimates the attitude of a vehicle using the Mahony filter.

    This estimator proposed by Robert Mahony et al. [Mahony2008] is formulated as a deterministic kinematic observer
    on the Special Orthogonal group SO(3) driven by an instantaneous attitude and angular velocity measurements.

    k1 and k2 tunning: The weights k1 and k2 are introduced to weight the confidence in each measure. In situations where
    the IMU is subject to high magnitude accelerations (such as during takeoff or landing manoeuvres) it may be wise to
    reduce the relative weighting of the accelerometer data (k1 << k2) compared to the magnetometer data. Conversely, in
    many applications the IMU is mounted in the proximity to powerful electric motors and their power supply busses
    leading to low confidence in the magnetometer readings (choose k1 >> k2). This is a very common situation in the case
    of mini aerial vehicles with electric motors. In extreme cases the magnetometer data is unusable and provides
    motivation for a filter based solely on accelerometer data.

    Args:
        angular_rate (Union[np.ndarray, List[float]]): Angular rate measurements (gyroscope data) in rad/s.
            Should be a 3xN or Nx3 array where N is the number of samples.
        acceleration (Union[np.ndarray, List[float]]): Acceleration measurements in m/s^2.
            Should be a 3xN or Nx3 array where N is the number of samples.
        time (Union[np.ndarray, List[float]]): Time vector in seconds. Should be a 1D array of length N.
        magnetic_field (Union[np.ndarray, List[float]], optional): Magnetic field measurements in microteslas.
            Should be a 3xN or Nx3 array where N is the number of samples. Defaults to None.
        reference_magnetic_field (Union[np.ndarray, List[float]], optional): Reference magnetic field vector.
            Should be a 1D array with 3 elements. Defaults to None.
        rph0 (Union[np.ndarray, List[float]], optional): Initial roll, pitch, and heading angles in radians.
        k1 (Union[float, int], optional): Gain for the accelerometer measurements. Defaults to 50.0.
        k2 (Union[float, int], optional): Gain for the magnetic field measurements. Defaults to 1.0.
        kp (Union[float, int], optional): Proportional gain. Defaults to 1.0.
        ki (Union[float, int], optional): Integral gain. Defaults to 0.3.

    Returns:
        np.ndarray: Estimated roll, pitch, and heading (yaw) angles in radians. The output is an Nx3 array where
        N is the number of samples.

    Raises:
        TypeError: If any of the inputs are not of the expected type.
        ValueError: If any of the inputs do not have the expected dimensions.

    References:
        Mahony, R., Hamel, T., & Pflimlin, J. M. (2008). Nonlinear complementary filters on the special orthogonal group.
        IEEE Transactions on automatic control, 53(5), 1203-1218.
    """
    # Convert lists to numpy arrays if necessary
    if isinstance(acceleration, list):
        acceleration = np.array(acceleration)
    if isinstance(angular_rate, list):
        angular_rate = np.array(angular_rate)
    if isinstance(time, list):
        time = np.array(time)
    if magnetic_field is not None and isinstance(magnetic_field, list):
        magnetic_field = np.array(magnetic_field)
    if reference_magnetic_field is not None and isinstance(
        reference_magnetic_field, list
    ):
        reference_magnetic_field = np.array(reference_magnetic_field)
    if rph0 is not None and isinstance(rph0, list):
        rph0 = np.array(rph0)

    # Validate inputs
    if not isinstance(acceleration, np.ndarray):
        raise TypeError("The acceleration must be a numpy array or a list.")
    if not isinstance(angular_rate, np.ndarray):
        raise TypeError("The angular rate must be a numpy array or a list.")
    if not isinstance(time, np.ndarray):
        raise TypeError("The time must be a numpy array or a list.")
    if magnetic_field is not None and not isinstance(magnetic_field, np.ndarray):
        raise TypeError("The magnetic field must be a numpy array or a list.")
    if reference_magnetic_field is not None and not isinstance(
        reference_magnetic_field, np.ndarray
    ):
        raise TypeError("The reference magnetic field must be a numpy array or a list.")
    if rph0 is not None and not isinstance(rph0, np.ndarray):
        raise TypeError(
            "The initial roll, pitch, and heading must be a numpy array or a list."
        )

    # Validate dimensions
    if acceleration.ndim != 2 or (
        acceleration.shape[0] != 3 and acceleration.shape[1] != 3
    ):
        raise ValueError("The acceleration must be a 3xN or Nx3 numpy array.")
    if angular_rate.ndim != 2 or (
        angular_rate.shape[0] != 3 and angular_rate.shape[1] != 3
    ):
        raise ValueError("The angular rate must be a 3xN or Nx3 numpy array.")
    if magnetic_field is not None:
        if magnetic_field.ndim != 2 or (
            magnetic_field.shape[0] != 3 and magnetic_field.shape[1] != 3
        ):
            raise ValueError("The magnetic field must be a 3xN or Nx3 numpy array.")
    if reference_magnetic_field is not None:
        reference_magnetic_field = reference_magnetic_field.squeeze()
        if reference_magnetic_field.ndim >= 2 or reference_magnetic_field.shape[0] != 3:
            raise ValueError(
                "The reference magnetic field must be a 1D numpy array with 3 elements."
            )
    if rph0 is not None:
        if rph0.ndim != 1 or rph0.shape[0] != 3:
            raise ValueError(
                "The initial roll, pitch, and heading must be a 1D numpy array with 3 elements."
            )

    # Ensure time is a 1D array
    time = time.squeeze()
    if time.ndim >= 2:
        raise ValueError("The time must be a (n, ), (n, 1) or (1, n) numpy array.")

    # Force Nx3 shape for acceleration, angular_rate, and magnetic_field
    if acceleration.shape[0] == 3 and acceleration.shape[1] != 3:
        acceleration = acceleration.T
    if angular_rate.shape[0] == 3 and angular_rate.shape[1] != 3:
        angular_rate = angular_rate.T
    if (
        magnetic_field is not None
        and magnetic_field.shape[0] == 3
        and magnetic_field.shape[1] != 3
    ):
        magnetic_field = magnetic_field.T

    # Validate gains
    if not isinstance(k1, (float, int)):
        raise TypeError("The k1 gain must be a float or integer.")
    k1 = float(k1)
    if not isinstance(k2, (float, int)):
        raise TypeError("The k2 gain must be a float or integer.")
    k2 = float(k2)
    if not isinstance(kp, (float, int)):
        raise TypeError("The kp gain must be a float or integer.")
    kp = float(kp)
    if not isinstance(ki, (float, int)):
        raise TypeError("The ki gain must be a float or integer.")
    ki = float(ki)

    # Create arrays to store the results
    samples = time.shape[0]
    rph_filtered = np.zeros([samples, 3])
    gyro_biases = np.zeros([samples, 3])

    if rph0 is not None:
        rph_filtered[0, :] = rph0

    # Reference gravity vector
    g_vec = np.array([0.0, 0.0, -1.0])
    g_vec = (g_vec / norm(g_vec)).reshape(3, 1)

    # Reference magnetic field vector
    if reference_magnetic_field is not None:
        m_vec = reference_magnetic_field
        m_vec = (m_vec / norm(m_vec)).reshape(3, 1)

    # Run the filter
    for ix in range(1, samples):
        # Gyroscope, accelerometer, and magnetic field measurements
        w = angular_rate[ix, :]
        a = acceleration[ix, :] / norm(acceleration[ix, :])
        if magnetic_field is not None:
            m = magnetic_field[ix, :] / norm(magnetic_field[ix, :])

        rot_mat = rph2rot(rph_filtered[ix - 1, :])

        # Error measurement using accelerometer and magnetometer
        wmes = k1 * (vec_to_so3(a) @ (rot_mat.T @ g_vec)).flatten()
        if magnetic_field is not None:
            wmes += k2 * (vec_to_so3(m) @ (rot_mat.T @ m_vec)).flatten()

        # Gyro bias update and filter adjustment
        rot_mat_dot = rot_mat @ (
            vec_to_so3(w - gyro_biases[ix - 1, :]) + kp * vec_to_so3(wmes)
        )
        gyro_biases_dot = -ki * wmes

        # Time step
        dt = time[ix] - time[ix - 1]

        # Update the gyro bias and the filtered roll, pitch, and heading
        gyro_biases[ix, :] = gyro_biases[ix - 1, :] + dt * gyro_biases_dot
        rph_filtered[ix, :] = rot2rph(so3_integrator(rot_mat, rot_mat_dot, dt))

    return rph_filtered, gyro_biases


def ahrs_hua_mahony_filter(
    angular_rate: Union[np.ndarray, List[float]],
    acceleration: Union[np.ndarray, List[float]],
    time: Union[np.ndarray, List[float]],
    magnetic_field: Union[np.ndarray, List[float]] = None,
    reference_magnetic_field: Union[np.ndarray, List[float]] = None,
    rph0: Union[np.ndarray, List[float]] = None,
    k1: Union[float, int] = 1.4,
    k2: Union[float, int] = 0.8,
    kp: Union[float, int] = 1.0,
    ki: Union[float, int] = 0.1,
    kb: Union[float, int] = 10.0,
    delta: Union[float, int] = 0.003,
) -> np.ndarray:
    """
    Estimates the attitude of a vehicle using the Hua-Mahony filter.

    This estimator proposed by Robert Mahony et al. [Mahony2008] is formulated as a deterministic kinematic observer
    on the Special Orthogonal group SO(3) driven by an instantaneous attitude and angular velocity measurements.
    The implementation includes modifications by Hua et al. [Hua2011] for measurement decoupling and anti-windup
    gyro-bias compensation.

    k1, k2, kp, ki, and kb tunning: Obtained from values proposed in [Hua2011].

    Args:
        angular_rate (Union[np.ndarray, List[float]]): Angular rate measurements (gyroscope data) in rad/s.
            Should be a 3xN or Nx3 array where N is the number of samples.
        acceleration (Union[np.ndarray, List[float]]): Acceleration measurements in m/s^2.
            Should be a 3xN or Nx3 array where N is the number of samples.
        time (Union[np.ndarray, List[float]]): Time vector in seconds. Should be a 1D array of length N.
        magnetic_field (Union[np.ndarray, List[float]], optional): Magnetic field measurements in microteslas.
            Should be a 3xN or Nx3 array where N is the number of samples. Defaults to None.
        reference_magnetic_field (Union[np.ndarray, List[float]], optional): Reference magnetic field vector.
            Should be a 1D array with 3 elements. Defaults to None.
        rph0 (Union[np.ndarray, List[float]], optional): Initial roll, pitch, and heading angles in radians.
        k1 (Union[float, int], optional): Gain for the accelerometer measurements. Defaults to 1.4.
        k2 (Union[float, int], optional): Gain for the magnetic field measurements. Defaults to 0.8.
        kp (Union[float, int], optional): Proportional gain. Defaults to 1.0.
        ki (Union[float, int], optional): Integral gain. Defaults to 0.1.
        kb (Union[float, int], optional): Anti-windup gain. Defaults to 10.0.
        delta (Union[float, int], optional): Saturation limit for the gyro biases. Defaults to 0.003.

    Returns:
        np.ndarray: Estimated roll, pitch, and heading (yaw) angles in radians. The output is an Nx3 array where
        N is the number of samples.

    Raises:
        TypeError: If any of the inputs are not of the expected type.
        ValueError: If any of the inputs do not have the expected dimensions.

    References:
        Mahony, R., Hamel, T., & Pflimlin, J. M. (2008). Nonlinear complementary filters on the special orthogonal group.
        IEEE Transactions on automatic control, 53(5), 1203-1218.
        Hua, M. D., Rudin, K., Ducard, G., Hamel, T., & Mahony, R. (2011). Nonlinear attitude estimation with measurement
        decoupling and anti-windup gyro-bias compensation. IFAC Proceedings Volumes, 44(1), 2972-2978.
        Martin, P., & Salaün, E. (2010). Design and implementation of a low-cost observer-based attitude and heading
        reference system. Control engineering practice, 18(7), 712-722.
    """
    # Convert lists to numpy arrays if necessary
    if isinstance(acceleration, list):
        acceleration = np.array(acceleration)
    if isinstance(angular_rate, list):
        angular_rate = np.array(angular_rate)
    if isinstance(time, list):
        time = np.array(time)
    if magnetic_field is not None and isinstance(magnetic_field, list):
        magnetic_field = np.array(magnetic_field)
    if reference_magnetic_field is not None and isinstance(
        reference_magnetic_field, list
    ):
        reference_magnetic_field = np.array(reference_magnetic_field)
    if rph0 is not None and isinstance(rph0, list):
        rph0 = np.array(rph0)

    # Validate inputs
    if not isinstance(acceleration, np.ndarray):
        raise TypeError("The acceleration must be a numpy array or a list.")
    if not isinstance(angular_rate, np.ndarray):
        raise TypeError("The angular rate must be a numpy array or a list.")
    if not isinstance(time, np.ndarray):
        raise TypeError("The time must be a numpy array or a list.")
    if magnetic_field is not None and not isinstance(magnetic_field, np.ndarray):
        raise TypeError("The magnetic field must be a numpy array or a list.")
    if reference_magnetic_field is not None and not isinstance(
        reference_magnetic_field, np.ndarray
    ):
        raise TypeError("The reference magnetic field must be a numpy array or a list.")
    if rph0 is not None and not isinstance(rph0, np.ndarray):
        raise TypeError(
            "The initial roll, pitch, and heading must be a numpy array or a list."
        )

    # Validate dimensions
    if acceleration.ndim != 2 or (
        acceleration.shape[0] != 3 and acceleration.shape[1] != 3
    ):
        raise ValueError("The acceleration must be a 3xN or Nx3 numpy array.")
    if angular_rate.ndim != 2 or (
        angular_rate.shape[0] != 3 and angular_rate.shape[1] != 3
    ):
        raise ValueError("The angular rate must be a 3xN or Nx3 numpy array.")
    if magnetic_field is not None:
        if magnetic_field.ndim != 2 or (
            magnetic_field.shape[0] != 3 and magnetic_field.shape[1] != 3
        ):
            raise ValueError("The magnetic field must be a 3xN or Nx3 numpy array.")
    if reference_magnetic_field is not None:
        reference_magnetic_field = reference_magnetic_field.squeeze()
        if reference_magnetic_field.ndim >= 2 or reference_magnetic_field.size != 3:
            raise ValueError(
                "The reference magnetic field must be a 1D numpy array with 3 elements."
            )
    if rph0 is not None:
        if rph0.ndim != 1 or rph0.shape[0] != 3:
            raise ValueError(
                "The initial roll, pitch, and heading must be a 1D numpy array with 3 elements."
            )

    # Ensure time is a 1D array
    time = time.squeeze()
    if time.ndim >= 2:
        raise ValueError("The time must be a (n, ), (n, 1) or (1, n) numpy array.")

    # Force Nx3 shape for acceleration, angular_rate, and magnetic_field
    if acceleration.shape[0] == 3 and acceleration.shape[1] != 3:
        acceleration = acceleration.T
    if angular_rate.shape[0] == 3 and angular_rate.shape[1] != 3:
        angular_rate = angular_rate.T
    if (
        magnetic_field is not None
        and magnetic_field.shape[0] == 3
        and magnetic_field.shape[1] != 3
    ):
        magnetic_field = magnetic_field.T

    # Validate gains
    if not isinstance(k1, (float, int)):
        raise TypeError("The k1 gain must be a float or integer.")
    k1 = float(k1)
    if not isinstance(k2, (float, int)):
        raise TypeError("The k2 gain must be a float or integer.")
    k2 = float(k2)
    if not isinstance(kp, (float, int)):
        raise TypeError("The kp gain must be a float or integer.")
    kp = float(kp)
    if not isinstance(ki, (float, int)):
        raise TypeError("The ki gain must be a float or integer.")
    ki = float(ki)
    if not isinstance(kb, (float, int)):
        raise TypeError("The kb gain must be a float or integer.")
    kb = float(kb)
    if not isinstance(delta, (float, int)):
        raise TypeError("The delta gain must be a float or integer.")
    delta = float(delta)

    # Create arrays to store the results
    samples = time.shape[0]
    rph_filtered = np.zeros([samples, 3])
    gyro_biases = np.zeros([samples, 3])

    if rph0 is not None:
        rph_filtered[0, :] = rph0

    # Reference gravity vector
    g_vec = np.array([0.0, 0.0, -1.0])
    g_vec = normalize(g_vec).reshape(3, 1)

    # Reference magnetic field vector
    if reference_magnetic_field is not None:
        m_vec = reference_magnetic_field
        m_vec = normalize(m_vec)
        m_vec = normalize(vec_to_so3(g_vec) @ m_vec).reshape(3, 1)  # Hua modification

    # Run the filter
    for ix in range(1, samples):
        # Gyroscope, accelerometer, and magnetic field measurements
        w = angular_rate[ix, :]
        a = normalize(acceleration[ix, :])
        if magnetic_field is not None:
            m = normalize(magnetic_field[ix, :])
            m = normalize(vec_to_so3(a) @ m)  # Hua modification

        rot_mat = rph2rot(rph_filtered[ix - 1, :])

        # Error measurement using accelerometer and magnetometer
        # Hua (2011) / Martin and Salaun (2010) - locally decouple
        wmes = k1 * (vec_to_so3(a) @ (rot_mat.T @ g_vec)).flatten()
        if magnetic_field is not None:
            wmes += k2 * (vec_to_so3(m) @ (rot_mat.T @ m_vec)).flatten()

        # Gyro bias update and filter adjustment
        rot_mat_dot = rot_mat @ (
            vec_to_so3(w - gyro_biases[ix - 1, :]) + kp * vec_to_so3(wmes)
        )
        # HUA modification
        gyro_biases_dot = -ki * wmes + kb * (
            saturate(gyro_biases[ix - 1, :], -delta, delta) - gyro_biases[ix - 1, :]
        )

        # Time step
        dt = time[ix] - time[ix - 1]

        # Update the gyro bias and the filtered roll, pitch, and heading
        gyro_biases[ix, :] = gyro_biases[ix - 1, :] + dt * gyro_biases_dot
        rph_filtered[ix, :] = rot2rph(so3_integrator(rot_mat, rot_mat_dot, dt))

    return rph_filtered, gyro_biases
