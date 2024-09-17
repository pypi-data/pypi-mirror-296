from typing import Tuple

import numpy as np
from scipy.linalg import expm

from navlib.math import vec_to_so3


def _kf_lti_discretize(
    Ac: np.ndarray,
    Bc: np.ndarray = None,
    Qc: np.ndarray = None,
    dt: float = 1,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Discretize a Linear Time-Invariant (LTI) system using the matrix fraction decomposition
    for use in a discrete-time Kalman filter.

    Args:
        Ac (np.ndarray): Continuos state transition matrix.
        Bc (np.ndarray): Continuos input matrix, by default None.
        Qc (np.ndarray): Continuos covariance matrix, by default None.
        dt (float): Time step, by default 1.

    Returns:
        np.ndarray: Discrete state transition matrix.
        np.ndarray: Discrete input matrix.
        np.ndarray: Discrete covariance matrix.
    """
    # Check the number of states
    n = Ac.shape[0]

    # Default to zero non provided matrices
    if Bc is None:
        Bc = np.zeros([n, 1])

    if Qc is None:
        Qc = np.zeros([n, n])

    # Discretize state transition and input matrix (close form)
    # Ad = expm(Ac*dt)
    M = np.vstack([np.hstack([Ac, Bc]), np.zeros([1, n+1])])
    ME = expm(M*dt)

    # Discretize state transition and input matrix
    Ad = ME[:n, :n]
    Bd = ME[:n, n:]

    # Discretize Covariance: by (Van Loan, 1978)
    F = np.vstack([np.hstack([-Ac, Qc]), np.hstack([np.zeros([n, n]), Ac.T])])
    G = expm(F*dt)
    Qd = np.dot(G[n:, n:].T, G[:n, n:])

    # # Discretize Covariance: by matrix fraction decomposition
    # Phi = vstack([hstack([Ac,            Qc]),
    #               hstack([np.zeros([n,n]),-Ac.T])])
    # AB  = np.dot (scipy.linalg.expm(Phi*dt), vstack([np.zeros([n,n]),np.eye(n)]))
    # Qd  = np.linalg.solve(AB[:n,:].T, AB[n:2*n,:].T).T

    return Ad, Bd, Qd


def _kf_predict(
    x: np.ndarray,
    P: np.ndarray,
    A: np.ndarray = None,
    Q: np.ndarray = None,
    B: np.ndarray = None,
    u: np.ndarray = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prediction step of the Kalman filter.

    Args:
        x (np.ndarray): State mean.
        P (np.ndarray): State covariance.
        A (np.ndarray): State transition matrix, by default None.
        Q (np.ndarray): Process noise covariance, by default None.
        B (np.ndarray): Input matrix, by default None.
        u (np.ndarray): Input vector, by default None.

    Returns:
        np.ndarray: Updated state mean.
        np.ndarray: Updated state covariance.
    """

    # Check Arguments
    n = A.shape[0]

    # Default state transition matrix to the identity matrix if not provided
    if A is None:
        A = np.eye(n)

    # Default process noise covariance to zero matrix if not provided
    if Q is None:
        Q = np.zeros([n, 1])

    # Default input matrix to the identity matrix if not provided
    if (B is None) and (u is not None):
        B = np.eye([n, u.shape(u)[0]])

    # Prediction step
    # State
    if u is None:
        x = np.dot(A, x)
    else:
        x = np.dot(A, x) + np.dot(B, u)

    # Covariance
    P = np.dot(np.dot(A, P), A.T) + Q

    return x, P


def _kf_update(
    x: np.ndarray,
    P: np.ndarray,
    y: np.ndarray,
    H: np.ndarray,
    R: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Update step of the Kalman filter.

    Args:
        x (np.ndarray): State mean.
        P (np.ndarray): State covariance.
        y (np.ndarray): Measurement.
        H (np.ndarray): Measurement matrix.
        R (np.ndarray): Measurement noise covariance.
    """
    # Compute measurement residual
    dy = y - np.dot(H, x)
    # Compute covariance residual
    S = R + np.dot(np.dot(H, P), H.T)
    # Compute Kalman Gain
    K = np.dot(np.dot(P, H.T), np.linalg.inv(S))

    # Update state estimate
    dy = dy.flatten()
    x = x + np.dot(K, dy)
    P = P - np.dot(np.dot(K, H), P)

    return x, P, K, dy, S


def _kf_transition_matrix(angular_rate: np.ndarray) -> np.ndarray:
    """
    Compute the transition matrix for the Kalman filter.
    """
    angular_rate = angular_rate.flatten() if isinstance(angular_rate, np.ndarray) else angular_rate
    skew_symmetric_angular_rate = vec_to_so3(angular_rate)
    a_matrix = np.zeros((6, 6))
    a_matrix[:3, :] = np.hstack([-skew_symmetric_angular_rate, skew_symmetric_angular_rate])
    return a_matrix
