# VASProcar Copyright (C) 2023
# GNU GPL-3.0 license

def execute_python_file(filename: str):
    return exec(open(main_dir + str(filename)).read(), globals())

#-----------------------------------------------------------------------
# Check whether the folder 'Spin' exists -------------------------------
#-----------------------------------------------------------------------
if os.path.isdir(dir_files + '/output/Spin'):
   0 == 0
else:
   os.mkdir(dir_files + '/output/Spin')
#--------------------------------------

#======================================================================
# Getting the input parameters ========================================
#======================================================================
execute_python_file(filename = DFT + '_info.py')

#======================================================================
# Get the input from user =============================================
#======================================================================

print ("##############################################################")
print ("########### 2D Plot of Spin Components (Sx|Sy|Sz): ###########")
print ("##############################################################") 
print (" ")

if (escolha == -1):
   
   if (len(inputs) == 0):
      print ("#######################################################################")  
      print ("Do you want to select over which orbitals the spin components =========")
      print ("(Sx|Sy|Sz) will be projected? =========================================")
      print ("[0] NOT                                                                ")
      print ("[1] YES                                                                ")
      print ("#######################################################################") 
      p_orb_spin = input (" "); p_orb_spin = int(p_orb_spin)
      print (" ")

      if (p_orb_spin == 1):
         Orb_spin = [0]*16
         print ("##############################################################")
         print ("Ions and orbitals can be added in any order ------------------")
         print ("==============================================================")
         print ("Use the nomenclature below to designate Orbitals:             ")
         if (n_orb == 3):  print ("s p d")
         if (n_orb == 4):  print ("s p d f")
         if (n_orb == 9):  print ("s p d px py pz dxy dyz dz2 dxz dx2")
         if (n_orb == 16): print ("s p d f px py pz dxy dyz dz2 dxz dx2 fyx2 fxyz fyz2 fzz2 fxz2 fzx2 fxx2")
         print ("==============================================================")
         print ("Enter the selected orbitals as in the examples below =========")
         print ("------------------------------------------------------------- ")
         print ("Orbitals_Spin  s                                              ")          
         print ("Orbitals_Spin  px py dxy fxyz                                 ")
         print ("Orbitals_Spin  s p d f                                        ")
         print ("##############################################################")
         orb_io = input ("Orbitals_Spin  ").replace(':', ' ').replace('-', ' ').replace('*', ' *').split( )
         print (" ")

         for i in range(len(orb_io)):
             if (orb_io[i] == 's' or orb_io[i] == 'S'): Orb_spin[0] = 1
             if (orb_io[i] == 'p' or orb_io[i] == 'P'): Orb_spin[1] = 1; Orb_spin[2] = 1; Orb_spin[3] = 1
             if (orb_io[i] == 'd' or orb_io[i] == 'D'): Orb_spin[4] = 1; Orb_spin[5] = 1; Orb_spin[6] = 1; Orb_spin[7] = 1; Orb_spin[8] = 1
             if (orb_io[i] == 'f' or orb_io[i] == 'F'): Orb_spin[9] = 1; Orb_spin[10] = 1; Orb_spin[11] = 1; Orb_spin[12] = 1; Orb_spin[13] = 1; Orb_spin[14] = 1; Orb_spin[1] = 1
             #--------------------------------------------------------------------------------
             if (orb_io[i] == 'py' or orb_io[i] == 'Py' or orb_io[i] == 'PY'): Orb_spin[1] = 1
             if (orb_io[i] == 'pz' or orb_io[i] == 'Pz' or orb_io[i] == 'PZ'): Orb_spin[2] = 1
             if (orb_io[i] == 'px' or orb_io[i] == 'Px' or orb_io[i] == 'PX'): Orb_spin[3] = 1
             #-----------------------------------------------------------------------------------
             if (orb_io[i] == 'dxy' or orb_io[i] == 'Dxy' or orb_io[i] == 'DXY'): Orb_spin[4] = 1
             if (orb_io[i] == 'dyz' or orb_io[i] == 'Dyz' or orb_io[i] == 'DYZ'): Orb_spin[5] = 1
             if (orb_io[i] == 'dz2' or orb_io[i] == 'Dz2' or orb_io[i] == 'DZ2'): Orb_spin[6] = 1
             if (orb_io[i] == 'dxz' or orb_io[i] == 'Dxz' or orb_io[i] == 'DXZ'): Orb_spin[7] = 1
             if (orb_io[i] == 'dx2' or orb_io[i] == 'Dx2' or orb_io[i] == 'DX2'): Orb_spin[8] = 1
             #---------------------------------------------------------------------------------------
             if (orb_io[i] == 'fyx2' or orb_io[i] == 'Fyx2' or orb_io[i] == 'FYX2'): Orb_spin[9]  = 1
             if (orb_io[i] == 'fxyz' or orb_io[i] == 'Fxyz' or orb_io[i] == 'FXYZ'): Orb_spin[10] = 1
             if (orb_io[i] == 'fyz2' or orb_io[i] == 'Fyz2' or orb_io[i] == 'FYZ2'): Orb_spin[11] = 1
             if (orb_io[i] == 'fzz2' or orb_io[i] == 'Fzz2' or orb_io[i] == 'FZZ2'): Orb_spin[12] = 1
             if (orb_io[i] == 'fxz2' or orb_io[i] == 'Fxz2' or orb_io[i] == 'FXZ2'): Orb_spin[13] = 1
             if (orb_io[i] == 'fzx2' or orb_io[i] == 'Fzx2' or orb_io[i] == 'FZX2'): Orb_spin[14] = 1
             if (orb_io[i] == 'fxx2' or orb_io[i] == 'Fxx2' or orb_io[i] == 'FXX2'): Orb_spin[15] = 1

   if (len(inputs) == 0):
      print ("#######################################################################") 
      print ("Do you want to change the color pattern of the Spin Up|Down Components ")
      print ("[0] NOT                                                                ")
      print ("[1] YES                                                                ")
      print ("#######################################################################") 
      esc_color = input (" "); esc_color = int(esc_color)
      print (" ")  

   if (esc_color == 1):
      if (len(inputs) == 0):
         print ("##############################################################")
         print ("color code:                                                   ")
         print ("0  White   | 1  Black | 2  Red    | 3  Green  | 4  Blue       ")
         print ("5  Yellow  | 6  Borwn | 7  Grey   | 8  Violet | 9  Cyan       ")
         print ("10 Magenta |11 Orange | 12 Indigo | 13 Maroon | 14 Turquesa   ")
         print ("15 Dark_Green                                                 ")
         print ("##############################################################")       
         print ("VASProcar color pattern:                                      ")
         print ("                                                              ")
         print ("Spin_Up | Spin_Down: 2 4 (Red, Blue)                          ")
         print ("##############################################################") 
         print (" ")
         print ("==============================================================") 
         print ("Enter the Spin Up and Spin Down colors in sequence:           ")
         cor_spin = input ("Spin_Up | Spin_Down: ")
         print (" ")  
      #-------------------------
      tcor = cor_spin.split()
      c_spin_up = int(tcor[0])
      c_spin_down = int(tcor[1])
      #-------------------------
   
   if (len(inputs) == 0):
      print ("##############################################################")
      print ("Regarding the Plot of Bands, choose ==========================")
      print ("[0] Plot/Analyze all bands ===================================")
      print ("[1] Plot/Analyze selected bands ==============================")
      print ("##############################################################")
      esc_bands = input (" "); esc_bands = int(esc_bands)
      print(" ")

   if (esc_bands == 0):
      bands_range = '1:' + str(nb)

   if (esc_bands == 1):     
      if (len(inputs) == 0): 
         print ("##############################################################")
         print ("Select the bands to be analyzed using intervals: =============")
         print ("Type as in the examples below =============================== ")
         print ("------------------------------------------------------------- ")
         print ("Bands can be added in any order ----------------------------- ")
         print ("------------------------------------------------------------- ")
         print ("bands_intervals  35:42                                        ")          
         print ("bands_intervals  1:15 27:69 18:19 76*                         ")
         print ("bands_intervals  7* 9* 11* 13* 16:21                          ")
         print ("##############################################################")
         bands_range = input ("bands_intervals  ")
         print (" ")
      #------------------------------------------------------------------------------------------
      selected_bands = bands_range.replace(':', ' ').replace('-', ' ').replace('*', ' *').split()
      loop = int(len(selected_bands)/2)
      #------------------------------------------------------------------------------------------
      
      for i in range (1,(loop+1)):
          #-----------------------------------------
          loop_i = int(selected_bands[(i-1)*2])
          if (selected_bands[((i-1)*2) +1] == "*"):
             selected_bands[((i-1)*2) +1] = selected_bands[(i-1)*2]
          loop_f = int(selected_bands[((i-1)*2) +1])
          #----------------------------------------------------------------------------------------
          if ((loop_i > nb) or (loop_f > nb) or (loop_i < 0) or (loop_f < 0) or (loop_i > loop_f)):
             print (" ")
             print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
             print ("ERROR: The values of the informed bands are incorrect %%%%")
             print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
             confirmation = input (" ")
             exit()

   if (len(inputs) == 0):
      print ("##############################################################") 
      print ("with respect to energy, would you like? ======================")
      print ("[0] Use the default energy value from DFT output =============")
      print ("[1] Shift the Fermi level to 0.0 eV  =========================")
      print ("##############################################################")
      esc_fermi = input (" "); esc_fermi = int(esc_fermi)
      print (" ")   

   if (len(inputs) == 0):
      print ("##############################################################") 
      print ("Do you want to modify the energy range to be plotted? ========")
      print ("[0] NOT                                                       ")
      print ("[1] YES                                                       ")
      print ("##############################################################")
      esc_range_E = input (" "); esc_range_E = int(esc_range_E)
      print (" ")

   if (esc_range_E == 1):
      if (len(inputs) == 0):
         print ("##############################################################") 
         print ("Enter the energy range to be plotted: ========================")
         print ("Note: Enter the lowest and highest energy value to be plotted ")
         print ("      in relation to the Fermi Level                          ")
         print ("Examples:                                                     ")
         print ("--------------------------------------------------------------")
         print ("E_min E_max: -3.0 15.0                                        ")
         print ("E_min E_max: -5.1 5.0                                         ")
         print ("##############################################################")      
         range_E = input ("E_min E_max:  ")
         print (" ")
      #---------------------------------------------------------------------------------------
      selected_energ = range_E.replace('-', ' -').replace('+', ' +').replace(':', ' ').split()
      #--------------------------------------------------------------------------------------- 
      E_min = float(selected_energ[0])
      E_max = float(selected_energ[1])

   if (len(inputs) == 0):
      print ("##############################################################")
      print ("What do you want to Plot/Analyze? ============================")
      print ("[0] to analyze all ions in the lattice =======================")
      print ("[1] to analyze selected ions =================================")
      print ("##############################################################")
      esc_ions = input (" "); esc_ions = int(esc_ions)
      print (" ")

      if (esc_ions == 1):

         #-------------------------
         sim_nao = ["nao"]*(ni + 1)  
         #-------------------------

         if (DFT == '_VASP/'):
            print ("##############################################################")
            print ("[0] Do you want to enter ions manually (ion ranges)? =========")
            print ("[1] Do you want to enter spatial location criteria? ==========")
            print ("##############################################################")
            esc_ions_tipo = input (" "); esc_ions_tipo = int(esc_ions_tipo)
            print (" ")

         if (DFT == '_QE/'):
            esc_ions_tipo = 0

         if (esc_ions_tipo == 0):
            print ("################################################################")
            print ("Choose the intervals_of_ions to be analyzed: ===================")
            print ("Type as in the examples below ==================================")
            print ("----------------------------------------------------------------")
            print ("The order in which the ions are added does not change the result")
            print ("----------------------------------------------------------------")
            print ("intervals_of_ions  1:5 3:9 11* 15:27                            ")          
            print ("intervals_of_ions  7:49 50:53                                   ")
            print ("intervals_of_ions  3* 6* 8:11                                   ")        
            print ("################################################################") 
            ion_range = input ("intervals_of_ions  ")
            print (" ")
            #-------------------------------------------------------------------------------
            selected_ions = ion_range.replace(':', ' ').replace('-', ' ').replace('*', ' *').split()
            loop = int(len(selected_ions)/2)
            #-------------------------------------------------------------------------------    
            for i in range (1,(loop+1)):
                #--------------------------------------------------------
                loop_i = int(selected_ions[(i-1)*2])
                if (selected_ions[((i-1)*2) +1] == "*"):
                   selected_ions[((i-1)*2) +1] = selected_ions[((i-1)*2)]
                loop_f = int(selected_ions[((i-1)*2) +1])
                #----------------------------------------------------------------------------------------
                if ((loop_i > ni) or (loop_f > ni) or (loop_i < 0) or (loop_f < 0) or (loop_i > loop_f)):
                   print (" ")
                   print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                   print ("ERROR: The informed ion values are incorrect %%%%%%%%%%%%%")
                   print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                   confirmation = input (" ")
                   exit()
                #----------------------------------------------------------------------           
                for j in range(loop_i, (loop_f + 1)):
                    sim_nao[j] = "sim" 

         if (esc_ions_tipo == 1):
            #------------------------------------------------------
            execute_python_file(filename = DFT + 'contcar_info.py')
            #------------------------------------------------------
            r_min = [-9999.0]*3; r_max = [+9999.0]*3
            #-----------------------------------------------------------------------
            print ("##############################################################")
            print ("To define a REGION to be projected in the band structure, you ")
            print ("must enter limits for the Cartesian coordinates (X|Y|Z  in ")
            print ("angstrom) selected below:                                     ")
            print ("==============================================================")
            print ("Examples:                                                     ")
            print ("X_min X_max: 0.0 14.0                                       ")
            print ("Y_min Y_max: 5.0 10.0                                       ")
            print ("Z_min Z_max: 7.0 7.5                                        ")
            print ("##############################################################")
            print ("What coordinates do you want to limit?                        ")
            print ("--------------------------------------------------------------")
            print ("[1] (X)      [2] (Y)      [3] (Z)                             ")
            print ("[4] (X,Y)    [5] (X,Z)    [6] (Y,Z)    [7] (X,Y,Z)            ")
            print ("##############################################################")
            esc_limit = input (" "); esc_limit = int(esc_limit)
            print (" ")
            #-----------------------------------------------------------------------
            print ("##############################################################")
            print ("Enter the values: ============================================")
            #-----------------------------------------------------------------------
            if (esc_limit == 1 or esc_limit == 4 or esc_limit == 5 or esc_limit == 7):
               print ("##############################################################")
               print ("Enter the limits of the X coordinate (in Angstrom): ==========")
               print ("##############################################################")
               r_range = input ("X_min X_max: "); selected_r = r_range.split()
               r_min[0] = float(selected_r[0]); r_max[0] = float(selected_r[1])
            if (esc_limit == 2 or esc_limit == 4 or esc_limit == 6 or esc_limit == 7):
               print ("##############################################################")
               print ("Enter the limits of the Y coordinate (in Angstrom): ==========")
               print ("##############################################################")
               r_range = input ("Y_min Y_max: "); selected_r = r_range.split()
               r_min[1] = float(selected_r[0]); r_max[1] = float(selected_r[1])
            if (esc_limit == 3 or esc_limit == 5 or esc_limit == 6 or esc_limit == 7):
               print ("##############################################################")
               print ("Enter the limits of the Z coordinate (in Angstrom): ==========")
               print ("##############################################################")
               r_range = input ("Z_min Z_max: "); selected_r = r_range.split()
               r_min[2] = float(selected_r[0]); r_max[2] = float(selected_r[1])
            print ("##############################################################")
            print (" ")
            #-----------------------------------------------------------------------
            ion_range = ''
            for ii in range(ni):
                if (ni_coord[ii][0] >= r_min[0] and ni_coord[ii][0] <= r_max[0]):
                   if (ni_coord[ii][1] >= r_min[1] and ni_coord[ii][1] <= r_max[1]):
                      if (ni_coord[ii][2] >= r_min[2] and ni_coord[ii][2] <= r_max[2]):
                         iion = ii+1; ion_range += str(iion) + '* '
            #-------------------------------------------------------------------------------
            print ("--------------------------------------------------------------")
            print (f'selected ions: {ion_range}')
            print ("--------------------------------------------------------------")
            print (" ")
            #-------------------------------------------------------------------------------
            selected_ions = ion_range.replace(':', ' ').replace('-', ' ').replace('*', ' *').split()
            loop = int(len(selected_ions)/2)
            #-------------------------------------------------------------------------------    
            for ij in range (1,(loop+1)):
                #--------------------------------------------------------
                loop_i = int(selected_ions[(ij-1)*2])
                if (selected_ions[((ij-1)*2) +1] == "*"):
                   selected_ions[((ij-1)*2) +1] = selected_ions[((ij-1)*2)]
                loop_f = int(selected_ions[((ij-1)*2) +1])
                #----------------------------------------------------------------------------------------
                if ((loop_i > ni) or (loop_f > ni) or (loop_i < 0) or (loop_f < 0) or (loop_i > loop_f)):
                   print (" ")
                   print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                   print ("ERROR: The informed ion values are incorrect %%%%%%%%%%%%%")
                   print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                   confirmation = input (" ")
                   exit()
                #----------------------------------------------------------------------           
                for j in range(loop_i, (loop_f + 1)):
                    sim_nao[j] = "sim" 

   if (len(inputs) == 0):
      print ("##############################################################")
      print ("Would you like to label the k-points?                         ")
      print ("[0] DO NOT label the k-points  ===============================")
      print ("[1] highlight k-points present in KPOINTS file ===============")
      print ("[2] Customize: highlight and Label k-points   ================")
      print ("##############################################################") 
      dest_k = input (" "); dest_k = int(dest_k)
      print (" ")

   if (DFT == '_QE/' and dest_k == 2 and len(inputs) == 0):
      print ("##############################################################")
      print ("Do you want to insert symmetries as k-point label?            ")
      print ("[0] NOT                                                       ")
      print ("[1] YES                                                       ")
      print ("##############################################################") 
      l_symmetry = input (" "); l_symmetry = int(l_symmetry)
      print (" ") 

   if (dest_k == 2):  Dimensao = 1

   if (dest_k != 2 and len(inputs) == 0):
      print ("##############################################################")
      print ("Would you like to choose k-axis units?                        ")
      print ("[1] 2pi/Param. (Param. in Angs.) =============================")
      print ("[2] 1/Angs. ==================================================")
      print ("[3] 1/nm.   ==================================================")
      print ("##############################################################")
      Dimensao = input (" "); Dimensao = int(Dimensao)
      print(" ")

   if (len(inputs) == 0):
      print ("##############################################################")
      print ("Enter the weight/size of the spheres in the projection: ======")
      print ("Enter a value between 0.0 and 1.0 ============================")
      print ("##############################################################")
      peso_total = input (" "); peso_total = float(peso_total)
      print(" ")

   if (len(inputs) == 0):
      print ("################################################################")
      print ("Enter the transparency value to apply to the projections:       ") 
      print ("This option is useful for checking for overlaps ================")   
      print ("Enter a value between 0.0 and 1.0 ==============================")
      print ("================================================================")
      print ("Hint: The higher the k-point density, the lower the transparency")
      print ("      value used, start with 0.5 ===============================")
      print ("################################################################")
      transp = input (" "); transp = float(transp)
      print(" ")           

