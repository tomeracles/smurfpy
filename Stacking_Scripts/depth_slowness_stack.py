'''
Depth_Slowness_Stack_Fig.py

Plot a depth stack and corresponding slowness stack on the same figure.
Automatically picks peaks based on depth ranges defined below line 83.

Requires previous running of depth_stack.py and slowness_stack.py
Edit filts, num_rfs, conversion below (lines 32, 33, 37).
'''

#------------Import all the relevant modules------------------#

import matplotlib.pyplot as plt
import numpy as np
import pickle
from matplotlib import gridspec
from scipy.signal import find_peaks
import compute_conversions
import matplotlib.pylab as pylab
import os,sys

#Set figure parameters
params = {'legend.fontsize': 'x-large',
              'figure.figsize': (8,10),
             'axes.labelsize': 'x-large',
             'axes.titlesize':'x-large',
             'xtick.labelsize':'x-large',
             'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

#------------------------------------------------------------#

# Command line help
if len(sys.argv) != 8 or str(sys.argv[1]).lower() == 'help':
    print('\n')
    print('-----------------------------------------------------------------------------------------------------------------------')
    print(sys.argv[0])
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('Description:           Combines previously calculated depth and slowness stack in one figure.')
    print('Inputs:                Depth and slowness stack pickle files')
    print('Outputs:               Combined depth and slowness stack image pdf/png)\n')
    print('Usage:                 >> python3 depth_stack.py conversion lonmin lonmax latmin latmax rffilter num_rfs')
    print('Format                 1: [str], 2-5: [int], 6: [str], 7: [int]')
    print('Recommended:           >> python3 depth_slowness_stack.py prem -179 179 -89 89 jgf1 339')
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('\n')
    sys.exit()


# Initial options
conv = str(sys.argv[1])
lonmin = int(sys.argv[2]) 
lonmax = int(sys.argv[3]) 
latmin = int(sys.argv[4]) 
latmax = int(sys.argv[5])
rffilter=str(sys.argv[6])
num_rfs = int(sys.argv[7])



#Set some values
direc='../'
conversion = conv
filt = rffilter
lat1 = latmax
lon1 = lonmin
lat2 = latmin
lon2 = lonmax

#Set place to save output files (plot and pickle of stack)
savedir=direc+'Final_Figures/'
if not os.path.exists(savedir):
    os.makedirs(savedir)
savepath=savedir+conversion
if not os.path.exists(savepath):
    os.makedirs(savepath)

s410 = []
s660 = []
sX = []

#--------------Depth Stack
fig = plt.figure(figsize=(24, 10))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 4])
stack1=pickle.load(open(direc+'Depth_Stacks/'+conversion+'/Depth_Stack_'+filt+'_'+conversion+'_'+str(num_rfs)+'RFs_loc'+str(lat1)+'_'+str(lat2)+'_'+str(lon1)+'_'+str(lon2)+'.PICKLE','rb'))

#Extract common values
depth=stack1['depth']
conversion=stack1['conversion']

#Extract Stack 1 Values
amp_rel_1=stack1['amp_rel']
amp_rel_1SE_P_1=stack1['amp_rel_1SE_P']
amp_rel_1SE_N_1=stack1['amp_rel_1SE_N']
amp_rel_2SE_P_1=stack1['amp_rel_2SE_P']
amp_rel_2SE_N_1=stack1['amp_rel_2SE_N']

#Find peaks in depth stack: Currently set to X,410 and 660. Edit accordingly

peaks, _ = find_peaks(amp_rel_1, width=1)

x_peaks = []
x_amps = []
four_ten_peaks = []
four_ten_amps = []
six_sixty_peaks = []
six_sixty_amps = []
isreal = False

for peak in peaks:
    if 230 < depth[peak] < 350:
        x_peaks.append(peak)
        x_amps.append(amp_rel_1[peak])
        isreal = True
    if 370 < depth[peak] < 450:
        four_ten_peaks.append(peak)
        four_ten_amps.append(amp_rel_1[peak])
    if 600 < depth[peak] < 720:
        six_sixty_peaks.append(peak)
        six_sixty_amps.append(amp_rel_1[peak])

#Create lists of max peak at each depth for each frequency band
if len(x_amps) >= 1:
    max_value = max(x_amps)
    max_index = x_amps.index(max_value)
    d1 = depth[x_peaks[max_index]]
    sX.append(d1)
else:
    sX.append('NaN')
if len(four_ten_amps) >= 1:
    max_value = max(four_ten_amps)
    max_index = four_ten_amps.index(max_value)
    d2 = depth[four_ten_peaks[max_index]]
    s410.append(d2)
else:
    s410.append('NaN')
if len(six_sixty_amps) >= 1:
    max_value = max(six_sixty_amps)
    max_index = six_sixty_amps.index(max_value)
    d3 = depth[six_sixty_peaks[max_index]]
    s660.append(d3)
else:
    s660.append('NaN')

#Set up axis
ax1 = fig.add_subplot(gs[0])

#Plot the relative amplitudes against the depth points
plt.plot(amp_rel_1, depth, 'k', lw = 1.5)

#Plot error lines
plt.plot(amp_rel_1SE_P_1, depth, 'k--', lw = 0.75, color='0.75')
plt.plot(amp_rel_1SE_N_1, depth, 'k--', lw = 0.75, color='0.75')
plt.plot(amp_rel_2SE_P_1, depth, 'k--', lw = 1, color='0.5')
plt.plot(amp_rel_2SE_N_1, depth, 'k--', lw = 1, color='0.5')

