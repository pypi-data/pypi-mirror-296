import numpy as np
from scipy.linalg import svd
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.interpolate import Akima1DInterpolator
from scipy.ndimage import gaussian_filter
import cam_ilt.utils as ut


def kernel_setup(t1, T1_min, T1_max, DataType, N_T1):
    """
    This returns the kernel matrix as K1 and a vector of N_T1 log spaced relaxation
    times or diffusion coefficients ranging from T1_min to T1_max as T1. If data type
    "custom" is used only T1 is returned. 
    
    Parameters
    ----------
    t1 : Logarithmically spaced time delays used for relaxation encoding or diffusion
    encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 (for reference:
    https://doi.org/10.1063/1.1673336 )
    
    T1_min : Minimum relaxation time or diffusion coefficient to consider
    
    T1_max : Maximum relaxation time or diffusion coefficient to consider
    
    DataType : Type of experiment. Options are 'T1sat' for  T1 saturation recovery,
    'T1inv' for T1 inversion recovery, 'D' for any Stejskal-Tanner (see above reference)
    like diffusion experiment, 'T2' for common mono-exponential T2 encodings and 'custom'
    if an user-defined custom kernel is provided
    
    N_T1 : Number of points in the vector T1
    
    """
    T1 = np.logspace(np.log10(T1_min), np.log10(T1_max), N_T1)

    if DataType == 'T1sat':
        Kernel_1 = lambda Tau, TimeConst: 1 - np.exp(-Tau * (1 / TimeConst))
        
    elif DataType == 'T1inv':
        Kernel_1 = lambda Tau, TimeConst: 1 - 2 * np.exp(-Tau * (1 / TimeConst))
        
    elif DataType == 'D':
        Kernel_1 = lambda Tau, Diff: np.exp(-Tau * Diff)
        
    elif DataType == 'T2':
        Kernel_1 = lambda Tau, TimeConst: np.exp(-Tau * (1 / TimeConst))
        
    elif DataType == 'custom':
        print('Using custom kernel')
        return T1
        
    else:
        raise ValueError('Invalid Data Type')

    K1 = Kernel_1(t1[:, None], T1)
        
    return K1, T1


def svd_kernel_compression(T1, NormNoise, N_max, NormData, K1):
    """
    This function uses singular value decomposition (SVD) to compress the kernel 
    matrix (K1) as well as the experimental data (NormData). Using SVD K1 can be
    rearranged to:
        
        K1 = U1 @ S1 @ V1.T
        
    S1 is a diagonal matrix and in the case of the applied compression, only elements
    with S1 > NormNoise are kept (also truncating columns of U1 and V1 accordingly). 
    Hence K1 can be rewritten:
        
        K1 = U1_com @ S1_com @ V1_com.T  with _com indicating compression
        
    Considering now that if noise is neglected the experimental data is given as:
        
        NormData = K1 @ Dis 
        
    with Dis being the distribution we want to estimate. Hence, the experimental
    data can be compressed as follows:
        
       CompressedData =  U1_com.T @ NormData = S1 @ V1.T @ Dis
       
    In this case, it was used that U1/U1_com (and V1/V1_com) are unitary and real 
    matrices, which have the property that the transpose equals the inverse.
    Consequently, this function returns CompressedData and the compressed kernel K
    given by S1 @ V1.T
    

    Parameters
    ----------
    T1 : Logarithmically spaced relaxation times or diffusion coefficient.
    
    NormNoise : Normalized noise, for normalization see cam_ilt.utils.norm_noise_and_data
    
    N_max : Square root of the maximum number of singular values kept in S1
    
    NormData : Normalized data, for normalization see cam_ilt.utils.norm_noise_and_data
        
    K1 : kernel matrix

    Returns
    -------
    K : Compressed kernel
    
    CompressedData : Compressed experimental data
    
    alpha_guess : initial guess for the hyperparameter alpha calculated from S1_com.
    For reference: https://doi.org/10.1016/j.pnmrs.2011.07.002
        
    n : number of diagonal elements in S1_com

    """
    print('Computing singular values...')
    U1, S1, V1 = svd(K1, full_matrices=False)
    V1 = V1.T
    index = S1 > NormNoise
    S = S1[index]
    if len(S) > N_max**2:
        S = S[:N_max**2]
        index[(N_max**2):] = False
    n = len(S)
    i1 = np.mod((np.where(index)[0] + 1), len(S1))
    i1[i1 == 0] = len(S1)
    i1 = i1 - 1 #due to 0 ind in py
    U = np.zeros((len(NormData.flatten('F')), n))
    V = np.zeros((len(T1), n))
    for i in range(n):
        U[:, i] = U1[:, i1[i]]
        V[:, i] = V1[:, i1[i]]

    alpha_guess = np.sum(S**2) / n
    CompressedData = U.T @ NormData.flatten('F')
    CompressedData /= np.max(np.abs(CompressedData))
    CompressedData = np.expand_dims(CompressedData, 1)
    K = np.diag(S) @ V.T
    print(f'Number of singular values = {n}')

    return K, CompressedData, alpha_guess, n


def calc_d2_mat(N_T1):
    """
    This returns the matrix D2 which performs the second derivative if applied to
    a vector. For reference: https://doi.org/10.1016/j.jmr.2017.08.017 

    Parameters
    ----------
    N_T1 : Number of relaxation times or diffusion coefficients

    """
    D2 = (np.diag(np.ones(N_T1 - 1), -1) + np.diag(-2 * np.ones(N_T1), 0) + 
         np.diag(np.ones(N_T1 - 1), 1))
    D2[-2:,:] = 0

    return D2


def init_primal_dual(K, N_T1):
    """
    Initializes variables for 1D primal dual algorithm.
    For reference: https://doi.org/10.1016/j.jmr.2017.08.017 

    Parameters
    ----------
    K : Compressed kernel, see cam_ilt.reg_inv.d1.svd_kernel_compression 
    
    N_T1 : Number of relaxation times or diffusion coefficients
        
    Returns
    -------
    Y1 : Initialized as zero vector of length N_T1
        
    Y2 : identical to Y1
    
    F : Initialized as uniform distribution of length K.shape[1]
        
    W : identical to F
    
    F_tilde : identical to F
    
    W_tilde :  identical to F
    
    """
    Y1 = np.zeros((N_T1, 1))
    Y2 = np.zeros((N_T1, 1))
    F = np.ones((K.shape[1], 1)) / K.shape[1]
    W = np.ones((K.shape[1], 1)) / K.shape[1]
    F_tilde = np.copy(F)
    W_tilde = np.copy(W)

    return Y1, Y2, F, W, F_tilde, W_tilde