if (escolha == 1 and len(inputs) == 0):
   if (n_procar == 1): bands_range = '1:' + str(nb)
   if (n_procar >  1): bands_range = '2:' + str(nb)
   esc_fermi = 1
   esc_range_E = 0  
   esc_ions = 0
   dest_k = 1
   Dimensao = 1
   Orb_spin = [1]*16
   l_symmetry = 0
   peso_total = 1.0
   transp = 1.0
  
#======================================================================
# Obtaining the results from DFT outpout files ========================
#======================================================================
read_spin = 1
execute_python_file(filename = DFT + '_nscf.py')  

#----------------------
if (Efermi == -1000.0):
   Efermi = 0.0
   esc_fermi = 0 

if (esc_fermi == 0):
   dE_fermi = 0.0
   dest_fermi = Efermi

if (esc_fermi == 1):
   dE_fermi = (Efermi)*(-1)
   dest_fermi = 0.0

if (esc_range_E == 0):
   E_min = energ_min - Efermi
   E_max = energ_max - Efermi
#----------------------------

#======================================================================
# Getting k-points / labels ===========================================
#======================================================================
execute_python_file(filename = DFT + '_label.py')

#======================================================================
# Copy Bandas.dat and Spin.dat to the output folder directory =========
#======================================================================

try: f = open(dir_files + '/output/Spin/Bandas.dat'); f.close(); os.remove(dir_files + '/output/Spin/Bandas.dat')
except: 0 == 0
  
