import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models

pandas = pd.read_table("swissmetro.dat")
database = db.Database("swissmetro",pandas)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

from headers import *

ASC_CAR = Beta('ASC_CAR',-0.608438,-20,20,0,'ASC_CAR' )
B_TIME = Beta('B_TIME',-0.0111253,-10,10,0,'B_TIME' )
B_CAR_COST = Beta('B_CAR_COST',-0.00935984,-10,10,0,'B_CAR_COST' )
B_SENIOR = Beta('B_SENIOR',-1.87838,-10,10,0,'B_SENIOR' )
ASC_SM = Beta('ASC_SM',-0.134682,-20,20,0,'ASC_SM' )
B_SM_COST = Beta('B_SM_COST',-0.0104322,-10,10,0,'B_SM_COST' )
B_HE = Beta('B_HE',-0.00586331,-10,10,0,'B_HE' )
B_GA = Beta('B_GA',0.556613,-10,80,0,'B_GA' )
ASC_SBB = Beta('ASC_SBB',0,-10,10,1,'ASC_SBB' )
B_TRAIN_COST = Beta('B_TRAIN_COST',-0.0268129,-10,10,0,'B_TRAIN_COST' )

#vc = bioMatrix(9,names,values)
#BIOGEME_OBJECT.VARCOVAR = vc

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

#Exclude
exclude = (((  PURPOSE   !=  1  ) * (  PURPOSE   !=  3  )) + (  CHOICE   ==  0  ) + (  AGE == 6  ) + ( INCOME !=  2 ))>0

#No need for estimating the model (it is already estimated). We want to obtain the individual probabilities and the market shares
prob1 = models.logit(V,av,1)
prob2 = models.logit(V,av,2)
prob3 = models.logit(V,av,3)

#Simulation output
simulate = {'choice': CHOICE,
            '01 Prob. SBB': prob1,
            '02 Prob. SM': prob2,
            '03 Prob. Car': prob3,
            '04 Elast SM_COST SBB': Derive(prob1,'SM_COST')*SM_COST/prob1,
            '05 Elast SM_COST SM': Derive(prob2,'SM_COST')*SM_COST/prob2,
            '06 Elast SM_COST Car': Derive(prob3,'SM_COST')*SM_COST/prob3}

biogeme  = bio.BIOGEME(database,simulate)
biogeme.modelName = "MNL_SM_socioec_Med_forecast"
results = biogeme.simulate()
print("Results=",results.describe())