def primal_dual_mtgv(CompressedData, Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, 
                     alpha, beta, tau, sigma, N_T1):
    """
    1D primal dual algorithm for MTGV regularization. 
    For reference: https://doi.org/10.1016/j.jmr.2017.08.017 

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    Y1 : Auxilliary vector for primal dual algorithm. See above reference for 
    further explanation. 
    
    Y2 : Also an auxilliary vector. See above reference for further explanation.
        
    F : Distribution to estimate, not normalized.
    
    W : Auxilliary vector to enforce smoothness on the to-be-estimated distribution.
    See above reference for further explanation.
    
    F_tilde : F_tilde_k = 2 * F_k - F_(k - 1), k indicating the kth iteration
    
    W_tilde : W_tilde_k = 2 * W_k - F_(k - 1), k indicating the kth iteration
        
    K : Compressed kernel  
        
    B : Proximal operator. See https://doi.org/10.17863/CAM.104179 chapter 3.4
    equation 3.19 for further reference.
        
    D2 : matrix which performs the second derivative. See cam_ilt.reg_inv.d1.calc_d2_mat
        
    alpha : Hyperparameter which controlls the fidelity of the to-be-estimated
    distribution towards the experimental data. See first reference for further 
    explanation.
    
    beta : Hyperparamater which controlls the amount of smoothness enforced on 
    the to-be-estimated distribution. 
        
    tau : Convergence parameter. See initial reference for further explanation
    
    sigma : Convergence parameter. See initial reference for further explanation
        
    N_T1 : Number of relaxation times or diffusion coefficients

    """
    Y1_tilde = Y1 + sigma * (F_tilde - W_tilde)
    Y1 = Y1_tilde / np.maximum(1, np.abs(Y1_tilde))
    F_ = np.copy(F)
    F = B @ (F - tau * Y1 + tau * alpha * (K.T @ CompressedData))
    F = np.maximum(0, F)
    Y2_tilde = Y2 + sigma * D2 @ W_tilde    
    X = np.abs(Y2_tilde)
    Y2 = Y2_tilde / np.maximum(1, X / beta)
    W_ = np.copy(W)
    W = W + tau * (Y1 - D2.T @ Y2)
    F_tilde = 2 * F - F_
    W_tilde = 2 * W - W_
    
    return Y1, Y2, F, W, F_tilde, W_tilde


