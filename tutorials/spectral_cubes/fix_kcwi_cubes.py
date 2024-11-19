'''
Lydia Haacke
08/2023
'''
import glob
import os
import sys
import math
import re
import numpy as np
from astropy.io import fits
from MontagePy.main import *


class Manipulate_icubes:
    def __init__(self, cube_path, cube_dict):
        self.cube_path = cube_path
        self.cut_cubes_path = ''.join([self.cube_path, 'icubes_cut_1'])
        
        self.data_gradient_corrected_path = ''.join([self.cube_path, 'icubes_gradient_corrected_data_2'])
        self.var_gradient_corrected_path = ''.join([self.cube_path, 'icubes_gradient_corrected_var_2'])
        self.gradient_corrected_path = ''.join([self.cube_path, 'icubes_gradient_corrected_2'])
        
        self.data_wcs_corrected_path = ''.join([self.cube_path, 'icubes_wcs_corrected_data_3'])
        self.var_wcs_corrected_path = ''.join([self.cube_path, 'icubes_wcs_corrected_var_3'])
        self.wcs_corrected_path = ''.join([self.cube_path, 'icubes_wcs_corrected_3'])
        
        self.data_rebinned_path = ''.join([self.cube_path, 'icubes_rebinned_data_4'])
        self.var_rebinned_path = ''.join([self.cube_path, 'icubes_rebinned_var_4'])
        self.rebinned_path = ''.join([self.cube_path, 'icubes_rebinned_4'])
        
        self.cube_dict = cube_dict
        
        self.reference_header = None


    def cut_cubes(self):
        '''
        Cuts overhang pixels and bad wavelengths off of cubes
        cube_path: path to cubes that need to be cut
        cube_dict: dictionary with info on cubes (pixels to be included)
        '''
        # check if the directory for the cut cubes is there
        # make cut cube directory if it is not
        if not os.path.exists(self.cut_cubes_path):
            os.mkdir(self.cut_cubes_path)
            
        # cut the cubes and save the cut cube into the cut cube directory 
        cubes = glob.glob(''.join([self.cube_path, '*icubes.fits']))
        for cube in cubes:
            key = self.get_key(cube)
            with fits.open(cube) as hdu:
                data = hdu[0].data
                data_header = hdu[0].header
                var = hdu[2].data
                var_header = hdu[2].header
                
            # cut data and variance cube
            cut_cube = data[self.cube_dict[key]['z_border'][0]-1:self.cube_dict[key]['z_border'][1],
                            self.cube_dict[key]['y_border'][0]-1:self.cube_dict[key]['y_border'][1],
                            self.cube_dict[key]['x_border'][0]-1:self.cube_dict[key]['x_border'][1]]
            cut_cube_variance = var[self.cube_dict[key]['z_border'][0]-1:self.cube_dict[key]['z_border'][1],
                                    self.cube_dict[key]['y_border'][0]-1:self.cube_dict[key]['y_border'][1],
                                    self.cube_dict[key]['x_border'][0]-1:self.cube_dict[key]['x_border'][1]]

            # correct header keywords
            data_header['NAXIS1'] = data.shape[0]
            data_header['NAXIS2'] = data.shape[1]
            data_header['NAXIS3'] = data.shape[2]
            data_header['CRPIX3'] -= (self.cube_dict[key]['z_border'][0]-1)
            data_header['WAVALL0'] = self.cube_dict[key]['WAVALL0']
            data_header['WAVALL1'] = self.cube_dict[key]['WAVALL1']
            
            var_header['NAXIS1'] = var.shape[0]
            var_header['NAXIS2'] = var.shape[1]
            var_header['NAXIS3'] = var.shape[2]

            # save cubes to new directory
            cut_cube_hdu = fits.PrimaryHDU(cut_cube, data_header)
            cut_cube_vdu = fits.ImageHDU(cut_cube_variance, var_header)
            cut_cube_hdul = fits.HDUList([cut_cube_hdu, cut_cube_vdu])
            cut_cube_hdul.writeto(''.join([self.cut_cubes_path, '/', key, '_icubes_cut.fits']), overwrite=True)
        
        return 0


    def compare_central_wavelengths(self, cut_suff='/*icubes_cut.fits'):
        '''
        checks if all the central wavelengths are the same
        cubes are saved as their exising name (without file extension) with cut_suff appended
        '''
        # get all the cubes in gradient corrected folder  
        cubes = glob.glob(''.join([self.cut_cubes_path, cut_suff]))
        
        # get the central wavelength of one cube as reference
        with fits.open(cubes[0]) as hdu:
            crval = hdu[0].header['CRVAL3']
            crpix = hdu[0].header['CRPIX3']
        
        # compare the central wavelengths for each file, change if slightly different
        for cube in cubes:
            key = self.get_key(cube)
            with fits.open(cube, 'update') as hdu:
                h1 = hdu[0].header
                if h1['CRVAL3'] == crval:
                    continue
                elif (h1['CRVAL3'] > (crval+1)) or (h1['CRVAL3'] < (crval-1)):
                    sys.exit('Difference in central wavelengths too big')
                else:
                    hdu[0].header['CRVAL3'] = crval
                    hdu[0].header['CRPIX3'] = crpix
        return 0


    def add_var_wcs_header(self, var_header, data_header, key):
        '''
        adds necessary keywords to variance cube header to 'have' a wcs and be rebinned according to it
        
        var_header: header of variance cube
        data_header: header of corresponding data cube
        key: kbyymmdd_xxxxx style name of the exposure
        '''
        # add necessary keywords to variance cube to 'add' a wcs
        var_header['CRPIX1'] = self.cube_dict[key]['xpix']
        var_header['CRPIX2'] = self.cube_dict[key]['ypix']
        var_header['CRPIX3'] = data_header['CRPIX3']
        var_header['CRVAL1'] = self.cube_dict[key]['xval']
        var_header['CRVAL2'] = self.cube_dict[key]['yval']
        var_header['CRVAL3'] = data_header['CRVAL3']
        var_header['CUNIT1'] = data_header['CUNIT1']
        var_header['CUNIT2'] = data_header['CUNIT2']
        var_header['CUNIT3'] = data_header['CUNIT3']
        var_header['CTYPE1'] = data_header['CTYPE1']
        var_header['CTYPE2'] = data_header['CTYPE2']
        var_header['CTYPE3'] = data_header['CTYPE3']
        var_header['CD1_1'] = data_header['CD1_1']
        var_header['CD2_1'] = data_header['CD2_1']
        var_header['CD1_2'] = data_header['CD1_2']
        var_header['CD2_2'] = data_header['CD2_2']
        var_header['CD3_3'] = data_header['CD3_3']
        var_header['BUNIT'] = data_header['BUNIT']
        var_header['WCSDIM'] = data_header['WCSDIM']
        var_header['WCSNAME'] = data_header['WCSNAME']
        var_header['RADESYS'] = data_header['RADESYS']
        var_header['SLSCL'] = data_header['SLSCL']
        var_header['PXSCL'] = data_header['PXSCL']
        var_header['WAVALL0'] = self.cube_dict[key]['WAVALL0']
        var_header['WAVALL1'] = self.cube_dict[key]['WAVALL1']
        var_header['WAVGOOD0'] = data_header['WAVGOOD0']
        var_header['WAVGOOD1'] = data_header['WAVGOOD1']
        
        return var_header


    def gradient_correction(self, cut_suff='/*icubes_cut.fits'):
        '''
        cut_cube_path: path where to find the cut icubes that need to be corrected
        '''
        # check if gradient_corrected path exists or not
        if not os.path.exists(self.data_gradient_corrected_path):
            os.mkdir(self.data_gradient_corrected_path)
        if not os.path.exists(self.var_gradient_corrected_path):
            os.mkdir(self.var_gradient_corrected_path)

        # correct the gradient along the x_axis
        cubes = glob.glob(''.join([self.cut_cubes_path, cut_suff]))
        for cube in cubes:
            key = self.get_key(cube)
            with fits.open(cube) as hdu:
                data = hdu[0].data
                data_header = hdu[0].header
                data_med = np.median(data, axis=1)
                var = hdu[1].data
                var_header = hdu[1].header
            for yind in range(data_header['NAXIS2']):
                data[:, yind, :] = data[:, yind, :]/data_med # data cube
                var[:, yind, :] = var[:, yind, :]/data_med # variance cube
                
            var_header_wcs = self.add_var_wcs_header(var_header, data_header, key)

            # save cubes to new directory
            cube_hdu = fits.PrimaryHDU(data, data_header)
            cube_vdu = fits.PrimaryHDU(var, var_header_wcs)
            cube_hdu.writeto(''.join([self.data_gradient_corrected_path, '/', key, '_gradient_corrected.fits']), overwrite=True)
            cube_vdu.writeto(''.join([self.var_gradient_corrected_path, '/', key, '_gradient_corrected.fits']), overwrite=True)
            
        # join cubes
        self.join_cubes(self.data_gradient_corrected_path, self.var_gradient_corrected_path,
                        self.gradient_corrected_path, '/*gradient_corrected.fits')
            
        return 0

    
    def join_cubes(self, data_path, var_path, joint_path, cut_suff):
        '''
        joins data and variance cube after rebinning
        takes cubes from self.data_rebinned_path and self.var_rebinned_path
        '''
        # check if joint path exists
        if not os.path.exists(joint_path):
            os.mkdir(joint_path)
        
        # data and var cubes have the exact same name
        # gobble and sort both groups results in two matching list where index matches index
        data_cubes = np.sort(glob.glob(''.join([data_path, cut_suff])))
        var_cubes = np.sort(glob.glob(''.join([var_path, cut_suff])))
        for data_cube, var_cube in zip(data_cubes, var_cubes):
            with fits.open(data_cube) as hdu:
                data = hdu[0].data
                data_header = hdu[0].header
            with fits.open(var_cube) as hdu:
                var = hdu[0].data
                var_header = hdu[0].header
        
            # find key using regex
            data_key, var_key = self.get_key(data_cube), self.get_key(var_cube)
        
            # save cubes to new directory in joint format
            cube_hdu = fits.PrimaryHDU(data, data_header)
            cube_vdu = fits.ImageHDU(var, var_header)
            cube_hdul = fits.HDUList([cube_hdu, cube_vdu])
            cube_hdul.writeto(''.join([joint_path, '/', data_key, '_rebinned_joint.fits']), overwrite=True)  
        
        return 0


    def get_area_ratio(self, file, header=True):
        '''
        calculate the area ratio of data cube pixels
        file: path to one of the fits files
        header: whether or not to return the header of the fits file
        '''
        with fits.open(file) as hdu:
            h1 = hdu[0].header
            ratio = h1['SLSCL']/h1['PXSCL']
        if header:
            return ratio, h1
        else:
            return ratio


    def fix_rebinned_hdr(self, cube, hdr0):
        '''
        add necessary keywords to stacked cubes' header
        (heavily based on Nikki Nielsen's function)

        cube: cube where keywords need to be added to the header
        hdr0: header of an original cube containing the keywords
        '''
        with fits.open(cube, 'update') as hdr1:
            hdr1[0].header['WAVALL0'] = hdr0['WAVALL0']
            hdr1[0].header['WAVALL1'] = hdr0['WAVALL1']
            hdr1[0].header['WAVGOOD0'] = hdr0['WAVGOOD0']
            hdr1[0].header['WAVGOOD1'] = hdr0['WAVGOOD1']
            hdr1[0].header['CRVAL3'] = hdr0['CRVAL3']
            hdr1[0].header['CRPIX3'] = hdr0['CRPIX3']
            hdr1[0].header['CUNIT3'] = hdr0['CUNIT3']
            hdr1[0].header['CTYPE3'] = hdr0['CTYPE3']
            hdr1[0].header['CDELT3'] = hdr0['CD3_3']
            hdr1[0].header['BUNIT'] = hdr0['BUNIT']
            hdr1[0].header['WCSDIM'] = hdr0['WCSDIM']
            hdr1[0].header['WCSNAME'] = hdr0['WCSNAME']
            hdr1[0].header['RADESYS'] = hdr0['RADESYS']

        return 0


    def wcs_correction(self, cut_suff='/*gradient_corrected.fits'):
        '''
        corrects the wcs system according to the pixel values in self.cube_dict
        '''
        # check data, var_wcs_corrected directories exist
        # make them if not
        if not os.path.exists(self.data_wcs_corrected_path):
            os.mkdir(self.data_wcs_corrected_path)
        if not os.path.exists(self.var_wcs_corrected_path):
            os.mkdir(self.var_wcs_corrected_path)
            
        # correct the wcs according to the values in self.cube_dict   
        data_cubes = np.sort(glob.glob(''.join([self.data_gradient_corrected_path, cut_suff])))
        var_cubes = np.sort(glob.glob(''.join([self.var_gradient_corrected_path, cut_suff])))
        for data_cube, var_cube in zip(data_cubes, var_cubes):
            data_key, var_key = self.get_key(data_cube), self.get_key(var_cube)
            if data_key != var_key:
                sys.exit('Keys must be the same.')
            with fits.open(data_cube) as hdu:
                data = hdu[0].data
                data_header = hdu[0].header
            with fits.open(var_cube) as hdu:
                var = hdu[0].data
                var_header = hdu[0].header
            
            # save cubes to new directory
            wcs_cube_hdu = fits.PrimaryHDU(data, data_header)
            wcs_cube_vdu = fits.PrimaryHDU(var, var_header)
            wcs_cube_hdu.writeto(''.join([self.data_wcs_corrected_path, '/', data_key, '_wcs_corrected.fits']), overwrite=True)
            wcs_cube_vdu.writeto(''.join([self.var_wcs_corrected_path, '/', var_key, '_wcs_corrected.fits']), overwrite=True)
            
            with fits.open(''.join([self.data_wcs_corrected_path, '/', data_key, '_wcs_corrected.fits']), 'update') as hdu:
                data = hdu[0].data
                data_header = hdu[0].header
                # change the header values in data cube to correct wcs reference
                data_header['CRPIX1'] = self.cube_dict[data_key]['xpix']
                data_header['CRPIX2'] = self.cube_dict[data_key]['ypix']
                data_header['CRVAL1'] = self.cube_dict[data_key]['xval']
                data_header['CRVAL2'] = self.cube_dict[data_key]['yval']
                
            with fits.open(''.join([self.var_wcs_corrected_path, '/', var_key, '_wcs_corrected.fits']), 'update') as hdu:
                var = hdu[0].data
                var_header = hdu[0].header
                # change the header values in variance cube to correct wcs reference
                var_header['CRPIX1'] = self.cube_dict[var_key]['xpix']
                var_header['CRPIX2'] = self.cube_dict[var_key]['ypix']
                var_header['CRVAL1'] = self.cube_dict[var_key]['xval']
                var_header['CRVAL2'] = self.cube_dict[var_key]['yval']
            
            
        # join cubes
        self.join_cubes(self.data_wcs_corrected_path, self.var_wcs_corrected_path,
                        self.wcs_corrected_path, '/*wcs_corrected.fits')

        return 0


    def rebin_cubes(self, header=True, cut_suff='/*wcs_corrected.fits'):
        '''
        rebin the cubes from rectangular to square pixels

        header: whether or not to return the header from get_area_ratio
        '''
        # check if the directories for rebinned cubes exist
        # make if they don't
        if not os.path.exists(self.data_rebinned_path):
            os.mkdir(self.data_rebinned_path)
        if not os.path.exists(self.var_rebinned_path):
            os.mkdir(self.var_rebinned_path)
            
        # Montage pre-processing for data and var separately
        imlist_data = mImgtbl(self.data_wcs_corrected_path, ''.join([self.data_rebinned_path, '/icubes.tbl']), showCorners=True)
        print(imlist_data)
        imlist_var = mImgtbl(self.var_wcs_corrected_path, ''.join([self.var_rebinned_path, '/icubes.tbl']), showCorners=True)
        print(imlist_var)

        # use mMakeHdr
        hdr_temp_data = mMakeHdr(''.join([self.data_rebinned_path, '/icubes.tbl']), ''.join([self.data_rebinned_path, '/icubes.hdr']))
        print(hdr_temp_data)
        hdr_temp_var = mMakeHdr(''.join([self.var_rebinned_path, '/icubes.tbl']), ''.join([self.var_rebinned_path, '/icubes.hdr']))
        print(hdr_temp_var)

        # rebin cubes
        data_cubes = np.sort(glob.glob(''.join([self.data_wcs_corrected_path, cut_suff])))
        var_cubes = np.sort(glob.glob(''.join([self.var_wcs_corrected_path, cut_suff])))
        
        # get arearatio and header data
        if header:
            arearatio_data, orig_header_data = self.get_area_ratio(data_cubes[0], header=True)
            arearatio_var, orig_header_var = self.get_area_ratio(var_cubes[0], header=True)
        else:
            arearatio_data = self.get_area_ratio(data_cubes[0])
            arearatio_var = self.get_area_ratio(var_cubes[0])
        for data_cube, var_cube in zip(data_cubes, var_cubes):
            data_key, var_key = self.get_key(data_cube), self.get_key(var_cube)
            if data_key != var_key:
                sys.exit('Matching data cube to wrong variance cube.')
            # reproject data cube
            rep_cube_data = mProjectCube(data_cube,
                                    ''.join([self.data_rebinned_path, '/', data_key, '_reproj.fits']),
                                    ''.join([self.data_rebinned_path, '/icubes.hdr']),
                                    drizzle=1.0, energyMode=False, fluxScale=arearatio_data)
            # reproject variance cube
            rep_cube_var = mProjectCube(var_cube,
                                    ''.join([self.var_rebinned_path, '/', var_key, '_reproj.fits']),
                                    ''.join([self.var_rebinned_path, '/icubes.hdr']),
                                    drizzle=1.0, energyMode=False, fluxScale=arearatio_var)                        
            if header:
                self.fix_rebinned_hdr(''.join([self.data_rebinned_path, '/', data_key, '_reproj.fits']), orig_header_data)
                self.fix_rebinned_hdr(''.join([self.var_rebinned_path, '/', var_key, '_reproj.fits']), orig_header_var)

            print(rep_cube_data)
            print(rep_cube_var)

        # fix the header of rebinned cubes

        return 0


        # join cubes
        self.join_cubes(self.data_rebinned_path, self.var_rebinned_path,
                        self.rebinned_path, '/*reproj.fits')

        return 0


    def stack_cubes(self, stacked_cubes_name):
        '''
        stacks all rebinned cubes in self.rebinned_cubes_path

        stacked_cubes_name: filename of the stacked cubes fits file (e.g. 'stacked.fits')
        '''
        # create image metadata table for reprojected data cubes
        im_meta_data = mImgtbl(self.data_rebinned_path,
                        ''.join([self.data_rebinned_path, '/icubes-proj.tbl']), showCorners=True)
        print(im_meta_data)
        # create image metadata table for reprojected variance cubes
        im_meta_var = mImgtbl(self.var_rebinned_path,
                        ''.join([self.var_rebinned_path, '/icubes-proj.tbl']), showCorners=True)
        print(im_meta_var)
        
        # actually add reprojected data cubes
        added_cubes_data = mAddCube(''.join([self.data_rebinned_path, '/']),
                            ''.join([self.data_rebinned_path, '/icubes-proj.tbl']),
                            ''.join([self.data_rebinned_path, '/icubes.hdr']),
                            ''.join([self.cube_path, 'data_', stacked_cubes_name]),
                            shrink=True)
        print(added_cubes_data)
        added_cubes_var = mAddCube(''.join([self.var_rebinned_path, '/']),
                            ''.join([self.var_rebinned_path, '/icubes-proj.tbl']),
                            ''.join([self.var_rebinned_path, '/icubes.hdr']),
                            ''.join([self.cube_path, 'var_', stacked_cubes_name]),
                            shrink=True)
        print(added_cubes_var)


        # update stacked data cube hdr
        orig_headers = glob.glob(''.join([self.data_wcs_corrected_path, '/*.fits'])) # get header with original axis data
        with fits.open(orig_headers[0]) as hdu:
            h1_stacked_template = hdu[0].header
        self.fix_stacked_hdr(''.join([self.cube_path, 'var_', stacked_cubes_name]), h1_stacked_template)
        self.fix_stacked_hdr(''.join([self.cube_path, 'data_', stacked_cubes_name]), h1_stacked_template)

        # join cubes
        # self.join_cubes(''.join([self.cube_path, 'data_', stacked_cubes_name]), ''.join([self.cube_path, 'var_', stacked_cubes_name]),
        #                 self.cube_path, stacked_cubes_name)

        return 0


    def fix_stacked_hdr(self, cube, hdr0):
        '''
        add all necessary keywords to header of stacked cube
        '''
        with fits.open(cube, 'update') as hdr1:
            hdr1[0].header['CUNIT3'] = hdr0['CUNIT3']
            hdr1[0].header['CTYPE3'] = hdr0['CTYPE3']
            hdr1[0].header['WAVALL0'] = hdr0['WAVALL0']
            hdr1[0].header['WAVALL1'] = hdr0['WAVALL1']
            hdr1[0].header['CDELT3'] = hdr0['CD3_3']
            hdr1[0].header['WAVGOOD0'] = hdr0['WAVGOOD0']
            hdr1[0].header['WAVGOOD1'] = hdr0['WAVGOOD1']
            hdr1[0].header['BUNIT'] = hdr0['BUNIT']

        return 0


    def get_key(self, cube):
        '''
        get the kbyymmdd_xxxxx string out of a file path
        
        cube: filepath to a certain data cube
        '''
        num = re.findall(r'[0-9]+_[0-9]+', cube)
        key = ''.join(['kb', num[0]])
        
        return key

        