source = dir_files + '/output/Bandas.dat'
destination = dir_files + '/output/Spin/Bandas.dat'
shutil.copyfile(source, destination)

os.remove(dir_files + '/output/Bandas.dat')

#----------------------------------------------------------------------

try: f = open(dir_files + '/output/Spin/Spin.dat'); f.close(); os.remove(dir_files + '/output/Spin/Spin.dat')
except: 0 == 0

source = dir_files + '/output/Spin.dat'
destination = dir_files + '/output/Spin/Spin.dat'
shutil.copyfile(source, destination)

os.remove(dir_files + '/output/Spin.dat')

#========================================================================
#========================================================================
# Projections Plot using (GRACE) ========================================
#======================================================================== 
#========================================================================

if (save_agr == 1):
    
   print(" ")
   print ("============== Plotting the Projections (Grace): ==============")

   execute_python_file(filename = 'plot/Grace/plot_projecao_spin.py')

   print ("Plot of projections via Grace (.agr files) completed ----------")

#========================================================================
#========================================================================
# Projections Plot using (Matplotlib) ===================================
#========================================================================
#========================================================================

#----------------------------------------------------------------------
# Copy Spin.py to the output folder directory -------------------------
#----------------------------------------------------------------------

try: f = open(dir_files + '/output/Spin/Spin.py'); f.close(); os.remove(dir_files + '/output/Spin/Spin.py')
except: 0 == 0
   
