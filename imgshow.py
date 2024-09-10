import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

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
