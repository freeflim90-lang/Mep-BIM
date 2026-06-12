from pprint import pprint
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element

# Function to find each wall having windows
def get_walls_have_windows(walls):
    walls_info = []
    
    # Loop through walls to find those with windows
    for wall in walls:
        related_windows = []

        # Check if the wall has openings
        if hasattr(wall, 'HasOpenings'):  # IfcRelVoidsElement-HasOpenings
            for related_opening in wall.HasOpenings:  # Loop through IfcRelVoidsElement
                related_element = related_opening.RelatedOpeningElement  # IfcOpeningElement

                # Check if the opening has fillings (windows)
                if hasattr(related_element, 'HasFillings'):  # IfcRelFillsElement-HasFillings
                    for related_filling in related_element.HasFillings:  # Loop through IfcRelFillsElement
                        if related_filling.RelatedBuildingElement.is_a('IfcWindow'):  # If the element is an IfcWindow
                            related_windows.append(related_filling.RelatedBuildingElement)  # Append window to list

        # If there are windows related to the wall, add it to the walls_info list
        if related_windows:
            walls_info.append((wall, related_windows))
    
    return walls_info


# Function to structure wall information
def wall_print(wall, height_wall, length_wall, width_wall, total_windows_area):
    return {
        'Dimensions': {'Height': height_wall, 'Length': length_wall, 'Width': width_wall},
        'GlobalId': wall.GlobalId,
        'WindowsArea': total_windows_area
    }

# Function to extract wall properties
def get_wall_dimensions(wall):
    psets_wall = ifcopenshell.util.element.get_psets(wall)
    if 'BaseQuantities' in psets_wall:
        base_quantities = psets_wall['BaseQuantities']
        return (
            base_quantities.get('Height'),
            base_quantities.get('Length'),
            base_quantities.get('Width')
        )
    return None, None, None

# Function to calculate total window area
def calculate_total_window_area(windows):
    total_windows_area = 0
    for window in windows:
        psets_window = ifcopenshell.util.element.get_psets(window)
        if 'Dimensions' in psets_window:
            window_area = psets_window['Dimensions'].get('Area')
            if window_area:
                total_windows_area += window_area
    return total_windows_area

# Main function
def main(model_path):
    model = ifcopenshell.open(model_path)
    walls = model.by_type('IfcWallStandardCase')
    
    walls_info = get_walls_have_windows(walls)  # Assuming this function exists
    
    results = []
    for wall, windows in walls_info:
        height_wall, length_wall, width_wall = get_wall_dimensions(wall)
        total_windows_area = calculate_total_window_area(windows)
        results.append(wall_print(wall, height_wall, length_wall, width_wall, total_windows_area))
    
    return results
         
# Main block
if __name__ == '__main__':
    model_path = 'BIM4EEB-TUD-2x3.ifc'
  
    walls_info = main(model_path)
    pprint(walls_info) #pprint A-Z