source = main_dir + '/plot/plot_projecao_spin.py'
destination = dir_files + '/output/Spin/Spin.py'
shutil.copyfile(source, destination)

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
# Allowing Bandas.py to be executed separatedly ---------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

file = open(dir_files + '/output/Spin/Spin.py', 'r')
lines = file.readlines()
file.close()

linha = 4

lines.insert(linha, '\n')
linha += 1; lines.insert(linha, '###################################################################### \n')
linha += 1; lines.insert(linha, f'# {VASProcar_name} Copyright (C) 2023 \n')
linha += 1; lines.insert(linha, f'# GNU GPL-3.0 license \n')
linha += 1; lines.insert(linha, f'# {url_1} \n')
linha += 1; lines.insert(linha, f'# {url_2} \n')
linha += 1; lines.insert(linha, f'# {url_3} \n')
linha += 1; lines.insert(linha, '###################################################################### \n')
linha += 1; lines.insert(linha, '# Authors:                                                             \n')
linha += 1; lines.insert(linha, '# ==================================================================== \n')
linha += 1; lines.insert(linha, '# Augusto de Lelis Araujo                                              \n')
linha += 1; lines.insert(linha, '# [2022-2023] CNPEM|Ilum|LNNano (Campinas-SP/Brazil)                   \n')
linha += 1; lines.insert(linha, '# [2007-2022] Federal University of Uberlandia (Uberlândia-MG/Brazil)  \n')
linha += 1; lines.insert(linha, '# e-mail: augusto-lelis@outlook.com                                    \n')
linha += 1; lines.insert(linha, '# ==================================================================== \n')
linha += 1; lines.insert(linha, '# Renan da Paixao Maciel                                               \n')
linha += 1; lines.insert(linha, '# Uppsala University (Uppsala/Sweden)                                  \n')
linha += 1; lines.insert(linha, '# e-mail: renan.maciel@physics.uu.se                                   \n')
linha += 1; lines.insert(linha, '###################################################################### \n')
linha += 1; lines.insert(linha, '\n')

