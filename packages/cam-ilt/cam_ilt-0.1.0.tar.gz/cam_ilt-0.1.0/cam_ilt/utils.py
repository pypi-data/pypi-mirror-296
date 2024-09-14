import numpy as np


def norm_noise_and_data(Data, NoiseStd):
    """
    This function normalizes the data to lie in a maximum range from -1 to 1. 
    Also the noise estimate is normalized accordingly.

    """
    NormData = Data / np.max(np.abs(Data))
    NormNoise = NoiseStd / np.max(np.abs(Data))
    
    return NormData, NormNoise


def min_u(u, S, Y_k, F_k, K, alpha_k, tau):
    """
    This is the cost function used to calculate the GCV estimate of alpha if MTGV
    or L1 regularization is employed. For more details, see the following 
    reference: https://doi.org/10.48550/arXiv.2311.11442
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv
    
    Parameters
    ----------
    u : Variable to optimize
        
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
        
    Y_k : kth iteration of the auxilliary vector Y
        
    F_k : kth iteration of the to-be-estimated distribution F
    
    K : Compressed kernel
    
    alpha_k : kth iteration of the hyperparameter alpha
    
    tau : Convergence parameter

    """
    u = np.expand_dims(u, 1)
    term1 = K @ u - (S - K @ (F_k - tau * Y_k))
    f_u = 0.5 * (term1.T @ term1) + 1 / (2 * tau * alpha_k) * (u.T @ u)
    
    return f_u


def grad_min_u(u, S, Y_k, F_k, K, alpha_k, tau):
    """
    Gradient of min_u. For more details check the docstring of cam_ilt.utils.min_u
    
    Parameters
    ----------
    u : Variable to optimize
        
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
        
    Y_k : kth iteration of the auxilliary vector Y
        
    F_k : kth iteration of the to-be-estimated distribution F
    
    K : Compressed kernel
    
    alpha_k : kth iteration of the hyperparameter alpha
    
    tau : Convergence parameter

    """
    u = np.expand_dims(u, 1)
    grad = K.T @ (K @ u) - K.T @ (S - K @ (F_k - tau * Y_k)) + 1 / (tau * alpha_k) * u
    
    return np.squeeze(grad, 1)


def hess_min_u(u, S, Y_k, F_k, K, alpha_k, tau):
    """
    Hessian of min_u. For more details check the docstring of cam_ilt.utils.min_u
    
    Parameters
    ----------
    u : Variable to optimize
        
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
        
    Y_k : kth iteration of the auxilliary vector Y
        
    F_k : kth iteration of the to-be-estimated distribution F
    
    K : Compressed kernel
    
    alpha_k : kth iteration of the hyperparameter alpha
    
    tau : Convergence parameter
    
    """
    hess = K.T @ K + 1 / (tau * alpha_k) * np.eye(K.shape[1])
    
    return hess


def min_l2(F, S, K, alpha):
    """
    This is the cost function used for L2 regularization if an uniform L2 penalty
    is employed. For more details, see the following reference: 
        https://doi.org/10.1016/j.pnmrs.2011.07.002
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter

    """
    F = np.expand_dims(F, 1)
    f_l2 = 1/2 * (alpha * (K @ F - S).T @ (K @ F - S) + F.T @ F)
    
    return f_l2


def min_l2_pen(F, S, K, alpha, D):
    """
    This is the cost function used for L2 regularization if an non-uniform L2 
    penalty is employed. For more details, see the following reference: 
        https://doi.org/10.1016/j.pnmrs.2011.07.002
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter
    
    D: Weight matrix which applies some sort of transformation or weighting to F.
    If D equals the identity matrix a uniform L2 penalty is the result.  

    """
    F = np.expand_dims(F, 1)
    f_l2 = 1/2 * (alpha * (K @ F - S).T @ (K @ F - S) + F.T @ D.T @ D @ F)
    
    return f_l2


def grad_min_l2(F, S, K, alpha):
    """
    Gradient of min_l2. For more details check the docstring of cam_ilt.utils.min_l2

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter

    """
    F = np.expand_dims(F, 1)
    grad = alpha * (K.T @ K @ F - K.T @ S) + F
    
    return np.squeeze(grad, 1)


