import warnings
import abel

import numpy as np

from scipy.interpolate import CubicSpline, interp1d, griddata, RegularGridInterpolator
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import minimize

from joblib import Parallel, delayed
import psutil

from tqdm import tqdm

n_jobs = psutil.cpu_count(logical=False)
FASTER = True
N_INTEG = 60

def create_knots(R, nknots, power=1):
    """
    Creates a sequence of knots for cubic spline interpolation, with an option to skew the distribution.

    Parameters:
    - R (float): The ending radial position.
    - nknots (int): The number of knots to be created between R0 and R.
    - power (float, optional): A factor to skew the distribution of the knots. A power > 1 skews the knots towards the ending position R, and a power < 1 skews them towards the starting position R0. Default is 1, which results in uniformly spaced knots.

    Returns:
    - array-like: A sequence of knot positions between R0 and R.
    """

    # Generate uniformly spaced points between 0 and 1.
    uniform_points = np.linspace(0, 1, nknots)

    # Skew the uniform points using the given power.
    skewed_points = np.power(uniform_points, power)

    # Scale and translate the skewed points to lie between R0 and R.
    return R * skewed_points


def PreCalculateF(kappa, theta, Np, Npy = 200, n_integ = N_INTEG):

    R   = Np // 2
    xj  = np.linspace(-R, R, Np)
    yi  = np.linspace(-R, R, Npy)

    if FASTER:
        X, Y = np.meshgrid(xj, yi)
        r = np.sqrt(X**2 + Y**2)

        # up_to_detector
        u = np.linspace(0, np.sqrt(r**2 - X**2), n_integ, axis=-1)
        a = kappa(np.sqrt(u**2 + X[..., np.newaxis]**2))
        
        A = np.trapz(a, x=u)
        A[Y<0] = 0.
        
        u = np.linspace(np.sqrt(r**2 - X**2),np.sqrt(R**2 - X**2) , n_integ, axis=-1)
        b = kappa(np.sqrt(u**2 + X[..., np.newaxis]**2))
        
        B = np.trapz(b, x=u)
        
        FS = 2*A+B
        
        # from_incoming_light
        rmin = np.cos(theta) * (X + Y * np.tan(theta))
        alpha = - 1 / np.tan(theta)
        beta  = X / np.tan(theta) + Y
        
        a       = 1 + alpha**2
        b       = 2 * alpha * beta
        c       = beta**2 - R**2
        Delta   = b**2 - 4 * a * c
        Delta_  = np.clip(Delta, 0, None)
        
        xleft = (-b - np.sqrt(Delta_))/2/a
        
        xmin = np.cos(theta) * rmin
        xright = np.where(rmin > 0, X, xmin)
        u = np.linspace(xleft, xright, n_integ, axis=-1)
        a = kappa((u**2 + (alpha * u + beta[..., np.newaxis])**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)
        A = np.trapz(a, x=u)

        A[rmin <= 0] = 0
        FI = A

        xright = np.where(rmin < 0, X, xmin)
        u = np.linspace(xleft, xright, n_integ, axis=-1)
        a = kappa((u**2 + (alpha * u + beta[..., np.newaxis])**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)
        A = np.trapz(a, x=u)

        A[rmin > 0] = 0
        FI += A

        FI[Delta<0] = 0.

    else:    

        def up_to_detector(x, y):
            r   = np.sqrt(x**2 + y**2)
            integrand   = lambda u: kappa(np.sqrt(u**2 + x**2))
            if y >= 0:
                return 2*quad(integrand, 0, np.sqrt(r**2 - x**2))[0] + quad(integrand, np.sqrt(r**2 - x**2), np.sqrt(R**2 - x**2))[0]
            else:
                return quad(integrand, np.sqrt(r**2 - x**2), np.sqrt(R**2 - x**2))[0]
        

        def from_incoming_light(x, y):
            rmin = np.cos(theta) * (x + y * np.tan(theta))
            alpha = - 1 / np.tan(theta)
            beta  = x / np.tan(theta) + y
            
            a       = 1 + alpha**2
            b       = 2 * alpha * beta
            c       = beta**2 - R**2
            Delta   = b**2 - 4 * a * c

            integrand = lambda w: kappa((w**2 + (alpha * w + beta)**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)

            if Delta >= 0:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", IntegrationWarning)
                    xleft   = (-b - np.sqrt(Delta))/2/a
                    if rmin >= 0:
                        xmin = np.cos(theta) * rmin
                        return quad(integrand, xleft, xmin)[0] + quad(integrand, xmin, x)[0]
                    else:
                        return quad(integrand, xleft, x)[0]
            else:
                return 0
        
        def calculate_values(j):
            FS_col = np.zeros(len(yi))
            FI_col = np.zeros(len(yi))
            for i in range(len(yi)):
                FS_col[i] = up_to_detector(xj[j], yi[i])
                FI_col[i] = from_incoming_light(xj[j], yi[i])
            return FS_col, FI_col


        results = Parallel(n_jobs=n_jobs)(delayed(calculate_values)(j) for j in range(len(xj)))

        FS = np.array([res[0] for res in results]).T
        FI = np.array([res[1] for res in results]).T
    FS = np.clip(FS, 0, 1)
    FI = np.clip(FI, 0, 1)
    
    return np.exp(-FS) * np.exp(-FI), np.exp(-FS), np.exp(-FI)


def forward_abel_transform(kappa, Np, F = None, n_integ = N_INTEG):
    R = Np // 2
    x = np.linspace(-R, R, Np)
    u = np.linspace(0, np.sqrt(R**2 - x**2), n_integ, axis=-1)
    ru = np.sqrt(x[..., np.newaxis]**2 + u**2)
    k = kappa(ru)

    if F is None:
        P = 2 * np.trapz(k, x=u)
    else:
        y = np.linspace(-R, R, F.shape[0])
        X, Y = np.meshgrid(x, y)
        ry = np.sqrt(X**2 + Y**2)
        
        mask = ~np.isnan(F)
        mask_pos = mask & (Y >= 0)
        mask_neg = mask & (Y <= 0)

        # Correctly handle the dimensions of the mask
        Fpos_interp = RegularGridInterpolator((y, x), np.where(mask_pos, F, 1), bounds_error=False, fill_value=1, method='linear')
        Fneg_interp = RegularGridInterpolator((y, x), np.where(mask_neg, F, 1), bounds_error=False, fill_value=1, method='linear')

        ru_flat = ru.flatten()
        x_flat = np.tile(x, n_integ)

        # Perform interpolation separately for Fpos and Fneg
        Fpos_flat = Fpos_interp((ru_flat, x_flat))
        Fneg_flat = Fneg_interp((ru_flat, x_flat))

        # Reshape to original ru shape
        Fpos = Fpos_flat.reshape(ru.shape)
        Fneg = Fneg_flat.reshape(ru.shape)

        P = np.trapz(k * (Fpos + Fneg), x=u)

    return P


def objective(params, S_exp, r_SAT, F, lambda_):
    """
    Objective function that calculates the root mean squared error between modeled and experimental data.

    Parameters:
    - params:
    - S_exp:
    - r_SAT:
    - F:
    - lambda_:

    Returns:
    - float:
    """

    *f_vals, alpha = params
    F       = F**alpha if F is not None else F

    f_vals = np.asarray(f_vals + [0])
    
    Np  = len(S_exp)
    R   = Np // 2

    kappa = CubicSpline(r_SAT, f_vals, bc_type = 'clamped')

    S_mod = forward_abel_transform(kappa, Np, F)
    # Compute the second derivative of the cubic spline
    kappa_double_prime = kappa.derivative(nu=2)

    # Compute the penalty term by integrating the squared second derivative over r_vals
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)  # This line will suppress the integration warnings
        penalty, _ = quad(lambda r: (kappa_double_prime(r))**2, r_SAT[0], R)
    
    error      = np.mean((S_mod - S_exp)**2)
    # if F is not None:
    #     print(f'Error: {error:.10e} | Penalty: {lambda_ * penalty:.10e} | Alpha: {alpha:.3f}')
    # else:
    #     print(f'Error: {error:.10e} | Penalty: {lambda_ * penalty:.10e}')
    return error + lambda_ * penalty
    
def OP(Sext, alpha = None, kappa = None):
    N   = len(Sext)
    A   = np.zeros((N, N))

    J, K = np.indices((N, N)) + 1

    mask        = J > K
    A[mask]     = 0

    mask        = J == K
    A[mask]   = np.sqrt(J[mask]**2 - (J[mask] - 0.5)**2)

    mask        = J < K
    A[mask]    = np.sqrt(K[mask]**2 - (J[mask] - 0.5)**2) - np.sqrt((K[mask] - 1)**2 - (J[mask] - 0.5)**2)

    if alpha is None:
        return np.linalg.solve(A, Sext / 2)
    else:
        L = np.zeros((N - 1, N))
        np.fill_diagonal(L, 1)
        np.fill_diagonal(L[:, 1:], -1)

        if kappa is None:
            return np.linalg.solve(A.T@A + alpha*A@L.T@L, A.T@Sext/2)
        else:
            C   = np.zeros((N , N))
            J, K = np.indices((N, N)) + 1

            sum_terms = np.array([[np.sum(A[j, k+1:] * kappa[k+1:]) for k in range(N)] for j in range(N)])
            sum_terms_2 = np.array([[np.sum(A[j, :k] * kappa[:k]) for k in range(N)] for j in range(N)])

            mask_j_eq_k = J == K
            mask_j_lt_k = J < K
            mask_k_lt_N = K < N

            # Case 2: j = k < N
            C[mask_j_eq_k & mask_k_lt_N] = A[mask_j_eq_k & mask_k_lt_N] * np.exp(-sum_terms[mask_j_eq_k & mask_k_lt_N]) * (1 + np.exp(-A[mask_j_eq_k & mask_k_lt_N] * kappa[K[mask_j_eq_k & mask_k_lt_N] - 1]))

            # Case 3: j < k < N
            C[mask_j_lt_k & mask_k_lt_N] = A[mask_j_lt_k & mask_k_lt_N] * np.exp(-sum_terms[mask_j_lt_k & mask_k_lt_N]) * (1 + np.exp(-2 * sum_terms_2[mask_j_lt_k & mask_k_lt_N] - A[mask_j_lt_k & mask_k_lt_N] * kappa[K[mask_j_lt_k & mask_k_lt_N] - 1]))

            # Case 4: j < k = N
            C[mask_j_lt_k & ~mask_k_lt_N] = A[mask_j_lt_k & ~mask_k_lt_N] * (1 + np.exp(-2 * sum_terms_2[mask_j_lt_k & ~mask_k_lt_N] - A[mask_j_lt_k & ~mask_k_lt_N] * kappa[K[mask_j_lt_k & ~mask_k_lt_N] - 1]))

            # Case 5: j = k = N
            C[mask_j_eq_k & ~mask_k_lt_N] = A[mask_j_eq_k & ~mask_k_lt_N] * (1 + np.exp(-A[mask_j_eq_k & ~mask_k_lt_N] * kappa[K[mask_j_eq_k & ~mask_k_lt_N] - 1]))

            A_array = C.T@C + alpha*C@L.T@L
            b_array = C.T@Sext

            x_array = np.linalg.solve(A_array, b_array)
            return x_array, np.linalg.inv(C.T) @ A_array @ x_array

def get_optimized_spline(S_exp, F=None, nknots=7, power=0.5, lambda_=1e3, bounds=None, initial_alpha=1.00, Kext = None):
    """
    Optimizes and returns a cubic spline based on the provided experimental signal.

    Parameters:
    - S_exp (array): The experimental signal data to fit.
    - F (array, optional): An optional trapping array.
    - nknots (int): Number of knots to use in the spline. Default is 7.
    - power (float): Power parameter for knot creation. Default is 0.5.
    - lambda_ (float): Regularization parameter for the optimization. Default is 1e3.
    - bounds (list of tuples, optional): Bounds for the spline parameters.
    - initial_alpha (float): Initial alpha value for extinction uncertainty. Default is 1.00.

    Returns:
    - CubicSpline object: The optimized cubic spline.
    - float: The optimized alpha value.
    - array: The optimized parameters except alpha.
    """

    Np  = len(S_exp)
    R   = Np // 2
    x   = np.linspace(-R, R, Np)
    
    if Kext is None:
        # Initial guess for inverse transform
        initial_guess = abel.daun.daun_transform(S_exp[x >= 0], direction='inverse', reg=('diff', 2e6), verbose = False)
    else:
        initial_guess = OP(S_exp[x>=0], alpha = 1e4, kappa = Kext)[0]
    
    # Create knots for spline
    knots = create_knots(R, nknots, power)
    
    if bounds is None:
        initial_spline = interp1d(np.linspace(0, R, len(initial_guess)), initial_guess, bounds_error=False, fill_value=0)
        spline_params = initial_spline(knots[:-1])  # Excluding the value at midpoint
        spline_params[spline_params < 0] = 0

        optimization_params = np.concatenate([spline_params, [initial_alpha]])
        bounds = [(0, None) for _ in spline_params] + [(1.00, 1.00)]
    else:
        spline_params = np.array([b for _, b in bounds])
        optimization_params = np.concatenate([spline_params, [initial_alpha]])
        bounds = bounds + [(1.00, 1.00)]

    # for i in range(1):
    #     objective(optimization_params,S_exp, knots, F, lambda_)
    # return
    # Optimization process
    optimization_result = minimize(objective, optimization_params, args=(S_exp, knots, F, lambda_), bounds=bounds, method='L-BFGS-B')
    
    return CubicSpline(knots, np.hstack([optimization_result.x[:-1], 0]), bc_type=((1, 0), (1, 0))), optimization_result.x[-1], optimization_result.x[:-1]

def sat(Sexp, Nknots=20, lambda_=1e6, power=0.5, parallel=False, N = None, center = None, CalculateF = False, Npy = 200, res = 1, Trapping = None, njobs = -1):
    """
    Performs Abel inversion on experimental data (Sexp) using optional parallel processing.

    The function adjusts each row in Sexp (considered as individual data sets) by fitting the integrated line-of-sight of the spline with specified parameters. The data can be processed either in parallel or sequentially.

    Parameters:
        Sexp (np.ndarray): The experimental data to be adjusted. Can be either 1D or 2D array.
        Nknots (int, optional): The number of knots to use for the spline fitting. Defaults to 20.
        lambda_ (float, optional): Regularization parameter for the spline fitting. Defaults to 1e6.
        power (float, optional): Knots distribution. Defaults to 0.5 (more knots in the outer region).
        parallel (bool, optional): Whether to process the data in parallel. Defaults to False.
        N (int, optional): The number of points to consider from the center of the data. If None, uses the full width.
        center (int, optional): The center point of the data for adjustment. If None, it is set to half of the data width.
        F (bool, optional): If True, the trapping factor is calculated.
        Npy (int, optional): Number of points for the calculation of trapping factor.
        res (float, optional): Resolution in px/mm or px/m. If the value is not given, then it is set to 1.
        Trapping (optional): If None, then trapping is not corrected like in LOSA. If an array is given, then trapping will be corrected.
    Returns:
        np.ndarray: The adjusted data as an array of the same shape as Sexp, with each row adjusted separately.

    Notes:
        - The spline adjustment is performed using the `get_optimized_spline` function.
        - When `parallel` is set to True, parallel computing is used to speed up the process, which is 
          especially beneficial for large data sets.
        - The `N` and `center` parameters allow focusing the adjustment on a specific segment of each data set.
    """
        
    # Check if data is 1D or 2D.
    if Sexp.ndim == 1:
        Sexp = Sexp.reshape(1, -1)
    
    if N is None:
        N = len(Sexp[0, :])  # Number of points
    
    if center is None:
        center = N//2
    
    Sexp = Sexp[:, center - N//2:center + N//2]

    if not parallel:
        # Sequential execution
        K = np.zeros((len(Sexp), N//2))
        F = np.zeros((len(Sexp), Npy, N))

        for i in range(len(Sexp)):
            if Trapping is None:
                fK, _, _ = get_optimized_spline(Sexp[i, :], nknots=Nknots, lambda_=lambda_, power=power)
                K[i] = fK(np.linspace(0, N//2, N//2))
                if CalculateF is True:
                    F[i] = PreCalculateF(fK, np.pi/4, N, Npy)[1]
            else:
                fK, _, _ = get_optimized_spline(Sexp[i, :], nknots=Nknots, lambda_=lambda_, power=power, F = Trapping[i])
                K[i] = fK(np.linspace(0, N//2, N//2))

        if CalculateF is True:
            return K, F
        else:
            return K
    else:
        ROWS, COLS = Sexp.shape

        args_list = []
        for j in range(ROWS):
            Kext_j = Trapping[j] if Trapping is not None else None

            args = (Sexp[j, :], COLS, Nknots, power, lambda_, Kext_j)
            args_list.append(args)

        with Parallel(n_jobs=njobs) as parallel:
            K = np.array(parallel(delayed(process_row)(*args) for args in tqdm(args_list)))
        
        K[K < 0] = 0

        return K.reshape((ROWS, COLS//2)) * res
    

def process_row(Sexp, COLS, nknots, power, lambda_, Kext_j = None):
    if Kext_j is None:
        fK, _, _ = get_optimized_spline(Sexp, nknots=nknots, power=power, lambda_=lambda_)
    else:
        knots = create_knots(COLS//2, nknots, power)
        fKext = CubicSpline(np.linspace(0, COLS//2, COLS//2), Kext_j, bc_type='clamped')
        fKext = CubicSpline(knots, fKext(knots), bc_type='clamped')
        F     = PreCalculateF(fKext, np.pi/4, COLS, Npy = 50)[1]
        fK, _, _ = get_optimized_spline(Sexp, nknots=nknots, power=power, lambda_=lambda_, F = F, Kext = Kext_j)

    return fK(np.linspace(0, COLS//2, COLS//2))

    # else:
    #     # Parallel execution
    #     # First, get all optimized splines in parallel
    #     optimized_splines = Parallel(n_jobs=-1)(
    #         delayed(lambda x: get_optimized_spline(x, nknots=Nknots, lambda_=lambda_, power=power)[0])(Sexp[i, :])
    #         for i in range(len(Sexp))
    #     )
    #     # Then, evaluate each spline over the desired range
    #     return np.array([
    #         spline(np.linspace(0, N // 2, N // 2))
    #         for spline in optimized_splines
    #     ])



