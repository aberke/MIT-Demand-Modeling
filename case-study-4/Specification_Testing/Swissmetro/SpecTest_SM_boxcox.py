# Translated to .py by Marti Montesinos
# Modified by Peiyu Jing

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio

pandas = pd.read_table("swissmetro.dat")
database = db.Database("swissmetro",pandas)

from headers import *

#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_CAR	 = Beta('ASC_CAR',0,-10,10,0)
ASC_SBB	 = Beta('ASC_SBB',0,-1,1,1)
ASC_SM	 = Beta('ASC_SM',0,-10,10,0)
B_CAR_COST	 = Beta('B_CAR_COST',0,-1,1,0)
B_CAR_TIME	 = Beta('B_CAR_TIME',0,-1,1,0)
B_GA	 = Beta('B_GA',0,-1,1,0)
B_HE	 = Beta('B_HE',0,-1,1,0)
B_SM_COST	 = Beta('B_SM_COST',0,-1,1,0)
B_SM_TIME	 = Beta('B_SM_TIME',0,-1,1,0)
B_TRAIN_COST	 = Beta('B_TRAIN_COST',0,-1,1,0)
B_TRAIN_TIME	 = Beta('B_TRAIN_TIME',0,-1,1,0)
LAMBDA	 = Beta('LAMBDA',0.2,-3,3,0)

# Define here arithmetic expressions for name that are not directly 
# available from the data

SENIOR  = DefineVariable('SENIOR', AGE   ==  5, database )
CAR_AV_SP  = DefineVariable('CAR_AV_SP', CAR_AV    *  (  SP   !=  0  ), database)
SM_COST  = DefineVariable('SM_COST', SM_CO   * (  GA   ==  0  ), database)
TRAIN_AV_SP  = DefineVariable('TRAIN_AV_SP', TRAIN_AV    *  (  SP   !=  0  ), database)
TRAIN_COST  = DefineVariable('TRAIN_COST', TRAIN_CO   * (  GA   ==  0  ), database)
TRAIN_TT_SQ  = DefineVariable('TRAIN_TT_SQ', TRAIN_TT   ** 2, database  )
one  = DefineVariable('one',1, database)

#Utilities
Car_SP = ASC_CAR * one + B_CAR_TIME * CAR_TT + B_CAR_COST * CAR_CO
SBB_SP = ASC_SBB * one + B_TRAIN_COST * TRAIN_COST + B_HE * TRAIN_HE + B_GA * GA +  B_TRAIN_TIME   * ( ( (  TRAIN_TT   **  LAMBDA   ) -  1  ) /  LAMBDA   )
SM_SP = ASC_SM * one + B_SM_TIME * SM_TT + B_SM_COST * SM_COST + B_HE * SM_HE + B_GA * GA
V = {3: Car_SP,1: SBB_SP,2: SM_SP}
av = {3: CAR_AV_SP,1: TRAIN_AV_SP,2: SM_AV}

# Exclude
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) + ( CHOICE == 0 )) + ( AGE   ==  6  ) > 0
database.remove(exclude)

# Estimation of the model
logprob = bioLogLogit(V,av,CHOICE)
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "SpecTest_SM_boxcox"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)
