%
% Curve clustering with the MixFRHLP model and the EM (or a CEM-like)
% algorithm
%
%%%% Faicel Chamroukhi (2011)%%%%%%%
%
%   When using this code please cite the following papers : The two first
%   ones concern the model and its use in clusterng and the two last ones
%   concern the model and its use in discrimination.
%
% @article{Chamroukhi-RHLP-2009,
% 	Author = {Chamroukhi, F. and Sam\'{e}, A. and Govaert, G. and Aknin, P.},
% 	Journal = {Neural Networks},
% 	Number = {5-6},
% 	Pages = {593--602},
% 	Publisher = {Elsevier Science Ltd.},
% 	Title = {Time series modeling by a regression approach based on a latent process},
% 	Volume = {22},
% 	Year = {2009}
%     }
%
% @article{Chamroukhi-MixRHLP-2011,
% 	Author = {Sam{\'e}, A. and Chamroukhi, F. and Govaert, G{\'e}rard and Aknin, P.},
% 	Issue = 4,
% 	Journal = {Advances in Data Analysis and Classification},
% 	Pages = {301--321},
% 	Publisher = {Springer Berlin / Heidelberg},
% 	Title = {Model-based clustering and segmentation of time series with changes in regime},
% 	Volume = 5,
% 	Year = {2011}
%     }
%
% @article{Chamroukhi-RHLP-FLDA,
% 	Author = {Chamroukhi, F. and Sam\'{e}, A. and Govaert, G. and Aknin, P.},
% 	Journal = {Neurocomputing},
% 	Number = {7-9},
% 	Pages = {1210--1221},
% 	Title = {A hidden process regression model for functional data description. Application to curve discrimination},
% 	Volume = {73},
% 	Year = {2010}
%     }
%
% @article{Chamroukhi-FMDA-2013,
% 	Author = {Chamroukhi, F. and Glotin, H. and Sam{\'e}, A.},
% 	Journal = {Neurocomputing},
% 	Pages = {153-163},
% 	Title = {Model-based functional mixture discriminant analysis with hidden process regression for curve classification},
% 	Volume = {112},
% 	Year = {2013}
%     }    


clear all;
close all;
clc;

%%% simulated data set and a benchmarck

%% simulated data 

n1 = 10 ;  n2 = 10 ;    n3 = 10;

%load mean_1_flou;
%y1 =ones(n1,1)*mean_1_flou'+ normrnd(5,1,length(mean_1_flou),n1)'+1;
%y3 = [normrnd(7,1,80,n2);normrnd(5,1,130,n2); normrnd(4,1,140,n2)]';
%y2 = [normrnd(5,1,120,n3);normrnd(7,1,70,n3);normrnd(5,1,160,n3)]';
%data = [y1 ; y2 ; y3];
data = importdata('generated_data_1.txt');

G = 3;% nombre de clusters
K = 3;% nombre de regimes
p = 1;% dimension de beta (ordre de reg polynomiale)
q = 1;% dimension de w (ordre de reg logistique)


%% waveform benchmark
% 
% load waveform;
% n = 50;  klas= [ones(n,1);2*ones(n,1);3*ones(n,1)];
% data = [waveform.clas1(1:n,:); waveform.clas2(1:n,:) ;waveform.clas3(1:n,:)];
% 
% G = 3;% nombre de clusters
% K = 2;% nombre de regimes
% p = 3;% dimension de beta (ordre de reg polynomiale)
% q = 1;% dimension de w (ordre de reg logistique)



%type_variance = 'common';
type_variance = 'free';
variance_type='free';
n_tries = 2;
max_iter = 1000;
init_kmeans = 1;
threshold = 1e-5;
verbose = 1; 
verbose_IRLS = 0;


[n, m]=size(data);

solution =  MixFRHLP_EM(data, G , K, p, q, type_variance, init_kmeans, n_tries, max_iter, threshold, verbose, verbose_IRLS);        

%solution =  MixFRHLP_CEM(data, G , K, p, q, type_variance, init_kmeans, n_tries, max_iter, threshold, verbose, verbose_IRLS);        

% bic(K)=solution.BIC;
% aic(K)=solution.AIC;
% icl(K)=solution.ICL1;
% end



%afficher_resultats(data,solution)











