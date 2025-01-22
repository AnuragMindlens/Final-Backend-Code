from PIL import Image
import torch
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Load Mask2Former model and processor
processor = AutoImageProcessor.from_pretrained("facebook/mask2former-swin-base-coco-panoptic")
model = Mask2FormerForUniversalSegmentation.from_pretrained("facebook/mask2former-swin-base-coco-panoptic")

# URL to the image
url = "/home/yuvaraj0702/aipose/media/tmp/poipoi.jpeg"

# Load the image and process it
image = Image.open(url).convert("RGB")
inputs = processor(images=image, return_tensors="pt")

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)

# Post-process the segmentation results
results = processor.post_process_panoptic_segmentation(outputs, target_sizes=[image.size[::-1]])[0]

# Map segment IDs to label IDs
segment_to_label = {segment['id']: segment['label_id'] for segment in results["segments_info"]}



def draw_panoptic_segmentation(segmentation, segments_info, output_file=None):
    # Choose a basic colormap
    cmap = plt.colormaps['viridis'] # You can also use cm.Set3 or other colormaps

    fig, ax = plt.subplots()
    ax.imshow(segmentation)
    instances_counter = {}
    handles = []
    
    for segment in segments_info:
        segment_id = segment['id']
        segment_label_id = segment['label_id']
        segment_label = model.config.id2label[segment_label_id]
        instances_counter[segment_label_id] = instances_counter.get(segment_label_id, 0) + 1
        label = f"{segment_label}-{instances_counter[segment_label_id]}"
        color = cmap(segment_id)
        handles.append(mpatches.Patch(color=color, label=label))
        
    legend = ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    if output_file:
        plt.savefig(output_file, bbox_extra_artists=(legend,), bbox_inches='tight')
    else:
        plt.show()

# Assuming results is a dictionary containing 'segmentation' and 'segments_info'
draw_panoptic_segmentation(**results, output_file='output.png')

