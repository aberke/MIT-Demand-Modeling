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

ASC_CAR	 = Beta('ASC_CAR',0,-30,30,0)
ASC_SBB	 = Beta('ASC_SBB',0,-10,10,1)
ASC_SM	 = Beta('ASC_SM',0,-30,30,0)
B_COST	 = Beta('B_COST',0,-10,10,0)
B_HE	 = Beta('B_HE',0,-10,10,0)
B_TIME	 = Beta('B_TIME',0,-10,10,0)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())


# Define here arithmetic expressions for name that are not directly 
# available from the data

CAR_AV_SP  = DefineVariable('CAR_AV_SP', CAR_AV    *  (  SP   !=  0  ),database)
SM_COST  = DefineVariable('SM_COST', SM_CO   * (  GA   ==  0  ),database)
TRAIN_AV_SP  = DefineVariable('TRAIN_AV_SP', TRAIN_AV    *  (  SP   !=  0  ),database)
TRAIN_COST  = DefineVariable('TRAIN_COST', TRAIN_CO   * (  GA   ==  0  ),database)
one  = DefineVariable('one',1,database)

#Utilities
Car_SP = ASC_CAR * one + B_TIME * CAR_TT + B_COST * CAR_CO
SBB_SP = ASC_SBB * one + B_TIME * TRAIN_TT + B_COST * TRAIN_COST + B_HE * TRAIN_HE
SM_SP = ASC_SM * one + B_TIME * SM_TT + B_COST * SM_COST + B_HE * SM_HE
V = {3: Car_SP,1: SBB_SP,2: SM_SP}
av = {3: CAR_AV_SP,1: TRAIN_AV_SP,2: SM_AV}

# Here we use the "biogeme" way for backward compatibility
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
database.remove(exclude)

# Estimation of the model
logprob = bioLogLogit(V,av,CHOICE)
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "MNL_SM_generic"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)
