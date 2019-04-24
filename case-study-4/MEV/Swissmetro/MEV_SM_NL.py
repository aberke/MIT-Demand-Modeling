# Translated to .py by Evanthia Kazagli
# Modified by Peiyu Jing

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models

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
ASC_CAR	 = Beta('ASC_CAR',0,-20,20,0)
ASC_SBB	 = Beta('ASC_SBB',0,-10,10,1)
ASC_SM	 = Beta('ASC_SM',0,-20,20,0)
B_HE	 = Beta('B_HE',0,-10,10,0)
B_COST	 = Beta('B_COST',0,-10,10,0)
B_CAR_TIME	 = Beta('B_CAR_TIME',0,-10,10,0)
B_SBB_TIME	 = Beta('B_SBB_TIME',0,-10,10,0)
B_SM_TIME	 = Beta('B_SM_TIME',0,-10,10,0)
B_SENIOR	 = Beta('B_SENIOR',0,-10,10,0)
B_GA	 = Beta('B_GA',0,-10,80,0)
# parameters relevant to the nests
MU_classic = Beta('MU_classic',1,1,10,0)

# Define here arithmetic expressions for name that are not directly 
# available from the data
SENIOR  = DefineVariable('SENIOR', AGE   ==  5, database )
CAR_AV_SP  = DefineVariable('CAR_AV_SP', CAR_AV    *  (  SP   !=  0  ), database)
SM_COST  = DefineVariable('SM_COST', SM_CO   * (  GA   ==  0  ), database)
TRAIN_AV_SP  = DefineVariable('TRAIN_AV_SP', TRAIN_AV    *  (  SP   !=  0  ), database)
TRAIN_COST  = DefineVariable('TRAIN_COST', TRAIN_CO   * (  GA   ==  0  ), database)
one  = DefineVariable('one',1, database)

# Utilities
Car_SP = ASC_CAR * one + B_CAR_TIME * CAR_TT + B_COST * CAR_CO
SBB_SP = ASC_SBB * one + B_SBB_TIME * TRAIN_TT + B_COST * TRAIN_COST + B_HE * TRAIN_HE + B_GA * GA
SM_SP = ASC_SM * one + B_SM_TIME * SM_TT + B_COST * SM_COST + B_HE * SM_HE + B_GA * GA
V = {3: Car_SP,1: SBB_SP,2: SM_SP}
av = {3: CAR_AV_SP,1: TRAIN_AV_SP,2: SM_AV}

# Exclude
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) + ( CHOICE == 0 )) + ( AGE   ==  6  ) > 0
database.remove(exclude)

# Definition of nests
innovative = 1.0, [2]
classic = MU_classic, [1, 3]

nests = classic, innovative

# Estimation of the model
logprob = models.lognested(V,av,nests,CHOICE)
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "MEV_SM_NL"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)
