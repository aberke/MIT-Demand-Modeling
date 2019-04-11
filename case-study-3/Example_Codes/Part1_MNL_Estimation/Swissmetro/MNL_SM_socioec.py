# Translated to .py by Marti Montesinos
# Modified by Peiyu Jing

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio

pandas = pd.read_table("swissmetro.dat")
database = db.Database("swissmetro",pandas)

from headers import *

# Specify parameters to estimate
#1: the name of the parameter,
#2: the default value,
#3: a lower bound (or None, if no bound is specified),
#4: an upper bound, (or None, if no bound is specified),
#5: a flag that indicates if the parameter must be estimated (0) or if it keeps its default value.
ASC_CAR	 = Beta('ASC_CAR',0,-20,20,0)
ASC_SBB	 = Beta('ASC_SBB',0,-10,10,1)
ASC_SM	 = Beta('ASC_SM',0,-20,20,0)
B_CAR_COST	 = Beta('B_CAR_COST',0,-10,10,0)
B_HE	 = Beta('B_HE',0,-10,10,0)
B_SM_COST	 = Beta('B_SM_COST',0,-10,10,0)
B_TIME	 = Beta('B_TIME',0,-10,10,0)
B_TRAIN_COST	 = Beta('B_TRAIN_COST',0,-10,10,0)
B_SENIOR	 = Beta('B_SENIOR',0,-10,10,0)
B_GA	 = Beta('B_GA',0,-10,80,0)

# Define here arithmetic expressions for name that are not directly 
# available from the data

SENIOR  = DefineVariable('SENIOR', AGE   ==  5,database )
CAR_AV_SP  = DefineVariable('CAR_AV_SP', CAR_AV    *  (  SP   !=  0  ),database)
SM_COST  = DefineVariable('SM_COST', SM_CO   * (  GA   ==  0  ),database)
TRAIN_AV_SP  = DefineVariable('TRAIN_AV_SP', TRAIN_AV    *  (  SP   !=  0  ),database)
TRAIN_COST  = DefineVariable('TRAIN_COST', TRAIN_CO   * (  GA   ==  0  ),database)
one  = DefineVariable('one',1,database)

#Utilities
Car_SP = ASC_CAR * one + B_TIME * CAR_TT + B_CAR_COST * CAR_CO + B_SENIOR * SENIOR
SBB_SP = ASC_SBB * one + B_TIME * TRAIN_TT + B_TRAIN_COST * TRAIN_COST + B_HE * TRAIN_HE + B_GA * GA
SM_SP = ASC_SM * one + B_TIME * SM_TT + B_SM_COST * SM_COST + B_HE * SM_HE + B_GA * GA + B_SENIOR * SENIOR
V = {3: Car_SP,1: SBB_SP,2: SM_SP}
av = {3: CAR_AV_SP,1: TRAIN_AV_SP,2: SM_AV}

# Here we use the "biogeme" way for backward compatibility
exclude = (((  PURPOSE   !=  1  ) * (  PURPOSE   !=  3  )) + (  CHOICE   ==  0  ) + (  AGE == 6  ))>0
database.remove(exclude)

# Estimation of the model
logprob = bioLogLogit(V,av,CHOICE)
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "MNL_SM_socioec"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)