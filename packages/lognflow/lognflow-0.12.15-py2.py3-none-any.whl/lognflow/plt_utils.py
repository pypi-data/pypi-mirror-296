import numpy as np
from   functools import partial
import matplotlib.pyplot as plt
import matplotlib.gridspec
from   matplotlib.colors import hsv_to_rgb
from   matplotlib.widgets import RangeSlider, TextBox, Button
from   mpl_toolkits.mplot3d import Axes3D
from   mpl_toolkits.axes_grid1 import make_axes_locatable
from   scipy.spatial.transform import Rotation as scipy_rotation
from   .printprogress import printprogress
from   itertools import cycle as itertools_cycle

matplotlib_lines_Line2D_markers_keys_cycle = itertools_cycle([
    's', '*', 'd', 'X', 'v', '.', 'x', '|', 'D', '<','^',  '8','p',  
    '_','P','o','h', 'H', '>', '1', '2','3', '4',  '+', 'x', ])

def complex2hsv(data_complex, vmin=None, vmax=None):
    """ complex2hsv
        Routine to visualise complex array as 2D image with color conveying
        phase information
        data_complex must be a complex 2d image
    """
    sx, sy = data_complex.shape

    data_abs = np.abs(data_complex)
    if vmin is None: vmin = data_abs.min()
    if vmax is None: vmax = data_abs.max()
    sat = (data_abs - vmin) / (vmax - vmin)
    data_angle = np.angle(data_complex) % (2 * np.pi)
    hue = data_angle / (2 * np.pi)
    a, b = np.divmod(hue, 1.0)

    H = np.zeros((sx, sy, 3))
    H[:, :, 0] = b
    H[:, :, 1] = np.ones([sx, sy])
    H[:, :, 2] = sat

    return hsv_to_rgb(H), data_abs, data_angle

def plt_hist2(data, bins=30, cmap='viridis', 
              xlabel=None, ylabel=None, zlabel=None, title=None, 
              colorbar=True, fig_ax=None, colorbar_label=None):
    """
    Plot a 3D histogram with a cmap based on the height of the bars.

    Parameters:
    data (array-like): N x 2 array of (x, y) points.
    bins (int): Number of bins in each dimension.
    cmap (str): Name of the matplotlib colormap to use.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    zlabel (str): Label for the z-axis.
    title (str): Title of the plot.
    colorbar (bool): Whether to show a colorbar.
    fig_ax (tuple): Optional tuple (fig, ax) to plot on.
    colorbar_label (str): Label for the colorbar.

    Returns:
    tuple: (fig, ax) - The figure and axis objects.
    """
    
    assert data.shape[1] == 2, "Data must have shape (N, 2)"
    
    # Get the 2D histogram data (counts) and the bin edges
    counts, x_edges, y_edges = np.histogram2d(data[:, 0], data[:, 1], bins=bins)

    # Create meshgrid for the bin edges
    x_pos, y_pos = np.meshgrid(x_edges[:-1] + 0.5 * (x_edges[1] - x_edges[0]),
                               y_edges[:-1] + 0.5 * (y_edges[1] - y_edges[0]))
    x_pos = x_pos.ravel()
    y_pos = y_pos.ravel()
    z_pos = np.zeros_like(x_pos)

    # The size of the bars in X and Y directions
    dx = dy = (x_edges[1] - x_edges[0])  # Same width for all bars
    dz = counts.ravel()  # The height of each bar is the count

    # Normalize dz (bar heights) to the range [0, 1] for the cmap
    norm_dz = dz / dz.max() if dz.max() > 0 else dz  # Avoid division by zero

    # Get a colormap based on the normalized dz values
    colors = plt.cm.get_cmap(cmap)(norm_dz)

    # Create the figure and 3D axis
    if fig_ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = fig_ax
    
    if use_bars:
        # Plot the bars with colors based on dz values
        bars = ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, 
                        color=colors, edgecolor=colors, alpha=1)
    else:
        im = ax.imshow(...)
    # Adjust viewing angle for better visibility
    # ax.view_init(elev=20, azim=30)  # Adjust the elevation and azimuthal angles as needed

    # Labels and title
    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)
    if zlabel is not None: ax.set_zlabel(zlabel)
    if title  is not None: ax.set_title(title)
    
    if colorbar:
        # Add a color bar to show the mapping between dz values and the cmap
        mappable = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=dz.min(), vmax=dz.max()))
        mappable.set_array([])  # Only necessary for some versions of matplotlib
        cbar = plt.colorbar(mappable, ax=ax)
        if colorbar_label is not None:
            cbar.set_label(colorbar_label)

    return fig, ax

def complex2hsv_colorbar(
        fig_and_ax=None, vmin=0, vmax=1, 
        min_angle=0, max_angle=0, 
        fontsize=8, angle_threshold=np.pi / 18):
    
    xx, yy = np.meshgrid(
        np.linspace(-1, 1, 1000),
        np.linspace(-1, 1, 1000))
    conv, sat, _ = complex2hsv(xx + 1j * yy, vmax=1)

    # Set outside the circle to transparent
    mask = (xx ** 2 + yy ** 2) > 1
    conv_rgba = np.zeros((conv.shape[0], conv.shape[1], 4))
    conv_rgba[..., :3] = conv
    conv_rgba[..., 3] = 1.0  # Set alpha to 1 for everything
    conv_rgba[mask, 3] = 0  # Set alpha to 0 outside the circle
    conv_rgba[conv_rgba < 0] = 0
    conv_rgba[conv_rgba > 1] = 1
    conv_rgba = conv_rgba[::-1, :]
    if fig_and_ax is None:
        fig, ax = plt.subplots()
    else:
        try:
            fig, ax = fig_and_ax
        except Exception as e:
            print('fig_and_ax should be a two-tuple of (fig, ax). Use:')
            print('>>> fig, ax = plt.subplots()')
            raise e

    im = ax.imshow(conv_rgba, interpolation='nearest')  # Flip the image vertically
    ax.axis('off')

    diff = np.abs(max_angle - min_angle)
    # Draw lines at min and max angles if they are not too close
    if np.minimum(diff, 2 * np.pi - diff) > angle_threshold:
        for angle in [min_angle, max_angle]:
            x_end = 500 + np.cos(angle) * 500
            y_end = 500 - np.sin(angle) * 500
            ax.plot([500, x_end], [500, y_end], '--', color='gray')

    # Add text annotations for min and max values
    if int(vmin*100)/100 > 0:   #because we are going to show .2f
        ax.text(500, 500, f'{vmin:.2f}', 
                ha='center', va='center', fontsize=fontsize, color='white')

    # Calculate position for max value text and invert color for readability
    angle = 45 * np.pi / 180  # 45 degrees in radians
    x_max = int(np.cos(angle) * 500 + 300)
    y_max = int(np.sin(angle) * 500 - 200)

    bck_color = conv_rgba[y_max, x_max, :3]
    text_color = 1 - bck_color  # Invert color

    ax.text(x_max, y_max, f'{vmax:.2f}',
            ha='center', va='center', fontsize=fontsize, color=text_color)

    return fig, ax

