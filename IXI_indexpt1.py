import pandas as pd
import glob as glob
import ants
import numpy as np
import matplotlib.pyplot as plt
import time as time

mgz_files = glob.glob("/home/jusun/taha/IXI_fastsurfer_seg/*/*/*aparc*")


##################################################################################################
def biparietal_length(rr):        #give me the array 
    full_array = np.where(rr[:,:,:])
    segmentation= full_array
    bbox = 0, 0, 0, 0, 0, 0
    if len(segmentation) != 0 and len(segmentation[1]) != 0 and len(segmentation[0]) != 0 and len(segmentation[2]) != 0:
        x_min = int(np.min(segmentation[1]))
        x_max = int(np.max(segmentation[1]))
        y_min = int(np.min(segmentation[0]))
        y_max = int(np.max(segmentation[0]))
        z_min = int(np.min(segmentation[2]))
        z_max = int(np.max(segmentation[2]))

    bbox = x_min, x_max, y_min, y_max, z_min, z_max

    x_min = bbox[0]
    x_max = bbox[1]
    y_min = bbox[2]
    y_max = bbox[3]
    z_min = bbox[4]
    z_max = bbox[5]
    
    er=[];

    f = lambda x: (x[1],x[0],x[2],x[3])        #TAKE THE 4-TUPLE FROM THE BOUNDING BOX AND UNPACK IT IN A CERTAIN WAY


    for i in range(z_min,z_max):
        slice=rr[:,i,:]        #first position is the Z, iterate through each z slice and chop off everything POSTERIOR TO FRONTAL HORNS LIKE THIS
        try:
            box = bbox2(slice)   #DRAW A BOUNDING BOX AROUND THAT SLICE, 
        except:
            continue
        z_min_i = box[2]         #SAVE THE BOUNDING BOX COORDINATESANCEF
        z_max_i = box[3]
    
        er.append((i,int(z_max_i - z_min_i), z_min_i, z_max_i))
        

#sort it, and find me the cut with the biggest width of the frontal horn
#give me that specific iterator

    fl = [f(x) for x in er]
    fl.sort()
    fl.reverse()
    distance,best_iterator,ymin,ymax  = fl[0]
    ####use the below to show the plot
    #fig, axes = plt.subplots(1)
    #axes.grid()
    #### use the below to show the plot
    slice=rr[:,best_iterator,:]

    a_min,a_max,b_min,b_max = bbox2(slice)
    

    
    #best iterator will tell you 
    
    occipital_distance=fl[0][0]
    #axes.scatter(ymax,a_min)
    #axes.scatter(ymin,a_min) 

    return best_iterator,ymin,ymax,a_min,a_max,occipital_distance,slice
#    return best_iterator,ymin,ymax,a_min,a_max,frontal_distance,slice


###############################################################
######### functioning definign
def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    return rmin, rmax, cmin, cmax

########################################################################################################################################

def frontal_length(rr):        #give me the array 
    full_array = np.where(rr[:,:,:])
    segmentation= full_array
    bbox = 0, 0, 0, 0, 0, 0
    if len(segmentation) != 0 and len(segmentation[1]) != 0 and len(segmentation[0]) != 0 and len(segmentation[2]) != 0:
        x_min = int(np.min(segmentation[1]))
        x_max = int(np.max(segmentation[1]))
        y_min = int(np.min(segmentation[0]))
        y_max = int(np.max(segmentation[0]))
        z_min = int(np.min(segmentation[2]))
        z_max = int(np.max(segmentation[2]))

    bbox = x_min, x_max, y_min, y_max, z_min, z_max

    x_min = bbox[0]
    x_max = bbox[1]
    y_min = bbox[2]
    y_max = bbox[3]
    z_min = bbox[4]
    z_max = bbox[5]
    
    er=[];

    f = lambda x: (x[1],x[0],x[2],x[3])        #TAKE THE 4-TUPLE FROM THE BOUNDING BOX AND UNPACK IT IN A CERTAIN WAY


    for i in range(z_min,z_max):
        slice=rr[:110,i,:]        #first position is the Z, iterate through each z slice and chop off everything POSTERIOR TO FRONTAL HORNS LIKE THIS
        try:
            box = bbox2(slice)   #DRAW A BOUNDING BOX AROUND THAT SLICE, 
        except:
            continue
        z_min_i = box[2]         #SAVE THE BOUNDING BOX COORDINATESANCEF
        z_max_i = box[3]
    
        er.append((i,int(z_max_i - z_min_i), z_min_i, z_max_i))
        

#sort it, and find me the cut with the biggest width of the frontal horn
#give me that specific iterator

    fl = [f(x) for x in er]
    fl.sort()
    fl.reverse()
    distance,best_iterator,ymin,ymax  = fl[0]
    ####use the below to show the plot
    #fig, axes = plt.subplots(1)
    #axes.grid()
    #### use the below to show the plot
    slice=rr[:,best_iterator,:]

    a_min,a_max,b_min,b_max = bbox2(slice)
    

    
    #best iterator will tell you 
    
    frontal_distance=fl[0][0]
    #axes.scatter(ymax,a_min)
    #axes.scatter(ymin,a_min) 

    return best_iterator,ymin,ymax,a_min,a_max,frontal_distance,slice

