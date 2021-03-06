# Python codes for functional data clustering and segmentation with the mixture of regressions with hidden logistic processes (MixRHLP) model: 

<< R and Matlab versions are aslo available on Github>>

python codes written by

**Faicel Chamrouckhi**
&
**Marius Bartcus**

firstname.lastname@unicaen.fr

The needed packages to run our code are: NumPy and matplotlib.



### SHORT DESCRIPTION OF EACH PYTHON FILE. For more detailed description, please see the individual files

1) main_MixFRHLP_EM _Main script to run the EM or CEM algorithm_
2) ModelLearner.py _Contains the two functions of the EM and the CEM algorithms._
3) datasets _Contains the object to load (mainly the dataset)_                        
4) MixModel.py _The MixModel class containts the data object and the model settings (number of clusters, the number of segments, the degree of polynomials, the order of the logistic regression)_
4) MixParam.py _Initializes and updates (the M-step) the model parameters._
5) MixStats.py _Calculates the conditional memberships (responsibilities) (E-step), the loglikelihood, the data partition, and information criterias BIC, ICL, etc_
6) ModelOptions.py _contains algorithm settings (like the number of runs/iterations, convergence threshold, type of initialization, etc)._
8) enums.py _Used to enumerate the variance type (heteroskedastic or homoscedastic)_
9) RegressionDesinger.py _Design matrices for the polynomial regression and the logistic regression_
10) utils.py _Contains mainly the model_logit function that calculates the multinomial logistic pobabilities, and an efficient Iteratively Reweighted Least-Squares (IRLS) algorithm.


When using this code please cite the following papers : The two first ones concern the model and its use in clustering and the last ones concern the model and its use in discrimination.


```
 @article{Chamroukhi-RHLP-2009,
 	Author = {Chamroukhi, F. and Sam\'{e}, A. and Govaert, G. and Aknin, P.},
 	Journal = {Neural Networks},
 	Number = {5-6},
 	Pages = {593--602},
	Publisher = {Elsevier Science Ltd.},
 	Title = {Time series modeling by a regression approach based on a latent process},
 	Volume = {22},
 	Year = {2009}
     }
 @article{Chamroukhi-MixRHLP-2011,
 	Author = {Sam{\'e}, A. and Chamroukhi, F. and Govaert, G{\'e}rard and Aknin, P.},
 	Issue = 4,
 	Journal = {Advances in Data Analysis and Classification},
 	Pages = {301--321},
 	Publisher = {Springer Berlin / Heidelberg},
 	Title = {Model-based clustering and segmentation of time series with changes in regime},
 	Volume = 5,
 	Year = {2011}
     }

 @article{Chamroukhi-RHLP-FLDA,
 	Author = {Chamroukhi, F. and Sam\'{e}, A. and Govaert, G. and Aknin, P.},
 	Journal = {Neurocomputing},
 	Number = {7-9},
 	Pages = {1210--1221},
 	Title = {A hidden process regression model for functional data description. Application to curve discrimination},
 	Volume = {73},
 	Year = {2010}
     }

 @article{Chamroukhi-FMDA-2013,
 	Author = {Chamroukhi, F. and Glotin, H. and Sam{\'e}, A.},
 	Journal = {Neurocomputing},
 	Pages = {153-163},
 	Title = {Model-based functional mixture discriminant analysis with hidden process regression for curve classification},
 	Volume = {112},
 	Year = {2013}
     }  
@article{Chamroukhi-FDA-2018,
 	Journal = {Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery},
 	Author = {Faicel Chamroukhi and Hien D. Nguyen},
 	Note = {DOI: 10.1002/widm.1298.},
 	Volume = {},
 	Title = {Model-Based Clustering and Classification of Functional Data},
 	Year = {2019},
 	Month = {to appear},
 	url =  {https://chamroukhi.com/papers/MBCC-FDA.pdf}
    }
```