def plt_colorbar(mappable, colorbar_aspect=3, colorbar_pad_fraction=0.05):
    """
    Add a colorbar to the current axis with consistent width.

    Parameters:
        mappable (AxesImage): The image to which the colorbar applies.
        colorbar_aspect (int): The aspect ratio of the colorbar width relative 
            to the axis width. Default is 2.
        colorbar_pad_fraction (float): The fraction of padding between the 
            axis and the colorbar. Default is 0.05.

    Returns:
        Colorbar: The colorbar added to the axis.
    """
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    width = ax.get_position().width / colorbar_aspect
    cax = divider.append_axes("right", size=width, pad=colorbar_pad_fraction)
    cbar = fig.colorbar(mappable, cax=cax)
    return cbar

def plt_violinplot(
        dataset:list, positions, facecolor = None, edgecolor = None, 
        alpha = 0.5, label = None, fig_and_ax : tuple = None, 
        plt_violinplot_kwargs = {}):
    
    if(fig_and_ax is None):
        fig, ax = plt.subplots(1)
    else:
        fig, ax = fig_and_ax
    violin_parts = ax.violinplot(dataset, positions, **plt_violinplot_kwargs)
    for partname in ('cbars','cmins','cmaxes','cmeans','cmedians','bodies'):
        vp = violin_parts.get(partname, [])
        if partname == 'bodies':
            for vp_body in vp:
                vp_body.set_facecolor(facecolor)
                vp_body.set_edgecolor(edgecolor)
                vp_body.set_alpha(alpha)
        else:
            if isinstance(vp, list):
                for v in vp:
                    v.set_edgecolor(facecolor)
            else:
                vp.set_edgecolor(facecolor)
    return fig, ax

class plt_imhist:
    def __init__(self, in_image, figsize=(12, 6), title=None, bins=None,
                 kwargs_for_imshow={}, kwargs_for_hist={}):
        if bins is not None:
            if not (bins in kwargs_for_hist):
                kwargs_for_hist['bins'] = bins
        
        # Adjust figsize to provide more space if needed
        self.fig, axs = plt.subplots(
            1, 2, figsize=figsize,
            gridspec_kw={'width_ratios': [5, 1], 'wspace': 0.1})
        self.fig.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9)
        
        # Display the image
        self.im = axs[0].imshow(in_image, **kwargs_for_imshow)
        if title is not None:
            axs[0].set_title(title)
        axs[0].axis('off')
        
        cm = self.im.get_cmap()
        
        # Histogram
        n, bins = np.histogram(in_image.ravel(), **kwargs_for_hist)
        bin_centres = 0.5 * (bins[:-1] + bins[1:])
        axs[1].barh(
            bin_centres, n, height=(bins[1]-bins[0]),
            color=cm((bin_centres - bin_centres.min()) /
                         (bin_centres.max() - bin_centres.min())))
        axs[1].invert_xaxis()
        
        axs[1].yaxis.set_visible(True)
        axs[1].xaxis.set_visible(False)
        
        # Create textbox axes
        upper_text_ax = self.fig.add_axes([0.88, 0.85, 0.05, 0.05])
        lower_text_ax = self.fig.add_axes([0.88, 0.1, 0.05, 0.05])
        
        self.upper_text_box = TextBox(
            upper_text_ax, 'Max', initial=f'{in_image.max():.6f}')
        self.lower_text_box = TextBox(
            lower_text_ax, 'Min', initial=f'{in_image.min():.6f}')
        
        # Calculate the position for the slider
        slider_top = 0.85 - 0.02  # Bottom of the upper text box
        slider_bottom = 0.1 + 0.07  # Top of the lower text box
        slider_height = slider_top - slider_bottom  # Height between the two text boxes
        
        # Create slider axes on the right side of the histogram
        slider_ax = self.fig.add_axes(
            [0.895, slider_bottom, 0.02, slider_height], 
            facecolor='lightgoldenrodyellow')
        self.slider = RangeSlider(
            slider_ax, '', in_image.min(), in_image.max(),
            valinit=[in_image.min(), in_image.max()], orientation='vertical')
        self.slider.label.set_visible(False)
        self.slider.valtext.set_visible(False)
        
        self.lower_limit_line = axs[1].axhline(
            self.slider.val[0], color='k', linestyle='--')
        self.upper_limit_line = axs[1].axhline(
            self.slider.val[1], color='k', linestyle='--')
        
        # Initial text annotations for vmin and vmax
        self.vmin_text = axs[1].text(
            0.5, self.slider.val[0], f'{self.slider.val[0]:.6f}',
            transform=axs[1].get_yaxis_transform(), 
            ha='right', va='bottom', color='k')
        self.vmax_text = axs[1].text(
            0.5, self.slider.val[1], f'{self.slider.val[1]:.6f}',
            transform=axs[1].get_yaxis_transform(),
            ha='right', va='top', color='k')
        
        self.slider.on_changed(self.update)
        self.lower_text_box.on_submit(self.update_from_text)
        self.upper_text_box.on_submit(self.update_from_text)
    
    def update(self, val):
        self.im.set_clim(val[0], val[1])
        self.lower_limit_line.set_ydata([val[0], val[0]])
        self.upper_limit_line.set_ydata([val[1], val[1]])
        
        # Update text annotations to reflect the new vmin and vmax
        self.vmin_text.set_position((0.5, val[0]))
        self.vmin_text.set_text(f'{val[0]:.6f}')
        self.vmax_text.set_position((0.5, val[1]))
        self.vmax_text.set_text(f'{val[1]:.6f}')
        
        # Update text boxes to reflect the new values
        self.lower_text_box.set_val(f'{val[0]:.6f}')
        self.upper_text_box.set_val(f'{val[1]:.6f}')
        
        self.fig.canvas.draw_idle()
    
    def update_from_text(self, text):
        try:
            lower_val = float(self.lower_text_box.text)
            upper_val = float(self.upper_text_box.text)
            if lower_val < upper_val:
                self.slider.set_val([lower_val, upper_val])
        except ValueError:
            pass
        
