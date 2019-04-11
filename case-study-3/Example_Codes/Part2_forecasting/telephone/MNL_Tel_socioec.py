# Translated to .py by Monique Stinson
# Modified by Peiyu Jing

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio

pandas = pd.read_table("telephone.dat")
database = db.Database("telephone",pandas)

from headers import *

# Specify parameters to estimate
#1: the name of the parameter,
#2: the default value,
#3: a lower bound (or None, if no bound is specified),
#4: an upper bound, (or None, if no bound is specified),
#5: a flag that indicates if the parameter must be estimated (0) or if it keeps its default value.
ASC_BM	 = Beta('ASC_BM',0,-10,10,0)
ASC_SM	 = Beta('ASC_SM',0,-10,10,1)
ASC_LF	 = Beta('ASC_LF',0,-10,10,0)
ASC_EF	 = Beta('ASC_EF',0,-10,10,0)
ASC_MF	 = Beta('ASC_MF',0,-10,10,0)
B_FCOST	 = Beta('B_FCOST',0,-10,10,0)
B_MCOST	 = Beta('B_MCOST',0,-10,10,0)
B_USERS	 = Beta('B_USERS',0,-10,10,0)

# Define here arithmetic expressions for name that are not directly
# available from the data

one  = DefineVariable('one',1,database)
logcostBM  = DefineVariable('logcostBM', log(cost1),database)
logcostSM  = DefineVariable('logcostSM', log(cost2),database)
logcostLF  = DefineVariable('logcostLF', log(cost3),database)
logcostEF  = DefineVariable('logcostEF', log(cost4),database)
logcostMF  = DefineVariable('logcostMF', log(cost5),database)

#Utilities
V_BM = ASC_BM * one + B_MCOST * logcostBM
V_SM = ASC_SM * one + B_MCOST * logcostSM
V_LF = ASC_LF * one + B_FCOST * logcostLF + B_USERS * users
V_EF = ASC_EF * one + B_FCOST * logcostEF + B_USERS * users
V_MF = ASC_MF * one + B_FCOST * logcostMF + B_USERS * users

V = {1: V_BM, 2: V_SM, 3: V_LF, 4: V_EF, 5: V_MF}
avail = {1: avail1, 2: avail2, 3: avail3, 4: avail4, 5: avail5}

# Here we use the "biogeme" way for backward compatibility
#exclude = choice == 0
#database.remove(exclude)

# Estimation of the model
logprob = bioLogLogit(V,avail,choice)
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "MNL_Tel_socioec"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)
