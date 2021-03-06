#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 09:26:16 2018

@author: Faïcel Chamroukhi & Bartcus Marius
"""
import numpy as np
import enums
import utils as utl
from sklearn.cluster import KMeans

class MixParam:
    def __init__(self, mixModel, options):
        """
        ({Wg},{alpha_g}, {beta_gk},{sigma_gk}) for g=1,...,G and k=1...K. 
              1. Wg = (Wg1,...,w_gK-1) parameters of the logistic process:
                  matrix of dimension [(q+1)x(K-1)] with q the order of logistic regression.
              2. beta_g = (beta_g1,...,beta_gK) polynomial regression coefficient vectors: matrix of
                  dimension [(p+1)xK] p being the polynomial  degree.
              3. sigma_g = (sigma_g1,...,sigma_gK) : the variances for the K regmies. vector of dimension [Kx1]
              4. pi_jgk :logistic proportions for cluster g
        """
        self.Wg = np.zeros([mixModel.G, mixModel.q+1, mixModel.K-1])
        self.beta_g = np.NaN * np.empty([mixModel.G, mixModel.p+1, mixModel.K])
        
        if options.variance_type == enums.variance_types.common:
            self.sigma_g = np.NaN * np.empty([mixModel.G, 1])
        else:
            self.sigma_g = np.NaN * np.empty([mixModel.G, mixModel.K])
        self.pi_jgk = np.NaN * np.empty([mixModel.G, mixModel.m*mixModel.n, mixModel.K])
        self.alpha_g = np.NaN * np.empty(mixModel.G)
    
    def initParam(self, mixModel, phi, mixOptions, try_algo):
        # 1. Initialization of cluster weights
        self.alpha_g=1/mixModel.G*np.ones(mixModel.G)
        
        # 2. Initialization of the model parameters for each cluster: W (pi_jgk), betak and sigmak    
        #self.Wg, self.pi_jgk = 
        self.__initHlp(mixModel, phi.Xw, try_algo)
        
        # 3. Initialization of betagk and sigmagk
        if mixOptions.init_kmeans:
            kmeans = KMeans(n_clusters = mixModel.G, init = 'k-means++', max_iter = 400, n_init = 20, random_state = 0)
            klas = kmeans.fit_predict(mixModel.X)
            
            for g in range(0,mixModel.G):
                Xg = mixModel.X[klas==g ,:]; #if kmeans  
                self.__initRegressionParam(Xg, g, mixModel.K, mixModel.p, phi.XBeta, mixOptions.variance_type, try_algo)
                
        else:
            print('todo: line 41 matlab initialize_MixFRHLP_EM')
            raise RuntimeError('todo: line 41 matlab initialize_MixFRHLP_EM')
            
    def __initRegressionParam(self, Xg, g, K, p, XBeta, variance_type, try_algo):
        """
        aim: initialize the Regresssion model with Hidden Logistic Process
        requires:
            data - the data set
            K - the number of regimes
            phi
            variance_type - variance type
            try_EM - em try
        ensures:
            sigma
            betak
        """
        n, m = Xg.shape
        if try_algo == 1:
            # Decoupage de l'echantillon (signal) en K segments
            zi = round(m/K) - 1
            #initialization of sigma and betak can be improved (todo)
            sigma=[]
            betak_list = []
            for k in range(1, K+1):
                i = (k-1)*zi;
                j = k*zi;
                Xij = Xg[:,i:j];
                Xij = np.reshape(Xij,(np.prod(Xij.shape), 1))
                phi_ij = XBeta[i:j,:];
                Phi_ij = np.matlib.repmat(phi_ij, n, 1);
                bk = np.linalg.inv(Phi_ij.T@Phi_ij)@Phi_ij.T@Xij;
                #para.betak(:,k) = bk;
                betak_list.append(bk)
                if variance_type == enums.variance_types.common:
                    sigma = np.var(Xij)
                else:
                    mk = j-i
                    z = Xij-Phi_ij@bk;
                    
                    sk = z.T@z/(n*mk); 
                    sigma.append(sk[0][0])
            #remake betak
            betak = np.hstack(betak_list)
        else:
            #random initialization
            Lmin= round(m/K)#nbr pts min dans un segments
            tk_init = [0] * (K+1)
            #tk_init[0]=-1
            K_1=K;
            #todo: verify indexes ???
            for k in range(1,K):
                K_1 = K_1-1
                start = tk_init[k-1]+Lmin
                stop = m-K_1*Lmin
                
                if start>stop:
                    stop = stop-1
                    step = -1
                else:
                    stop = stop+1
                    step=1
                
                temp = list(range(start,stop,step))
                ind = np.random.permutation(len(temp))
                tk_init[k]= temp[ind[0]];
               
            tk_init[K] = m; 
            #print(tk_init) 
            sigma=[]
            betak_list = []
            for k in range(0, K):
                i = tk_init[k]+1;
                j = tk_init[k+1];
                Xij = Xg[:,i:j];
                Xij = np.reshape(Xij,(np.prod(Xij.shape), 1))
                phi_ij = XBeta[i:j,:];
                Phi_ij = np.matlib.repmat(phi_ij, n, 1);
                bk = np.linalg.inv(Phi_ij.T@Phi_ij)@Phi_ij.T@Xij;
                betak_list.append(bk)
                if variance_type == enums.variance_types.common:
                    sigma = np.var(Xij)
                else:
                    mk = j-i
                    z = Xij-Phi_ij@bk;
                    sk = z.T@z/(n*mk); 
                    sigma.append(sk[0][0])
            #remake betak
            betak = np.hstack(betak_list)
        
        self.beta_g[g,:,:] = betak;
        if variance_type == enums.variance_types.common:
            self.sigma_g[g] = sigma;
        else:
            self.sigma_g[g,:] = sigma;
        
    def __initHlp(self, mixModel, Xw, try_algo):
        """
            Initialize the Hidden Logistic Process
        """
        # 1. Initialisation de W (pi_jgk)
        nm, q1 = Xw.shape;
        if  try_algo ==1:
            for g in range(0,mixModel.G):
                self.pi_jgk[g,:,:] = utl.modele_logit(self.Wg[g,:,:],Xw)[0];
        else:
            for g in range(0,mixModel.G):
                self.Wg[g,:,:] = np.random.rand(mixModel.q+1,mixModel.K-1); #random initialization of the parameter vector of IRLS
                self.pi_jgk[g,:,:] = utl.modele_logit(self.Wg[g,:,:],Xw)[0];
    
    def CMStep(self, mixModel, mixStats, phi, mixOptions):
        self.alpha_g = mixStats.c_ig.sum(0).T/mixModel.n
        # Maximization w.r.t betagk et sigmagk
        cluster_labels =  np.matlib.repmat(mixStats.klas,1,mixModel.m).T # [m x n]
        cluster_labels = cluster_labels.T.ravel()
        # Maximization w.r.t betagk et sigmagk
        for g in range(0,mixModel.G):
            Xg = mixModel.XR[cluster_labels==g ,:]; # cluster g (found from a hard clustering)
            tauijk = mixStats.tau_ijgk[g,cluster_labels==g,:]
            if mixOptions.variance_type == enums.variance_types.common:
                s = 0 
            else:
                sigma_gk = np.zeros((mixModel.K,1))
                
            beta_gk = np.NaN * np.empty([mixModel.p+1, mixModel.K])
            for k in range(0,mixModel.K):
                segment_weights = np.array([tauijk[:,k]]).T #weight for the hth segment of cluster g  
                phigk = (np.sqrt(segment_weights)@np.ones((1,mixModel.p+1)))*phi.phiBeta[cluster_labels==g,:] #[(n*m)*(p+1)]
                Xgk = np.sqrt(segment_weights)*Xg
                # maximization w.r.t beta_gk: Weighted least squares 
                temp = np.linalg.inv(phigk.T@phigk + np.spacing(1)*np.eye(mixModel.p+1))@phigk.T@Xgk
                beta_gk[:,k] = temp.ravel() # Maximization w.r.t betagk
                # Maximization w.r.t au sigma_gk :  
                if mixOptions.variance_type == enums.variance_types.common:
                    sk = sum((Xgk-phigk@beta_gk[:,k])**2)
                    s = s+sk
                    sigma_gk = s/sum(sum(tauijk))
                else:
                    temp = phigk@np.array([beta_gk[:,k]]).T
                    if (sum(segment_weights)==0):
                        good_segmentation = False
                        return 0, good_segmentation
                    sigma_gk[k]= sum((Xgk-temp)**2)/(sum(segment_weights))
                    
            self.beta_g[g,:,:] = beta_gk
            self.sigma_g[g,:] = list(sigma_gk)
            
            """
            Maximization w.r.t W 
            IRLS : Regression logistique multinomiale pondérée par cluster
            """
            Wg_init = self.Wg[g,:,:]
            
            wk, piik, reg_irls, _, _ = utl.IRLS(tauijk, phi.Xw[cluster_labels==g,:], Wg_init)
            
            self.Wg[g,:,:]=wk;             
            self.pi_jgk[g,:,:] = np.matlib.repmat(piik[0:mixModel.m,:],mixModel.n,1)
            
        return reg_irls, True
            
    def MStep(self, mixModel, mixStats, phi, mixOptions):
        """
        M-step
        """
        # Maximization w.r.t alpha_g
        self.alpha_g = np.array([mixStats.h_ig.sum(axis=0)]).T/mixModel.n
        
        # Maximization w.r.t betagk et sigmagk
        for g in range(0,mixModel.G):
            temp =  np.matlib.repmat(mixStats.h_ig[:,g],mixModel.m,1) # [m x n]
            cluster_weights = temp.T.reshape(temp.size,1)
            tauijk = mixStats.tau_ijgk[g,:,:] #[(nxm) x K]
            if mixOptions.variance_type == enums.variance_types.common:  
                s = 0 
            else:
                sigma_gk = np.zeros((mixModel.K,1))
            
            beta_gk = np.NaN * np.empty([mixModel.p +1, mixModel.K])
            for k in range(0,mixModel.K):
                segment_weights = np.array([tauijk[:,k]]).T #weight for kth segment of cluster g
                # weights to get K smoothed segments  for the gth smoothed cluster 
                phigk = (np.sqrt(cluster_weights*segment_weights)@np.ones((1,mixModel.p+1)))*phi.XBeta #[(n*m)*(p+1)]
                Xgk = np.sqrt(cluster_weights*segment_weights)*mixModel.XR
                
                # maximization w.r.t beta_gk: Weighted least squares
                temp = np.linalg.inv(phigk.T@phigk + np.spacing(1)*np.eye(mixModel.p+1))@phigk.T@Xgk
                beta_gk[:,k] = temp.ravel() # Maximization w.r.t betagk
                
                # Maximization w.r.t au sigma_gk :   
                if mixOptions.variance_type == enums.variance_types.common:
                    sk = sum((Xgk-np.array([phigk@beta_gk[:,k]]).T)**2)
                    s = s+sk;
                    sigma_gk = s/sum(sum(cluster_weights@np.ones((1,mixModel.K))*tauijk))
                else:
                    temp = phigk@np.array([beta_gk[:,k]]).T
                    sigma_gk[k]= sum((Xgk-temp)**2)/(sum(cluster_weights*segment_weights))
                    
            self.beta_g[g,:,:] = beta_gk
            self.sigma_g[g,:] = list(sigma_gk)
            
            """
            Maximization w.r.t W 
            IRLS : Regression logistique multinomiale pondérée par cluster
            """
            Wg_init = self.Wg[g,:,:]
            
            wk, piik, _, _, _ = utl.IRLS(tauijk, phi.Xw, Wg_init, cluster_weights)
            
            self.Wg[g,:,:]=wk;             
            self.pi_jgk[g,:,:] = np.matlib.repmat(piik[0:mixModel.m,:],mixModel.n,1); 
    