def plt_imshow(img, 
               colorbar = True, 
               remove_axis_ticks = False, 
               title = None, 
               cmap = None,
               angle_cmap = None,
               portrait = None,
               complex_type = 'abs_angle',
               **kwargs):
    vmin = kwargs['vmin'] if 'vmin' in kwargs else None
    vmax = kwargs['vmax'] if 'vmax' in kwargs else None
    if(not np.iscomplexobj(img)):
        fig, ax = plt.subplots()
        im = ax.imshow(img, cmap = cmap, **kwargs)
        if(colorbar):
            plt_colorbar(im)
        if(remove_axis_ticks):
            plt.setp(ax, xticks=[], yticks=[])
    else:
        if (cmap == 'complex') | (complex_type == 'complex'):
            # Convert complex data to RGB
                
            complex_image, data_abs, data_angle = complex2hsv(
                img, vmin = vmin, vmax = vmax)
        
            # Calculate min and max angles
            if vmin is None: vmin = data_abs.min()
            if vmax is None: vmax = data_abs.max()
            
            try:
                min_angle = data_angle[data_abs > 0].min()
            except:
                min_angle = 0
            try:
                max_angle = data_angle[data_abs > 0].max()
            except:
                max_angle = 0
        
            # Plot the complex image
            fig, ax = plt.subplots()
            im = ax.imshow(complex_image)
            if(remove_axis_ticks):
                plt.setp(ax, xticks=[], yticks=[])

            if(colorbar):
                # Create and plot the color disc as an inset
                fig, ax_inset = complex2hsv_colorbar(
                    (fig, ax.inset_axes([0.79, 0.03, 0.18, 0.18], 
                                        transform=ax.transAxes)),
                    vmin=vmin, vmax=vmax, min_angle=min_angle, max_angle=max_angle)
                ax_inset.patch.set_alpha(0)  # Make the background of the inset axis transparent
        else:
            fig = plt.figure()
            window = plt.get_current_fig_manager().window
            if (window.height() > window.width()) & (portrait is None):
                portrait = True
            if portrait:
                ax = [fig.add_subplot(2, 1, 1), fig.add_subplot(2, 1, 2)]
            else:
                ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
            
            if complex_type == 'abs_angle':
                im = ax[0].imshow(np.abs(img), cmap = cmap, **kwargs)
                if(colorbar):
                    plt_colorbar(im)
                ax[0].set_title('abs')    
                if angle_cmap is None:
                    angle_cmap = 'twilight_shifted'
                im = ax[1].imshow(np.angle(img), cmap = angle_cmap, **kwargs)
                if(colorbar):
                    plt_colorbar(im)
                ax[1].set_title('angle')
            elif complex_type == 'real_imag':
                im = ax[0].imshow(np.real(img), cmap = cmap, **kwargs)
                if(colorbar):
                    plt_colorbar(im)
                ax[0].set_title('real')
                im = ax[1].imshow(np.imag(img), cmap = angle_cmap, **kwargs)
                if(colorbar):
                    plt_colorbar(im)
                ax[1].set_title('imag')
            
            if(remove_axis_ticks):
                plt.setp(ax[0], xticks=[], yticks=[])
                ax[0].xaxis.set_ticks_position('none')
                ax[0].yaxis.set_ticks_position('none')
                plt.setp(ax[1], xticks=[], yticks=[])
                ax[1].xaxis.set_ticks_position('none')
                ax[1].yaxis.set_ticks_position('none')
    if title is not None:
        fig.suptitle(title)
    return fig, ax

def plt_hist(vectors_list, fig_ax = None,
             n_bins = 10, alpha = 0.5, normalize = False, 
             labels_list = None, **kwargs):
    
    if fig_ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig, ax = fig_ax
    
    if not (type(vectors_list) is list):
        vectors_list = [vectors_list]
    for vec_cnt, vec in enumerate(vectors_list):
        bins, edges = np.histogram(vec, n_bins)
        if normalize:
            bins = bins / bins.max()
        ax.bar(edges[:-1], bins, 
                width =np.diff(edges).mean(), alpha=alpha)
        if labels_list is None:
            ax.plot(edges[:-1], bins, **kwargs)
        else:
            assert len(labels_list) == len(vectors_list)
            ax.plot(edges[:-1], bins, 
                     label = f'{labels_list[vec_cnt]}', **kwargs)
    return fig, ax

def plt_scatter3(
        data_N_by_3, fig_ax = None, title = None, 
        elev_list = [20, 70], azim_list = np.arange(0, 360, 20),
        make_animation = False, **kwargs):
    assert (len(data_N_by_3.shape)==2) & (data_N_by_3.shape[1] == 3), \
        'The first argument must be N x 3'
    if fig_ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = fig_ax
    ax.scatter(data_N_by_3[:, 0], 
               data_N_by_3[:, 1], 
               data_N_by_3[:, 2], **kwargs)
    
    if title is not None:
            ax.set_title(title)

    try: elev_list = [int(elev_list)]
    except: pass
    try: azim_list = [int(azim_list)]
    except: pass

    if make_animation:
        stack = []
        for elev in elev_list:
            for azim in azim_list:
                ax.view_init(elev=elev, azim=azim)
                img = plt_fig_to_numpy_3ch(fig)
                stack.append(img)
        return fig, ax, stack
    else:
        elev = None if elev_list is None else elev_list[0]
        azim = None if azim_list is None else azim_list[0]
        if (elev is not None) | (azim is not None):
            ax.view_init(elev=elev, azim=azim)
        return fig, ax

def plt_surface(stack, fig_ax = None, **kwargs):
    n_r, n_c = stack.shape

    if fig_ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = fig_ax

    X, Y = np.meshgrid(np.arange(n_r, dtype='int'), 
                       np.arange(n_c, dtype='int'))
    ax.plot_surface(X, Y, stack, **kwargs)
    return fig, ax

def plt_fig_to_numpy_3ch(fig):
    """Convert a matplotlib figure to a numpy 2D array (RGB)."""
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (h, w, 4)  # Shape should be (height, width, 4) for RGBA
    buf = np.copy(buf)  # Ensure we have a copy, not a view
    return buf

def plt_fig_to_numpy(fig):
    """ from https://www.icare.univ-lille.fr/how-to-
                    convert-a-matplotlib-figure-to-a-numpy-array-or-a-pil-image/
    """
    fig.canvas.draw()
    w,h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.ubyte)
    buf.shape = (w, h, 4)
    return buf.sum(2)

