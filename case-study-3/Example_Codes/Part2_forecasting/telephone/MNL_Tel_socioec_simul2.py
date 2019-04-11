import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models

pandas = pd.read_table("telephone.dat")
database = db.Database("telephone",pandas)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

from headers import *

ASC_SM = Beta('ASC_SM',0,-10,10,1,'ASC_SM' )

B_MCOST = Beta('B_MCOST',-1.95834,-10,10,0,'B_MCOST' )

ASC_BM = Beta('ASC_BM',-0.730993,-10,10,0,'ASC_BM' )

ASC_MF = Beta('ASC_MF',0.273599,-10,10,0,'ASC_MF' )

B_FCOST = Beta('B_FCOST',-1.78858,-10,10,0,'B_FCOST' )

B_USERS = Beta('B_USERS',0.39403,-10,10,0,'B_USERS' )

ASC_LF = Beta('ASC_LF',-0.0870587,-10,10,0,'ASC_LF' )

ASC_EF = Beta('ASC_EF',-0.319299,-10,10,0,'ASC_EF' )


# Define here arithmetic expressions for name that are not directly
# available from the data

one  = DefineVariable('one',1,database)
logcostBM  = DefineVariable('logcostBM', log(cost1),database)
logcostSM  = DefineVariable('logcostSM', log(cost2)+4,database)
logcostLF  = DefineVariable('logcostLF', log(cost3)+6,database)
logcostEF  = DefineVariable('logcostEF', log(cost4)+7,database)
logcostMF  = DefineVariable('logcostMF', log(cost5)+11,database)

#Utilities
V_BM = ASC_BM * one + B_MCOST * logcostBM
V_SM = ASC_SM * one + B_MCOST * logcostSM
V_LF = ASC_LF * one + B_FCOST * logcostLF + B_USERS * users
V_EF = ASC_EF * one + B_FCOST * logcostEF + B_USERS * users
V_MF = ASC_MF * one + B_FCOST * logcostMF + B_USERS * users

V = {1: V_BM, 2: V_SM, 3: V_LF, 4: V_EF, 5: V_MF}
avail = {1: avail1, 2: avail2, 3: avail3, 4: avail4, 5: avail5}


#No need for estimating the model (it is already estimated). We want to obtain the individual probabilities and the market shares
probBM = models.logit(V,avail,1)
probSM = models.logit(V,avail,2)
probLF = models.logit(V,avail,3)
probEF = models.logit(V,avail,4)
probMF = models.logit(V,avail,5)
probChosen = models.logit(V,avail,choice)
#Instead of reporting the choice in the simulation file, the probability of the chosen can be printed

#Simulation output
simulate = {'choice':choice,
            '01 Prob. BM': probBM,
            '02 Prob. SM': probSM,
            '03 Prob. LF': probLF,
            '04 Prob. EF': probEF,
            '05 Prob. MF': probMF,
            '06 Elast BM_COST BM': Derive(probBM,'logcostBM')*logcostBM/probBM,
            '07 Elast BM_COST SM': Derive(probSM,'logcostBM')*logcostBM/probSM,
            '08 Elast BM_COST LF': Derive(probLF,'logcostBM')*logcostBM/probLF,
                  '09 Elast BM_COST EF': Derive(probEF,'logcostBM')*logcostBM/probEF,
            '10 Elast BM_COST MF': Derive(probMF,'logcostBM')*logcostBM/probMF}

biogeme  = bio.BIOGEME(database,simulate)
biogeme.modelName = "MNL_Tel_socioec_simul2"
results = biogeme.simulate()
print("Results=",results.describe())

