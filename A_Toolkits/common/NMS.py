# %% [markdown]
# # パッケージの導入

# %%
import numpy as np

# %% [markdown]
# # IoUの計算

# %%
def IoU(box1, box2):
    # Calculate the intersection area
    x1 = np.maximum(box1[0], box2[0])
    y1 = np.maximum(box1[1], box2[1])
    x2 = np.minimum(box1[2], box2[2])
    y2 = np.minimum(box1[3], box2[3])

    intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)

    # Calculate the union area
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Calculate the IoU
    union = area1 + area2 - intersection + 1e-5

    return intersection / union

# %% [markdown]
# # エリアは重ね合わせるの検出

# %%
def is_contained(box1, box2):
    """Check if box1 is contained within box2"""
    return (
            box1[0] >= box2[0] and box1[1] >= box2[1] and
            box1[2] <= box2[2] and box1[3] <= box2[3]
    )

# %% [markdown]
# # NMSの計算

# %%
def nms_kernel(boxes, iou_threshold=0.5):
    # Extract the coordinates, confidences, and class_ids
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    confidences = boxes[:, 4]

    # Calculate areas of the boxes
    areas = (x2 - x1) * (y2 - y1)

    # Sort by confidence
    sorted_indices = np.argsort(confidences)[::-1]
    sorted_boxes = boxes[sorted_indices]

    keep = []

    while len(sorted_boxes) > 0:
        # Take the box with the highest confidence
        box = sorted_boxes[0]
        keep.append(box)

        if len(sorted_boxes) == 1:
            break

        # Compute IoU with the rest of the boxes
        rest_boxes = sorted_boxes[1:]
        ious = np.array([IoU(box, rest_box) for rest_box in rest_boxes])

        # Determine which boxes to keep
        keep_boxes = []
        for i, rest_box in enumerate(rest_boxes):
            if ious[i] > iou_threshold:
                continue
            if is_contained(box, rest_box) or is_contained(rest_box, box):
                if areas[sorted_indices[1:][i]] < areas[sorted_indices[0]]:
                    continue
            keep_boxes.append(rest_box)

        sorted_boxes = np.array(keep_boxes)

    return np.stack(keep) if keep else np.array([])

# %%
# NMS function
def non_max_suppression(boxes, iou_threshold=0.5):
    """Perform Non-maximum Suppression on the boxes
    Args:
        boxes: tensor, has shape[batch_size, num_boxes, 6] in [x1, y1, x2, y2, confidence, class_id] format
        iou_threshold: IoU threshold for overlapping
    Returns:
        output_boxes: tensor of boxes after NMS
    """

    # Get the batch, number of boxes, and box shape
    if boxes.ndim == 2:
        # Add the batch dimension
        boxes = boxes.reshape(1, -1, 6)

    # Initialize the final output
    final_output = []

    # Apply NMS for each batch
    for b_boxes in boxes:
        # Divide the boxes into classes
        class_ids = b_boxes[:, 5]

        # Get the unique class IDs
        unique_class_ids = np.unique(class_ids)

        # Use NMS for each class
        for class_id in unique_class_ids:
            # Get the boxes whose ids are same as the class_id
            class_boxes = b_boxes[class_ids == class_id]

            # Apply NMS
            nms_boxes = nms_kernel(class_boxes, iou_threshold)

            # Append the NMS boxes to the final output
            final_output.extend(nms_boxes)

    # Convert the final output to the tensor
    if len(final_output) > 0:
        final_output = np.stack(final_output)
        return final_output
    else:
        return None

# %% [markdown]
# # テスト

# %%
def test_nms():
    # For the performance, the data will be organized to GPU format: (batch, bboxes, 6)
    # And the 6 is the format of [x1, y1, x2, y2, confidence, class_id]
    test_data = [
        [100, 100, 150, 150, 0.5, 1.0],
        [100, 100, 200, 200, 0.9, 1.0],
        [110, 110, 210, 210, 0.75, 1.0],
        [200, 200, 300, 300, 0.6, 2.0],
        [400, 400, 500, 500, 0.95, 2.0]
    ]

    test_data = np.array(test_data)
    test_data = test_data.reshape(1, -1, 6)

    # Define the expected output
    expected_output = [
        [100.0, 100.0, 200.0, 200.0, 0.9, 1.0],
        [400.0, 400.0, 500.0, 500.0, 0.95, 2.0],
        [200.0, 200.0, 300.0, 300.0, 0.6, 2.0]
    ]

    expected_output = np.array(expected_output)
    expected_output = expected_output.reshape(1, -1, 6)

    output = non_max_suppression(test_data, iou_threshold=0.5)

    assert np.allclose(output, expected_output), f"Expected {expected_output}, but got {output}"


if __name__ == "__main__":
    test_nms()
    print("所有测试通过！")