linha += 1; lines.insert(linha, '#===================================================================== \n')
linha += 1; lines.insert(linha, '# These are the parameters that allows the code to run separatedly === \n')
linha += 1; lines.insert(linha, '#===================================================================== \n')
linha += 1; lines.insert(linha, '\n')
linha += 1; lines.insert(linha, f'n_procar = {n_procar}  #  Total Number of PROCAR files \n')
linha += 1; lines.insert(linha, f'nk = {nk}              #  Total Number of k-points \n')
linha += 1; lines.insert(linha, f'nb = {nb}              #  Total Number of bands \n')
linha += 1; lines.insert(linha, f'bands_range = "{bands_range}"  # Bands to be Plotted/Analyzed \n')
linha += 1; lines.insert(linha, f'E_min = {E_min}        #  Lower energy value of the bands in the plot (in relation to the Fermi level) \n')
linha += 1; lines.insert(linha, f'E_max = {E_max}        #  Higher energy value of the bands in the plot (in relation to the Fermi level) \n')
linha += 1; lines.insert(linha, f'Efermi = {Efermi}        #  Fermi energy from DFT outpout files \n')
linha += 1; lines.insert(linha, f'esc_fermi = {esc_fermi}  #  Would you like to shift the Fermi level? [0] No, use the value obtained from VASP [1] Yes, shift the Fermi level to 0.0 eV \n')
linha += 1; lines.insert(linha, f'Dimensao = {Dimensao}    #  [1] (kx,ky,kz) in 2pi/Param.; [2] (kx,ky,kz) in 1/Angs.; [3] (kx,ky,kz) in 1/nm.; [4] (k1,k2,k3) \n')
linha += 1; lines.insert(linha, f'peso_total = {peso_total}  #  weight/size of spheres in the projections plot \n')
linha += 1; lines.insert(linha, f'transp = {transp}          #  Transparency applied to the plot of projections \n')
linha += 1; lines.insert(linha, f'dest_k = {dest_k}          #  [0] DO NOT label the k-points; [1] highlight k-points present in KPOINTS file; [2] Customize: highlight and Label k-points \n')
linha += 1; lines.insert(linha, f'dest_pk = {dest_pk}        #  K-points coordinates to be highlighted in the band structure \n')