def mtgv_gcv_brd_optim(NormNoise, n, N_max, beta_guess, N_T1, K, alpha_guess, 
                       CompressedData, tol_alpha, tol, beta_lim):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and the Butler-Reeds-Dawson (BRD) method. 
    For further reference: https://doi.org/10.48550/arXiv.2311.11442

    Parameters
    ----------
    NormNoise : Normalized noise, for normalization see cam_ilt.utils.norm_noise_and_data
    
    n : Number of diagonal elements in the diagonal matrix S. For more details 
    see cam_ilt.reg_inv.svd_kernel_compression
        
    N_max : Maximum number of iterations
    
    beta_guess : Initial guess for the hyperparameter beta. In practise, for the
    author of this toolbox 1e-10 was usually a very reliable initial guess, but
    as long as it is not choosen too large (because beta updates will increase its
    value) larger values such as 1e-8 will most likely also be fine.
    
    N_T1 : Number of relaxation times or diffusion coefficients
    
    K : Compressed Kernel
    
    alpha_guess : Initial guess of the hyperparameter alpha. For more details
    see cam_ilt.reg_inv.svd_kernel_compression
    
    CompressedData : Compressed experimental data
    
    tol_alpha : Relative convergence tolerance for alpha calculated such that:
        
        abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < tol_alpha
        
    with k indicating the kth iteration.
        
    tol : Relative convergence tolerance for F calculated such that:
        
        norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < tol
        
    with k indicatin the kth iteration and F being the non-normalized estimated 
    distribution.
        
    beta_lim : Limits for the hyperparameter beta. In practise, for the author
    of this toolbox [1e-12, 1e2] turned out be very realliable limits. The Butler-
    Reeds-Dawson (BRD) beta update is usually highly sparse and often less than 10 beta 
    values will be explored if the proposed range is used. Also the lower limit
    should be choosen smaller than beta_guess, because although very rarely observed 
    it is not to exclude that the BRD beta update might lead to a decrease in beta
    value although in the vast majority of cases beta does monotonically increase
    from beta_guess up to the upper beta limit

    Returns
    -------
    Dis : A list of normalized distributions. The number of distributions is equal
    to the number of betas explored because a new distribution is estimated for
    every beta.
    
    Score : Dictionary with the entries 'Chis' and 'Chis_beta'. 'Chis' will include
    a list of vectors with every vector including the GCV scores calculated for 
    every iteration during a single alpha estimation. The number of GCV score 
    vectors in the list is equal to the number of betas explored, because a full 
    alpha estimation is run for every explored beta. 'Chis_beta' will include a 
    single vector including the BRD scores for every explored beta.
        
    Hy_Par : Dictionary with the entries 'Alphas' and 'Betas'. 'Alphas' will include
    a list of vectors with every vector including the alpha values calculated for
    every iteration during a single alpha estimation. The number of alpha vectors 
    in the list is equal to the number of betas explored, because a full alpha 
    estimation is run for every explored beta. 'Betas' will include a single 
    vector including the beta values for every explored beta.

    """
    tau = 0.1
    sigma = 0.1
    Score = {'Chis': [None] * N_max.item(), 'Chis_beta': np.zeros(N_max)}
    Hy_Par = {'Alphas': [None] * N_max.item(), 'Betas': np.zeros(N_max)}
    Dis = [None] * N_max.item()
    con_beta = True
    beta = np.copy(beta_guess)
    i = 0
    D2 = calc_d2_mat(N_T1)
    options = {'disp': False, 'maxiter': 100}

    while con_beta:
        Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
        con = True
        Hy_Par['Alphas'][i] = np.zeros(N_max)
        Score['Chis'][i] = np.zeros(N_max)
        k = 0
        alpha = 1 / alpha_guess
        u_ = np.ones(K.shape[1])
        arg = (CompressedData, Y1, F, K, alpha, tau)

        while con:
            result = minimize(ut.min_u, u_, args = arg, method = 'trust-krylov', 
                              jac = ut.grad_min_u, hess = ut.hess_min_u, options = options)
            u = np.maximum(-F + tau * Y1, np.expand_dims(result.x, 1))
            u_ = np.squeeze(u, 1)

            Hy_Par['Alphas'][i][k] = np.copy(alpha)
            alpha, chi = ut.gcv_alpha_primal_dual(CompressedData, K, Y1, F, u, n, 
                                               alpha, tau)
            Score['Chis'][i][k] = np.copy(chi)
            
            if k > 0:
                delta = np.abs((Score['Chis'][i][k] - Score['Chis'][i][k - 1]) 
                            / Score['Chis'][i][k - 1])
                
                if (k == (N_max - 1) or delta < tol_alpha or Hy_Par['Alphas'][i][k] 
                    < 1e-12 or Hy_Par['Alphas'][i][k] > 1e12):  
                    
                    con = False
                    Score['Chis'][i] = Score['Chis'][i][Hy_Par['Alphas'][i] > 0]
                    Hy_Par['Alphas'][i] = Hy_Par['Alphas'][i][Hy_Par['Alphas'][i] > 0]                    
            
            print('----------------------------')
            print('1st Primal Dual: Alpha-Estimation')
            print(f'Alpha = {alpha}')
            print(f'Chi = {chi}')
            print(f'Count = {k}')
            print(f'Beta = {beta}')
            print('----------------------------')
            
            k += 1
            B = ut.calc_b_mat(K, tau, alpha)    
            Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
                CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
                beta, tau, sigma, N_T1)

        Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
        epsilon = 1
        Count = 0
        alpha = Hy_Par['Alphas'][i][k - 1]
        B = ut.calc_b_mat(K, tau, alpha)

        while epsilon > tol:
            Count += 1
            F_ = np.copy(F)
            Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
                CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
                beta, tau, sigma, N_T1)
            epsilon = np.linalg.norm(F - F_, 2) / np.linalg.norm(F_, 2)

            if Count >= 1e5:
                break

        Hy_Par['Betas'][i] = beta
        beta, chi_beta = ut.brd_beta(CompressedData, K, F, NormNoise, n, beta)
        Score['Chis_beta'][i] = np.copy(chi_beta)
        
        if i > 0:
            if (Hy_Par['Betas'][i] < beta_lim[0] or i == (N_max - 1) or 
                Hy_Par['Betas'][i] > beta_lim[1]):
                
                con_beta = False
                Hy_Par['Betas'] = Hy_Par['Betas'][:i + 1]
                Score['Chis_beta'] = Score['Chis_beta'][:i + 1]
        
        Dis[i] = F / np.sum(F)
        
        print('----------------------------')
        print('2nd Primal Dual: Dis-Estimation')
        print(f'Alpha = {alpha}')
        print(f'Count = {Count}')
        print(f'Beta = {Hy_Par["Betas"][i]}')
        print(f'Chi_beta = {Score["Chis_beta"][i]}')
        print('----------------------------')
        
        i += 1

    Hy_Par['Alphas'] = [alpha for alpha in Hy_Par['Alphas'] if alpha is not None]
    Score['Chis'] = [chi for chi in Score['Chis'] if chi is not None]
    Dis = [d for d in Dis if d is not None]

    return Dis, Score, Hy_Par


def mtgv_gcv_bp_optim(NormNoise, n, N_max, beta_guess, N_T1, K, 
                       alpha_guess, CompressedData, tol_alpha, tol, gamma):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and balancing principle (BP). 
    
    For further reference: 
        
       General method: https://doi.org/10.48550/arXiv.2311.11442
       BP: https://doi.org/10.1016/j.amc.2022.127809
       
    In comparison to cam_ilt.reg_inv.d1.mtgv_gcv_brd_optim, which employs BRD for
    updating beta and tends to explore beta across many orders of magnitude, the 
    BP method does quite the opposite and tends to vary beta only across a small
    range. Hence, this algorithm is more sensitive regarding the initial choice of
    beta_guess.

    Parameters
    ----------
    NormNoise : Normalized noise, for normalization see cam_ilt.utils.norm_noise_and_data
    
    n : Number of diagonal elements in the diagonal matrix S. For more details 
    see cam_ilt.reg_inv.svd_kernel_compression
        
    N_max : Maximum number of iterations
    
    beta_guess : Initial guess for the hyperparameter beta. In practise, for the
    author of this toolbox 1e-8 was usually a very reliable initial guess, but
    this might need some tweaking depending on the users data. 
    
    N_T1 : Number of relaxation times or diffusion coefficients
    
    K : Compressed Kernel
    
    alpha_guess : Initial guess of the hyperparameter alpha. For more details
    see cam_ilt.reg_inv.svd_kernel_compression
    
    CompressedData : Compressed experimental data
    
    tol_alpha : Relative convergence tolerance for alpha calculated such that:
        
        abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < tol_alpha
        
    with k indicating the kth iteration.
        
    tol : Relative convergence tolerance for F calculated such that:
        
        norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2)
        
    with k indicatin the kth iteration and F being the non-normalized estimated 
    distribution.
    
    gamma: Additional hyperparameter. In practise, for the author of this toolbox
    a value of 1e-7 worked well, but changes might be necessary here depending
    on the users data.

    Returns
    -------
    Dis :  Normalized distribution
    
    """
    tau = 0.1
    sigma = 0.1
    Score = {'Chis': [None] * N_max.item()}
    Hy_Par = {'Alphas': [None] * N_max.item(), 'Betas': np.zeros(N_max)}
    con_beta = True
    beta = np.copy(beta_guess)
    i = 0
    D2 = calc_d2_mat(N_T1)
    options = {'disp': False, 'maxiter': 100}

    while con_beta:
        Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
        con = True
        Hy_Par['Alphas'][i] = np.zeros(N_max)
        Score['Chis'][i] = np.zeros(N_max)
        k = 0
        alpha = 1 / alpha_guess
        u_ = np.ones(K.shape[1])
        arg = (CompressedData, Y1, F, K, alpha, tau)

        while con:
            result = minimize(ut.min_u, u_, args = arg, method = 'trust-krylov', 
                              jac = ut.grad_min_u, hess = ut.hess_min_u, options = options)
            u = np.maximum(-F + tau * Y1, np.expand_dims(result.x, 1))
            u_ = np.squeeze(u, 1)

            Hy_Par['Alphas'][i][k] = np.copy(alpha)
            alpha, chi = ut.gcv_alpha_primal_dual(CompressedData, K, Y1, F, u, n, 
                                               alpha, tau)
            Score['Chis'][i][k] = np.copy(chi)
            
            if k > 0:
                delta = np.abs((Score['Chis'][i][k] - Score['Chis'][i][k - 1]) 
                            / Score['Chis'][i][k - 1])
                
                if (k == (N_max - 1) or delta < tol_alpha or Hy_Par['Alphas'][i][k] 
                    < 1e-12 or Hy_Par['Alphas'][i][k] > 1e12):  
                    
                    con = False
                    Score['Chis'][i] = Score['Chis'][i][Hy_Par['Alphas'][i] > 0]
                    Hy_Par['Alphas'][i] = Hy_Par['Alphas'][i][Hy_Par['Alphas'][i] > 0]                    
            
            print('----------------------------')
            print('1st Primal Dual: Alpha-Estimation')
            print(f'Alpha = {alpha}')
            print(f'Chi = {chi}')
            print(f'Count = {k}')
            print(f'Beta = {beta}')
            print('----------------------------')
            
            k += 1
            B = ut.calc_b_mat(K, tau, alpha)
            Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
                CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
                beta, tau, sigma, N_T1)

        Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
        epsilon = 1
        Count = 0
        alpha = Hy_Par['Alphas'][i][k - 1]
        B = ut.calc_b_mat(K, tau, alpha)

        while epsilon > tol:
            Count += 1
            F_ = np.copy(F)
            Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
                CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
                beta, tau, sigma, N_T1)
            epsilon = np.linalg.norm(F - F_, 2) / np.linalg.norm(F_, 2)

            if Count >= 1e5:
                break

        Hy_Par['Betas'][i] = beta
        beta = ut.bp_beta(CompressedData, K, F, W, D2, alpha, gamma)     
        
        if i > 0:
            delta_beta = np.abs((Hy_Par['Betas'][i] - Hy_Par['Betas'][i - 1]) / 
                       Hy_Par['Betas'][i - 1])
            
            if (delta_beta < tol_alpha or i == (N_max - 1) or Hy_Par['Betas'][i] 
                < 1e-12 or Hy_Par['Betas'][i] > 1e12):
                
                con_beta = False
                Hy_Par['Betas'] = Hy_Par['Betas'][:i + 1]
                
        print('----------------------------')
        print('2nd Primal Dual: Dis-Estimation')
        print(f'Alpha = {alpha}')
        print(f'Count = {Count}')
        print(f'Beta = {Hy_Par["Betas"][i]}')
        print('----------------------------')
        
        i += 1

    Dis = F / np.sum(F)

    return Dis


