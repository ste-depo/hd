import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
from stardist import random_label_cmap, _draw_polygons

#  ------- functions to define color palettes : START

def create_palette_matplotlib(n):
    cmap = plt.get_cmap('hsv')  # Puoi cambiare 'hsv' con qualsiasi colormap disponibile in matplotlib
    colors = [cmap(i / n) for i in range(n)]
    colors = [(1, 1, 1, 1)] + colors
    return ListedColormap(colors)

def create_palette_uniform(n):
    colors = [(0, 0, 0, 0)] + ['yellow' for x in range(n)]
    return ListedColormap(colors)

#  ------- functions to define color palettes : END

# function to display:
#  - the full H&E image [with a box of the highlighted region]
#  - the zoom of the highlighted region with nuclei calls. 
# By default shows thicker lines for nuclei with high scores
# to see nuclei with lines of equal thickness set probs = False

def show_cropped_nuclei(img, labels, x_bottom=0, y_bottom=0, x_width=500, y_width=500, alpha = 0.3):
    
    nuclei_matrix = (labels > 0).astype(int)
    
    bbox = (x_bottom, y_bottom, x_bottom+x_width, y_bottom+y_width)
    
    cropped = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    cropped_nuclei = labels[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    cropped_mask = nuclei_matrix[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # Create a Rectangle patch
    rect = patches.Rectangle((x_bottom, y_bottom), x_width, y_width, linewidth=1, edgecolor='r', facecolor='none')
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 20)) 
    axes[0].imshow(img)
    # Add the patch to the Axes
    axes[0].add_patch(rect)
    axes[1].imshow(cropped)
    axes[1].imshow(cropped_mask, alpha = alpha)
    axes[2].imshow(cropped_nuclei, cmap = create_palette_matplotlib(len(np.unique(cropped_nuclei))-1))

# function to display:
#  - the full H&E image [with a box of the highlighted region]
#  - the zoom of the highlighted H&E region with nuclei colored with 
#     a yellow mask on them (transparency can be modulated by alpha argument)
#  - the zoom of the highlighted region with only the nuclei calls
# By default shows thicker lines for nuclei with high scores
# to see nuclei with lines of equal thickness set probs = False

def show_cropped_nuclei2(img, labels, details=None, 
                        x_bottom=0, y_bottom=0, x_width=500, y_width=500, probs=True):

    bbox = (x_bottom, y_bottom, x_bottom+x_width, y_bottom+y_width)
    
    nuclei_matrix = (labels > 0).astype(int)
    cropped = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    cropped_nuclei = labels[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    cropped_mask = nuclei_matrix[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # identify cropped ids
    cropped_nuclei_ids = set(np.unique(cropped_nuclei)).difference([0])
    cropped_nuclei_idx = np.array(list(cropped_nuclei_ids)) - 1

    # select details of the cropped nuclei and translate according to new coordinates
    coord, points, prob = details['coord'], details['points'], details['prob']    
    coord = [[coord[idx][0] - y_bottom, coord[idx][1] - x_bottom] for idx in cropped_nuclei_idx]
    points = [points[idx] - [y_bottom, x_bottom] for idx in cropped_nuclei_idx]
    prob = [prob[idx] for idx in cropped_nuclei_idx]

    # panel 1 - full image with red rectangle on the selection

    fig, axes = plt.subplots(1, 2, figsize=(20, 20)) 
    axes[0].imshow(img)
    # Create a Rectangle patch and add the patch to the Axes
    rect = patches.Rectangle((x_bottom, y_bottom), x_width, y_width, linewidth=1, edgecolor='r', facecolor='none')
    axes[0].add_patch(rect)
    
    plt.subplot(122); plt.imshow(cropped); plt.axis('off')
    a = plt.axis()
    if probs != True:
        prob = None
    _draw_polygons(polygons = coord,
                   scores = prob, 
                   show_dist=False, 
                   cmap = create_palette_uniform(len(coord))
                  )
    plt.axis(a)

