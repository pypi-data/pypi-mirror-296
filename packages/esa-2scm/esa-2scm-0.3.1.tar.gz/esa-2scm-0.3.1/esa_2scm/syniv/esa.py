"""
The esa-2scm package is an implementation of the ESA-2SCM algorithm (Sanghoon Lee, 2024)
For documentation and algorithm/methodology details, please refer to my original article: http://www.snbperi.org/article/230

Should you use this package, please cite my article as follows:
- Lee, Sanghoon (2024). ESA-2SCM for Causal Discovery: Causal Modeling with Elastic Segmentation-based Synthetic Instrumental Variable, SnB Political and Economic Research Institute, 1, 21. <snbperi.org/article/230>


   Copyright 2024 Sanghoon Lee (DSsoli). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import numpy as np
import scipy.stats as ss
import warnings


class SynIV:
    
    _warning_status = False
    
    @staticmethod
    def dense_rank(x):
        z = ss.rankdata(x, method="dense")
        if len(np.unique(z))==1:
            warnings.warn("0 variance for given sample", UserWarning)
            SynIV._warning_status = True
        
        return z
    
    @staticmethod
    def minmax_scale(x):
        x_scaled = []
        for datum in x:
            datum_scaled = (datum - min(x)) / (max(x) - min(x))
            x_scaled.append(datum_scaled)
        return np.array(x_scaled)
    
    @staticmethod
    def check_concentration(x, M, data_type, tau):
        if data_type not in ['discrete', 'continuous']:
            raise ValueError("data type should be either 'discrete' or 'continuous'")
        n = len(x)
        if data_type == 'discrete':
            unique_elements, counts = np.unique(x, return_counts=True)
            max_concentration_threshold = 1 / M
            max_concentration = np.max(counts) / n
            return counts, max_concentration, max_concentration_threshold, max_concentration <= (max_concentration_threshold + tau)
        elif data_type == 'continuous':
            x_scaled = SynIV.minmax_scale(x)
            T = 1 / M
            C_v_list = []
            for i in range(M):
                C_v = len([x for x in x_scaled if x >= i * T and x < (i+1) * T])
                if i == M-1:
                    C_v = len([x for x in x_scaled if x >= i * T and x <= 1])
                C_v_list.append(C_v)
            max_concentration = np.max(C_v_list) / n
            return C_v_list, max_concentration, T, max_concentration <= (T + tau)
        
    @staticmethod
    def esa(x, M=2, data_type='continuous', tau=0):
        n = len(x)
        idx_sorted = np.argsort(x)
        original_M = M
                
        if M < 2: raise ValueError("Minimum number of segments (M) must be a positive integer greater than or equal to 2")

        fixed_thres = 1/M
        while M >= 2:
            if n % M != 0:
                M -= 1
            _, max_concent, max_concent_threshold, threshold_check = SynIV.check_concentration(x=x, M=M, data_type=data_type, tau=tau)
            if threshold_check:
                break
            M -= 1
        
        if M < 2:
            warnings.warn(f"""
                            Data is excessively concentrated on a single segment to perform meaningful ESA. Using Dense Rank method instead. This may indicate bias in the dataset.
                            Consider either checking data imbalance or increasing the regularization term tau.
                            (Single segment under post-optimization accounts for {max_concent*100:.2f}% of the total dataset while single segment threshold for M={original_M} is fixed at {fixed_thres*100:.2f}%).
                            """, UserWarning)
            return SynIV.dense_rank(x)
        
        if M != original_M:
            warnings.warn(f"""
                            Data is excessively concentrated on a single segment to perform meaningful ESA. Using M={M} instead of M={original_M}.
                            Consider either checking data imbalance or increasing the regularization term tau.
                            (Single segment under post-optimization accounts for {max_concent*100:.2f}% of the total dataset while single segment threshold for M={original_M} is fixed at {fixed_thres*100:.2f}%).
                            """, UserWarning)

        segment_sizes = [n // M + (1 if i < n % M else 0) for i in range(M)]
        boundaries = np.cumsum(segment_sizes)
        z = np.zeros(n, dtype=int)  
        
        start_idx = 0
        for assign_segment_value, boundary in enumerate(boundaries, start=1):
            segment_indices = idx_sorted[start_idx:boundary]
            z[segment_indices] = assign_segment_value
            start_idx = boundary
        
        return z
    
    
    @staticmethod
    def m_split(x, strategy: str = 'auto'):
        strategies = ['auto', 'median', 'mean']
        if strategy not in strategies: raise ValueError(f"Invalid strategy name '{strategy}'")
        
        mean_val, med_val = np.mean(x), np.median(x)
        
        def auto_strategy():
            if med_val != np.max(x):
                z = np.array([1 if i > med_val else -1 for i in x])
                if len(np.unique(z))==1:
                    z = np.array([1 if i > mean_val else -1 for i in x])
                    if len(np.unique(z))==1:
                        z = SynIV.dense_rank(x)
                        
            else: z = SynIV.dense_rank(x)
            return z
        
        def median_strategy():
            return np.array([1 if i > med_val else -1 for i in x])
        
        def mean_strategy():
            return np.array([1 if i > mean_val else -1 for i in x])
        
        strategy_funcs = {
            'auto': auto_strategy,
            'median': median_strategy,
            'mean': mean_strategy
        }
        
        z = strategy_funcs[strategy]()
        
        if len(np.unique(z))==1 and not SynIV._warning_status:
            warnings.warn("0 variance for given sample", UserWarning)
            SynIV._warning_status = True
            
        return z
    
    
    @staticmethod
    def get_syniv(method="esa"):
        syniv_map = {
            "esa": SynIV.esa,
            "dense_rank": SynIV.dense_rank,
            "m_split": SynIV.m_split
        }
        
        try:
            return syniv_map[method]
        except:
            raise ValueError(f"Invalid method name '{method}'")


def r2_score(y_true, y_pred):
    r2 = 1 - np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2)
    return r2
