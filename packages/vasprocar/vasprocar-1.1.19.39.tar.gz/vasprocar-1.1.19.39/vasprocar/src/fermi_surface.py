# VASProcar Copyright (C) 2023
# GNU GPL-3.0 license

import numpy as np

def execute_python_file(filename: str):
    return exec(open(main_dir + str(filename)).read(), globals())

#-----------------------------------------------------------------------
# Check whether the folder 'Fermi_Surface' exists ----------------------
#-----------------------------------------------------------------------
if os.path.isdir(dir_files + '/output/Fermi_Surface'):
   0 == 0
else:
   os.mkdir(dir_files + '/output/Fermi_Surface')
#-----------------------------------------------

#-----------------------------------------------------------------------
# Check whether the folder 'figures' exists ----------------------------
#-----------------------------------------------------------------------
if os.path.isdir(dir_files + '/output/Fermi_Surface/figures'):
   0 == 0
else:
   os.mkdir(dir_files + '/output/Fermi_Surface/figures')
#-------------------------------------------------------    

#======================================================================
# Getting the input parameters ========================================
#======================================================================
execute_python_file(filename = DFT + '_info.py')

#======================================================================
# Analyzing the variation of the coordinates of the K-points ==========
#======================================================================
execute_python_file(filename = DFT + '_var_kpoints.py')

soma_1 = dk[0] + dk[1] + dk[2]
soma_2 = dk[3] + dk[4] + dk[5]

if (soma_1 != 2 and soma_2 != 2):
   print ("============================================================")
   print ("!!! ERROR !!!                                               ")
   print ("============================================================")
   print ("The calculation performed does not correspond to a 2D plan  ")
   print ("in the BZ. kikj-plan (i,j = x,y,z or i,j = 1,2,3)           ")
   print ("------------------------------------------------------------")
   print ("Please, use the option [665] to get the correct KPOINTS file")
   print ("============================================================")
   confirmation = input (" ")
   exit()

#======================================================================
# Get the input from user =============================================
#======================================================================

print ("##############################################################")
print ("#################### Fermi's surface plot ####################")
print ("##############################################################")
print (" ")

if (escolha == -1):
  
   print ("##############################################################")
   print ("Regarding the bands, what do you want to analyze? ============")
   print ("[0] Plot all bands on the Fermi Surface ======================")
   print ("[1] Plot a selected range of bands on Sup. from Fermi ========")
   print ("##############################################################")
   esc_band = input (" "); esc_band = int(esc_band)
   print (" ")

   if (esc_band == 1):
      print ("##############################################################")
      print ("Inform the Band interval to be plotted: ===================== ")
      print ("--------------------------------------------------------------")
      print ("Examples:                                                     ")
      print ("Initial_band  Final_band: 5:27                                ")
      print ("Initial_band  Final_band: 13:49                               ")
      print ("Initial_band  Final_band: 7:7   or   7*                       ")
      print ("##############################################################") 
      bands_range = input ("Initial_band  Final_band: ")
      print (" ")
      #------------------------------------------------------------------------------------------
      selected_bands = bands_range.replace(':', ' ').replace('-', ' ').replace('*', ' *').split()
      #------------------------------------------------------------------------------------------
      if (selected_bands[1] == "*"):
         Band_i = int(selected_bands[0])
         Band_f = Band_i
      if (selected_bands[1] != "*"):
         Band_i = int(selected_bands[0])
         Band_f = int(selected_bands[1])
      #---------------------------------

   print ("##############################################################") 
   print ("with respect to energy, would you like? ======================")
   print ("[0] Use the default energy value from DFT output =============")
   print ("[1] Shift the Fermi level to 0.0 eV  =========================")
   print ("##############################################################")
   esc_fermi = input (" "); esc_fermi = int(esc_fermi)
   print (" ") 

print ("##############################################################")
print ("What number of Energies do you want to analyze? ==============")
print ("##############################################################")
n_energ = input (" "); n_energ = int(n_energ)
print(" ")

