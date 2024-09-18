import re
import os
import sys
import numpy as np
import random
###################
def read_(path_:str):
  file_ = open(path_,'r')
  return file_.readlines()
def extract_floats(s):
    # Split the string into individual words or tokens
    tokens = s.split()
    floats = []
    
    # Iterate over the tokens
    for token in tokens:
        try:
            # Try to convert the token to a float
            number = float(token)
            floats.append(number)
        except ValueError:
            # If it cannot be converted, move to the next token
            continue
    
    return floats

def read_input():
  file_ = str(input('Please enter the full the path to the input file (including the file name): '))
  file_ = file_.replace(" ","")  
  if not os.path.exists(str(file_)): sys.exit (str(file_)+'   file not exist. EXIT')
  x = read_(file_)  
  VarMin=[]
  VarMax =[]
  VarLabel=[]
  VarNum= []
  TotVarScanned = 0
  
  TargetMin=[]
  TargetMax =[]
  TargetLabel=[]
  TargetNum= []
  TargetResNum=[]
  TotVarTarget = 0
  
  for line in x:
    if str('TotVarScanned') in line: 
      TotVarScanned = int(extract_floats(line)[0])
    if str('VarMin') in line:
      l = float(extract_floats(line)[0])
      VarMin.append(float(l))
    if str('VarMax') in line:
      l = float(extract_floats(line)[0])
      VarMax.append(float(l))  
    if str('VarLabel') in line:
      l = line.rsplit(":")[-1]
      l = ''.join(l).strip()
      l= l.replace("\n","")
      VarLabel.append(str(l))  
    if str('VarNum') in line:
      l = int(extract_floats(line)[0])
      VarNum.append(int(l))  
    if str('pathS') in line:
      l = line.rsplit()[-1]
      l= l.replace(" ","")
      l= l.replace("\n","")
      pathS= l.replace("'","")  
      pathS= str(pathS)+'/'
      
    if str('Lesh:') in line:
      l = line.rsplit()[-1]
      l= l.replace(" ","")
      l= l.replace("\n","")
      Lesh= l.replace("'","")    
    if str('SPHENOMODEL') in line:
      l = line.rsplit()[-1]
      l= l.replace(" ","")
      l= l.replace("\n","")
      SPHENOMODEL= l.replace("'","")   
      
    if str('output_dir') in line:
      l = line.rsplit()[-1]
      l= l.replace(" ","")
      l= l.replace("\n","")
      output_dir= l.replace("'","")       
    
    if str('TotTarget') in line: 
      TotVarTarget= int(extract_floats(line)[0])
    if str('TargetMin') in line:
      l = float(extract_floats(line)[0])
      TargetMin.append(float(l))
    if str('TargetMax') in line:
      l = float(extract_floats(line)[0])
      TargetMax.append(float(l))  
    if str('TargetLabel') in line:
      l = line.rsplit(":")[-1]
      l = ''.join(l).strip()
      l= l.replace("\n","")
      TargetLabel.append(str(l))  
    if str('TargetNum') in line:
      l = int(extract_floats(line)[0])
      TargetNum.append(int(l))  
    if str('TargetResNum') in line:
      l = int(extract_floats(line)[0])
      TargetResNum.append(int(l))      
      
  VarMin = VarMin[:TotVarScanned] 
  VarMax = VarMax[:TotVarScanned]   
  VarLabel = VarLabel[:TotVarScanned]    
  VarNum = VarNum[:TotVarScanned]  
  
  TargetMin = TargetMin[:TotVarTarget] 
  TargetMax = TargetMax[:TotVarTarget]   
  TargetLabel = TargetLabel[:TotVarTarget]    
  TargetNum = TargetNum[:TotVarTarget]   
  TargetResNum = TargetResNum[:TotVarTarget]   
  return pathS, Lesh,SPHENOMODEL,output_dir,TotVarScanned, VarMin , VarMax,VarLabel,VarNum,TotVarTarget, TargetMin , TargetMax,TargetLabel,TargetNum ,TargetResNum  
  
