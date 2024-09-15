import x4c
import numpy as np

class RESTART:
    def __init__(self, ds, ds_h, comp, grid):
        self.ds = ds
        self.ds_h = ds_h
        self.ds.attrs['comp'] = comp
        self.ds.attrs['grid'] = grid

        # modify the coords
        if comp == 'ocn':
            ds_tmp = self.ds.rename({'i': 'nlon', 'j': 'nlat', 'k': 'z_t'})
        else:
            raise ValueError('Unknown `comp`!')
        
        ds_tmp = ds_tmp.assign_coords(self.ds_h.coords)
        self.ds = ds_tmp
        del(ds_tmp)

        for vn in self.ds.data_vars:
            self.ds[vn].attrs['comp'] = comp
            self.ds[vn].attrs['grid'] = grid
            if comp == 'ocn':
                vn_real = vn.split('_')[0]
                if vn_real in self.ds_h.data_vars:
                    # mask NaN area
                    mask = self.ds_h[vn_real].isnull().squeeze()
                    self.ds[vn].values[mask.values] = np.nan

    def __getitem__(self, vn):
        return self.ds[vn]