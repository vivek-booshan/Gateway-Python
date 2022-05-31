# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def main():
    # fileName = 'mri.raw'
    # I = Image2D(256, 176, 'uint16', fileName=fileName, order='F')
    # H = I.makeGaussMatrix([7, 7], 1, normalize=False)
    # Hnorm = I.makeGaussMatrix([7, 7], 1)
    # gaussfilt = I.gaussFilt(Hnorm)
    # bilatfilt = I.bilateralFilt(H, sigma_r=60)
    # #gaussfilt.write('mri_smooth_gauss_771.raw')
    # #bilatfilt.write('mri_smooth_bilateral_771_60.raw')
    # I.showSub(gaussfilt, 'Original Image', 'Gaussian smoothed 771')
    pass
    

class Image2D:
    def __init__(self, width, height, dType, dataArray=None, fileName=None, order='F'):
        """Initializes instances of Image2D object

        Args:
            width (int): # of cols in image matrix
            height (int): # of rows in image matrix
            dType (str): data type of image
            dataArray (np.array, optional): numpy array. Defaults to None.
            fileName (str, optional): Binary file. Defaults to None.
            order (str, optional): Determines if image is processed Fortran or C-like style. Defaults to 'F'.

        Raises:
            Exception: if class object is provided with both file name and data array
            Exception: if mismatched data array dimensions and provided width & height
            IOError: if file not found. Initializes matrix to zeroes
        """        
        self.dType = dType
        self.height = height
        self.width = width
        
        try:
            #if dataArray and file name are provided: raises error
            if type(dataArray) != type(None) and type(fileName) != type(None):
                raise Exception("Cannot provide a file name and data array at the same time!")
            #if neither provided: initializes pixels to zero matrix of image shape
            elif type(dataArray) == type(None) and type(fileName) == type(None):
                self.pixels = np.zeros((height, width), dType, order)
            #if file name provided: reads file and catches potential errors
            elif type(dataArray) == type(None) and type(fileName) != type(None):
                try:
                    self.read(fileName, order)
                except IOError as err:
                    print(err)
                    print('cannot find file or read data\nIssue with processing {fileName} file. Initializing image 2d array to all zeros')
                    self.pixels = np.zeros((height, width), dType, order)
            #if dataArray provided: tests dimensions, then initializes pixels to dataArray
            elif type(dataArray) != type(None):
                if not np.size(dataArray, 1) == width and np.size(dataArray, 0) == height:
                    raise Exception("width or height are not matching the provided data array dimensions!")
                else:
                    self.pixels = dataArray
        except Exception as err:
            print(err)

    def __repr__(self):
        """
        String representation of image2D object pixels.
        Display the first and last 10 rows.

        Returns:
            str: string representation of self.pixels
        """     
        #set # of rows   
        rows = len(self.pixels)
        #tests if self.pixels is NoneType and returns blank string
        if np.all(self.pixels) == None:
            return ''
        #first 10 rows 
        display = str(self.pixels[0:10])
        if rows > 10:
            #prints ellipses after first 10 rows
            display += '\n...\n'
            # if rows less than 20, displays remaining rows
            if rows < 20:
                display += str(self.pixels[rows - rows%10: rows])
            #else: prints last 10 rows and ignores otherwise
            else:
                display += str(self.pixels[rows - 10: rows])
        return display

    def read(self, fileName, order='F'):
        """
        Read in binary file and initialize to Image2D attribute pixels.

        Args:
            fileName (str): binary file
            order (str, optional): Determine if file should be read with Fortran or C-Like indexing. Defaults to 'F'.

        Raises:
            IOError: if program fails to find file
        """        
        try:
            with open(fileName, 'rb') as file:
                array = np.fromfile(file, self.dType)
                self.pixels = array.reshape((self.height, self.width), order=order)
        except IOError as err:
            raise err('Error: cannot find file or read data')
    
    def write(self, fileName):
        """writes Image2D attribute pixels onto new binary file of name fileName.

        Args:
            fileName (str): binary file
        """        
        try:
            with open(fileName, 'wb') as file:
                file.write(self.pixels.tobytes())
        except:
            print('An error occurred trying to write the file')
        pass
   
    def show(self, title=''):
        """Display Image2D as a grayscale pyplot

        Args:
            title (str, optional): Figure title. Defaults to ''.
        """
        #display self.pixels and set to grayscale        
        plt.imshow(self.pixels, cmap='gray')
        plt.title(title)
        plt.axis('off')
        plt.show()
        pass       
    
    def showSub(self, other, titleSelf='', titleOther=''):
        """Display two Image2D objects in a (1, 2) subplot window in grayscale

        Args:
            other (Image2D): Image2D object
            titleSelf (str, optional): title of Image2D object "self". Defaults to ''.
            titleOther (str, optional): title of Image2D object "other". Defaults to ''.
        """
        #set axes for first and second subplots
        #display self with titleSelf        
        _, (ax1, ax2) = plt.subplots(1, 2)
        ax1.set_title(titleSelf)
        ax1.imshow(self.pixels, cmap='gray')
        ax1.axis('off')
        #display other with titleOther
        ax2.set_title(titleOther)
        ax2.imshow(other.pixels, cmap='gray')
        ax2.axis('off')
        plt.show()
        pass
        
    def getWidth(self):
        """width of Image2D attribute pixels

        Returns:
            int: width
        """        
        return self.width
        pass
    def getHeight(self):
        """height of Image2D attribute pixels

        Returns:
            int: height
        """        
        return self.height
        pass
    
    def transpose(self):
        """Generates new Image2D object using transpose

        Returns:
            Image2D: Transposed Image2D object
        """        
        return Image2D(self.height, self.width, self.dType, self.pixels.T)
        
    def getDataType(self):
        """get Image2D attribute dType

        Returns:
            str: Data type of image
        """        
        return self.dType
        pass
        
    def makeGaussMatrix(self, size, sigma=1, normalize=True):
        """Create smoothing kernel using a discrete 2d Gaussian.

        Args:
            size (list): Dimension of kernel
            sigma (int, optional): spatial standard deviation. Defaults to 1.
            normalize (bool, optional): normalizes gaussian matrix. Defaults to True.

        Raises:
            ValueError: 
                if size is not list
                if size has non-integer elements
                if size has even values
                if size is not len(2)
        Returns:
            np.array: smoothing kernel
        """        
        if type(size) != list or (type(size[0]) != int or type(size[1]) != int) or (size[0]%2 == 0 or size[1]%2 == 0) or len(size) != 2:
            raise ValueError('size input argument should be  alist with 2 odd integer numbers')
        #set indices of matrix center
        s1, s2 = size[1], size[0]
        r1, r2 = (s1 - 1) // 2, (s2 - 1) // 2
        #generate row and column range for m and n
        m = np.arange(s1)
        n = np.arange(s2)[:, np.newaxis]
        #implement gaussian function and set to kernel
        kernel = np.exp(-((m-r1)**2 + (n-r2)**2)/(2*sigma**2))
        #normalize kernel by scaling all values by total sum of the kernel
        if normalize:
            return kernel/np.sum(kernel)
        else:
            return kernel

    def gaussFilt(self, H):
        """
        Performs gaussian filtering/blurring over an Image. 
        Prone to blurred edges.

        Args:
            H (np.array): normalized smoothing kernel

        Returns:
            Image2D: initializes new Image2D object with image after gaussian filtration.
        """
        #set indices of filter    
        img = self.pixels
        m, n = H.shape
        m, n = m // 2, n // 2
        #pad edges with zeros within constraints of smoothing kernel
        new = np.pad(img, ((m, m), (n,n)), constant_values=(0,0))
        #initialize filtered pixels to all zeros
        IMfiltered = np.zeros(img.shape)
        #set none edge values to img values
        new[m:new.shape[0]-m, n:new.shape[1]-n] = img
        #iterate through each pixel 
        for i in range(m, new.shape[0]-m):
            for j in range(n, new.shape[1]-n):
                #set temporary matrix using padded new of dimensions H and centered at pixel
                temp = new[i-m:i+m+1, j-n:j+n+1]
                #multiply temporary matrix with H
                result = temp*H
                #update final filtered pixel with sum of result
                IMfiltered[i - m, j - n] = result.sum()
        #convert float values back to int16
        IMfiltered = np.uint16(IMfiltered)
        return Image2D(self.width, self.height, self.dType, IMfiltered) 

    def bilateralFilt(self, H, sigma_r=100):
        """
        Performs a filtering method that calculates a new matrix based on differing intensities between neighboring pixels.
        Allows for the preservation of edges during the filter.

        Args:
            H (np.array): non normalized Gaussian matrix
            sigma_r (int, optional): Standard deviation of pixel intensities. Defaults to 100.

        Returns:
            Image2D: New class object with the bilaterally filtered image.
        """        
        #set indexs to iterate over
        img = self.pixels
        n, m = (len(H) - 1)//2, (len(H[0]) - 1)//2
        #pad new matrix with zeros
        new = np.pad(img, ((n, n), (m, m)), constant_values = (0, 0))
        #initialize filtered image of size new
        img2 = np.zeros(np.shape(new))
        #iterate over each pixel
        gaussian = lambda r2, sigma: (np.exp(-0.5*(r2/sigma)**2))
        for y in range(n, n + self.height):
            for x in range(m, m + self.width):
                #slice of padded array set to imgS (imageSlice)
                imgS = new[y-n : y+n+1, x-m : x+m+1]
                #set center of imgS
                center = imgS[n, m]
                #initalize img_pixel value to zero
                img_pixel = 0
                #initialize bilateral matrix to zero
                img_bilat = np.zeros(np.shape(imgS))
                #iterate through each pixel in imgS and calculate the offset between pixel and center
                for j, _ in enumerate(imgS):
                    for i, _ in enumerate(imgS[0]):
                        pixel, offset = imgS[j,i], 0
                        if pixel > center:
                            offset = pixel - center
                        elif pixel < center:
                            offset = center - pixel
                        #update img_bilat with respective smoothing kernel index and gaussian value of offset
                        img_bilat[j,i] = H[j,i] * gaussian(offset, sigma_r)
                #normalize img_bilat
                img_norm_bilat = img_bilat / np.sum(img_bilat)
                #iterate through each pixel in imgS and update pixel values with normalized bilateral filtering
                for j, _ in enumerate(imgS):
                    for i, _ in enumerate(imgS[0]):
                        img_pixel += (imgS[j, i] * img_norm_bilat[j, i]) 
                #update img2 with img_pixel values
                img2[y, x] = img_pixel
        #convert from float back to int16
        img2 = np.uint16(img2[n:n+self.height, m:m+self.width])
        return Image2D(self.width, self.height, self.dType, img2)
        pass


if __name__ == "__main__": 
    main()