def generate_init_HEP(n,TotVarScanned,paths,Lesh,VarLabel,VarMin,VarMax):
    AI_2 = np.empty(shape=[0,TotVarScanned])
    for i in range(n):
        LHEfile = open(str(paths)+str(Lesh),'r+')
        AI_1 = []
        for line in LHEfile: 
            NewlineAdded = 0
            for yy in range(0,TotVarScanned):
                if str(VarLabel[yy]) in line:
                    value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                    AI_1.append(value)
        AI_1= np.array(AI_1).reshape(1,TotVarScanned)   
        AI_2 = np.append(AI_2,AI_1,axis=0)    
    return AI_2       
    
    
def check_(pathS:str,Lesh:str,SPHENOMODEL:str,output:str):
  if not os.path.exists(str(pathS)+('bin/SPheno')):
    sys.exit ('"/bin/SPheno" NOT EXIST, PLEASE TYPE make.')
  if not  os.path.exists(str(pathS)+str(Lesh)):
    sys.exit (str(pathS)+str(Lesh)+' NOT EXIST.')
  if not  os.path.exists(str(pathS)+'/bin/SPheno%s'%(str(SPHENOMODEL))):
    sys.exit (str(paths)+'/bin/SPheno%s'%(str(SPHENOMODEL))+' NOT EXIST.')
  if  not os.path.exists(str(output)+'/'):
    os.mkdir(str(output)+'/')   
  return None  

def const(i,TotConstScanned,ConstLabel,ConstNum,ConstResNum,ConstMin,ConstMax):
   for Xz in range(0,TotConstScanned):
      null = os.system("grep '%s' %s  >/dev/null"%(str(ConstLabel[Xz]),str(i))) 
      if (null == 256):
         return 0 
   f=open(str(i), 'r')
   for xxx in f: 
      for zz in range(0,TotConstScanned):
          if (str(ConstNum[zz])  and str(ConstLabel[zz])) in xxx:
            r = xxx.rsplit()
            Xmm = int(ConstResNum[zz])
            if (Xmm == 1) :
               l = int(float(r[Xmm]))
               if (l not in range(int(ConstMin[zz]),int(ConstMax[zz])) and str(r[0])!= 'DECAY'):
                  return 0
               else: return 1   
            if (Xmm != 1) :
               l =  float(r[Xmm])
               mm = float(ConstMin[zz])
               nm = float(ConstMax[zz])
               if (l < mm):
                  return 0
               else: return 1   
               if (l > nm):
                  return 0  
               else: return 1 

def run_train(npoints,TotVarScanned,Lesh,VarMin,VarMax,VarNum,VarLabel,SPHENOMODEL,pathS,TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax):      
    os.chdir(pathS)
    AI_X = np.empty(shape=[0,TotVarScanned])
    AI_Y = []
    ###########################
    for xx in range(0,npoints):
        sys.stdout.write('\r'+' Running the initial random scanning to collect points to train the ML network: %s / %s ' %(xx+1, npoints)) 
        newrunfile = open('newfile','w')
        oldrunfile = open(str(Lesh),'r+')
        AI_L = []
        for line in oldrunfile: 
            NewlineAdded = 0
            for yy in range(0,TotVarScanned):
                if str(VarLabel[yy]) in line:
                    value = VarMin[yy] + (VarMax[yy] - VarMin[yy])*random.random()
                    AI_L.append(value)
                    valuestr = str("%.4E" % value)
                    newrunfile.write(str(VarNum[yy])+'   '+valuestr +str('     ')+ VarLabel[yy]+'\n')
                    NewlineAdded = 1
            if NewlineAdded == 0:
                newrunfile.write(line)
        newrunfile.close()
        oldrunfile.close()
        os.remove(str(Lesh))
        AI_L= np.array(AI_L).reshape(1,TotVarScanned)
        ############################    
        os.rename('newfile',str(Lesh))
        os.system('./bin/SPheno'+str(SPHENOMODEL)+' '+str(Lesh)+' spc.slha'+' >  out.txt ')
        out = open(str(pathS)+'out.txt','r+')
        for l in out:
            if str('Finished!') in l:
              label = const('spc.slha',TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax)
              AI_Y.append(label)          
              AI_X = np.append(AI_X,AI_L,axis=0)
        os.remove('out.txt')
    return np.array(AI_X),np.array(AI_Y)  