def mtgv_gcv_fb_optim(NormNoise, n, N_max, beta, N_T1, K, alpha_guess, 
                      CompressedData, tol_alpha, tol):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and a fixed value for beta. 
    For further reference: https://doi.org/10.48550/arXiv.2311.11442

    Parameters
    ----------
    NormNoise : Normalized noise, for normalization see cam_ilt.utils.norm_noise_and_data
    
    n : Number of diagonal elements in the diagonal matrix S. For more details 
    see cam_ilt.reg_inv.svd_kernel_compression
        
    N_max : Maximum number of iterations
    
    beta : Fixed value for the hyperparameter beta
    
    N_T1 : Number of relaxation times or diffusion coefficients
    
    K : Compressed Kernel
    
    alpha_guess : Initial guess of the hyperparameter alpha. For more details
    see cam_ilt.reg_inv.svd_kernel_compression
    
    CompressedData : Compressed experimental data
    
    tol_alpha : Relative convergence tolerance for alpha calculated such that:
        
        abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < tol_alpha
        
    with k indicating the kth iteration.
        
    tol : Relative convergence tolerance for F calculated such that:
        
        norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2)
        
    with k indicatin the kth iteration and F being the non-normalized estimated 
    distribution.

    Returns
    -------
    Dis : Normalized distribution
    
    """
    tau = 0.1
    sigma = 0.1
    i = 0
    D2 = calc_d2_mat(N_T1)
    options = {'disp': False, 'maxiter': 100}
    Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
    con = True
    Hy_Par = {'Alphas': np.zeros(N_max)}
    Score = {'Chis': np.zeros(N_max)}
    alpha = 1 / alpha_guess
    u_ = np.ones(K.shape[1])
    arg = (CompressedData, Y1, F, K, alpha, tau)

    while con:
        result = minimize(ut.min_u, u_, args = arg, method = 'trust-krylov', 
                          jac = ut.grad_min_u, hess = ut.hess_min_u, options = options)
        u = np.maximum(-F + tau * Y1, np.expand_dims(result.x, 1))
        u_ = np.squeeze(u, 1)

        Hy_Par['Alphas'][i] = np.copy(alpha)
        alpha, chi = ut.gcv_alpha_primal_dual(CompressedData, K, Y1, F, u, n, 
                                           alpha, tau)
        Score['Chis'][i] = np.copy(chi)
        
        if i > 0:
            delta = np.abs((Score['Chis'][i] - Score['Chis'][i - 1]) 
                        / Score['Chis'][i - 1])
            
            if (i == (N_max - 1) or delta < tol_alpha or Hy_Par['Alphas'][i] 
                < 1e-12 or Hy_Par['Alphas'][i] > 1e12):  
                
                con = False
                Score['Chis'] = Score['Chis'][Hy_Par['Alphas'] > 0]
                Hy_Par['Alphas'] = Hy_Par['Alphas'][Hy_Par['Alphas'] > 0]                
        
        print('----------------------------')
        print('1st Primal Dual: Alpha-Estimation')
        print(f'Alpha = {alpha}')
        print(f'Chi = {chi}')
        print(f'Count = {i}')
        print(f'Beta = {beta}')
        print('----------------------------')
        
        i += 1
        B = ut.calc_b_mat(K, tau, alpha)
        Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
            CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
            beta, tau, sigma, N_T1)

    Y1, Y2, F, W, F_tilde, W_tilde = init_primal_dual(K, N_T1)
    epsilon = 1
    Count = 0
    alpha = Hy_Par['Alphas'][i - 1]
    B = ut.calc_b_mat(K, tau, alpha)

    while epsilon > tol:
        Count += 1
        F_ = np.copy(F)
        Y1, Y2, F, W, F_tilde, W_tilde = primal_dual_mtgv(
            CompressedData,Y1, Y2, F, W, F_tilde, W_tilde, K, B, D2, alpha, 
            beta, tau, sigma, N_T1)
        epsilon = np.linalg.norm(F - F_, 2) / np.linalg.norm(F_, 2)

        if Count >= 1e5:
            break
    
    print('----------------------------')
    print('2nd Primal Dual: Dis-Estimation')
    print(f'Alpha = {alpha}')
    print(f'Count = {Count}')
    print(f'Beta = {beta}')
    print('----------------------------')

    Dis = F / np.sum(F)           

    return Dis


def l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                 CompressedData, tol_alpha, tol):
    """
    Algorithm to estimate the searched for distribution using L1 regularization
    in combination with generalized cross-validation (GCV).
    
    For further reference: 
        
        GCV: https://doi.org/10.48550/arXiv.2311.11442
        L1 regularization: https://doi.org/10.1016/j.jmr.2017.05.010

    Parameters
    ----------
    NormNoise : Normalized noise, for normalization see cam_ilt.utils.norm_noise_and_data
    
    n : Number of diagonal elements in the diagonal matrix S. For more details 
    see cam_ilt.reg_inv.svd_kernel_compression
        
    N_max : Maximum number of iterations
    
    beta : Fixed value for the hyperparameter beta
    
    N_T1 : Number of relaxation times or diffusion coefficients
    
    K : Compressed Kernel
    
    alpha_guess : Initial guess of the hyperparameter alpha. For more details
    see cam_ilt.reg_inv.svd_kernel_compression
    
    CompressedData : Compressed experimental data
    
    tol_alpha : Relative convergence tolerance for alpha calculated such that:
        
        abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < tol_alpha
        
    with k indicating the kth iteration.
        
    tol : Relative convergence tolerance for F calculated such that:
        
        norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2)
        
    with k indicatin the kth iteration and F being the non-normalized estimated 
    distribution.

    Returns
    -------
    Dis : Normalized distribution

    """
    tau = 0.1
    sigma = 10
    Score = {'Chis': np.zeros(N_max)}
    Hy_Par = {'Alphas': np.zeros(N_max)}
    i = 0
    options = {'disp': False, 'maxiter': 100}
    Y1, _, F, _, F_tilde, _ = init_primal_dual(K, N_T1)
    con = True
    alpha = 1 / alpha_guess
    u_ = np.ones(K.shape[1])
    arg = (CompressedData, Y1, F, K, alpha, tau)

    while con:
        result = minimize(ut.min_u, u_, args = arg, method = 'trust-krylov', 
                          jac = ut.grad_min_u, hess = ut.hess_min_u, options = options)
        u = np.maximum(-F + tau * Y1, np.expand_dims(result.x, 1))
        u_ = np.squeeze(u, 1)

        Hy_Par['Alphas'][i] = np.copy(alpha)
        alpha, chi = ut.gcv_alpha_primal_dual(CompressedData, K, Y1, F, u, n, 
                                           alpha, tau)
        Score['Chis'][i] = np.copy(chi)
        
        if i > 0:
            delta = np.abs((Score['Chis'][i] - Score['Chis'][i - 1]) 
                        / Score['Chis'][i - 1])
            
            if (i == (N_max - 1) or delta < tol_alpha or Hy_Par['Alphas'][i] 
                < 1e-12 or Hy_Par['Alphas'][i] > 1e12):  
                
                con = False
                Score['Chis'] = Score['Chis'][Hy_Par['Alphas'] > 0]
                Hy_Par['Alphas'] = Hy_Par['Alphas'][Hy_Par['Alphas'] > 0]                  
        
        print('----------------------------')
        print('1st Primal Dual: Alpha-Estimation')
        print(f'Alpha = {alpha}')
        print(f'Chi = {chi}')
        print(f'Count = {i}')
        print('----------------------------')
        
        i += 1
        B = ut.calc_b_mat(K, tau, alpha)
        Y1, F, F_tilde = ut.primal_dual_l1(CompressedData, Y1, F, F_tilde, K, B, 
                                        alpha, tau, sigma)      
        
    Y1, _, F, _, F_tilde, _ = init_primal_dual(K, N_T1)
    epsilon = 1
    Count = 0
    alpha = Hy_Par['Alphas'][i - 1]
    B = ut.calc_b_mat(K, tau, alpha)

    while epsilon > tol:
        Count += 1
        F_ = np.copy(F)
        Y1, F, F_tilde = ut.primal_dual_l1(CompressedData, Y1, F, F_tilde, K, B, 
                                        alpha, tau, sigma)  
        epsilon = np.linalg.norm(F - F_, 2) / np.linalg.norm(F_, 2)

        if Count >= 1e5:
            break
     
    print('----------------------------')
    print('2nd Primal Dual: Dis-Estimation')
    print(f'Alpha = {alpha}')
    print(f'Count = {Count}')
    print('----------------------------')    
    
    Dis = F / np.sum(F)
    
    return Dis


def l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, tol_alpha, *args):
    """
    Algorithm to estimate the searched for distribution using L2 regularization
    in combination with generalized cross-validation (GCV).
    For further reference: https://doi.org/10.1016/j.pnmrs.2011.07.002
        
    Parameters
    ---------- 
    N_max : Maximum number of iterations
    
    N_T1 : Number of relaxation times or diffusion coefficients
    
    n : Number of diagonal elements in the diagonal matrix S. For more details 
    see cam_ilt.reg_inv.svd_kernel_compression
    
    K : Compressed Kernel
    
    alpha_guess : Initial guess of the hyperparameter alpha. For more details
    see cam_ilt.reg_inv.svd_kernel_compression
    
    CompressedData : Compressed experimental data
    
    tol_alpha : Relative convergence tolerance for alpha calculated such that:
        
        abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < tol_alpha
        
    with k indicating the kth iteration.
        
    tol : Relative convergence tolerance for F calculated such that:
        
        norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2)
        
    with k indicatin the kth iteration and F being the non-normalized estimated 
    distribution.
    
    *args: Additional arguments. This is used to pass a weight matrix, in the case
    that an non-uniform L2 penalty is employed. 

    Returns
    -------
    Dis : Normalized distribution

    """
    Score = {'Chis': np.zeros(N_max)}
    Hy_Par = {'Alphas': np.zeros(N_max)}
    con = True
    i = 0
    options = {'disp': False, 'maxiter': 100}
    F_ = np.ones(K.shape[1]) / K.shape[1]   
    alpha = np.copy(alpha_guess)
   
    while con:
        
        if args:
            result = minimize(ut.min_l2_pen, F_, args = (CompressedData, K, alpha, args[0]), 
                              method = 'trust-krylov', jac = ut.grad_min_l2_pen, 
                              hess = ut.hess_min_l2_pen, options = options)
            
        else:
            result = minimize(ut.min_l2, F_, args = (CompressedData, K, alpha), 
                              method = 'trust-krylov', jac = ut.grad_min_l2, 
                              hess = ut.hess_min_l2, options = options)
            
        F = np.maximum(0, np.expand_dims(result.x, 1))
        F_ = np.squeeze(F, 1)
        
        Hy_Par['Alphas'][i] = np.copy(alpha)
        alpha, chi = ut.gcv_alpha_l2(CompressedData, K, F, alpha, n) 
        Score['Chis'][i] = np.copy(chi)
        
        if i > 0:
            delta = np.abs((Score['Chis'][i] - Score['Chis'][i - 1]) 
                        / Score['Chis'][i - 1])
            
            if (i == (N_max - 1) or delta < tol_alpha or Hy_Par['Alphas'][i] 
                < 1e-12 or Hy_Par['Alphas'][i] > 1e12):  
                
                con = False
                Score['Chis'] = Score['Chis'][Hy_Par['Alphas'] > 0]
                Hy_Par['Alphas'] = Hy_Par['Alphas'][Hy_Par['Alphas'] > 0]
        
        print('----------------------------')
        print('L2: Dis-Estimation')
        print(f'Alpha = {alpha}')
        print(f'Chi = {chi}')
        print(f'Count = {i}')
        print('----------------------------')
        
        i += 1
    
    Dis = F / np.sum(F)
    
    return Dis


def mtgv_gcv_brd(opt, *args):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and the Butler-Reeds-Dawson (BRD) method. 
    For further reference: https://doi.org/10.48550/arXiv.2311.11442

    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1': 128,
               't1': t1,
               'beta guess': 1e-10,
               'exp type': 'T2',
               'max iter': 500,
               'beta lim': [1e-12, 1e2],
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1),)
        
        #T1: Number of values in the to-be-estimated distribution
        
        noise: Noise estimate of your data. This should be a single number.

        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for the
        author of this toolbox 1e-10 was usually a very reliable initial guess, but
        as long as it is not choosen too large (because beta updates will increase its
        value) larger values such as 1e-8 will most likely also be fine.

        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        max iter: Maximum number of iterations
        
        beta lim: Limits for the hyperparameter beta. In practise, for the author
        of this toolbox [1e-12, 1e2] turned out be very realliable limits. The 
        Butler-Reeds-Dawson (BRD) beta update is usually highly sparse and often 
        less than 10 beta values will be explored if the proposed range is used. 
        Also the lower limit should be choosen smaller than beta_guess, because 
        although very rarely observed it is not to exclude that the BRD beta update 
        might lead to a decrease in beta value although in the vast majority of 
        cases beta does monotonically increase from beta_guess up to the upper 
        beta limit.
        
        alpha tol: Relative convergence tolerance for alpha calculated such that
            
            abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < alpha tol
            
        with k indicating the kth iteration.
            
        inv tol : Relative convergence tolerance for F calculated such that
            
            norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < inv tol
            
        with k indicatin the kth iteration and F being the non-normalized estimated 
        distribution.
        
        pen type: String which defines the type of "weighting" applied. Options
        are 'uniform' and 'gaussian'. 'uniform' is the method as described in the 
        first paper. 'gaussian' builts on this method but firstly the L1 regularization
        is used to get a first sparse estimate of the distribution which is then
        smoothed by a gaussian filter resulting in the distribution Dis_gf. This
        is then used to generate the weight matrix pen for the L2 algorithm as 
        follows:
            
            pen = diag(1 / (0.1 + Dis_gf)) 
        
        with Dis_gf normalized to be ranging from 0 to 1. The weighted L2 results
        is then multiplied with the 'uniform' estimate to generate the final
        distribution
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : A list of normalized distributions. The number of distributions is equal
    to the number of betas explored because a new distribution is estimated for
    every beta.
    
    Score : Dictionary with the entries 'Chis' and 'Chis_beta'. 'Chis' will include
    a list of vectors with every vector including the GCV scores calculated for 
    every iteration during a single alpha estimation. The number of GCV score 
    vectors in the list is equal to the number of betas explored, because a full 
    alpha estimation is run for every explored beta. 'Chis_beta' will include a 
    single vector including the BRD scores for every explored beta.
        
    Hy_Par : Dictionary with the entries 'Alphas' and 'Betas'. 'Alphas' will include
    a list of vectors with every vector including the alpha values calculated for
    every iteration during a single alpha estimation. The number of alpha vectors 
    in the list is equal to the number of betas explored, because a full alpha 
    estimation is run for every explored beta. 'Betas' will include a single 
    vector including the beta values for every explored beta.
    
    T1: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    Data = np.copy(opt['data'])
    NoiseStd = np.copy(opt['noise'])
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    t1 = np.copy(opt['t1'])
    beta_guess = np.copy(opt['beta guess'])
    DataType = np.copy(opt['exp type'])
    pen_type = np.copy(opt['pen type'])
    N_max = np.copy(opt['max iter'])
    tol = np.copy(opt['inv tol'])
    tol_alpha = np.copy(opt['alpha tol'])
    beta_lim = np.copy(opt['beta lim'])
    del opt
 
    if DataType == 'custom':   
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K1 = np.copy(args[0])

    else:
        K1, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        
    NormData, NormNoise = ut.norm_noise_and_data(Data, NoiseStd)
    K, CompressedData, alpha_guess, n = svd_kernel_compression(T1, NormNoise,
                                                               N_max, NormData, K1)
    
    if pen_type == 'uniform':
        Dis, Score, Hy_Par = mtgv_gcv_brd_optim(NormNoise, n, N_max, beta_guess, N_T1,  
                                                K, alpha_guess, CompressedData, tol_alpha,
                                                tol, beta_lim)
    
    elif pen_type == 'gaussian':        
        F_l1 = l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                            CompressedData, tol_alpha, tol)
        F_l1 = np.squeeze(gaussian_filter(F_l1, sigma = 10))
        F_l1 /= np.max(F_l1) 
        pen = np.diag(1 / (0.1 + F_l1)) 
        F_l2 = l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, 
                        tol_alpha, pen)
        Dis, Score, Hy_Par = mtgv_gcv_brd_optim(NormNoise, n, N_max, beta_guess, N_T1,  
                                                K, alpha_guess, CompressedData, tol_alpha,
                                                tol, beta_lim)
        Dis = [F_l2 * elem for elem in Dis]
        Dis = [elem / np.sum(elem) for elem in Dis]
        
    else:
        raise ValueError('Invalid Penalty Type')   

    return Dis, T1, Score, Hy_Par


def mtgv_gcv_bp(opt, *args):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and balancing principle (BP). 
    
    For further reference: 
        
       General method: https://doi.org/10.48550/arXiv.2311.11442
       BP: https://doi.org/10.1016/j.amc.2022.127809
       
    In comparison to cam_ilt.reg_inv.d1.mtgv_gcv_brd which employs BRD for
    updating beta and tends to explore beta across many orders of magnitude, the 
    BP method does quite the opposite and tends to vary beta only across a small
    range. Hence, this algorithm is more sensitive regarding the initial choice of
    beta_guess.

    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1': 128,
               't1': t1,
               'beta guess': 1e-8,
               'exp type': 'T2',
               'max iter': 500,
               'gamma': 1e-7,
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1),) 
        
        #T1: Number of values in the to-be-estimated distribution
        
        noise: Noise estimate of your data. This should be a single number.

        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for the
        author of this toolbox 1e-8 was usually a very reliable initial guess, but
        this might need some tweaking depending on the users data.

        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        max iter: Maximum number of iterations
        
        gamma: Additional hyperparameter. In practise, for the author of this 
        toolbox a value of 1e-7 worked well, but changes might be necessary here 
        depending on the users data.
        
        alpha tol: Relative convergence tolerance for alpha calculated such that
            
            abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < alpha tol
            
        with k indicating the kth iteration.
            
        inv tol : Relative convergence tolerance for F calculated such that
            
            norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < inv tol
            
        with k indicatin the kth iteration and F being the non-normalized estimated 
        distribution.
        
        pen type: String which defines the type of "weighting" applied. Options
        are 'uniform' and 'gaussian'. 'uniform' is the method as described in the 
        first paper. 'gaussian' builts on this method but firstly the L1 regularization
        is used to get a first sparse estimate of the distribution which is then
        smoothed by a gaussian filter resulting in the distribution Dis_gf. This
        is then used to generate the weight matrix pen for the L2 algorithm as 
        follows:
            
            pen = diag(1 / (0.1 + Dis_gf)) 
        
        with Dis_gf normalized to be ranging from 0 to 1. The weighted L2 results
        is then multiplied with the 'uniform' estimate to generate the final
        distribution
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    Data = np.copy(opt['data'])
    NoiseStd = np.copy(opt['noise'])
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    t1 = np.copy(opt['t1'])
    beta_guess = np.copy(opt['beta guess'])
    DataType = np.copy(opt['exp type'])
    pen_type = np.copy(opt['pen type'])
    N_max = np.copy(opt['max iter'])
    tol = np.copy(opt['inv tol'])
    tol_alpha = np.copy(opt['alpha tol'])
    gamma = np.copy(opt['gamma'])
    del opt
 
    if DataType == 'custom':   
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K1 = np.copy(args[0])

    else:
        K1, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        
    NormData, NormNoise = ut.norm_noise_and_data(Data, NoiseStd)
    K, CompressedData, alpha_guess, n = svd_kernel_compression(T1, NormNoise,
                                                               N_max, NormData, K1)
    
    if pen_type == 'uniform':       
        Dis = mtgv_gcv_bp_optim(NormNoise, n, N_max, beta_guess, N_T1, K, 
                                alpha_guess, CompressedData, tol_alpha, tol, gamma)
        
    elif pen_type == 'gaussian':
        F_l1 = l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                            CompressedData, tol_alpha, tol)
        F_l1 = np.squeeze(gaussian_filter(F_l1, sigma = 10))
        F_l1 /= np.max(F_l1) 
        pen = np.diag(1 / (0.1 + F_l1)) 
        F_l2 = l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, 
                        tol_alpha, pen)
        Dis = mtgv_gcv_bp_optim(NormNoise, n, N_max, beta_guess, N_T1, K, 
                                alpha_guess, CompressedData, tol_alpha, tol, gamma)
        Dis *= F_l2
        Dis /= np.sum(Dis)
        
    else:
        raise ValueError('Invalid Penalty Type')   

    return Dis, T1


def mtgv_gcv_fb(opt, *args):
    """
    Algorithm to estimate the searched for distribution using MTGV (modified total
    generalized variation) regularization in combination with generalized cross-
    validation (GCV) and the Butler-Reeds-Dawson (BRD) method. Additionally, the
    received BRD curve is fitted with a spline and the optimal beta at the sigmoidal
    heel of the interpolated curve is estimated. Then the algorithm is rerun with
    beta fixed to this particular value.
    
    For further reference: 
        
        General method: https://doi.org/10.48550/arXiv.2311.11442
        BRD heel: https://doi.org/10.1016/j.pnmrs.2011.07.002

    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1': 128,
               't1': t1,
               'beta guess': 1e-10,
               'exp type': 'T2',
               'max iter': 500,
               'beta lim': [1e-12, 1e2],
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1),) 
        
        #T1: Number of values in the to-be-estimated distribution
        
        noise: Noise estimate of your data. This should be a single number.

        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for 
        the author of this toolbox 1e-10 was usually a very reliable initial guess, 
        but as long as it is not choosen too large (because beta updates will 
        increase its value) larger values such as 1e-8 will most likely also be 
        fine.
        
        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        max iter: Maximum number of iterations
        
        beta lim: Limits for the hyperparameter beta. In practise, for the author
        of this toolbox [1e-12, 1e2] turned out be very realliable limits. The 
        Butler-Reeds-Dawson (BRD) beta update is usually highly sparse and often 
        less than 10 beta values will be explored if the proposed range is used. 
        Also the lower limit should be choosen smaller than beta_guess, because 
        although very rarely observed it is not to exclude that the BRD beta update 
        might lead to a decrease in beta value although in the vast majority of 
        cases beta does monotonically increase from beta_guess up to the upper 
        beta limit.
        
        alpha tol: Relative convergence tolerance for alpha calculated such that
            
            abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < alpha tol
            
        with k indicating the kth iteration.
            
        inv tol : Relative convergence tolerance for F calculated such that
            
            norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < inv tol
            
        with k indicatin the kth iteration and F being the non-normalized estimated 
        distribution.
        
        pen type: String which defines the type of "weighting" applied. Options
        are 'uniform' and 'gaussian'. 'uniform' is the method as described in the 
        first paper. 'gaussian' builts on this method but firstly the L1 regularization
        is used to get a first sparse estimate of the distribution which is then
        smoothed by a gaussian filter resulting in the distribution Dis_gf. This
        is then used to generate the weight matrix pen for the L2 algorithm as 
        follows:
            
            pen = diag(1 / (0.1 + Dis_gf)) 
        
        with Dis_gf normalized to be ranging from 0 to 1. The weighted L2 results
        is then multiplied with the 'uniform' estimate to generate the final
        distribution
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    Data = np.copy(opt['data'])
    NoiseStd = np.copy(opt['noise'])
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    t1 = np.copy(opt['t1'])
    beta_guess = np.copy(opt['beta guess'])
    DataType = np.copy(opt['exp type'])
    pen_type = np.copy(opt['pen type'])
    N_max = np.copy(opt['max iter'])
    tol = np.copy(opt['inv tol'])
    tol_alpha = np.copy(opt['alpha tol'])
    beta_lim = np.copy(opt['beta lim'])
    del opt
 
    if DataType == 'custom':   
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K1 = np.copy(args[0])

    else:
        K1, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        
    NormData, NormNoise = ut.norm_noise_and_data(Data, NoiseStd)
    K, CompressedData, alpha_guess, n = svd_kernel_compression(T1, NormNoise,
                                                               N_max, NormData, K1)
    _, Score, Hy_Par = mtgv_gcv_brd_optim(NormNoise, n, N_max, beta_guess, N_T1, 
                                     K, alpha_guess, CompressedData, tol_alpha, tol, 
                                     beta_lim)
    beta_int = np.logspace(np.log10(np.min(Hy_Par['Betas'])), np.log10(np.max(
        Hy_Par['Betas'])), 1000)
    chi_int = Akima1DInterpolator(np.log10(Hy_Par['Betas']), 
                               Score['Chis_beta'])(np.log10(beta_int))
    grad = np.gradient(chi_int, np.log10(beta_int))
    curv = np.gradient(grad, np.log10(beta_int))
    
    if chi_int[0] < chi_int[-1]:
        curv = curv[:np.argmax(grad)]
        beta_int = beta_int[:np.argmax(grad)]
        
    else:
        curv = curv[np.argmax(grad):]
        beta_int = beta_int[np.argmax(grad):]
        
    beta = beta_int[np.argmin(curv)]
    
    if pen_type == 'uniform':
        Dis = mtgv_gcv_fb_optim(NormNoise, n, N_max, beta, N_T1, K, 
                                alpha_guess, CompressedData, tol_alpha, tol)
        
    elif pen_type == 'gaussian':
        F_l1 = l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                            CompressedData, tol_alpha, tol)
        F_l1 = np.squeeze(gaussian_filter(F_l1, sigma = 10))
        F_l1 /= np.max(F_l1) 
        pen = np.diag(1 / (0.1 + F_l1)) 
        F_l2 = l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, 
                        tol_alpha, pen)
        Dis = mtgv_gcv_fb_optim(NormNoise, n, N_max, beta, N_T1, K, 
                                alpha_guess, CompressedData, tol_alpha, tol)
        Dis *= F_l2
        Dis /= np.sum(Dis)
        
    else:
        raise ValueError('Invalid Penalty Type') 

    return Dis, T1