def grad_min_l2_pen(F, S, K, alpha, D):
    """
    Gradient of min_l2_pen. For more details check the docstring of 
    cam_ilt.utils.min_l2_pen

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter

    D: Weight matrix which applies some sort of transformation or weighting to F.
    If D equals the identity matrix a uniform L2 penalty is the result.  

    """
    F = np.expand_dims(F, 1)
    grad = alpha * (K.T @ K @ F - K.T @ S) + D @ F
    
    return np.squeeze(grad, 1)


def hess_min_l2(F, S, K, alpha):
    """
    Hessian of min_l2. For more details check the docstring of cam_ilt.utils.min_l2

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter

    """
    hess = alpha * (K.T @ K) + np.identity(K.shape[1])
    
    return hess


def hess_min_l2_pen(F, S, K, alpha, D):
    """
    Hessian of min_l2_pen. For more details check the docstring of 
    cam_ilt.utils.min_l2_pen

    Parameters
    ----------
    F : To-be-estimated distribution
    
    S : Experimental data, not to confuse with the diagonal matrix S generated
    via singular value decomposition
    
    K : Compressed kernel
    
    alpha : hyperparameter

    D: Weight matrix which applies some sort of transformation or weighting to F.
    If D equals the identity matrix a uniform L2 penalty is the result.  

    """
    hess = alpha * (K.T @ K) + D
    
    return hess


def calc_l1_star(vec):
    """
    This function calculates the L1* norm as defined in the following paper:
        https://doi.org/10.1016/j.jmr.2017.08.017

    """
    lim1 = 3
    lim2 = int(len(vec) / lim1)
    l1_star = 0
    
    for i in range(lim2):       
            ind = i + np.arange(lim1, dtype = np.int32) * lim2
            l1_star += np.sqrt(np.sum(vec[ind]**2))
            
    return l1_star


def calc_b_mat(K, tau, alpha):
    """
    This function calculates the proximal operator B as defined in the following 
    paper: https://doi.org/10.1016/j.jmr.2017.08.017
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv
    
    Parameters
    ----------
    
    K: Compressed Kernel
    
    tau: Convergence parameter
    
    alpha: Hyperparameter

    """
    B = np.linalg.inv(np.eye(K.shape[1]) + tau * alpha * (K.T @ K))
    
    return B


def gcv_alpha_primal_dual(CompressedData, K, Y1, F, u, n, alpha, tau):
    """
    This function calculates the GCV score and the alpha update if MTGV or L1 
    regularization is employed. For more details, see the following 
    reference: https://doi.org/10.48550/arXiv.2311.11442
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    K : Compressed Kernel
    
    Y1 : Auxilliary vector 
        
    F : Non-normalized to-be-estimated distribution
        
    u : Vector which minimizes cam_ilt.utils.min_u
        
    n : Number of diagonal elements in the diagonal matrix S
        
    alpha : Hyperparameter
    
    tau : Convergence parameter

    Returns
    -------
    alpha : Updated version of alpha
    
    chi : GCV score for initial alpha

    """
    A = K.T @ K + (1 / (tau * alpha)) * np.eye(K.shape[1])
    S_ = CompressedData - K @ (F - tau * Y1)
    P = np.eye(K.shape[0]) - K @ np.linalg.inv(A) @ K.T
    r_2 = (P @ S_).T @ (P @ S_)
    tr_P = np.trace(P)
    chi = n * r_2 / (tr_P**2)
    lambda_ = r_2 * np.trace(np.linalg.inv(A) - 1 / (tau * alpha) 
                             * np.linalg.inv(A)**2) / (u.T @ np.linalg.inv(A) 
                                                       @ u * tr_P)
    alpha = 1 / (lambda_ * tau)
    
    return alpha, chi