def numbers_as_images_3D(data3D_shape: tuple,
                         fontsize: int, 
                         text_loc: tuple = None,
                         verbose: bool = True):
    """ Numbers3D
    This function generates a 4D dataset of images with shape
    (n_x, n_r, n_c) where in each image the value "x" is written as a text
    that fills the image. As such, later when working with such a dataset you can
    look at the image and know which index it had before you use it.
    
    Follow this recipe to make good images:
    
    1- set n_x to 10, Set the desired n_r, n_c and width. 
    2- find fontsize that is the largest and still fits
    3- Increase n_x to desired size.
    
    You can provide a logs_root, log_dir or simply select a directory to save the
    output 3D array.
    
    """
    n_x, n_r, n_c = data3D_shape
    
    if text_loc is None:
        text_loc = (n_r//2 - fontsize, n_c//2 - fontsize)
    
    dataset = np.zeros(data3D_shape)    
    txt_width = int(np.log(n_x)/np.log(n_x)) + 1
    number_text_base = '{ind_x:0{width}}}'
    if(verbose):
        pBar = printprogress(n_x)
    for ind_x in range(n_x):
        mat = np.ones((n_r, n_c))
        number_text = number_text_base.format(ind_x = ind_x, 
                                              width = txt_width)
        fig = plt.figure(figsize = (n_rr, n_cc), dpi = n_rc)
        ax = fig.add_subplot(111)
        ax.imshow(mat, cmap = 'gray', vmin = 0, vmax = 1)
        ax.text(text_loc[0], text_loc[1],
                number_text, fontsize = fontsize)
        ax.axis('off')
        buf = plt_fig_to_numpy(fig)
        plt.close()
        dataset[ind_x] = buf.copy()
        if(verbose):
            pBar()
    return dataset

def numbers_as_images_4D(data4D_shape: tuple,
                         fontsize: int, 
                         text_loc: tuple = None,
                         verbose: bool = True):
    """ Numbers4D
    This function generates a 4D dataset of images with shape
    (n_x, n_y, n_r, n_c) where in each image the value "x, y" is written as a text
    that fills the image. As such, later when working with such a dataset you can
    look at the image and know which index it had before you use it.
    
    Follow this recipe to make good images:
    
    1- set n_x, n_y to 10, Set the desired n_r, n_c and width. 
    2- try fontsize that is the largest
    3- Increase n_x and n_y to desired size.
    
    You can provide a logs_root, log_dir or simply select a directory to save the
    output 4D array.
    
    :param text__loc:
        text_loc should be a tuple of the location of bottom left corner of the
        text in the image.
    
    """
    n_x, n_y, n_r, n_c = data4D_shape

    if text_loc is None:
        text_loc = (n_r//2 - fontsize, n_c//2 - fontsize)
    
    dataset = np.zeros((n_x, n_y, n_r, n_c))    
    txt_width = int(np.log(np.maximum(n_x, n_y))
                    / np.log(np.maximum(n_x, n_y))) + 1
    number_text_base = '{ind_x:0{width}}, {ind_y:0{width}}'
    if(verbose):
        pBar = printprogress(n_x * n_y)
    for ind_x in range(n_x):
        for ind_y in range(n_y):
            mat = np.ones((n_r, n_c))
            number_text = number_text_base.format(
                ind_x = ind_x, ind_y = ind_y, width = txt_width)
            n_rc = np.minimum(n_r, n_c)
            n_rr = n_r / n_rc
            n_cc = n_c / n_rc
            fig = plt.figure(figsize = (n_rr, n_cc), dpi = n_rc)
            ax = fig.add_subplot(111)
            ax.imshow(mat, cmap = 'gray', vmin = 0, vmax = 1)
            ax.text(text_loc[0], text_loc[1], number_text, fontsize = fontsize)
            ax.axis('off')
            buf = plt_fig_to_numpy(fig)
            plt.close()
            dataset[ind_x, ind_y] = buf.copy()
            if(verbose):
                pBar()
    return dataset

class plot_gaussian_gradient:
    """ Orignally developed for RobustGaussinFittingLibrary
    Plot curves by showing their average, and standard deviatoin
    by shading the area around the average according to a Gaussian that
    reduces the alpha as it gets away from the average.
    You need to init() the object then add() plots and then show() it.
    refer to the tests.py
    """
    def __init__(self, xlabel = None, ylabel = None, num_bars = 100, 
                       title = None, xmin = None, xmax = None, 
                       ymin = None, ymax = None, fontsize = 14):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.num_bars = num_bars
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        LWidth = 1
        font = {
                'weight' : 'bold',
                'size'   : fontsize}
        plt.rc('font', **font)
        params = {'legend.fontsize': 'x-large',
                 'axes.labelsize': 'x-large',
                 'axes.titlesize':'x-large',
                 'xtick.labelsize':'x-large',
                 'ytick.labelsize':'x-large'}
        plt.rcParams.update(params)
        plt.figure(figsize=(8, 6), dpi=50)
        self.ax1 = plt.subplot(111)
    
    def addPlot(self, x, mu, std, gradient_color, label, 
                snr = 3.0, mu_color = None, general_alpha = 1,
                mu_linewidth = 1):

        for idx in range(self.num_bars-1):
            y1 = ((self.num_bars-idx)*mu + idx*(mu + snr*std))/self.num_bars
            y2 = y1 + snr*std/self.num_bars
            
            prob = np.exp(-(snr*idx/self.num_bars)**2/2)
            plt.fill_between(
                x, y1, y2, 
                color = (gradient_color + (prob*general_alpha,)), 
                edgecolor=(gradient_color + (0,)))

            y1 = ((self.num_bars-idx)*mu + idx*(mu - snr*std))/self.num_bars
            y2 = y1 - snr*std/self.num_bars
            
            plt.fill_between(
                x, y1, y2, 
                color = (gradient_color + (prob*general_alpha,)), 
                edgecolor=(gradient_color + (0,)))
        if(mu_color is None):
            mu_color = gradient_color
        plt.plot(x, mu, linewidth = mu_linewidth, color = mu_color, 
                 label = label)
        
    def show(self, show_legend = True):
        if(self.xmin is not None) & (self.xmax is not None):
            plt.xlim([self.xmin, self.xmax])
        if(self.ymin is not None) & (self.ymax is not None):
            plt.ylim([self.ymin, self.ymax])
        if(self.xlabel is not None):
            plt.xlabel(self.xlabel, weight='bold')
        if(self.ylabel is not None):
            plt.ylabel(self.ylabel, weight='bold')
        if(self.title is not None):
            plt.title(self.title)
        if(show_legend):
            plt.legend()
        plt.grid()
        
        plt.show()
        
    def __call__(self, *args, **kwargs):
        self.addPlot(*args, **kwargs)

def imshow_series(list_of_stacks, 
                  list_of_masks = None,
                  figsize = None,
                  figsize_ratio = 1,
                  text_as_colorbar = False,
                  colorbar = False,
                  cmap = 'viridis',
                  list_of_titles_columns = None,
                  list_of_titles_rows = None,
                  fontsize = None,
                  transpose = True,
                  ):
    """ imshow a stack of images or sets of images in a shelf,
        input must be a list or array of images
        
        Each element of the list can appear as either:
        * n_im, n_r x n_c
        * n_im, n_r x  3  x 1
        * n_im, n_r x n_c x 3

        :param list_of_stacks
                list_of_stacks would include arrays iterable by their
                first dimension.
        :param borders: float
                borders between tiles will be filled with this variable
                default: np.nan
    """
    n_stacks = len(list_of_stacks)
    if(list_of_masks is not None):
        assert len(list_of_masks) == n_stacks, \
            f'the number of masks, {len(list_of_masks)} and ' \
            + f'stacks {n_stacks} should be the same'
     
    n_imgs = list_of_stacks[0].shape[0]
    for ind, stack in enumerate(list_of_stacks):
        assert stack.shape[0] == n_imgs, \
            'All members of the given list should have same number of images.' \
            f' while the stack indexed as {ind} has length {len(stack)}.'
        assert (len(stack.shape) == 3) | (len(stack.shape) == 4), \
            f'The shape of the stack {ind} must have length 3 or 4, it has '\
            f'shape of {stack.shape}. Perhaps you wanted to have only '\
             'one set of images. If thats the case, put that single '\
             'image in a list.'

    if (list_of_titles_columns is not None):
        assert len(list_of_titles_columns) == n_stacks, \
            'len(list_of_titles_columns) should be len(list_of_stacks)' \
            + f' but it is {len(list_of_titles_columns)}.'
    if (list_of_titles_rows is not None):
        assert len(list_of_titles_rows) == n_imgs, \
            'len(list_of_titles_rows) should be len(list_of_stacks[0])' \
            + f' but it is {len(list_of_titles_rows)}.'
            
    if figsize is None:
        figsize = (n_imgs*figsize_ratio,n_stacks*figsize_ratio)
        if transpose:
            figsize = (n_stacks*figsize_ratio,n_imgs*figsize_ratio)
    if fontsize is None:
        fontsize = int(max(figsize)/4)
    
    fig = plt.figure(figsize = figsize)
    if transpose:
        gs1 = matplotlib.gridspec.GridSpec(n_stacks, n_imgs)
    else:
        gs1 = matplotlib.gridspec.GridSpec(n_imgs, n_stacks)
    if(colorbar):
        gs1.update(wspace=0.25, hspace=0)
    else:
        gs1.update(wspace=0.025, hspace=0) 
    
    for img_cnt in range(n_imgs):
        for stack_cnt in range(n_stacks):
            if transpose:
                ax = plt.subplot(gs1[stack_cnt, img_cnt])
            else:
                ax = plt.subplot(gs1[img_cnt, stack_cnt])
            plt.axis('on')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            data_canvas = list_of_stacks[stack_cnt][img_cnt].copy()
            if(list_of_masks is not None):
                mask = list_of_masks[stack_cnt]
                if(mask is not None):
                    if(data_canvas.shape == mask.shape):
                        data_canvas[mask==0] = 0
                        data_canvas_stat = data_canvas[mask>0]
            else:
                data_canvas_stat = data_canvas.copy()
            data_canvas_stat = data_canvas_stat[
                np.isnan(data_canvas_stat) == 0]
            data_canvas_stat = data_canvas_stat[
                np.isinf(data_canvas_stat) == 0]
            vmin = data_canvas_stat.min()
            vmax = data_canvas_stat.max()
            im = ax.imshow(data_canvas, 
                            vmin = vmin, 
                            vmax = vmax,
                            cmap = cmap)
            if(text_as_colorbar):
                ax.text(data_canvas.shape[0]*0,
                         data_canvas.shape[1]*0.05,
                         f'{data_canvas.max():.6f}', 
                         color = 'yellow',
                         fontsize = fontsize)
                ax.text(data_canvas.shape[0]*0,
                         data_canvas.shape[1]*0.5, 
                         f'{data_canvas.mean():.6f}', 
                         color = 'yellow',
                         fontsize = fontsize)
                ax.text(data_canvas.shape[0]*0,
                         data_canvas.shape[1]*0.95, 
                         f'{data_canvas.min():.6f}', 
                         color = 'yellow',
                         fontsize = fontsize)
            ax.set_aspect('equal')
            if (list_of_titles_columns is not None):
                if img_cnt == 0:
                    ax.set_title(list_of_titles_columns[stack_cnt])
            if (list_of_titles_rows is not None):
                if stack_cnt == 0:
                    ax.set_ylabel(list_of_titles_rows[img_cnt])
            if (img_cnt > 0) & (stack_cnt > 0):
                ax.axis('off')
            if(colorbar):
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.ax.tick_params(labelsize=1)
    return fig, None

def imshow_by_subplots(
        images, grid_locations=None, frame_shape = None, title = None,
        titles=[], cmaps=[], colorbar=True, margin = 0.025, inter_image_margin = 0.01,
        colorbar_aspect=2, colorbar_pad_fraction=0.05,
        figsize=None, remove_axis_ticks=True, **kwargs):
    """
    Plots a list of 2D images at specified 2D grid_locations with titles 
    and colormaps.
    
    Parameters:
    images (list of 2D arrays): List of 2D images to plot.
    grid_locations (list of tuples or None): List of subplot grid_locations 
        in (rows, cols, index) format or None to generate a grid.
    titles (list of str): List of titles for each image.
    cmaps (list of str): List of colormaps for each image.
    colorbar (bool): Whether to add a colorbar beside each image. 
        Default is True.
    colorbar_aspect (int): Aspect ratio for the colorbars. Default is 2.
    colorbar_pad_fraction (float): Padding fraction for the colorbars. 
        Default is 0.05.
    figsize (tuple): Size of the figure.
    remove_axis_ticks (bool): Whether to remove axis ticks. Default is True.
    """
    try:
        dims = images.shape
        if len(dims) == 2:
            dims = [dims]
    except: pass
    
    if colorbar:
        margin = np.maximum(margin, 0.4)
        inter_image_margin = np.maximum(margin, 0.4)
    
    N = len(images)
    # Determine the maximum image size
    max_width = max(img.shape[1] for img in images)
    max_height = max(img.shape[0] for img in images)
    
    if grid_locations is None:
        if frame_shape is None:
            cols = int(np.ceil(np.sqrt(N)))
            rows = int(np.ceil(N / cols))
        else:
            cols, rows = frame_shape
            N = np.maximum(N, cols * rows)
        
        # Generate grid locations with dynamic spacing
        spacing = max(max_width, max_height) * (1 + inter_image_margin)
        grid_locations = np.array([[col * spacing, 1 - row * spacing] for row in range(rows) for col in range(cols)])
        grid_locations = grid_locations[:N]  # Trim to number of images
            
    lefts = grid_locations[:, 0]
    bottoms = grid_locations[:, 1]
    rights = lefts + np.array([img.shape[1] for img in images])
    tops = bottoms + np.array([img.shape[0] for img in images])
    min_left = lefts.min() - margin * max_width
    min_bottom = bottoms.min() - margin * max_height
    max_right = rights.max() + margin * max_width
    max_top = tops.max() + margin * max_height
    lefts = (lefts - min_left) / (max_right - min_left)
    bottoms = (bottoms - min_bottom) / (max_top - min_bottom)
    rights = (rights - min_left) / (max_right - min_left)
    tops = (tops - min_bottom) / (max_top - min_bottom)

    fig = plt.figure()
    for cnt in range(N):
        gs = matplotlib.gridspec.GridSpec(1, 1, left=lefts[cnt], right=rights[cnt], 
                                          top=tops[cnt], bottom=bottoms[cnt])
        ax = fig.add_subplot(gs[0])
        image = images[cnt]
        if image is not None:
            if 'cmap' in kwargs:
                cax = ax.imshow(image, **kwargs)
            else:
                try:
                    _cmap = cmaps[i]
                except:
                    _cmap = None
                cax = ax.imshow(image, cmap=_cmap, **kwargs)

            try:
                ax.set_title(titles[cnt])
            except:
                pass

            if remove_axis_ticks:
                ax.axis('off')    
            if colorbar:
                plt_colorbar(cax, colorbar_aspect=colorbar_aspect,
                             colorbar_pad_fraction=colorbar_pad_fraction)
    if title is not None:
        fig.suptitle(title)
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.margins(margin)
    return fig, ax

class transform3D_viewer:
    """
    A 3D viewer for point cloud transformations using matplotlib.

    Attributes:
        in_pointcloud (numpy.ndarray): The input point cloud.
        pt_cls (numpy.ndarray): there must be a class for each point.
            class 0 is movable others will only have different colors
    """
    def __init__(self, in_pointcloud, pt_cls = None):
        error_msg = 'input point cloud must be Nx3, where N >= 3'
        assert len(in_pointcloud.shape) == 2, error_msg
        assert in_pointcloud.shape[0] >= 3, error_msg
        assert in_pointcloud.shape[1] == 3, error_msg
        self.PC = in_pointcloud
    
        if pt_cls is None:
            pt_cls = np.zeros(len(in_pointcloud), dtype='int')
        self.pt_cls = pt_cls
        self.moving_inds = np.where(self.pt_cls == 0)[0]
        assert len(self.moving_inds) > 3, \
            'at least 3 data points must have class 0'
        self.params = {}
        self.figure()
        self.textboxevalues = np.array([
            float(self.params["Tx_text_box"].text),
            float(self.params["Ty_text_box"].text),
            float(self.params["Tz_text_box"].text),
            float(self.params["Sx_text_box"].text),
            float(self.params["Sy_text_box"].text),
            float(self.params["Sz_text_box"].text),
            float(self.params["Rx_text_box"].text),
            float(self.params["Ry_text_box"].text),
            float(self.params["Rz_text_box"].text)])

    def figure(self):
        self.Theta_init, self.Vt_init = self.get_Theta(self.PC[self.moving_inds])
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.subplots_adjust(left=0.05, right=0.5, bottom=0.1, top=0.9)
        
        # Create step size text boxes
        self.create_text_box("T_step", 0.75, 0.88, 1.0, self.update_steps)
        # Create transformation widgets
        self.create_text_box("Tx", 0.75, 0.81, self.Theta_init["Tx"], self.update_from_text)
        self.create_text_box("Ty", 0.75, 0.74, self.Theta_init["Ty"], self.update_from_text)
        self.create_text_box("Tz", 0.75, 0.67, self.Theta_init["Tz"], self.update_from_text)

        self.create_buttons("Tx", 0.70, 0.81, partial(self.update_value, "Tx", "T_step", -1), partial(self.update_value, "Tx", "T_step", 1))
        self.create_buttons("Ty", 0.70, 0.74, partial(self.update_value, "Ty", "T_step", -1), partial(self.update_value, "Ty", "T_step", 1))
        self.create_buttons("Tz", 0.70, 0.67, partial(self.update_value, "Tz", "T_step", -1), partial(self.update_value, "Tz", "T_step", 1))
        
        self.create_text_box("S_step", 0.75, 0.59, 0.1, self.update_steps)
        self.create_text_box("Sx", 0.75, 0.52, self.Theta_init["Sx"], self.update_from_text)
        self.create_text_box("Sy", 0.75, 0.45, self.Theta_init["Sy"], self.update_from_text)
        self.create_text_box("Sz", 0.75, 0.38, self.Theta_init["Sz"], self.update_from_text)
        
        self.create_buttons("Sx", 0.70, 0.52, partial(self.update_value, "Sx", "S_step", -1), partial(self.update_value, "Sx", "S_step", 1))
        self.create_buttons("Sy", 0.70, 0.45, partial(self.update_value, "Sy", "S_step", -1), partial(self.update_value, "Sy", "S_step", 1))
        self.create_buttons("Sz", 0.70, 0.38, partial(self.update_value, "Sz", "S_step", -1), partial(self.update_value, "Sz", "S_step", 1))
        
        self.create_text_box("R_step", 0.75, 0.3, 5.0, self.update_steps)
        self.create_text_box("Rx", 0.75, 0.23, self.Theta_init["Rx"], self.update_from_text)
        self.create_text_box("Ry", 0.75, 0.18, self.Theta_init["Ry"], self.update_from_text)
        self.create_text_box("Rz", 0.75, 0.13, self.Theta_init["Rz"], self.update_from_text)
        
        self.create_buttons("Rx", 0.70, 0.23, partial(self.update_value, "Rx", "R_step", -1), partial(self.update_value, "Rx", "R_step", 1))
        self.create_buttons("Ry", 0.70, 0.18, partial(self.update_value, "Ry", "R_step", -1), partial(self.update_value, "Ry", "R_step", 1))
        self.create_buttons("Rz", 0.70, 0.13, partial(self.update_value, "Rz", "R_step", -1), partial(self.update_value, "Rz", "R_step", 1))

        self.draw()
        
    def draw(self):
        # Display the point cloud
        self.ax.cla()
        for cls_cnt in np.unique(self.pt_cls):
            self.ax.scatter(self.PC[self.pt_cls == cls_cnt, 0],
                            self.PC[self.pt_cls == cls_cnt, 1],
                            self.PC[self.pt_cls == cls_cnt, 2], 
                            label=f'cls_{cls_cnt}')
        cls_values = np.unique(self.pt_cls)
        if len(cls_values) > 1:
            for cls_cnt in cls_values[:-1] :
                self.ax.plot([self.PC[self.pt_cls == cls_cnt, 0][-1], self.PC[self.pt_cls == cls_cnt + 1, 0][0]],
                             [self.PC[self.pt_cls == cls_cnt, 1][-1], self.PC[self.pt_cls == cls_cnt + 1, 1][0]],
                             [self.PC[self.pt_cls == cls_cnt, 2][-1], self.PC[self.pt_cls == cls_cnt + 1, 2][0]], 
                             color = 'black', linewidth = 2)
    
        # Calculate the bounding box for the moving_inds using SVD
        points = self.PC[self.moving_inds]
        mean = points.mean(axis=0)
        centered_points = points - mean
        U, S, Vt = np.linalg.svd(centered_points)
    
        # Project points onto principal axes
        projections = centered_points @ Vt.T
    
        # Get the min and max along each principal axis
        min_proj = projections.min(axis=0)
        max_proj = projections.max(axis=0)
    
        # Define the bounding box corners in the projected space
        bbox_proj = np.array([[min_proj[0], min_proj[1], min_proj[2]],
                              [max_proj[0], min_proj[1], min_proj[2]],
                              [max_proj[0], max_proj[1], min_proj[2]],
                              [min_proj[0], max_proj[1], min_proj[2]],
                              [min_proj[0], min_proj[1], max_proj[2]],
                              [max_proj[0], min_proj[1], max_proj[2]],
                              [max_proj[0], max_proj[1], max_proj[2]],
                              [min_proj[0], max_proj[1], max_proj[2]]])
    
        # Rotate bounding box corners back to the original coordinate system
        bbox = bbox_proj @ Vt + mean
    
        # Draw bounding box lines
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), # Bottom square
                 (4, 5), (5, 6), (6, 7), (7, 4), # Top square
                 (0, 4), (1, 5), (2, 6), (3, 7)] # Vertical lines
    
        for edge in edges:
            self.ax.plot3D(*zip(bbox[edge[0]], bbox[edge[1]]), '--', color='blue')
    
        self.fig.canvas.draw()

    def get_Theta(self, PC):
        # Calculate the initial SVD of the centered movable part
        Theta = {}
        mean_vec = PC.mean(0)
        Theta["Tx"], Theta["Ty"], Theta["Tz"] = mean_vec
        PC_moving_centered = PC - mean_vec
        U, S_vec, Vt = np.linalg.svd(PC_moving_centered.T)
        Theta["Sx"], Theta["Sy"], Theta["Sz"] = S_vec
        r = scipy_rotation.from_matrix(U)
        Theta["Rx"], Theta["Ry"], Theta["Rz"] = r.as_euler('xyz', degrees=True)
        return Theta, Vt[:3]
    
    def apply(self, PC):
        Theta_in, Vt_in = self.get_Theta(PC)
        Theta, _ = self.get_Theta(self.PC[self.moving_inds])
        
        translation = np.array(
            [Theta_in['Tx'] + Theta["Tx"] - self.Theta_init['Tx'],
             Theta_in['Ty'] + Theta["Ty"] - self.Theta_init['Ty'],
             Theta_in['Tz'] + Theta["Tz"] - self.Theta_init['Tz']])
        new_S = np.diag(
            [Theta_in["Sx"] * Theta["Sx"] / self.Theta_init["Sx"],
             Theta_in["Sy"] * Theta["Sy"] / self.Theta_init["Sy"],
             Theta_in["Sz"] * Theta["Sz"] / self.Theta_init["Sz"]])
        r = scipy_rotation.from_euler('xyz',
            np.array([Theta_in["Rx"] + Theta["Rx"] - self.Theta_init["Rx"],
                      Theta_in["Ry"] + Theta["Ry"] - self.Theta_init["Ry"],
                      Theta_in["Rz"] + Theta["Rz"] - self.Theta_init["Rz"]]),
            degrees=True)
        new_U = r.as_matrix()
        PC_transformed = (new_U @ new_S @ Vt_in).T + translation
        return PC_transformed
        
    def create_text_box(self, label, x, y, initial_val, on_submit):
        text_ax = self.fig.add_axes([x, y, 0.13, 0.05])
        text_box = TextBox(text_ax, label + '         ', 
                           initial=f'{initial_val:.6f}')
        text_box.on_submit(on_submit)
        self.params[f"{label}_text_box"] = text_box
    
    def create_buttons(self, label, x, y, on_click_minus, on_click_plus):
        minus_ax = self.fig.add_axes([x, y, 0.04, 0.05])
        plus_ax = self.fig.add_axes([x + 0.19, y, 0.04, 0.05])
        minus_button = Button(minus_ax, '-')
        plus_button = Button(plus_ax, '+')
        minus_button.on_clicked(on_click_minus)
        plus_button.on_clicked(on_click_plus)
        self.params[f"{label}_minus_button"] = minus_button
        self.params[f"{label}_plus_button"] = plus_button
    
    def update_steps(self, text):
        try:
            self.params["T_step"] = float(self.params["T_step_text_box"].text)
            self.params["S_step"] = float(self.params["S_step_text_box"].text)
            self.params["R_step"] = float(self.params["R_step_text_box"].text)
        except ValueError:
            pass

    def update_from_text(self, text):
        try: # Read new transformation values
            self.textboxevalues = np.array([
                float(self.params["Tx_text_box"].text),
                float(self.params["Ty_text_box"].text),
                float(self.params["Tz_text_box"].text),
                float(self.params["Sx_text_box"].text),
                float(self.params["Sy_text_box"].text),
                float(self.params["Sz_text_box"].text),
                float(self.params["Rx_text_box"].text),
                float(self.params["Ry_text_box"].text),
                float(self.params["Rz_text_box"].text)])
        except ValueError:
            pass
            
        translation = self.textboxevalues[:3].copy()
        new_S = np.diag(self.textboxevalues[3:6].copy())
        r = scipy_rotation.from_euler(
            'xyz',self.textboxevalues[6:].copy(), degrees=True)
        new_U = r.as_matrix()
        PC_transformed = (new_U @ new_S @ self.Vt_init).T + translation
        # Update the movable part of the point cloud
        self.PC[self.moving_inds] = PC_transformed
        
        self.draw()

    def update_value(self, label, step_label, direction, event):
        current_val = float(self.params[f"{label}_text_box"].text)
        step_size = float(self.params[f"{step_label}_text_box"].text)
        new_val = current_val + direction * step_size
        self.params[f"{label}_text_box"].set_val(f"{new_val:.6f}")
                
