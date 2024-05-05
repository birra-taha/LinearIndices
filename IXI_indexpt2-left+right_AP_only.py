#!/bin/python

import pandas as pd
import glob as glob
import ants
import numpy as np
import matplotlib.pyplot as plt
import time as time

mgz_files = glob.glob("/home/jusun/taha/IXI_fastsurfer_seg/*/*/*aparc*")


######

##.  Find the total brain mask volume (including cerebellum), supracortical volume (whole brain minus cerebellum and brainstem )






def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    return rmin, rmax, cmin, cmax

#####



def thal_iterator(mgz_file):
    
   # fullname = "/home/jusun/taha/peds_vents/vents_only/" + basename_nifti_file
    seg = ants.image_read(mgz_file)
    #print(img)
    seg_arr = seg.numpy()
    seg_arr_LV = np.where((seg_arr == 9.0) | (seg_arr == 10.0) | (seg_arr == 48.0) | (seg_arr == 49.0), 1.0, 0)     # turn off everything except the LV
    seg_LV = seg.new_image_like(seg_arr_LV)             # create the ants seg object for LV only
    seg_T = seg_arr_LV.T
#rr = seg_T
    rr_thal = np.flip(seg_T, axis=0)
    
    full_array = np.where(rr_thal[:,:,:])
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
    
    seg_arr = seg.numpy()
    seg_arr_LV = np.where((seg_arr == 4.0) | (seg_arr == 5.0) | (seg_arr == 43.0) | (seg_arr == 44.0), 1.0, 0)     # turn off everything except the LV
    seg_arr_brain_mask = np.where((seg_arr != 0.0), 1.0, 0)     # turn ON everything-- call it the brain mask
    tt = [2,41,10,11,12,13,17,18,26,28,49,50,51,52,53,54,58,60,1002, 1003, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012,
       1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023,
       1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1034, 1035, 2002,
       2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
       2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025,
       2026, 2027, 2028, 2029, 2030, 2031, 2034, 2035]
#seg_arr_cortex = np.where(np.array(seg_arr).any() ==  np.array(tt).any(), 1.0, 0)

    seg_arr_cortex = np.where(np.isin(seg_arr, tt), 1.0, 0)
    cortex_vol = np.count_nonzero(seg_arr_cortex) * seg.spacing[0] *  seg.spacing[1]  *  seg.spacing[2]  
    seg_LV = seg.new_image_like(seg_arr_LV)             # create the ants seg object for LV only
    seg_T = seg_arr_LV.T
    seg_brain_mask = seg_arr_brain_mask.T
    
#rr = seg_T
    rr_LV = np.flip(seg_T, axis=0)
    rr_brain_mask = np.flip(seg_brain_mask, axis=0)
    
    slice = rr_LV[:,bbox[0]-1,:]
    slice_bm = rr_brain_mask[:,bbox[0]-1,:]
    
    left_slice = rr_LV[:,bbox[0]-1,128:]
    right_slice = rr_LV[:,bbox[0]-1,:128]
    
    a_bm,b_bm,c_bm,d_bm = bbox2(slice_bm)
    
    #slice_2=rr_thal[:,bbox[0],:]
    a,b,c,d = bbox2(left_slice)
    left_AP = (b-a)*seg.spacing[0]        #distance from bottom to top on left side
    a,b,c,d = bbox2(right_slice)
    right_AP = (b-a)*seg.spacing[0]        #distance from bottom to top on left side
    
    AP_mask = (b_bm - a_bm)*seg.spacing[0]
    
  #  return left_AP, right_AP
 #   return left_AP, right_AP, AP_mask, slice_bm,slice
    return left_AP, right_AP, AP_mask, cortex_vol


##################################################################################################

    

    
############################

df1 = pd.DataFrame()


for scan in mgz_files: 


    #nifti_file = mgz_file.replace(".mgz", "_vents-only.nii.gz")
    print(scan)
    scan_name_formatted = scan.split("/")[-3].replace("-T1", "")        #      IXI012-HH-1211
    
    try:
        left_AP, right_AP, AP_mask_dist, cortex_vol = thal_iterator(scan)
        
    except:
        print("error")
        continue
    #a,b,c,d,e = frontal_length(rr)
   # print("max frontal distance: %s, max occipital distance: %s, max biparietal length: %s, Approximate total volume: %s " % (frontal_distance * spacing[0], occipital_distance * spacing[0], biparietal_distance * spacing[0], np.count_nonzero(rr) * spacing_vol))
    
    df2 = pd.DataFrame([scan_name_formatted, left_AP, right_AP, AP_mask_dist, cortex_vol])
    
    df1 = pd.concat([df1, df2.T])
    
    
    
print(df1)
df1.columns = ["Name", "Left AP", "Right AP", "Full AP (midline)", "Supratentorial volume"]

df1.to_csv("/home/jusun/taha//vent_indices_projects/IXI_data_AP.tsv", sep="\t", index=False)
    
    
    
    
    
    #print("ymin: %s; ymax: %s; b_min: %s, b_max: %s" % (occipital_length(rr)[1],occipital_length(rr)[2], occipital_length(rr)[3], occipital_length(rr)[4]))
    #print("ymin: %s; ymax: %s; b_min: %s, b_max: %s" % (frontal_length(rr)[1],frontal_length(rr)[2], frontal_length(rr)[3], frontal_length(rr)[4]))
 
    #plt.scatter(ymax,a_min)
   # plt.scatter(ymin,a_min) 
    #plt.scatter()
   # fig, (ax1,ax2) = plt.subplots(1,2)
    
  #  ax1.hlines(occipital_length(rr)[2],occipital_length(rr)[3],occipital_length(rr)[4])
 #   ax1.imshow(occipital_length(rr)[6])
#    ax2.hlines(frontal_length(rr)[3],frontal_length(rr)[1],frontal_length(rr)[2])

    #ax2.imshow(frontal_length(rr)[6])
    #plt.pause(0.05)
    
    #img_ventricles = img.new_image_like(img_arr)
    #print(fullname)

    
    
    
    
    
    #img_ventricles.to_file(fullname)
    
    
    