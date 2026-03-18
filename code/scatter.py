import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
 
plt.rcParams['font.family'] = 'Arial'
 
folder_path = r"D:\LM_Master\2022ESRI\paper\python"
hotspot_file = os.path.join(folder_path, "Hotspot_scatter.csv")
non_hotspot_file = os.path.join(folder_path, "non-Hotspot_scatter.csv")
 
hotspot_df = pd.read_csv(hotspot_file)
non_hotspot_df = pd.read_csv(non_hotspot_file)
 
hotspot_df_log = np.log1p(hotspot_df)
non_hotspot_df_log = np.log1p(non_hotspot_df)
 
before_idx = [0, 1]
after_idx = [2, 3, 4]
 
hotspot_before_mean = hotspot_df_log.iloc[:, before_idx].mean(axis=1)
hotspot_after_mean = hotspot_df_log.iloc[:, after_idx].mean(axis=1)
non_hotspot_before_mean = non_hotspot_df_log.iloc[:, before_idx].mean(axis=1)
non_hotspot_after_mean = non_hotspot_df_log.iloc[:, after_idx].mean(axis=1)
 
hotspot_var = np.log1p(hotspot_df_log.var(axis=0))
non_hotspot_var = np.log1p(non_hotspot_df_log.var(axis=0))
 
# ── 配色 ──────────────────────────────────────────
SCATTER_NON  = '#7ab8d4'   # 中蓝：non-hotspot 散点
SCATTER_HOT  = '#c0392b'   # 深红：hotspot 散点
BAR_BEFORE   = '#a8d4e8'   # 浅青蓝：冲突前柱
BAR_AFTER_N  = '#7ab8d4'   # 中蓝：non-hotspot 冲突后柱
BAR_AFTER_H  = '#d46060'   # 中红粉：hotspot 冲突后柱
REFLINE      = '#444444'   # 参考线
# ─────────────────────────────────────────────────
 
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
letters = ['(a)', '(b)', '(c)', '(d)']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
axis_min, axis_max = 0, 9
 
# ── (a) non-hotspot scatter ──
axs[0, 0].scatter(non_hotspot_before_mean, non_hotspot_after_mean,
                  color=SCATTER_NON, alpha=0.7, edgecolors='white', linewidths=0.4)
axs[0, 0].plot([axis_min, axis_max], [axis_min, axis_max],
               '--', color=REFLINE, linewidth=1.8)
axs[0, 0].set_xlabel("Before conflict (log(DN))", fontsize=16)
axs[0, 0].set_ylabel("After conflict (log(DN))", fontsize=16)
axs[0, 0].set_xlim(axis_min, axis_max)
axs[0, 0].set_ylim(axis_min, axis_max)
axs[0, 0].set_box_aspect(1)
axs[0, 0].text(0.06, 0.93, letters[0], transform=axs[0, 0].transAxes,
               fontsize=16, fontweight='bold')
axs[0, 0].tick_params(axis='both', labelsize=14)
 
# ── (b) hotspot scatter ──
axs[0, 1].scatter(hotspot_before_mean, hotspot_after_mean,
                  color=SCATTER_HOT, alpha=0.75, edgecolors='white', linewidths=0.4)
axs[0, 1].plot([axis_min, axis_max], [axis_min, axis_max],
               '--', color=REFLINE, linewidth=1.8)
axs[0, 1].set_xlabel("Before conflict (log(DN))", fontsize=16)
axs[0, 1].set_ylabel("After conflict (log(DN))", fontsize=16)
axs[0, 1].set_xlim(axis_min, axis_max)
axs[0, 1].set_ylim(axis_min, axis_max)
axs[0, 1].set_box_aspect(1)
axs[0, 1].text(0.06, 0.93, letters[1], transform=axs[0, 1].transAxes,
               fontsize=16, fontweight='bold')
axs[0, 1].tick_params(axis='both', labelsize=14)
 
# ── (c) non-hotspot variance bars ──
before_vals_non = [non_hotspot_var.iloc[i] for i in before_idx]
after_vals_non  = [non_hotspot_var.iloc[i] for i in after_idx]
axs[1, 0].bar(months[:2], before_vals_non, color=BAR_BEFORE,
              edgecolor='white', linewidth=0.6, label='Before')
axs[1, 0].bar(months[2:],  after_vals_non,  color=BAR_AFTER_N,
              edgecolor='white', linewidth=0.6, label='After')
axs[1, 0].set_xlabel("Month", fontsize=16)
axs[1, 0].set_ylabel("log1p(Var)", fontsize=16)
axs[1, 0].set_ylim(0, 0.15)
axs[1, 0].legend(fontsize=12, framealpha=0.6)
axs[1, 0].set_box_aspect(1)
axs[1, 0].text(0.06, 0.93, letters[2], transform=axs[1, 0].transAxes,
               fontsize=16, fontweight='bold')
axs[1, 0].tick_params(axis='both', labelsize=14)
 
# ── (d) hotspot variance bars ──
before_vals_hot = [hotspot_var.iloc[i] for i in before_idx]
after_vals_hot  = [hotspot_var.iloc[i] for i in after_idx]
axs[1, 1].bar(months[:2], before_vals_hot, color=BAR_BEFORE,
              edgecolor='white', linewidth=0.6, label='Before')
axs[1, 1].bar(months[2:],  after_vals_hot,  color=BAR_AFTER_H,
              edgecolor='white', linewidth=0.6, label='After')
axs[1, 1].set_xlabel("Month", fontsize=16)
axs[1, 1].set_ylabel("log1p(Var)", fontsize=16)
axs[1, 1].set_ylim(0)
axs[1, 1].legend(fontsize=12, framealpha=0.6)
axs[1, 1].set_box_aspect(1)
axs[1, 1].text(0.06, 0.93, letters[3], transform=axs[1, 1].transAxes,
               fontsize=16, fontweight='bold')
axs[1, 1].tick_params(axis='both', labelsize=14)
 
plt.tight_layout(pad=1.5)
plt.subplots_adjust(left=0.07, right=0.97, top=0.95, bottom=0.08)
plt.savefig("D:\\LM_Master\\2022ESRI\\paper\\python\\scatter.jpg", dpi=300)
plt.show()