def l2_gcv(opt, *args):
    """
    Algorithm to estimate the searched for distribution using L2 regularization
    in combination with generalized cross-validation (GCV).
    For further reference: https://doi.org/10.1016/j.pnmrs.2011.07.002

    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1': 128,
               't1': t1,
               'exp type': 'T2',
               'max iter': 500,
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1),) 
        
        #T1: Number of values in the to-be-estimated distribution
        
        noise: Noise estimate of your data. This should be a single number.

        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 
        
        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        max iter: Maximum number of iterations
        
        alpha tol: Relative convergence tolerance for alpha calculated such that
            
            abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < alpha tol
            
        with k indicating the kth iteration.
            
        inv tol : Relative convergence tolerance for F calculated such that
            
            norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < inv tol
            
        with k indicatin the kth iteration and F being the non-normalized estimated 
        distribution.
        
        pen type: String which defines the type of "weighting" applied. Options
        are 'uniform' and 'gaussian'. 'uniform' is the method as described in the 
        first paper. 'gaussian' builts on this method but firstly the L1 regularization
        is used to get a first sparse estimate of the distribution which is then
        smoothed by a gaussian filter resulting in the distribution Dis_gf. This
        is then used to generate the weight matrix pen for the L2 algorithm as 
        follows:
            
            pen = diag(1 / (0.1 + Dis_gf)) 
        
        with Dis_gf normalized to be ranging from 0 to 1. This is then used to 
        weight the L2 penalty.
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    Data = np.copy(opt['data'])
    NoiseStd = np.copy(opt['noise'])
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    t1 = np.copy(opt['t1'])
    DataType = np.copy(opt['exp type'])
    pen_type = np.copy(opt['pen type'])
    N_max = np.copy(opt['max iter'])
    tol = np.copy(opt['inv tol'])
    tol_alpha = np.copy(opt['alpha tol'])
 
    if DataType == 'custom':   
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K1 = np.copy(args[0])

    else:
        K1, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
    
    NormData, NormNoise = ut.norm_noise_and_data(Data, NoiseStd)
    K, CompressedData, alpha_guess, n = svd_kernel_compression(T1, NormNoise,
                                                               N_max, NormData, K1)
    
    if pen_type == 'uniform':
        Dis = l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, tol_alpha)
        
    elif pen_type == 'gaussian':
        F_l1 = l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                          CompressedData, tol_alpha, tol)
        F_l1 = np.squeeze(gaussian_filter(F_l1, sigma = 10))
        F_l1 /= np.max(F_l1) 
        pen = np.diag(1 / (0.1 + F_l1)) 
        Dis = l2_optim(N_max, CompressedData, K, alpha_guess, n, N_T1, tol, 
                       tol_alpha, pen)
        
    else:
        raise ValueError('Invalid Penalty Type')
    
    return Dis, T1


def l1_gcv(opt, *args):
    """
    Algorithm to estimate the searched for distribution using L1 regularization
    in combination with generalized cross-validation (GCV).
    
    For further reference: 
        
        GCV: https://doi.org/10.48550/arXiv.2311.11442
        L1 regularization: https://doi.org/10.1016/j.jmr.2017.05.010
        
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1': 128,
               't1': t1,
               'exp type': 'T2',
               'max iter': 500,
               'inv tol': 1e-3,
               'alpha tol': 1e-2}
        
        data: Experimental data given as a numpy array of shape (len(t1),)
        
        #T1: Number of values in the to-be-estimated distribution
        
        noise: Noise estimate of your data. This should be a single number.

        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 
        
        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        max iter: Maximum number of iterations
        
        alpha tol: Relative convergence tolerance for alpha calculated such that
            
            abs(gcv_score_k - gcv_score_(k - 1)) / gcv_score_(k - 1) < alpha tol
            
        with k indicating the kth iteration.
            
        inv tol : Relative convergence tolerance for F calculated such that
            
            norm(F_k - F_(k - 1), 2) / norm(F_(k - 1), 2) < inv tol
            
        with k indicatin the kth iteration and F being the non-normalized estimated 
        distribution.
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    Data = np.copy(opt['data'])
    NoiseStd = np.copy(opt['noise'])
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    t1 = np.copy(opt['t1'])
    DataType = np.copy(opt['exp type'])
    N_max = np.copy(opt['max iter'])
    tol = np.copy(opt['inv tol'])
    tol_alpha = np.copy(opt['alpha tol'])
    del opt
 
    if DataType == 'custom':   
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K1 = np.copy(args[0])

    else:
        K1, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        
    NormData, NormNoise = ut.norm_noise_and_data(Data, NoiseStd)
    K, CompressedData, alpha_guess, n = svd_kernel_compression(T1, NormNoise,
                                                               N_max, NormData, K1)
    Dis = l1_gcv_optim(NormNoise, n, N_max, N_T1, K, alpha_guess, 
                       CompressedData, tol_alpha, tol)
    
    return Dis, T1
    