class _questdiag:
    def __init__(self,
        question = '', 
        figsize=(6, 2), 
        buttons = {'Yes'    : True, 
                   'No'     : False, 
                   'Cancel' : None},
        row_spacing=0.05):
    
        assert isinstance(buttons, dict), \
            ('buttons arg must be a dictionary of texts appearing on '
             'the buttons values to be returned.')
        
        self.buttons = buttons
        self.result = None
        _, ax = plt.subplots(figsize=figsize)
        plt.subplots_adjust(bottom=0.2) 
    
        ax.text(0.5, 0.85, question, ha='center', va='center', fontsize=12)
        plt.axis('off')
    
        # Calculate grid size
        N = len(buttons)
        n_rows = int(np.ceil(N ** 0.5))
        n_clms = int(np.ceil(N / n_rows))

        # Button size and position
        button_width = 0.8 / n_clms
        button_height = 0.3 / n_rows
        horizontal_spacing = (1 - button_width * n_clms) / (n_clms + 1)
        vertical_spacing = (0.2 - button_height * n_rows) / (n_rows + 1)

        # Adjust vertical_spacing to add more space between rows
        vertical_spacing += row_spacing
    
        button_objects = []
        for i, button_label in enumerate(buttons.keys()):
            row = i // n_clms
            col = i % n_clms

            button_ax = plt.axes([
                horizontal_spacing + col * (button_width + horizontal_spacing),
                0.2 + (n_rows - row - 1) * (button_height + vertical_spacing),  # Start from top
                button_width,
                button_height
            ])
            button = Button(button_ax, str(button_label))
            button.on_clicked(self.button_click)
            button_objects.append(button)
    
        plt.show()
    
    def button_click(self, event):
        ind = event.inaxes.texts[0].get_text()
        self.result = self.buttons[ind]   # Return the corresponding output
        plt.close()