if (n_energ <= 0):
   n_energ = 1

print ("##############################################################")
print ("Regarding the energy values: =================================")
print ("[0] Must be obtained automatically by code ===================")
print ("[1] Must sweep a certain range of energy =====================")
print ("[2] I want to specify each energy value manually =============")   
print ("##############################################################")
esc_energ = input (" "); esc_energ = int(esc_energ)
print(" ")

if (esc_energ == 1):
   print ("##############################################################")
   print ("Choose the Energy range to be analyzed: ===================== ")
   print ("Type as in the examples below =============================== ")
   print ("--------------------------------------------------------------")
   print ("Initial_energ Final_Energ: -4.5 6.9                           ")
   print ("Initial_energ Final_Energ:  0.0 5.5                           ")
   print ("##############################################################") 
   print (" ")
   energ_i, energ_f = input ("Initial_energ Final_Energ: ").split()
   energ_i = float(energ_i)
   energ_f = float(energ_f)
   print (" ")

if (esc_energ == 2):
   #----------------
   E = [0.0]*n_energ
   #----------------
   print ("##############################################################")
   print ("Enter Energy values as in the examples below ================ ")
   print ("--------------------------------------------------------------")
   print ("Energies: -4.5 -2.0 -1.0  0.0  1.0  3.0 5.0                   ")
   print ("Energies:  0.2  0.5  0.78 1.23 9.97                           ")
   print ("--------------------------------------------------------------")
   print ("!!! important note !!! ====================================== ")
   print ("Always enter energy values in ascending order =============== ")
   print ("##############################################################") 
   print (" ")
   E = input ("Energies: ").split()
   for i in range(n_energ):
       E[i] = float(E[i])
   print (" ")

#-----------------------------------------------------------------------------

if (soma_1 == 2 or soma_2 == 2):
   #----------------------------------   
   if (soma_2 == 2 and escolha == -1):
      print ("##############################################################")
      print (" Would you like to choose k-axis units?                       ")
      print (" [1] (kx,ky,kz) 2pi/Param. (Param. in Angs.) =================")
      print (" [2] (kx,ky,kz) 1/Angs. ======================================")
      print (" [3] (kx,ky,kz) 1/nm.   ======================================")   
   #----------------------------------
   if (soma_1 == 2 and soma_2 == 2 and escolha == -1):    
      print (" [4] (k1,k2,k3) Fractional coord: K = k1*B1 + k2*B2 + k3*B3 ==")    
   #----------------------------------
   if (soma_2 == 2 and escolha == -1): 
      print ("##############################################################") 
      Dimensao = input (" "); Dimensao = int(Dimensao)
      print (" ")
   #----------------------------------
   if (soma_2 != 2):
      Dimensao = 4
   #----------------------------------   
   if (soma_1 != 2 and escolha == 1):
      Dimensao = 1
   #----------------------------------   
   if (soma_1 == 2 and soma_2 == 2 and escolha == 1):
      Dimensao = 4
   #----------------------------------   
     
   if (Dimensao < 4):
      if (dk[3] == 1 and dk[4] == 1): Plano_k = 1  #  kxky-plan
      if (dk[3] == 1 and dk[5] == 1): Plano_k = 2  #  kxkz-plan
      if (dk[4] == 1 and dk[5] == 1): Plano_k = 3  #  kykz-plan
   
   if (Dimensao == 4):
      if (dk[0] == 1 and dk[1] == 1): Plano_k = 1  #  k1k2-plan
      if (dk[0] == 1 and dk[2] == 1): Plano_k = 2  #  k1k3-plan
      if (dk[1] == 1 and dk[2] == 1): Plano_k = 3  #  k2k3-plan   

#-----------------------------------------------------------------------------   