def simulate(opt, *args):
    """
    This function allows to simulate experimental data with a freely adjustable
    signal to noise ratio (SNR). 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'T1 bounds': [0.001, 10],
               '#T1': 128,
               '#t1': 128,
               'exp type': 'T2',
               'weights': [0.5, 0.5],
               'log mean T1': [-2, 0],
               'log std T1': [0.1, 0.25],
               'SNR': 1e3}
        
        #T1: Number of relaxation times or diffusion coefficients in the simulated
        distribution
        
        #t1: Number of time delays used for relaxation encoding or diffusion 
        encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 
        
        T1 bounds: The lower and upper limit of the to-be-estimated distribution. 
        
        exp type: String which defines the type of kernel used. Options are 'T1inv'
        for T1 inversion recovery, 'T1sat' for T1 saturation recovery, 'D' for 
        any Stejskal-Tanner (see latter reference) like diffusion experiment, 
        'T2' for common mono-exponential T2 encodings and 'custom' if an 
        user-defined custom kernel is provided
        
        weights: Weights of different relaxation or diffusion components. Should
        add up to 1.
        
        log mean T1: log10(T1) mean for every relaxation or diffusion component
        
        log std T1: log10(T1) standard deviation for every relaxation or diffusion
        component
        
        SNR: signal to noise ratio which the simulated data should have
        
    Returns
    -------
    Sig: Simulated experimental data
    
    Dis: Simulated distribution
    
    T1: Logarithmically spaced relaxation times or diffusion coefficient in the
    range of T1 bounds
    
    t1: Logarithmically spaced time delays used for relaxation encoding or diffusion 
    encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
    For reference: https://doi.org/10.1063/1.1673336 
       
    NoiseStd: Noise estimate calculated that the simulated data fits the given SNR 
        
    """
    T1_min = np.copy(opt['T1 bounds'][0])
    T1_max = np.copy(opt['T1 bounds'][1])
    N_T1 = np.copy(opt['#T1'])
    N_t1 = np.copy(opt['#t1'])
    DataType = np.copy(opt['exp type'])
    w = np.copy(opt['weights'])
    log_mean_T1 = np.copy(opt['log mean T1'])
    log_std_T1 = np.copy(opt['log std T1'])
    snr = np.copy(opt['SNR'])
    del opt
    
    if DataType == 'T1sat' or DataType == 'T1inv' or DataType == 'T2':
        t1 = np.logspace(np.log10(T1_min), np.log10(T1_max), N_t1)
        
    elif DataType == 'D':
        t1 = np.logspace(np.log10(1 / T1_max), np.log10(1 / T1_min), N_t1)
        
    else:
        raise ValueError('Invalid Data Type')
 
    if DataType == 'custom':  
        t1 = np.copy(args[0])
        T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
        K = np.copy(args[2])

    else:
        K, T1 = kernel_setup(t1, T1_min, T1_max, DataType, N_T1)
    
    N_comp = len(w)
        
    for k in range(N_comp):
        pdf_T1 = norm.pdf(np.log10(T1), log_mean_T1[k], log_std_T1[k])

        if k == 0:
            Dis = w[k] * pdf_T1
        else:
            Dis += w[k] * pdf_T1

    Dis = Dis / np.sum(Dis)
    Dis = np.round(Dis, 8)  # 8 digits are emperically chosen to ensure sparsity
    Sig = K @ Dis
    NoiseStd = np.max(np.abs(Sig)) / snr
    Sig = Sig + NoiseStd * np.random.randn(N_t1)
    NoiseStd = NoiseStd / np.max(np.abs(Sig))
    Sig = Sig / np.max(np.abs(Sig))

    return Sig, Dis, T1, t1, NoiseStd