if (dest_k != 2):
   label_pk = ['null']*len(dest_pk) 
#-------------------------------------------------------------------------------
if (dest_k == 2): 
   for i in range(contador2):
       for j in range(34):
           if (label_pk[i] == '#' + str(j+1)):
              label_pk[i] = r_matplot[j]    
       if (DFT == '_QE/' and l_symmetry == 1):
          label_pk[i] = label_pk[i] + '$_{(' + symmetry_pk[i] + ')}$' 
#------------------------------------------------------------------------------ 
linha += 1; lines.insert(linha, f'label_pk = {label_pk}  #  K-points label \n')
#------------------------------------------------------------------------------

if (sum_save == 0): save_png = 1
linha += 1; lines.insert(linha, f'save_png = {save_png}; save_pdf = {save_pdf}; save_svg = {save_svg}; save_eps = {save_eps}  #  Plotting output format, where [0] = NOT and [1] = YES \n')                          
linha += 1; lines.insert(linha, '\n')
linha += 1; lines.insert(linha, '#======================================================================== \n')
linha += 1; lines.insert(linha, '# Color code:                                                             \n')
linha += 1; lines.insert(linha, '# 0  White  | 1  Black  | 2  Red    | 3  Green    | 4  Blue    | 5 Yellow \n')
linha += 1; lines.insert(linha, '# 6  Borwn  | 7  Grey   | 8  Violet | 9  Cyan     | 10 Magenta |          \n')
linha += 1; lines.insert(linha, '# 11 Orange | 12 Indigo | 13 Maroon | 14 Turquesa | 15 Green   |          \n')
linha += 1; lines.insert(linha, '#------------------------------------------------------------------------ \n')
linha += 1; lines.insert(linha, '# Colors applied to Spin Up and Down components:                          \n')
linha += 1; lines.insert(linha, f'c_spin_up = {c_spin_up}; c_spin_down = {c_spin_down}                     \n') 
linha += 1; lines.insert(linha, '#======================================================================== \n')

file = open(dir_files + '/output/Spin/Spin.py', 'w')
file.writelines(lines)
file.close()

#-------------------------------------------------------
if (sum_save != 0):
   exec(open(dir_files + '/output/Spin/Spin.py').read())
#-------------------------------------------------------

#=======================================================================

print(" ")
print("=============================================================")
print("= Edit the Plot of projections using the following Spin.py or")
print("= .agr files (via Grace) generated in the output/Spin folder.")   
print("=============================================================")

#-----------------------------------------------------------------
print(" ")
print("======================= Completed =======================")
print(" ")
#-----------------------------------------------------------------


#=======================================================================
# User option to perform another calculation or finished the code ======
#=======================================================================
if (len(inputs) == 0):
   execute_python_file(filename = '_loop.py')