def refine_points(npoints,TotVarScanned,Lesh,VarMin,VarMax,VarNum,VarLabel,SPHENOMODEL,pathS,TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax):      
  os.chdir(pathS)
  AI_X = np.empty(shape=[0,TotVarScanned])
  AI_Y = []
  ######
  for xx in range(0,npoints.shape[0]):
        #sys.stdout.write('\r'+'Correcting the predicted points: %s / %s ' %(xx+1, npoints.shape[0])) 
        newrunfile = open('newfile','w')
        oldrunfile = open(str(Lesh),'r+')
        AI_L = []
        for line in oldrunfile: 
            NewlineAdded = 0
            for yy in range(0,TotVarScanned):
                if str(VarLabel[yy]) in line:
                    value = npoints[xx,yy]
                    AI_L.append(value)
                    valuestr = str("%.4E" % value)
                    newrunfile.write(str(VarNum[yy])+'   '+valuestr +str('     ')+ VarLabel[yy]+'\n')
                    NewlineAdded = 1
            if NewlineAdded == 0:
                newrunfile.write(line)
        newrunfile.close()
        oldrunfile.close()
        os.remove(str(Lesh))
        AI_L= np.array(AI_L).reshape(1,TotVarScanned)
        ############################    
        os.rename('newfile',str(Lesh))
        os.system('./bin/SPheno'+str(SPHENOMODEL)+' '+str(Lesh)+' spc.slha'+' >  out.txt')
        out = open(str(pathS)+'out.txt','r+')
        for l in out:
            if str('Finished!') in l:
              label = const('spc.slha',TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax)
              AI_Y.append(label)          
              AI_X = np.append(AI_X,AI_L,axis=0)
        os.remove('out.txt')
  return np.array(AI_X),np.array(AI_Y)  

 
