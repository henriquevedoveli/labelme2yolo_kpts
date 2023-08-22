import json
import os
import glob
import argparse
from conversions import *
from typing import Dict, List, Tuple

class AnnotationProcessor:
    """Handles processing of JSON annotation files and generates annotation files in a specified format."""
    
    def __init__(self, args: argparse.Namespace):
        """
        Initializes the AnnotationProcessor instance.

        Args:
            args (argparse.Namespace): Parsed command-line arguments.
        """
        self.path = args.path
        self.final_path = args.final_path
        self.all_classes = args.all_classes
        self.main_class = args.main_class

    def process_shape(self, shape: Dict[str, any], image_w: int, image_h: int) -> Tuple[str, str, List[Tuple[float, float]]]:
        """
        Processes a shape from the JSON annotation data.

        Args:
            shape (Dict[str, any]): Shape data from the annotation.
            image_w (int): Width of the image.
            image_h (int): Height of the image.

        Returns:
            Tuple[str, str, List[Tuple[float, float]]]: Processed group ID, label, and points.
        """
        group_id = shape['group_id']
        label = shape['label']
        points = shape['points']

        if shape['shape_type'] == 'point':
            points = [points]

        return group_id, label, points

    def generate_annotation(self, data: Dict[str, any], image_w: int, image_h: int) -> Dict[str, str]:
        """
        Generates annotation data for a given JSON annotation.

        Args:
            data (Dict[str, any]): JSON annotation data.
            image_w (int): Width of the image.
            image_h (int): Height of the image.

        Returns:
            Dict[str, str]: Generated annotation data.
        """
        result_dict = {}

        for shape in data['shapes']:
            group_id, label, points = self.process_shape(shape, image_w, image_h)

            try:
                if label == self.main_class:
                    x_prop, y_prop, w_prop, h_prop = bounding_box_coord(points, image_w, image_h)
                    result_dict.setdefault(group_id, {})[label] = f"0 {x_prop} {y_prop} {w_prop} {h_prop}"
                else:
                    x_prop, y_prop = kpts_coord(points, image_w, image_h)
                    result_dict.setdefault(group_id, {})[label] = f"{x_prop} {y_prop} 2"
            except Exception as e:
                raise Exception(f"ERROR cannot convert the annotation {label} - {e}")

        for group_id in result_dict:
            for label in self.all_classes:
                result_dict[group_id].setdefault(label, '0 0 0')

        return result_dict

    def process_annotations(self):
        """Processes JSON annotation files and generates annotation files."""
        for file in glob.glob(os.path.join(self.path, "*.json")):
            with open(file, 'r') as json_file:
                filename = os.path.splitext(os.path.basename(file))[0]
                data = json.load(json_file)
                image_h = data['imageHeight']
                image_w = data['imageWidth']

                try:
                    result_dict = self.generate_annotation(data, image_w, image_h)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue

                try:
                    output_path = os.path.join(self.final_path, f'{filename}.txt')
                    print(output_path)
                    with open(output_path, 'w') as output_file:
                        for group_id in result_dict:
                            annotation = ' '.join([result_dict[group_id][label] for label in self.all_classes])
                            output_file.write(annotation + '\n')
                except Exception as e:
                    print(f'Error writing annotation {filename}: {e}')

def main():
    parser = argparse.ArgumentParser(description='Process JSON annotations and generate annotation files.')
    parser.add_argument('--path', required=True, help='Path to JSON annotation files')
    parser.add_argument('--final-path', required=True, help='Path to save annotation files')
    parser.add_argument('--all-classes', nargs='+', required=True, help='List of all classes')
    parser.add_argument('--main-class', required=True, help='Main class name')

    args = parser.parse_args()

    processor = AnnotationProcessor(args)
    processor.process_annotations()

if __name__ == "__main__":
    main()
