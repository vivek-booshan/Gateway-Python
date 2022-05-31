from PIL.Image import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.extras import mask_cols

def main():
    # array = np.fromfile('mri.raw')
    # print(np.size(array))
    data = np.random.randint(0, 10, size=(6, 6))
    fileName = 'mri.raw'
    #print(data)
    I = Image2D(256, 176, 'uint16', fileName=fileName)
    H = I.makeGaussMatrix([7, 7], 1, normalize=False)
    Hnorm = I.makeGaussMatrix([7, 7], 1)
    gaussfilt = I.gaussFilt(Hnorm)
    gauss = Image2D(256, 176, 'uint16', gaussfilt)
    bilatfilt = I.bilateralFilt(H, sigma_d=1, sigma_r=60)
    bilat = Image2D(256, 176, 'uint16', bilatfilt)
    # gauss.write('mri_smooth_gauss_771.raw')
    # bilat.write('mri_smooth_bilateral_771_60.raw')
    I.showSub(bilat, 'Original Image', 'Bilateral smoothed 771_60')

    pass
    
    
class Image2D:
    def __init__(self, height, width, dType, dataArray=None, fileName=None, order='F'):

        self.dType = dType
        self.height = height
        self.width = width
        
        # self.dataArray = np.reshape(dataArray, (height, width))
        try:
            if type(dataArray) != type(None) and type(fileName) != type(None):
                raise Exception("Cannot provide a file name and data array at the same time!")
            elif type(dataArray) == type(None) and type(fileName) == type(None):
                self.pixels = np.zeros((height, width))
            elif type(dataArray) == type(None) and type(fileName) != type(None):
                self.pixels = self.read(fileName, order)
            elif type(dataArray) != type(None):
                if not np.size(dataArray, 1) == width and np.size(dataArray, 0) == height:
                    raise Exception("width or height are not matching the provided data array dimensions!")
                self.pixels = dataArray
        except Exception as err:
            self.pixels = err
        self.dataArray = self.pixels
    
    def __repr__(self):
        return str(self.dataArray)
    
    def read(self, fileName, order='F'):
        try:
            array = np.fromfile(fileName, self.dType)
            IM2d_array = np.reshape(array, (self.width, self.height), order)
            return IM2d_array
        except:
            array = np.zeros((self.height, self.width))
            IM2d_array = np.reshape(array, (self.height, self.width), order)
            print(f'cannot find file or read data\nIssue with processing {fileName} file. Initializing image 2d array to all zeros')
            return IM2d_array            
    
    def write(self, fileName):
        try:
            file = open(fileName, 'wb')
            file.write(self.pixels.tobytes())
        except:
            print('An error occurred trying to write the file')
        pass
   
    def show(self, title=''):
        plt.imshow(self.pixels, cmap='gray')
        plt.title(title)
        plt.axis('off')
        plt.show()
        pass       
    
    def showSub(self, other, titleSelf='', titleOther=''):
        _, (ax1, ax2) = plt.subplots(1, 2)
        ax1.set_title(titleSelf)
        ax1.imshow(self.pixels, cmap='gray')
        ax1.axis('off')
        ax2.set_title(titleOther)
        ax2.imshow(other.pixels, cmap='gray')
        ax2.axis('off')
        plt.show()
        pass
        
    def getWidth(self):
        return self.width
        pass
    def getHeight(self):
        return self.height
        pass
    
    def transpose(self):
        return np.linalg.inv(self.pixels)
        pass
        
    def getDataType(self):
        return type(self.dtype)
        pass
        
    def makeGaussMatrix(self, size, sigma=1, normalize=True):
        try:
            if size[0]%2 == 0 or size[1]%2 == 0 or len(size) != 2:
                raise Exception('size input argument should be  alist with 2 odd integer numbers')
        except Exception as err:
            return err
        s1, s2 = size[0], size[1]
        r1, r2 = (s1 - 1) // 2, (s2 - 1) // 2
        ax = np.linspace(-r1, r2, s1)
        gauss = np.exp(-0.5*np.square(ax) / np.square(sigma))
        kernel = np.outer(gauss, gauss)
        if normalize == True:
            return kernel/np.sum(kernel)
        else:
            return kernel

    def gaussFilt(self, H):
        img = self.pixels
        row, col = self.width, self.height
        m, n = H.shape
        new = np.zeros((row + m - 1, col + n - 1))
        m, n = m//2, n//2
        IMfiltered = np.zeros(img.shape)
        new[m:new.shape[0]-m, n:new.shape[1]-n] = img
        for i in range(m, new.shape[0]-m):
            for j in range(n, new.shape[1]-n):
                temp = new[i-m:i+m+1, j-m:j+m+1]
                result = temp*H
                IMfiltered[i -m, j - n] = result.sum()
        return IMfiltered
    
    def bilateralFilt(self, H, sigma_d, sigma_r):
        # img = self.pixels
        # row, col = self.width, self.height
        # s1, s2 = H.shape
        # new = np.zeros((row + s1 - 1, col + s2 - 1))
        # r1, r2 = s1 // 2, s2 // 2
        # bilat = np.zeros(img.shape)
        # new[r1:new.shape[0]-r1, r2:new.shape[1]-r2] = img
        # ax = np.linspace(-r1, r2, s1)
        # thing1 = (-0.5*np.square(ax) / np.square(sigma_d))
        # thing2 = (-0.5 * np.square(np.linalg.norm(new - H))) / np.square(sigma_r)
        # bilat = np.exp(thing1 + thing2)
        # normbilat = bilat/np.sum(bilat)
        # return normbilat
        img = self.pixels
        gaussian = lambda r2, sigma: (np.exp(-0.5*r2/sigma**2)).astype(int)
        win_width = int(3*sigma_d + 1)
        wgt_sum = np.zeros(img.shape)
        result = 0
        for shft_x in range(-win_width, win_width+1):
            for shft_y in range(-win_width, win_width+1):
                w = gaussian( shft_x**2+shft_y**2, sigma_d)
                off = np.roll(img, [shft_y, shft_x], axis=[0, 1])
                tw = w*gaussian( (off-img)**2, sigma_r)
                result += off*tw
                wgt_sum += tw
        return result/wgt_sum

        pass


if __name__ == "__main__": 
    main()