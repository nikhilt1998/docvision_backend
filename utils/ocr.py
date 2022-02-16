"""Contains helper functions for the OCR text."""

def get_lined_text(sorted_bounding_boxes):
  """
  Join the boxes to get the text line wise as in document
  Input: List of sorted bounding boxes
  Output: Lined text
  """

  lined_text = \
        [' '.join([desired[-1] for desired in cord])for cord in sorted_bounding_boxes]
  return lined_text

def get_spaced_text(sorted_bounding_boxes):
  """
  Join the boxes to get the paragraph of text
  Input: List of sorted bounding boxes
  Output: Paragraph of text
  """
  
  spaced_text = ' '.join([desired[-1] for cord in sorted_bounding_boxes for desired in cord])
  return spaced_text