print ("##############################################################")
print ("Do you want to compile a video from the generated pictures? ==")
print ("[0] NO =======================================================")
print ("[1] YES ======================================================")
print ("==============================================================")
print ("Note: Images will not be generated in .pdf|.svg|.eps =========")
print ("##############################################################")
video = input (" "); video = int(video)
print (" ")

if (video == 1):
   #-----------------------------------------------------------------------
   print ("##############################################################")
   print ("How many figures should appear per second (fps) in the video? ")
   print ("tip 1: =======================================================")
   print ("Choose between 1 and 30 figures ==============================")
   print ("tip 2: =======================================================")
   print ("The greater the number of images and the greater the number of")
   print ("images per second (fps), the smoother the video.              ")
   print ("##############################################################")
   n_fig = input (" "); n_fig = int(n_fig)  
   print (" ")
   #-------------------------
   if (n_fig <= 0): n_fig = 1
   #-------------------------
   save_png = 1
   save_pdf = 0
   save_eps = 0

if (escolha == -1):
   print ("##############################################################")
   print ("Choose the K-mesh grid (DxD) to be interpolated: =============")
   print ("Note:  The k-mesh grid used in your VASP calculation can be   ")
   print ("       used as a reference. You are free to increase/decrease ")
   print ("       the number of kpoints to be interpolated.              ")
   print ("Hint:  use 101 (unless more precision is required).           ")
   print ("##############################################################") 
   n_d = input (" "); n_d = int(n_d)  
   print (" ")   

if (escolha == 1):
   esc_fermi = 1
   esc_band = 0
   n_d = 101

#----------------------
if (Efermi == -1000.0):
   Efermi = 0.0
   esc_fermi = 0 

if (esc_fermi == 0): dE_fermi = 0.0
if (esc_fermi == 1): dE_fermi = (Efermi)*(-1)
#--------------------------------------------

if (esc_band == 0):
   Band_i = 1
   Band_f = nb

bands_range = '1:' + str(nb)

#======================================================================
# Obtaining the results from DFT outpout files ========================
#======================================================================
execute_python_file(filename = DFT + '_nscf.py')

#======================================================================
# Saving data to plot the Fermi =======================================
#======================================================================     

#------------------------------------------------------------------------
inform = open(dir_files + '/output/informacoes.txt', "r")
bandas = open(dir_files + '/output/Bandas.dat', "r") 
sfermi = open(dir_files + '/output/Fermi_Surface/Fermi_Surface.dat', "w")
#------------------------------------------------------------------------

palavra = 'k-points |'                          

for line in inform:   
    if palavra in line: 
       break

VTemp = inform.readline()
VTemp = inform.readline()
       
for i in range (n_procar*nk):
    VTemp = inform.readline().split()
    k1 = float(VTemp[1]); k2 = float(VTemp[2]); k3 = float(VTemp[3])
    kx = float(VTemp[4]); ky = float(VTemp[5]); kz = float(VTemp[6])

    if (Dimensao != 4):
       sfermi.write(f'{kx} {ky} {kz} ')   
    if (Dimensao == 4):
       sfermi.write(f'{k1} {k2} {k3} ')

    VTemp = bandas.readline().split()
    for j in range (1,(nb+1)):
        energ = float(VTemp[j])
        sfermi.write(f'{energ} ')
    sfermi.write("\n")

#-------------
inform.close()
bandas.close()
sfermi.close()
#-------------

os.remove(dir_files + '/output/Bandas.dat')

#----------------------------------------------------------------------
# Copy Fermi_Surface.py to the output folder directory  ---------------
#----------------------------------------------------------------------

try: f = open(dir_files + '/output/Fermi_Surface/Fermi_Surface.py'); f.close(); os.remove(dir_files + '/output/Fermi_Surface/Fermi_Surface.py')
except: 0 == 0
 
source = main_dir + '/plot/plot_fermi_surface.py'
destination = dir_files + '/output/Fermi_Surface/Fermi_Surface.py'
shutil.copyfile(source, destination)

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Allowing the Plot to be executed separatedly -------------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

