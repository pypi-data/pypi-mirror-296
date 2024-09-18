def input_format_Spheno():
   print('''
Format of the SPHENO input file. Please see the manual for more information.
________________________________
pathS:  /home/SPheno-4.0.3
Lesh: LesHouches.in.MSSM_low_wino_inp_1
SPHENOMODEL: MSSM    
output_dir: /home/output_try
            
#################################
TotVarScanned: 3


VarMin.append: 1.00000E+02  
VarMax.append: 1.5000E+03   
VarLabel.append: # M1input     
VarNum.append:  1

VarMin.append: 1.00000E+02
VarMax.append: 1.5000E+03    
VarLabel.append: # M2input  
VarNum.append:  2

VarMin.append: -1.500000E+03   
VarMax.append: 1.500000E+03
VarLabel.append: # Muinput        
VarNum.append:  23

#####################
### Define the traget region below#
#####################

TotTarget: 1

TargetMin: 122  
TargetMax: 128  
TargetLabel: # hh_1 
TargetNum: 25 
TargetResNum: 1

''')