def question_dialog(
    question = 'Yes/No/Cancel?', figsize=(6, 2), 
    buttons = {'Yes' : True, 'No' : False, 'Cancel' : None}):
    return _questdiag(question, figsize, buttons).result

def plot_marker(
        coords, fig_ax=None, figsize=(2, 2),
        marker=None, markersize = None, return_markersize = False):
    """
    Plots a grid of dots with a dynamic figure size to avoid overlap.
    
    Parameters:
    - coords: numpy array of shape (N, 2), where each row is [x, y] coordinates
    - fig_ax: 2-tuple of (fig, ax) or None; if None, a new figure and axis are created
    - figsize: tuple of two floats, figure size in inches (width, height)
    - marker: str, marker style (e.g., 'x', 'o', '.', etc.); if None, use the next marker in the cycle
    - marker_sizer: float, the marker size
    
    Returns:
    - 2-tuple of (fig, ax), and the markersize used for plotting
    """
    if fig_ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        if figsize is None:
            figsize = fig.get_size_inches()
    else:
        fig, ax = fig_ax
    
    if markersize is None:
        markersize = 12 * min(figsize[0], figsize[1])/ len(coords)
        markersize = np.maximum(markersize, 1)

    if marker is None:
        marker = next(matplotlib_lines_Line2D_markers_keys_cycle)
    
    ax.plot(coords[:, 0], coords[:, 1], 
            marker=marker, markersize=markersize, linestyle='')

    if return_markersize:
        return fig, ax, markersize
    else:
        return fig, ax
    