def occipital_length(rr):        #give me the array 
    full_array = np.where(rr[:,:,:])
    segmentation= full_array
    bbox = 0, 0, 0, 0, 0, 0
    if len(segmentation) != 0 and len(segmentation[1]) != 0 and len(segmentation[0]) != 0 and len(segmentation[2]) != 0:
        x_min = int(np.min(segmentation[1]))
        x_max = int(np.max(segmentation[1]))
        y_min = int(np.min(segmentation[0]))
        y_max = int(np.max(segmentation[0]))
        z_min = int(np.min(segmentation[2]))
        z_max = int(np.max(segmentation[2]))

    bbox = x_min, x_max, y_min, y_max, z_min, z_max

    x_min = bbox[0]
    x_max = bbox[1]
    y_min = bbox[2]
    y_max = bbox[3]
    z_min = bbox[4]
    z_max = bbox[5]
    
    er=[];

    f = lambda x: (x[1],x[0],x[2],x[3])        #TAKE THE 4-TUPLE FROM THE BOUNDING BOX AND UNPACK IT IN A CERTAIN WAY


    for i in range(z_min,z_max):
        slice=rr[165:,i,:]        #first position is the Z, iterate through each z slice and chop off everything POSTERIOR TO FRONTAL HORNS LIKE THIS
        try:
            box = bbox2(slice)   #DRAW A BOUNDING BOX AROUND THAT SLICE, 
        except:
            continue
        z_min_i = box[2]         #SAVE THE BOUNDING BOX COORDINATESANCEF
        z_max_i = box[3]
    
        er.append((i,int(z_max_i - z_min_i), z_min_i, z_max_i))
        

#sort it, and find me the cut with the biggest width of the frontal horn
#give me that specific iterator

    fl = [f(x) for x in er]
    fl.sort()
    fl.reverse()
    distance,best_iterator,ymin,ymax  = fl[0]
    ####use the below to show the plot
    #fig, axes = plt.subplots(1)
    #axes.grid()
    #### use the below to show the plot
    slice=rr[:,best_iterator,:]

    a_min,a_max,b_min,b_max = bbox2(slice)
    

    
    #best iterator will tell you 
    
    occipital_distance=fl[0][0]
    #axes.scatter(ymax,a_min)
    #axes.scatter(ymin,a_min) 
    occipital_distance = b_max - b_min

    return best_iterator,256-ymin,ymax,b_min,b_max,occipital_distance,slice

############################

df1 = pd.DataFrame()


for scan in mgz_files: 


    #nifti_file = mgz_file.replace(".mgz", "_vents-only.nii.gz")
    print(scan)
    scan_name_formatted = scan.split("/")[-3].replace("-T1", "")        #      IXI012-HH-1211


   # fullname = "/home/jusun/taha/peds_vents/vents_only/" + basename_nifti_file
    seg = ants.image_read(scan)
    #print(img)
    seg_arr = seg.numpy()
    seg_arr_LV = np.where((seg_arr == 4.0) | (seg_arr == 5.0) | (seg_arr == 43.0) | (seg_arr == 44.0), 1.0, 0)     # turn off everything except the LV
    seg_LV = seg.new_image_like(seg_arr_LV)             # create the ants seg object for LV only
    seg_T = seg_arr_LV.T
#rr = seg_T
    rr = np.flip(seg_T, axis=0)
    
    orig_img = ants.image_read(scan.replace("aparc.DKTatlas+aseg.deep.mgz", "mask.mgz"))
    orig_img_arr = orig_img.numpy()
    orig_arr_T = orig_img_arr.T
    orig_rr = np.flip(orig_arr_T, axis=0)
    
    spacing = seg.spacing
    spacing_vol = spacing[0] * spacing[1] * spacing[2]

    try:
        best_iterator_anterior,ymin_anterior,ymax_anterior,a_min,a_max,frontal_distance,slice_anterior = frontal_length(rr)
        f_d = frontal_distance * spacing[0]
        
    except:
        f_d = "NA"

    try:
        best_iterator_posterior,ymin_posterior,ymax_posterior,b_min,b_max,occipital_distance,slice_posterior = occipital_length(rr)
        o_d = occipital_distance * spacing[0]
    
    except:
        o_d = "NA"

    try:
        best_iterator_biparietal,ymin_posterior,ymax_posterior,b_min,b_max,biparietal_distance,slice_bp = biparietal_length(orig_rr)
        b_p = biparietal_distance * spacing[0]
        
    except:
        b_p = "NA"
#        biparietal_length(orig_rr)
 #   except:
  #      print("error")
   #     continue
    #a,b,c,d,e = frontal_length(rr)
   # print("max frontal distance: %s, max occipital distance: %s, max biparietal length: %s, Approximate total volume: %s " % (frontal_distance * spacing[0], occipital_distance * spacing[0], biparietal_distance * spacing[0], np.count_nonzero(rr) * spacing_vol))
    
    df2 = pd.DataFrame([scan_name_formatted, f_d, o_d, b_p, np.count_nonzero(rr) * spacing_vol])
    
    print(df2)
    df1 = pd.concat([df1, df2.T])
    
    
    
print(df1)
df1.columns = ["Name", "Frontal Horn Width", "Occipital Horn Width", "Biparietal Width", "Lateral Ventricular Volume"]

df1.to_csv("/home/jusun/taha/IXI_data_2.tsv", sep="\t", index=False)
    
    
    
    