# imports 
import matplotlib.pyplot as plt 
import numpy as np

from matplotlib.widgets import Slider


class hyperspectral_figure:

    def __init__(self, filename):
        """
        Load in hyperspectral image
        
        
        """
        with open(filename, 'rb') as file:
            self.data = np.load(file, allow_pickle = True)

        # check file
        if self.data.ndim != 3:
            print("This dataset is not a hyperspectral image, must have 3 dimensions, X, Y and frequency.")

        # make channel array
        self.chan = np.linspace(1, self.data.shape[2], self.data.shape[2])
        self.nchan = self.data.shape[2]
        self.npix = self.data.shape[0] * self.data.shape[1]

        # set rgb channels
        self.rgb = np.array([int(self.nchan * 0.1), int(self.nchan * 0.3), int(self.nchan * 0.6)])
        self.max = np.max(self.data)
        self.x = 0
        self.y = 0

        # set initial spectra
        self.spectra = None


    def _set_image(self):
        """
        Make image based on r, g, b values

        """

        self.img.set(data = np.asarray(self.data[:, :, self.rgb] / self.max * 255, dtype = 'uint8'))

        self.fig.canvas.draw()

        
        return



    def _get_pixel_spectra(self, x, y):
        """
        Get spectra of given pixel
        
        """

        self.spectra = self.data[x, y]

        return





    def plot_pixel_spectra(self, event):
        """
        Plot pixel spectra of pixel that user has clicked
        
        """

        # check if the left mouse button was pressed
        if event.button != 1:
            return

        # check if within imag axes
        if event.inaxes is None:
            return 

        if not self.ax_img.in_axes(event):
            return

        # get pixel position
        self.x = int(event.xdata)
        self.y = int(event.ydata)

        # get spectra of pixel
        self._get_pixel_spectra(self.x, self.y)

        # update spectra plot
        self._update_spec_plot()


    def _update_spec_plot(self):
        """
        Update spectra plot

        
        """

        # update spectra
        self.ax_spec.clear()
        self.ax_spec.plot(self.chan, self.spectra)
        self.ax_spec.grid(True)
        ylim = self.ax_spec.get_ylim()
        self.ax_spec.plot([self.rgb[0]]*2, ylim, 'r--')
        self.ax_spec.plot([self.rgb[1]]*2, ylim, 'g--')
        self.ax_spec.plot([self.rgb[2]]*2, ylim, 'b--')
        self.ax_spec.set_ylim(ylim)
        self.ax_spec.set_xlim([1, self.nchan])
        self.ax_spec.set_title(f"X: {self.x}, Y: {self.y}")
        self.fig.canvas.draw()
    

    def change_red_chan(self, val):
        """
        Change value of red chan
        
        """

        self.rgb[0] = int(val)

        self._set_image()
        # update spectra plot
        self._update_spec_plot()

        
    def change_green_chan(self, val):
        """
        Change value of red chan
        
        """

        self.rgb[1] = int(val)

        self._set_image()
        # update spectra plot
        self._update_spec_plot()


    def change_blue_chan(self, val):
        """
        Change value of red chan
        
        """

        self.rgb[2] = int(val)

        self._set_image()
        # update spectra plot
        self._update_spec_plot()



    def plot(self):
        """
        Plot hyperspectral image
        
        
        """

        # create figure
        self.fig = plt.figure(figsize = (10, 8))

        # add axes
        self.ax_img = self.fig.add_axes([0.05, 0.05, 0.5, 0.90])
        self.ax_img.get_xaxis().set_visible(False)
        self.ax_img.get_yaxis().set_visible(False)

        self.ax_spec = self.fig.add_axes([0.60, 0.70, 0.35, 0.25],)


        # add sliders
        self.ax_r = plt.axes([0.60, 0.50, 0.35, 0.05])
        self.slider_r = Slider(self.ax_r, valmin = 1, label = "", valmax = self.nchan, valinit=self.rgb[0],
                                valstep = 1, color = 'red', initcolor = 'k')
        self.slider_r.on_changed(self.change_red_chan)

        self.ax_g = plt.axes([0.60, 0.40, 0.35, 0.05])
        self.slider_g = Slider(self.ax_g, valmin = 1, label = "", valmax = self.nchan, valinit=self.rgb[1],
                                valstep = 1, color = 'green', initcolor = 'k')
        self.slider_g.on_changed(self.change_green_chan)

        self.ax_b = plt.axes([0.60, 0.30, 0.35, 0.05])
        self.slider_b = Slider(self.ax_b, valmin = 1, label = "", valmax = self.nchan, valinit=self.rgb[2],
                                valstep = 1, color = 'blue', initcolor = 'k')
        self.slider_b.on_changed(self.change_blue_chan)



        # PLOT!
        self.img = self.ax_img.imshow([[0]], aspect = 'auto', extent = [1, self.data.shape[0], 1, self.data.shape[1]])
        self._set_image()

        # add event callbacks
        self.fig.canvas.mpl_connect("button_press_event", self.plot_pixel_spectra)


        plt.show()







# main program
if __name__ == "__main__":

    # make class
    hsfig = hyperspectral_figure("PaviaU.npy")
    
    # plot 
    hsfig.plot()