file = open(dir_files + '/output/Fermi_Surface/Fermi_Surface.py', 'r')
lines = file.readlines()
file.close()

linha = 11

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
linha += 1; lines.insert(linha, f'Dimensao  = {Dimensao}  #  [1] (kx,ky,kz) in 2pi/Param.; [2] (kx,ky,kz) in 1/Angs.; [3] (kx,ky,kz) in 1/nm.; [4] (k1,k2,k3) \n')
linha += 1; lines.insert(linha, f'Plano_k   = {Plano_k}   #  [1] kxky or k1k2; [2] kxkz or k1k3; [3] kykz or k2k3  \n')
linha += 1; lines.insert(linha, f'ispin = {ispin}         #  [1] Calculation without Spin polarization; [2] Calculation with Spin polarization \n')
linha += 1; lines.insert(linha, f'Band_i = {Band_i}       #  Initial band to be plotted \n')
linha += 1; lines.insert(linha, f'Band_f = {Band_f}       #  Final band to be plotted \n')
linha += 1; lines.insert(linha, f'bands_range = "{bands_range}" \n')
linha += 1; lines.insert(linha, f'n_d = {n_d}             #  Interpolation grid (DxD) \n')
linha += 1; lines.insert(linha, f'Efermi = {Efermi}       #  Fermi energy from DFT outpout files \n')
linha += 1; lines.insert(linha, f'esc_fermi = {esc_fermi} #  Would you like to shift the Fermi level? [0] No, use the value obtained from VASP [1] Yes, shift the Fermi level to 0.0 eV \n')
linha += 1; lines.insert(linha, f'esc_energ = {esc_energ} #  How to obtain energies: Where [0] is automatic; [1] energy range and [2] entered manually \n')
linha += 1; lines.insert(linha, f'n_energ = {n_energ}     #  Number of energies to be used in the plot of Fermi Surfaces \n')
#--------------------------------
if (esc_energ == 1):
   linha += 1; lines.insert(linha, f'energ_i = {energ_i}; energ_f = {energ_f}  #  Starting and ending energy of the Energy Range in the Fermi Surfaces plot \n')
if (esc_energ == 2):
   linha += 1; lines.insert(linha, f'E = {E}  #  Energy values specified manually in the plot of Fermi Surfaces \n')
if (esc_energ < 2):
   linha += 1; lines.insert(linha, f'E = [0.0, 0.0, 0.0, 0.0, 0.0]  #  Values of the Levels Contours specified manually \n')
#--------------------------------
linha += 1; lines.insert(linha, f'video = {video}  #  Choose if a video should be generated or not, where [0] = NO and [1] = YES \n')
if (video == 1):
   linha += 1; lines.insert(linha, f'n_fig = {n_fig}  #  Number of figures that appear in the video per second (fps) \n')

if (sum_save == 0): save_png = 1
linha += 1; lines.insert(linha, f'save_png = {save_png}; save_pdf = {save_pdf}; save_svg = {save_svg}; save_eps = {save_eps}  #  Plotting output format, where [0] = NOT and [1] = YES \n')
linha += 1; lines.insert(linha, '\n')
linha += 1; lines.insert(linha, '#===================================================================== \n')

file = open(dir_files + '/output/Fermi_Surface/Fermi_Surface.py', 'w')
file.writelines(lines)
file.close()

#----------------------------------------------------------------------
exec(open(dir_files + '/output/Fermi_Surface/Fermi_Surface.py').read())
#----------------------------------------------------------------------

#=======================================================================
   
print(" ")
print("=========================================================")
print("= Edit the Plots through the Fermi_Surface.py file ======")
print("= generated in the output/Fermi_Surface folder ==========")   
print("=========================================================")

#-----------------------------------------------------------------
print(" ")
print("======================= Completed =======================")
#-----------------------------------------------------------------

#=======================================================================
# User option to perform another calculation or finished the code ======
#=======================================================================
execute_python_file(filename = '_loop.py')