class scan():
    import sklearn
    def __init__(self,iteration,L1,L,K, period,frac,K_smote):
        self.iteration= iteration
        self.L1 = L1
        self.L =L
        self.K = K
        #self.th_value = th_value
        #self.function_dim = function_dim 
        self.period = period
        self.frac = frac
        self.K_smote=K_smote

    def labeler(self,x,th):
        ll=[]
        for q,item in enumerate(x):
            if item < th:
                ll.append(1)
            else:
                ll.append(0)
        return np.array(ll).ravel()        

    def run_RFC(self,learning_rate=0.01,n_estimators=300,max_depth=50,print_output=True):
        import sklearn
        from sklearn.ensemble import RandomForestClassifier
        import time
        pathS, Lesh,SPHENOMODEL,output_dir,TotVarScanned, VarMin , VarMax,VarLabel,VarNum,TotVarTarget, TargetMin , TargetMax,TargetLabel,TargetNum ,TargetResNum   = read_input() 
        check_(pathS,Lesh,SPHENOMODEL,output_dir)  
        RFC =RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth)
        Xf,ob1=run_train(self.L1,TotVarScanned,Lesh,VarMin,VarMax,VarNum,VarLabel,SPHENOMODEL,pathS,TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax)

        RFC.fit(Xf, ob1)
        X_g = Xf[ob1==1]    # It is good to have some initial guide
        obs1_g = ob1[ob1==1]
        X_b =Xf[ob1==0][:len(obs1_g)]
        obs1_b =ob1[ob1==0][:(len(obs1_g))]
        print('\nNumber of initial points in the traget region:  ', len(obs1_g) )
        print('Number of initial points outside the traget region:  ', len(obs1_b) )
        time.sleep(8)
        for q in range(self.iteration):
            x = generate_init_HEP(self.L,TotVarScanned,pathS,Lesh,VarLabel,VarMin,VarMax)
            pred = RFC.predict(x).flatten()
            qs = np.argsort(pred)[::-1]
            if len(x[pred>0.9]) > round(self.K*self.frac): # How to choose the good points
                xsel1 = x[pred>0.9][:round(self.K*(1-self.frac))]
            else:
                xsel1 = x[qs][:round(self.K*(1-self.frac))]
            xsel1 = np.append(xsel1,x[:round(self.K*(self.frac))],axis=0)
            xsel2,ob = refine_points(xsel1,TotVarScanned,Lesh,VarMin,VarMax,VarNum,VarLabel,SPHENOMODEL,pathS,TotVarTarget,TargetLabel,TargetNum,TargetResNum,TargetMin,TargetMax)
            X_g = np.append(X_g,xsel2[ob==1],axis=0)
            obs1_g = np.append(obs1_g,ob[ob==1],axis=0)
            X_b = np.append(X_b,xsel2[ob==0],axis=0)
            obs1_b = np.append(obs1_b,ob[ob==0],axis=0)
            if (q%self.period==0 or q+1 == self.iteration):
                X = np.concatenate([X_g,X_b],axis=0)
                obs = np.concatenate([obs1_g,obs1_b],axis=0)
                X_shuffled, Y_shuffled = sklearn.utils.shuffle(X, obs)
                RFC.fit(X_shuffled, Y_shuffled)

            else:
                X = np.concatenate([xsel2[ob==1],xsel2[ob==0]],axis=0)
                obs=np.concatenate([ob[ob==1],ob[ob==0]],axis=0)
                X_shuffled, Y_shuffled = sklearn.utils.shuffle(X, obs)
                RFC.fit(X_shuffled, Y_shuffled)
            if print_output == True:
                print('DNN_model- Run Number {} - Number of collected points= {}'.format(q,len(X)))

        if os.path.exists(str(output_dir)+"/Accumelated_points.txt"): os.system('rm -rf %s/Accumelated_points.txt '%str(output_dir)) 
        f= open(str(output_dir)+"/Accumelated_points.txt","x")
        header = '\t'.join(VarLabel)
        f.write(header+' \n')
        f.close()
        np.savetxt(str(output_dir)+'/a.txt',X_g, delimiter=',')
        os.system('cat %s/a.txt >> %s/Accumelated_points.txt '%(str(output_dir),str(output_dir)))
        os.system('rm -rf %s/a.txt'%str(output_dir))
        
        print('Output saved in %s' %str(output_dir))
        return
###############################################################
# Create an instanace of the calss to access all functions    #
###############################################################
def RFC(iteration=10,L1=100,L=1000,K=100,period=1,frac=0.2,K_smote=1,learning_rate=0.01,n_estimators=300,max_depth=50,print_output=True):
  ''' Function to run the scan over SPheno Package using Random Forest Calssifier.
  Requirements:
                       1) Input file specifies the spheno directory, output directory, scan ranges and target ranges.
                       2) Sklearn is used to import the RandomForest Classifier
                       
  Input args: 
                  1) iteration: Number of iterations to collect the points
                  2) L1: Number of random scanned points at the zero step to train the network
                  3) L: Number of the generated points to the network for prediction
                  4) K: Number of the predicted points to be refined using the SPheno package
                  5) period: Number to define the period to train the network
                  6) frac: Fraction of the randomly added points to cover the full parameter space, e.g. 0.2 for 20% random points.
                  7)K_smote: Number of nearest neighbours used by SMOTE
                  8) learning_rate: Value of the learning rate of the network
                  9)n_estimator: Number of estimator used by the Random Forest. See the Sklearn manual for more details
                  10) max_depth: maximum depth of the reandom forest. See the Sklearn manual for more details
                  11) print_output: if True, the code will print information about the collected points during the run
  Output args:
                     text file contains the valid points in the output directory.
  Defalut initialization:           
    RFC(iteration=10,L1=100,L=1000,K=100,period=1,frac=0.2,K_smote=1,learning_rate=0.01,n_estimators=300,max_depth=50,print_output=True)                         
  ''' 
  model = scan(iteration,L1,L,K,period,frac,K_smote)  
  model.run_RFC(learning_rate=learning_rate,n_estimators=n_estimators,max_depth=n_estimators,print_output=True)
  return
  
