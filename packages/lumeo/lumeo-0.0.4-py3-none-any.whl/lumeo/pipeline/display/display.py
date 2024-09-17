import cv2
import textwrap

class Display:
    @staticmethod
    def write_label_on_frame(mat, xidx, yidx, label):
        # Auxiliary function to write text label on frame
        #
        my_font_scale = 0.75
        my_wrap_width = 120

        frame_width = mat.shape[1]
        if frame_width <= 640:
            my_font_scale = 0.75
            my_wrap_width = 120
        elif frame_width <= 1280:
            my_font_scale = 1.0
            my_wrap_width = 160
        else:
            my_font_scale = 1.5
            my_wrap_width = 200

        wrapped_label = textwrap.wrap(label, width=my_wrap_width)
        total_label_height = 0

        for line in wrapped_label:
            (label_width, label_height), baseline = cv2.getTextSize(line, cv2.FONT_HERSHEY_PLAIN,
                                                                    my_font_scale, 1)
            label_height = label_height + 5
            cv2.rectangle(mat, (xidx, yidx), (xidx + label_width, yidx + label_height + baseline),
                          (0, 255, 255), -1)
            cv2.putText(mat, line, (xidx, yidx + label_height), cv2.FONT_HERSHEY_PLAIN,
                        my_font_scale, (0, 0, 0), 1, cv2.LINE_AA)
            yidx = yidx + label_height + baseline
            total_label_height = total_label_height + label_height + baseline

        return (label_width, total_label_height)

# Expose methods at the module level
#     This is necessary if you want to import these methods directly from display.py without referencing the Display class.
#     This setup allows you to re-export these methods in the __init__.py file of the utils module, making them directly
#     accessible when importing from lumeo.display.
write_label_on_frame = Display.write_label_on_frame