def gcv_alpha_l2(CompressedData, K, F, alpha, n):
    """
    This function calculates the GCV score and the alpha update if L2 
    regularization is employed. For more details, see the following 
    reference: https://doi.org/10.1016/j.pnmrs.2011.07.002
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    K : Compressed Kernel
        
    F : Non-normalized to-be-estimated distribution
        
    n : Number of diagonal elements in the diagonal matrix S
        
    alpha : Hyperparameter
    

    Returns
    -------
    alpha : Updated version of alpha
    
    chi : GCV score for initial alpha

    """
    A = K.T @ K + alpha * np.eye(K.shape[1])
    P = np.eye(K.shape[0]) - K @ np.linalg.inv(A) @ K.T
    r_2 = (P @ CompressedData).T @ (P @ CompressedData)
    tr_P = np.trace(P)
    chi = n * r_2 / (tr_P)**2
    alpha = r_2 * np.trace(np.linalg.inv(A) - alpha * np.linalg.inv(A) 
                           @ np.linalg.inv(A)) / (F.T @ np.linalg.inv(A) 
                                                  @ F * tr_P)

    return alpha, chi                                             


def brd_beta(CompressedData, K, F, NormNoise, n, beta):
    """
    This function calculates the BRD score and the beta update if MTGV
    regularization is employed. For more details, see the following 
    reference: https://doi.org/10.48550/arXiv.2311.11442
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    K : Compressed Kernel
        
    F : Non-normalized to-be-estimated distribution
        
    n : Number of diagonal elements in the diagonal matrix S
        
    beta: Hyperparameter
    
    NormNoise: Normalized noise estimate

    Returns
    -------
    beta : Updated version of beta
    
    chi_beta : BRD score for initial beta

    """
    beta = np.sqrt(n) * beta / np.linalg.norm(K @ F - CompressedData, 2)
    chi_beta = np.linalg.norm(K @ F - CompressedData, 2) / NormNoise
    
    return beta, chi_beta


def bp_beta(CompressedData, K, F, W, D2, alpha, gamma):
    """
    This function calculates the BP score and the beta update if MTGV
    regularization is employed. For more details, see the following 
    reference: https://doi.org/10.1016/j.amc.2022.127809
    
    In the following, I will give very brief explanations of the variables employed 
    in this function. For more details check the given reference or the docstrings
    of the various functions included in the subpackage cam_ilt.reg_inv

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    K : Compressed Kernel
    
    D2: Matrix which performs the second derivative
    
    W: Auxilliary vector to enforce smoothness on F
        
    F : Non-normalized to-be-estimated distribution
        
    n : Number of diagonal elements in the diagonal matrix S
        
    gamma: Hyperparameter
    
    alpha: Hyperparameter

    Returns
    -------
    beta : Updated version of beta

    """
    beta = gamma * (alpha / 2 * np.linalg.norm(K @ F - CompressedData, 2)**2 +
                    np.linalg.norm(F - W, 1)) / (calc_l1_star(D2 @ W) + 1e-10)
    
    return beta


def primal_dual_l1(CompressedData, Y1, F, F_tilde, K, B, alpha, tau, sigma):
    """
    Primal dual algorithm for L1 regularization. 
    For reference: https://doi.org/10.1016/j.jmr.2017.05.010

    Parameters
    ----------
    CompressedData : Compressed experimental data
        
    Y1 : Auxilliary vector for primal dual algorithm. See above reference for 
    further explanation. 
        
    F : Distribution to estimate, not normalized.
    
    F_tilde : F_tilde_k = 2 * F_k - F_(k - 1), k indicating the kth iteration
        
    K : Compressed kernel  
        
    B : Proximal operator. See https://doi.org/10.17863/CAM.104179 chapter 3.4
    equation 3.19 for further reference.
        
    alpha : Hyperparameter which controlls the fidelity of the to-be-estimated
    distribution towards the experimental data. See first reference for further 
    explanation.
        
    tau : Convergence parameter. See initial reference for further explanation
    
    sigma : Convergence parameter. See initial reference for further explanation

    """
    Y1_tilde = Y1 + sigma * F_tilde
    Y1 = Y1_tilde / np.maximum(1, np.abs(Y1_tilde))
    F_ = np.copy(F)
    F = B @ (F - tau * Y1 + tau * alpha * (K.T @ CompressedData))
    F = np.maximum(0, F)
    F_tilde = 2 * F - F_
    
    return Y1, F, F_tilde
