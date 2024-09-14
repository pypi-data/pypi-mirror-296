import numpy as np
from scipy.interpolate import Akima1DInterpolator
from cam_ilt.reg_inv import d2


def mtgv_gcv_brd(opt, *args):
    """
    This function employs the 2d version of mtgv_gcv_brd to calculate a 1d
    distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.mtgv_gcv_brd.
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. However, the marginal 
    distributions tend to span across less data points than it would be normally
    expected for a 1d distribution. Hence, the average marginal distribution is
    interpolated via the Akima method to a return a final 1d distribution covering
    a number of data points more suitable to the problem of interest. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1 2d': 18,
               '#T1 1d': 128,
               't1': t1,
               'beta guess': 1e-10,
               'exp type': 'T2T2',
               'max iter': 500,
               'beta lim': [1e-12, 1e2],
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1), len(t1)) 
        
        noise: Noise estimate of your data. This should be a single number

        #T1 2d: Number of values in both dimensions of the to-be-estimated 2d 
        distribution
        
        #T1 1d: Number of values in the final interpolated 1d distribution

        T1 bounds: The lower and upper limit of the to-be-estimated 2d distribution

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for the
        author of this toolbox 1e-10 was usually a very reliable initial guess, but
        as long as it is not choosen too large (because beta updates will increase its
        value) larger values such as 1e-8 will most likely also be fine.

        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
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
    
    T1_int: Logarithmically spaced relaxation times or diffusion coefficients.

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T1'] = np.copy(opt['#T1 2d'])
    opt['#T2'] = np.copy(opt['#T1 2d'])
    opt['t2'] = np.copy(opt['t1'])
       
    if DataType == 'custom':
        Dis, T1, _, Score, Hy_Par = d2.mtgv_gcv_brd(opt, args[0], args[0])
        
    elif DataType == 'T1T1' or DataType == 'T2T2':
        Dis, T1, _, Score, Hy_Par = d2.mtgv_gcv_brd(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    T1_int = np.logspace(np.log10(np.min(T1)), np.log10(np.max(T1)), 
                         opt['#T1 1d'])
    
    for k, elem in enumerate(Dis):
        proj_1 = np.sum(elem, axis = 0)
        proj_1 /= np.sum(proj_1)
        proj_2 = np.sum(elem, axis = 1)
        proj_2 /= np.sum(proj_2)
        Dis[k] = (proj_1 + proj_2) / 2
        Dis[k] = Akima1DInterpolator(np.log10(T1), Dis[k])(np.log10(T1_int))
    
    return Dis, T1_int, Score, Hy_Par


def mtgv_gcv_bp(opt, *args):
    """
    This function employs the 2d version of mtgv_gcv_bp to calculate a 1d
    distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.mtgv_gcv_bp.
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. However, the marginal 
    distributions tend to span across less data points than it would be normally
    expected for a 1d distribution. Hence, the average marginal distribution is
    interpolated via the Akima method to a return a final 1d distribution covering
    a number of data points more suitable to the problem of interest. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1 2d': 18,
               '#T1 1d': 128,
               't1': t1,
               'beta guess': 1e-8,
               'exp type': 'T2T2',
               'max iter': 500,
               'gamma': 1e-7,
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1), len(t1)) 
        
        noise: Noise estimate of your data. This should be a single number

        #T1 2d: Number of values in both dimensions of the to-be-estimated 2d 
        distribution
        
        #T1 1d: Number of values in the final interpolated 1d distribution

        T1 bounds: The lower and upper limit of the to-be-estimated 2d distribution

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for the
        author of this toolbox 1e-10 was usually a very reliable initial guess, but
        as long as it is not choosen too large (because beta updates will increase its
        value) larger values such as 1e-8 will most likely also be fine.

        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
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
    
    T1_int: Logarithmically spaced relaxation times or diffusion coefficients

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T1'] = np.copy(opt['#T1 2d'])
    opt['#T2'] = np.copy(opt['#T1 2d'])
    opt['t2'] = np.copy(opt['t1'])
       
    if DataType == 'custom':
        Dis, T1, _ = d2.mtgv_gcv_bp(opt, args[0], args[0])
        
    elif DataType == 'T1T1' or DataType == 'T2T2':
        Dis, T1, _ = d2.mtgv_gcv_bp(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    proj_1 = np.sum(Dis, axis = 0)
    proj_1 /= np.sum(proj_1)
    proj_2 = np.sum(Dis, axis = 1)
    proj_2 /= np.sum(proj_2)
    Dis = (proj_1 + proj_2) / 2 
    T1_int = np.logspace(np.log10(np.min(T1)), np.log10(np.max(T1)), 
                         opt['#T1 1d'])
    Dis = Akima1DInterpolator(np.log10(T1), Dis)(np.log10(T1_int))
    
    return Dis, T1_int


def mtgv_gcv_fb(opt, *args):
    """
    This function employs the 2d version of mtgv_gcv_fb to calculate a 1d
    distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.mtgv_gcv_fb.
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. However, the marginal 
    distributions tend to span across less data points than it would be normally
    expected for a 1d distribution. Hence, the average marginal distribution is
    interpolated via the Akima method to a return a final 1d distribution covering
    a number of data points more suitable to the problem of interest. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1 2d': 18,
               '#T1 1d': 128,
               't1': t1,
               'beta guess': 1e-10,
               'exp type': 'T2T2',
               'max iter': 500,
               'beta lim': [1e-12, 1e2],
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1), len(t1)) 
        
        noise: Noise estimate of your data. This should be a single number

        #T1 2d: Number of values in both dimensions of the to-be-estimated 2d 
        distribution
        
        #T1 1d: Number of values in the final interpolated 1d distribution

        T1 bounds: The lower and upper limit of the to-be-estimated 2d distribution

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        beta guess: Initial guess for the hyperparameter beta. In practise, for the
        author of this toolbox 1e-10 was usually a very reliable initial guess, but
        as long as it is not choosen too large (because beta updates will increase its
        value) larger values such as 1e-8 will most likely also be fine.

        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
        max iter: Maximum number of iterations
        
        beta lim: Limits for the hyperparameter beta. In practise, for the author
        of this toolbox [1e-12, 1e2] turned out be very realliable limits. The 
        Butler-Reeds-Dawson (BRD) beta update is usually highly sparse and often 
        less than 10 beta values will be explored if the proposed range is used. 
        Also the lower limit should be choosen smaller than beta_guess, because 
        although very rarely observed it is not to exclude that the BRD beta update 
        might lead to a decrease in beta value although in the vast majority of 
        cases beta does monotonically increase from beta_guess up to the upper 
        beta limit
        
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
    
    T1_int: Logarithmically spaced relaxation times or diffusion coefficients

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T1'] = np.copy(opt['#T1 2d'])
    opt['#T2'] = np.copy(opt['#T1 2d'])
    opt['t2'] = np.copy(opt['t1'])
       
    if DataType == 'custom':
        Dis, T1, _ = d2.mtgv_gcv_fb(opt, args[0], args[0])
        
    elif DataType == 'T1T1' or DataType == 'T2T2':
        Dis, T1, _ = d2.mtgv_gcv_fb(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    proj_1 = np.sum(Dis, axis = 0)
    proj_1 /= np.sum(proj_1)
    proj_2 = np.sum(Dis, axis = 1)
    proj_2 /= np.sum(proj_2)
    Dis = (proj_1 + proj_2) / 2 
    T1_int = np.logspace(np.log10(np.min(T1)), np.log10(np.max(T1)), 
                         opt['#T1 1d'])
    Dis = Akima1DInterpolator(np.log10(T1), Dis)(np.log10(T1_int))
    
    return Dis, T1_int


def l2_gcv(opt, *args):
    """
    This function employs the 2d version of l2_gcv to calculate a 1d
    distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.l2_gcv
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. However, the marginal 
    distributions tend to span across less data points than it would be normally
    expected for a 1d distribution. Hence, the average marginal distribution is
    interpolated via the Akima method to a return a final 1d distribution covering
    a number of data points more suitable to the problem of interest. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1 2d': 18,
               '#T1 1d': 128,
               't1': t1,
               'exp type': 'T2T2',
               'max iter': 500,
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1), len(t1)) 
        
        noise: Noise estimate of your data. This should be a single number

        #T1 2d: Number of values in both dimensions of the to-be-estimated 2d 
        distribution
        
        #T1 1d: Number of values in the final interpolated 1d distribution

        T1 bounds: The lower and upper limit of the to-be-estimated 2d distribution

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
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
        
        with Dis_gf normalized to be ranging from 0 to 1. The weighted L2 results
        is then multiplied with the 'uniform' estimate to generate the final
        distribution
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1_int: Logarithmically spaced relaxation times or diffusion coefficients

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T1'] = np.copy(opt['#T1 2d'])
    opt['#T2'] = np.copy(opt['#T1 2d'])
    opt['t2'] = np.copy(opt['t1'])
       
    if DataType == 'custom':
        Dis, T1, _ = d2.l2_gcv(opt, args[0], args[0])
        
    elif DataType == 'T1T1' or DataType == 'T2T2':
        Dis, T1, _ = d2.l2_gcv(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    proj_1 = np.sum(Dis, axis = 0)
    proj_1 /= np.sum(proj_1)
    proj_2 = np.sum(Dis, axis = 1)
    proj_2 /= np.sum(proj_2)
    Dis = (proj_1 + proj_2) / 2 
    T1_int = np.logspace(np.log10(np.min(T1)), np.log10(np.max(T1)), 
                         opt['#T1 1d'])
    Dis = Akima1DInterpolator(np.log10(T1), Dis)(np.log10(T1_int))
    
    return Dis, T1_int


def l1_gcv(opt, *args):
    """
    This function employs the 2d version of l1_gcv to calculate a 1d
    distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.l1_gcv
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. However, the marginal 
    distributions tend to span across less data points than it would be normally
    expected for a 1d distribution. Hence, the average marginal distribution is
    interpolated via the Akima method to a return a final 1d distribution covering
    a number of data points more suitable to the problem of interest. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'data': Sig,
               'noise': NoiseStd,
               'T1 bounds': [0.001, 10],
               '#T1 2d': 18,
               '#T1 1d': 128,
               't1': t1,
               'exp type': 'T2T2',
               'max iter': 500,
               'inv tol': 1e-3,
               'alpha tol': 1e-2,
               'pen type': 'gaussian'}
        
        data: Experimental data given as a numpy array of shape (len(t1), len(t1)) 
        
        noise: Noise estimate of your data. This should be a single number

        #T1 2d: Number of values in both dimensions of the to-be-estimated 2d 
        distribution
        
        #T1 1d: Number of values in the final interpolated 1d distribution

        T1 bounds: The lower and upper limit of the to-be-estimated 2d distribution

        t1: Logarithmically spaced time delays used for relaxation encoding or 
        diffusion encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
        For reference: https://doi.org/10.1063/1.1673336 

        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
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
        
        with Dis_gf normalized to be ranging from 0 to 1. The weighted L2 results
        is then multiplied with the 'uniform' estimate to generate the final
        distribution
        
    *args : Additional arguments. Used to pass a custom kernel if DataType is
    'custom'

    Returns
    -------
    Dis : Normalized distribution
    
    T1_int: Logarithmically spaced relaxation times or diffusion coefficients

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T1'] = np.copy(opt['#T1 2d'])
    opt['#T2'] = np.copy(opt['#T1 2d'])
    opt['t2'] = np.copy(opt['t1'])
       
    if DataType == 'custom':
        Dis, T1, _ = d2.l1_gcv(opt, args[0], args[0])
        
    elif DataType == 'T1T1' or DataType == 'T2T2':
        Dis, T1, _ = d2.l1_gcv(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    proj_1 = np.sum(Dis, axis = 0)
    proj_1 /= np.sum(proj_1)
    proj_2 = np.sum(Dis, axis = 1)
    proj_2 /= np.sum(proj_2)
    Dis = (proj_1 + proj_2) / 2 
    T1_int = np.logspace(np.log10(np.min(T1)), np.log10(np.max(T1)), 
                         opt['#T1 1d'])
    Dis = Akima1DInterpolator(np.log10(T1), Dis)(np.log10(T1_int))
    
    return Dis, T1_int


def simulate(opt, *args):
    """
    This function employs the 2d version of the simulate fucntion to calculate 
    a 1d distribution. For further details on the original 2d algorithm, see the
    docstring of cam_ilt.reg_inv.d2.simulate
    
    It assumes a 'T1T1', 'T2T2' or 'DD' exchange experiment with an effective 
    exchange time being close to zero. A 2d distribution is estimated via the 
    2d algorithm and the 1d distribution is calculated as the average of the marginal
    distributions stemming from the 2d distribution. 
    
    Parameters
    ----------
    opt : Dictionary which collects all necessary inputs. For further details, 
    see the following example:
        
        opt = {'T1 bounds': [0.001, 10],
               '#T1': 18,
               '#t1': 18,
               'exp type': 'T2T2',
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
        
        exp type: String which defines the type of kernel used. Options are 'T2T2'
        for T2-T2 exchange with monoexponential encodings in both dimensions, 
        'T1T1' for a T1-T1 exchange like experiment with a saturation recovery 
        encoding in both dimensions, 'DD' for D-D exchange with Stejskal-Tanner 
        like encodings in both dimensions and 'custom' if an user-defined custom 
        kernel is provided. 
        
        weights: Weights of different relaxation or diffusion components. Should
        add up to 1.
        
        log mean T1: log10(T1) mean for every relaxation or diffusion component
        
        log std T1: log10(T1) standard deviation for every relaxation or diffusion
        component
        
        SNR: signal to noise ratio which the simulated data should have
    
    Returns
    -------
    Sig: Simulated experimental data which is 2-dimensional
    
    Dis: Simulated distribution which is 1-dimensional
    
    T1: Logarithmically spaced relaxation times or diffusion coefficient in the
    range of T1 bounds
    
    t1: Logarithmically spaced time delays used for relaxation encoding or diffusion 
    encodings of the type gamma^2 delta^2 (big_delta - delta / 3) g^2 
    For reference: https://doi.org/10.1063/1.1673336 
       
    NoiseStd: Noise estimate calculated that the simulated data fits the given SNR 

    """
    DataType = np.copy(opt['exp type'])
    opt['T2 bounds'] = np.copy(opt['T1 bounds'])
    opt['#T2'] = np.copy(opt['#T1'])
    opt['#t2'] = np.copy(opt['#t1'])
    opt['log mean T2'] = np.copy(opt['log mean T1'])
    opt['log std T2'] = np.copy(opt['log std T1'])
       
    if DataType == 'custom':
        Sig, Dis, T1, _, t1, _, NoiseStd = d2.simulate(opt, args[0], args[0], 
                                                       args[1], args[1])
        
    elif DataType == 'T1T1' or DataType == 'T2T2' or DataType == 'DD':
        Sig, Dis, T1, _, t1, _, NoiseStd = d2.simulate(opt)
        
    else:
        raise ValueError('Invalid Data Type')
        
    proj_1 = np.sum(Dis, axis = 0)
    proj_1 /= np.sum(proj_1)
    proj_2 = np.sum(Dis, axis = 1)
    proj_2 /= np.sum(proj_2)
    Dis = (proj_1 + proj_2) / 2 
    
    return Sig, Dis, T1, t1, NoiseStd
