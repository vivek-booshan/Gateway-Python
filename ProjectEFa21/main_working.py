# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def main():
    fileName = 'mri.raw'
    I = Image2D(256, 176, 'uint16', fileName=fileName, order='F')
    H = I.makeGaussMatrix([7, 7], 1, normalize=False)
    Hnorm = I.makeGaussMatrix([7, 7], 1)
    gaussfilt = I.gaussFilt(Hnorm)
    bilatfilt = I.bilateralFilt(H, sigma_r=60)
    #gaussfilt.write('mri_smooth_gauss_771.raw')
    #bilatfilt.write('mri_smooth_bilateral_771_60.raw')
    I.showSub(gaussfilt, 'Original Image', 'Gaussian smoothed 771')
    pass
    

class Image2D:
    def __init__(self, width, height, dType, dataArray=None, fileName=None, order='F'):

        self.dType = dType
        self.height = height
        self.width = width
        
        # self.dataArray = np.reshape(dataArray, (height, width))
        try:
            if type(dataArray) != type(None) and type(fileName) != type(None):
                raise Exception("Cannot provide a file name and data array at the same time!")
            elif type(dataArray) == type(None) and type(fileName) == type(None):
                self.pixels = np.zeros((height, width), dType, order)
            elif type(dataArray) == type(None) and type(fileName) != type(None):
                try:
                    self.read(fileName, order)
                except IOError as err:
                    print(err)
                    print('cannot find file or read data\nIssue with processing {fileName} file. Initializing image 2d array to all zeros')
                    self.pixels = np.zeros((height, width), dType, order)
            elif type(dataArray) != type(None):
                if not np.size(dataArray, 1) == width and np.size(dataArray, 0) == height:
                    raise Exception("width or height are not matching the provided data array dimensions!")
                else:
                    self.pixels = dataArray
        except Exception as err:
            print(err)

    def __repr__(self):
        rows = len(self.pixels)
        if np.all(self.pixels) == None:
            return ''
        display = str(self.pixels[0:10])
        if rows > 10:
            display += '\n...\n'
            if rows < 20:
                display += str(self.pixels[rows - rows%10: rows])
            else:
                display += str(self.pixels[rows - 10: rows])
        return display

    def read(self, fileName, order='F'):
        try:
            with open(fileName, 'rb') as file:
                array = np.fromfile(file, self.dType)
                self.pixels = array.reshape((self.height, self.width), order=order)
                #return self.pixels
        except IOError as err:
            raise err('Error: cannot find file or read data')
    
    def write(self, fileName):
        try:
            with open(fileName, 'wb') as file:
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
        return Image2D(self.height, self.width, self.dType, self.pixels.T)
    def getTranspose(self):
        return Image2D(self.height, self.width, self.dType, self.pixels.T)
        pass
        
    def getDataType(self):
        return self.dType
        pass
        
    def makeGaussMatrix(self, size, sigma=1, normalize=True):
        if (size[0]%2 == 0 or size[1]%2 == 0) or len(size) != 2:
            raise ValueError('size input argument should be  alist with 2 odd integer numbers')
        s1, s2 = size[1], size[0]
        r1, r2 = (s1 - 1) // 2, (s2 - 1) // 2
        m = np.arange(s1)
        n = np.arange(s2)[:, np.newaxis]
        kernel = np.exp(-((m-r1)**2 + (n-r2)**2)/(2*sigma**2))

        if normalize:
            return kernel/np.sum(kernel)
        else:
            return kernel

    def gaussFilt(self, H):
        img = self.pixels
        m, n = H.shape
        m, n = m // 2, n // 2
        new = np.pad(img, ((m, m), (n,n)), constant_values=(0,0))
        IMfiltered = np.zeros(img.shape)
        new[m:new.shape[0]-m, n:new.shape[1]-n] = img
        for i in range(m, new.shape[0]-m):
            for j in range(n, new.shape[1]-n):
                temp = new[i-m:i+m+1, j-n:j+n+1]
                result = temp*H
                IMfiltered[i - m, j - n] = result.sum()
        #return IMfiltered.T
        IMfiltered = np.uint16(IMfiltered)
        return Image2D(self.width, self.height, self.dType, IMfiltered) 
    
    # def bilateralFilt(self, H, sigma_r=60, sigma_d=1):
    #     # img = self.pixels
    #     # row, col = self.width, self.height
    #     # s1, s2 = H.shape
    #     # new = np.zeros((row + s1 - 1, col + s2 - 1))
    #     # r1, r2 = s1 // 2, s2 // 2
    #     # bilat = np.zeros(img.shape)
    #     # new[r1:new.shape[0]-r1, r2:new.shape[1]-r2] = img
    #     # ax = np.linspace(-r1, r2, s1)
    #     # thing1 = (-0.5*np.square(ax) / np.square(sigma_d))
    #     # thing2 = (-0.5 * np.square(np.linalg.norm(new - H))) / np.square(sigma_r)
    #     # bilat = np.exp(thing1 + thing2)
    #     # normbilat = bilat/np.sum(bilat)
    # #     # return normbilat
    #     img = self.pixels
    #     gaussian = lambda r2, sigma: (np.exp(-0.5*r2/sigma**2)).astype(int)
    #     win_width = int(3*sigma_d + 1)
    #     wgt_sum = np.zeros(img.shape)
    #     result = 0
    #     for shft_x in range(-win_width, win_width+1):
    #         for shft_y in range(-win_width, win_width+1):
    #             w = gaussian( shft_x**2+shft_y**2, sigma_d)
    #             off = np.roll(img, [shft_y, shft_x], axis=[0, 1])
    #             tw = w*gaussian( (off-img)**2, sigma_r)
    #             result += off*tw
    #             wgt_sum += tw
    #     bilatfilt = np.uint16(result/wgt_sum)
    #     return Image2D(self.width, self.height, self.dType, bilatfilt)

    @staticmethod
    def get_slice(img, x, y, kernel_size):
        half = kernel_size // 2
        return img[x - half: x + half + 1, y - half : y + half + 1]

    def bilateralFilt(self, H, sigma_r=60):
        # img = self.pixels
        # m, n = H.shape
        # m, n = m//2, n//2
        # img2 = np.zeros(img.shape, self.dType)
        # new = np.pad(img, ((m, m), (n, n)), constant_values = (0, 0))

        # #gaussian = lambda r2, sigma: (1/(sigma*math.sqrt(2*math.pi)))*(np.exp(-0.5*(r2/sigma)**2)).astype(int)
        # sizex, sizey = self.width, self.height
        # print(sizex, sizey)
        # for j in range(n, new.shape[1] - n):
        #     for i in range(m, new.shape[0] - m):
        #         if i < sizex or j < sizey:
        #             imgS = new[j - m: j + m + 1, i - n : i + n + 1]
        #             imgI = imgS - imgS[m, n]
        #             imgIG = self.makeGaussMatrix(imgI.shape, sigma=sigma_r, normalize=False)
        #             #imgIG = gaussian(imgI, sigma_r)
        #             weights = np.multiply(H, imgIG)
        #             vals = np.multiply(imgS, weights)
        #             val = np.sum(vals) / np.sum(weights)
        #             img2[i, j] = val
        #         else:
        #             continue
        # return Image2D(self.width, self.height, self.dType, np.uint16(img2)) 
        img = self.pixels
        n = (len(H) - 1)//2
        m = (len(H[0]) - 1)//2
        new = np.pad(img, ((n, n), (m, m)), constant_values = (0, 0))
        img2 = np.empty(np.shape(new))
        for y in range(n, n + self.height):
            for x in range(m, m + self.width):
                imgS = new[y-n : y+n+1, x-m : x+m+1]
                center = imgS[n, m]
                img_pixel = 0
                img_bilat = np.empty(np.shape(imgS))
                for j, _ in enumerate(imgS):
                    for i, _ in enumerate(imgS[0]):
                        pixel = imgS[j,i]
                        offset = 0
                        if pixel > center:
                            offset = pixel - center
                        elif pixel < center:
                            offset = center - pixel
                        img_bilat[j,i] = H[j,i] * np.e ** (-0.5 * (offset/sigma_r) ** 2)
                img_norm_bilat = img_bilat / np.sum(img_bilat)
                for j, _ in enumerate(imgS):
                    for i, _ in enumerate(imgS[0]):
                        img_pixel += (imgS[j][i] * img_norm_bilat[j][i]) 
                img2[y][x] = img_pixel
        img2 = np.uint16(img2)
        return Image2D(self.width, self.height, self.dType, img2[n:n + self.height, m:m + self.width])
        pass


if __name__ == "__main__": 
    main()