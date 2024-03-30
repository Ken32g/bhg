
from brainspace.datasets import load_conte69
from brainspace.plotting import plot_hemispheres
from brainspace.datasets import load_group_fc, load_parcellation
from brainspace.utils.parcellation import map_to_labels
import numpy as np
import pandas as pd

def bhg_brain_plot(regions, reg_vals):
  """ 
  Regions, reg_vals are lists of the same length
  """
  conte69_to_aparc_path = f"aparc-a2009s_conte69.csv"
  aparc_to_ui_path = f"aparc-ui.xlsx"
  
  conte69_to_aparc = pd.read_csv(conte69_to_aparc_path, header=None, names=["r"])
  labeling = conte69_to_aparc.r.to_numpy()
  aparc_uniq = np.unique(labeling)
  nlab = len(aparc_uniq)
  
  aparc_to_ui = pd.read_excel(aparc_to_ui_path)
  lab_idx = aparc_to_ui[["uAI Label Name", "Freesurfer Index"]]
  lab_idx.rename(
      columns={"uAI Label Name": "lab", "Freesurfer Index": "idx"}, inplace=True
  )
  
  for element in aparc_uniq:
      if element not in lab_idx['idx'].values:
          new_row = pd.DataFrame({'idx': [element]})
          lab_idx = pd.concat([lab_idx, new_row], ignore_index=True)
  
  reg_dict = dict(zip(regions, reg_vals))
  
  lab_idx['reg_val'] = lab_idx['lab'].map(reg_dict)
  lab_idx_sorted = lab_idx.sort_values(by='idx', ascending=True)
  plot_arr = lab_idx_sorted.reg_val.to_numpy()
  plot_arr[np.isnan(plot_arr)]=0
  
  # Load left and right hemispheres
  surf_lh, surf_rh = load_conte69()
  surf_lh.n_points
  
  grad = map_to_labels(plot_arr, labeling, mask=labeling != 0,fill=np.nan)
  plot_hemispheres(surf_lh, surf_rh, array_name=grad, cmap = "RdBu_r",size=(800, 200),nan_color=(255, 255, 255, 1))
