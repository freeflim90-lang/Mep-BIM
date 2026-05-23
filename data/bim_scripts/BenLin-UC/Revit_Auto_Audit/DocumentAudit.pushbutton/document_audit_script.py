# -*- coding: utf-8 -*-
"""
Document Audit Script - Main execution script
Compatible with IronPython 2.7 for PyRevit.
"""
from __future__ import print_function, division

import clr
import os
import csv
import re
import codecs

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

from lib import (
    GridAnalyzer,
    LevelAnalyzer,
    SurveyAnalyzer,
    logger
)
from lib.ui import show_dialog, show_data_preview, show_coordinate_system_dialog
from lib.unit_utils import normalize_coordinate_system
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document


def sanitize_filename(filename):
    """Sanitize filename for Windows compatibility"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename.strip('. ')


def combine_data_for_csv(grid_data, level_data, survey_data):
    """Combine all data into a single structured format"""
    combined_data = []
    
    # Process host document
    if grid_data and 'host_doc' in grid_data:
        host_doc = grid_data['host_doc']
        host_name = host_doc['name']
        
        # Find corresponding level and survey data
        host_levels = None
        host_survey = None
        
        for data in level_data:
            if data['Document Name'] == host_name:
                host_levels = data
                break
        
        for data in survey_data:
            if data['Document Name'] == host_name:
                host_survey = data
                break
        
        # Format True North to 3 decimal places if it's a number
        true_north = host_survey['True North Angle'] if host_survey else 'No Data'
        if true_north != 'No Data':
            try:
                true_north = "{0:.3f}".format(float(true_north))
            except (ValueError, TypeError):
                pass
        
        combined_data.append({
            'Document Name': host_name,
            'Document Type': 'Host',
            'Project Base Point': host_survey['Project Base Coordinate'] if host_survey else 'No Data',
            'True North': true_north,
            'Survey Point': host_survey['Survey Coordinate'] if host_survey else 'No Data',
            'Level Data': host_levels['Level Data'] if host_levels else 'No Data',
            'Grid Data': host_doc.get('grid_data', 'No Data'),
        })
    
    # Process linked documents
    if grid_data and 'linked_docs' in grid_data:
        for doc_name, link_data in grid_data['linked_docs'].items():
            # Find corresponding level and survey data
            link_levels = None
            link_survey = None
            
            for data in level_data:
                if data['Document Name'] == doc_name:
                    link_levels = data
                    break
            
            for data in survey_data:
                if data['Document Name'] == doc_name:
                    link_survey = data
                    break
            
            # Format True North to 3 decimal places if it's a number
            true_north = link_survey['True North Angle'] if link_survey else 'No Data'
            if true_north != 'No Data':
                try:
                    true_north = "{0:.3f}".format(float(true_north))
                except (ValueError, TypeError):
                    pass
            
            combined_data.append({
                'Document Name': doc_name,
                'Document Type': 'Linked',
                'Project Base Point': link_survey['Project Base Coordinate'] if link_survey else 'No Data',
                'True North': true_north,
                'Survey Point': link_survey['Survey Coordinate'] if link_survey else 'No Data',
                'Level Data': link_levels['Level Data'] if link_levels else 'No Data',
                'Grid Data': link_data.get('grid_data', 'No Data'),
            })
    
    return combined_data


def write_csv_data(data, filepath):
    """Write data to CSV file"""
    try:
        # Define field order explicitly
        fieldnames = [
            'Document Name',
            'Document Type',
            'Project Base Point',
            'True North',
            'Survey Point',
            'Level Data',
            'Grid Data'
        ]
        
        # Use codecs.open for Python 2.7 UTF-8 support
        with codecs.open(filepath, 'w', encoding='utf-8') as csvfile:
            # Write UTF-8 BOM for Excel compatibility
            csvfile.write(u'\ufeff')
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                # Handle encoding for Python 2.7
                encoded_row = {}
                for key, value in row.items():
                    if isinstance(value, unicode):
                        encoded_row[key] = value.encode('utf-8')
                    elif isinstance(value, str):
                        encoded_row[key] = value
                    else:
                        encoded_row[key] = str(value)
                writer.writerow(encoded_row)
        return True
    except Exception as e:
        logger.error("Error writing CSV file {0}: {1}".format(filepath, str(e)))
        return False


def process_document():
    """Process the active document and its linked documents"""
    try:
        # First, ask the user to select a coordinate system
        coordinate_system = show_coordinate_system_dialog()
        if not coordinate_system:
            logger.info("Operation cancelled - no coordinate system selected")
            return False
            
        logger.info("Selected coordinate system: {0}".format(coordinate_system))
        
        # Initialize analyzers
        grid_analyzer = GridAnalyzer(doc)
        level_analyzer = LevelAnalyzer(doc)
        survey_analyzer = SurveyAnalyzer(doc)

        # Collect data using the selected coordinate system
        grid_data = grid_analyzer.collect_all_grid_data(coordinate_system)
        level_data = level_analyzer.collect_all_level_data()
        survey_data = survey_analyzer.collect_all_survey_data()

        # Format data for preview
        grid_csv_data = grid_analyzer.format_for_csv(grid_data)
        level_csv_data = level_analyzer.format_for_csv(level_data)
        survey_csv_data = survey_analyzer.format_for_csv(survey_data)

        # Show preview with the selected coordinate system
        preview_result = show_data_preview(grid_csv_data, level_csv_data, survey_csv_data, coordinate_system)
        if not preview_result:
            logger.info("Operation cancelled after preview")
            return False

        # Show UI and get user inputs
        user_inputs = show_dialog()
        if not user_inputs:
            logger.info("Operation cancelled by user")
            return False

        # Create output directory if it doesn't exist
        output_dir = user_inputs['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Combine and write data
        combined_data = combine_data_for_csv(grid_data, level_csv_data, survey_csv_data)
        
        # Create filename with coordinate system indicator
        coordinate_system = normalize_coordinate_system(coordinate_system)
        combined_path = os.path.join(output_dir, 'document_audit_data_{0}.csv'.format(coordinate_system))
        
        if write_csv_data(combined_data, combined_path):
            forms.alert(
                'Document audit completed successfully.',
                title='Success',
                sub_msg='Data has been exported to: {0}'.format(combined_path)
            )
            logger.info("Document audit completed successfully: {0}".format(combined_path))
            return True
        else:
            forms.alert(
                'Failed to export audit data.',
                title='Error',
                sub_msg='Check the log file for details.'
            )
            logger.error("Failed to export audit data")
            return False

    except Exception as e:
        logger.error("Error in document audit: {0}".format(str(e)))
        forms.alert(
            'An error occurred during document audit.',
            title='Error',
            sub_msg=str(e)
        )
        return False


if __name__ == '__main__':
    process_document()