def plt_contours(Z_list, X_Y = None, fig_ax=None, levels=10, colors_list=None, 
                 linestyles_list=None, title=None):
    """
    Plot contours of multiple surfaces overlaid on the same plot.
    
    Parameters:
    - Z_list: List of 2D arrays representing the surface heights at each 
              grid point.
    - X_Y: tuple where the (X, Y) describe the meshgrid over which Z is defined
    - fig_ax: Tuple (fig, ax) where fig is the figure and ax is the axes.
              If None, creates a new figure and axes.
    - levels: Number of contour levels for all surfaces.
    - colors_list: List of colors for the contours of each surface. 
                   If None, defaults to a colormap.
    - linestyles_list: List of line styles for the contours of each surface. 
                If None, defaults to a pattern.
    - title: Optional title for the plot.
    """
    
    # Create figure and axes if not provided
    if fig_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_ax
    
    # Default colors and linestyles if not provided
    if colors_list is None:
        colors_list = plt.cm.jet(np.linspace(0, 1, len(Z_list)))
    if linestyles_list is None:
        linestyles_list = ['dashed', 'solid'] * (len(Z_list) // 2 + 1)
    
    # Plot contours for each surface in Z_list
    for i, Z in enumerate(Z_list):
        if X_Y is None:
            Y, X = np.meshgrid(np.arange(Z.shape[1]), np.arange(Z.shape[0]))
        else:
            X, Y = X_Y
        color = colors_list[i % len(colors_list)]
        linestyle = linestyles_list[i % len(linestyles_list)]
        
        contour = ax.contour(X, Y, Z, levels=levels, colors=[color],linestyles=linestyle)
        
        # Add labels to contours
        ax.clabel(contour, inline=True, fontsize=8, fmt='%.2f')
        
    if title is not None:
        ax.set_title(title)
    
    return fig, ax