#Fill the postive values with red, negative with blue
plt.fill_betweenx(depth, 0, amp_rel_2SE_N_1, where=amp_rel_2SE_N_1 >= 0, facecolor=[1,0.4,0.4])
plt.fill_betweenx(depth, 0, amp_rel_2SE_P_1, where=amp_rel_2SE_P_1 <= 0, facecolor=[0.4, 0.4, 1])

#Make label for y axis (none for x)
plt.ylabel('Depth (km)', fontsize=24)
plt.xticks([])

#Create dotted lines to show where there are new normalisations
x=[-0.5,1.1]
y1=[150,150]
plt.plot(x,y1, 'k--')

#Set axis limits and invert y axis
plt.gca().set_xlim([-0.5,1.1])
plt.gca().set_ylim([0,900])
plt.gca().invert_yaxis()
plt.gca().tick_params(labelsize=24)

#Set title for axis
ax1.title.set_size(24)

#Labels
if isreal:
    plt.plot(0.97, d1, marker="s", color='orange', markersize=12, markeredgewidth=1.6)
    plt.annotate(str(d1),xy=(0.4, d1), xytext=(0.70, d1), arrowprops=dict(facecolor='black'), fontsize=16, va='center')
plt.plot(0.97, d2, marker="o", color='green', markersize=12, markeredgewidth=1.6)
plt.plot(0.97, d3, marker="^", color='purple', markersize=12, markeredgewidth=1.6)
plt.annotate(str(d2),xy=(0.4, d2), xytext=(0.70, d2), arrowprops=dict(facecolor='black'), fontsize=16, va='center')
plt.annotate(str(d3),xy=(0.4, d3), xytext=(0.70, d3), arrowprops=dict(facecolor='black'), fontsize=16, va='center')

#--------------Slowness Stack

stack2=pickle.load(open(direc+'Slowness_Stacks/Slowness_'+filt+'_'+str(num_rfs)+'RFs'+'.PICKLE','rb'))

STACK2=stack2['STACK_nonnorm']

STACK2=STACK2/np.max(np.abs(STACK2))
SE=stack2['STACK_SE']
time=stack2['time']
slow=stack2['slow']

for c in range(201):
    for d in range(1751):
        if STACK2[c,d] > 0:
            STACK2[c,d] = STACK2[c,d] - 2*SE[c,d]
            if STACK2[c,d] < 0:
                STACK2[c,d] = 0
        elif STACK2[c,d] < 0:
            STACK2[c,d] = STACK2[c,d] + 2*SE[c,d]
            if STACK2[c,d] > 0:
                STACK2[c,d] = 0

#---------------Plot 2
#Set up axis
ax2 = fig.add_subplot(gs[1])

#---------------------Plot Predicted Travel Times and Slowness of converted phases-----------------
#

lines= compute_conversions.compute_arrivals(conversion=conversion)

plt.plot(lines[0][1] ,lines[0][2],'k-', linewidth=2,label='conversion Pds')

plt.plot(lines[2][1], lines[2][2], 'k:', linewidth=2,label='topside multiple PPds')

plt.legend(loc=2,fontsize=18)

#Plot locations of peaks in depth stack on slowness stacks
#arr[0][] = Pds, arr[1][] = PSvds, arr[2][]= PPvds
if isreal:
    arr1 = compute_conversions.compute_arrivals_one_depth(d1,conversion=conversion)
    plt.plot(arr1[0][1], arr1[0][2], marker="s", color='orange', markersize=12, markeredgewidth=1.6)
    #plt.plot(arr1[1][1], arr1[1][2], marker="s", color='orange', markersize=12, markeredgewidth=1.6)
    plt.plot(arr1[2][1], arr1[2][2], marker="s", color='orange', markersize=12, markeredgewidth=1.6)

arr2 = compute_conversions.compute_arrivals_one_depth(d2,conversion=conversion)
plt.plot(arr2[0][1], arr2[0][2], marker="o", color='green', markersize=12, markeredgewidth=1.6)
#plt.plot(arr2[1][1], arr2[1][2], marker="o", color='green', markersize=12, markeredgewidth=1.6)
plt.plot(arr2[2][1], arr2[2][2], marker="o", color='green', markersize=12, markeredgewidth=1.6)
arr3 = compute_conversions.compute_arrivals_one_depth(d3,conversion=conversion)
plt.plot(arr3[0][1], arr3[0][2], marker="^", color='purple', markersize=12, markeredgewidth=1.6)
#plt.plot(arr3[1][1], arr3[1][2], marker="^", color='purple', markersize=12, markeredgewidth=1.6)
plt.plot(arr3[2][1], arr3[2][2], marker="^", color='purple', markersize=12, markeredgewidth=1.6)

#-----------------Plot the stack----------------------------

#Plotting using contourf (time_axis (RF time), slowness_range, slowness_matrix, contour_levels , colourmap , extend (extend grid if data lies outside range))
contour_levels = np.linspace(-.05,.0501,int(20))
cs = plt.contourf(time,slow,STACK2,contour_levels, cmap=plt.cm.seismic, extend="both")
cbar = plt.colorbar(format="%0.2f")

#Set axes limits
plt.ylim(-0.8,0.8)
plt.xlim(0,150)

#Axes labels and title
plt.ylabel ('Slowness (s/deg)', fontsize=24)
plt.xlabel ('Time w.r.t. P (s)', fontsize=24)
plt.gca().tick_params(labelsize=24)

#Set title for axis
ax2.title.set_size(24)

#-------------Final Plotting

#Save figures
plt.savefig(savepath+'Dep_Slow_Stack_'+str(num_rfs)+'_'+filt+'.pdf')
plt.savefig(savepath+'Dep_Slow_Stack_'+str(num_rfs)+'_'+filt+'.png')

#Show the plot
plt.show()

print(sX)
print(s410)
print(s660)
