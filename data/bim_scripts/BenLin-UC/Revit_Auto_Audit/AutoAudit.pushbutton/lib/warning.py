# -*- coding: utf-8 -*-

import clr
import csv
import os
from pyrevit import script
from _collections import deque

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

from __init__ import logger  # Import the logger from __init__.py

def generate_table_html(data, fieldnames, max_rows=10):
    """
    Generate an HTML table string from the given data.

    Args:
        data (list): A list of dictionaries containing the data.
        fieldnames (list): A list of fieldnames for the table headers.
        max_rows (int): The maximum number of rows to include in the table.

    Returns:
        str: An HTML string representing the table.
    """
    table_html = "<table>"
    table_html += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>".format(*fieldnames)
    for row in deque(data, maxlen=max_rows):
        table_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            row['Document Name'], 
            row['Document Type'],
            row['Warning Descriptions'], 
            row['Related Elements']
        )
    table_html += "</table>"
    return table_html

def collect_warning_data(docs, output_dir, file_name):
    """
    Collect warning data from a list of Revit documents and export to a CSV file.

    Args:
        docs (list): A list of Revit document objects.
        output_dir (str): The directory path where the CSV file will be saved.
        file_name (str): The name of the CSV file.

    Returns:
        str: A success message if the CSV export is successful, or an error message if an exception occurs.
    """
    output_path = os.path.join(output_dir, file_name)
    fieldnames = ['Document Name', 'Document Type', 'Warning Descriptions', 'Related Elements']
    data = []
    
    if not docs:
        logger.error("No documents provided for warning data collection")
        return "Error: No documents provided for processing."
    
    # Log how many documents we're processing
    logger.info("Processing {} documents for warning data collection".format(len(docs)))
    
    # Process each document, marking the first one as the host
    for i, doc in enumerate(docs):
        if doc:
            try:
                # Determine if this is the host document or a linked document
                doc_type = "Host" if i == 0 else "Linked"
                
                # Log which document we're currently processing
                logger.info("Processing warnings for {}: {}".format(doc_type, doc.Title))
                
                warnings = doc.GetWarnings()
                workset_table = doc.GetWorksetTable()  # Get the workset table from the document
                
                logger.info("Found {} warnings in {}".format(len(warnings), doc.Title))

                for warning in warnings:
                    description = warning.GetDescriptionText()
                    failing_elements = warning.GetFailingElements()
                    elements_detail = []

                    for elem_id in failing_elements:
                        elem = doc.GetElement(elem_id)
                        if elem:
                            try:
                                category = elem.Category.Name if elem.Category else "No Category"
                            except Exception:
                                category = "Category Error"
                                
                            try:
                                # Try to access the Name property directly
                                name = elem.Name
                            except (TypeError, AttributeError):
                                # Handles cases where elem.Name is not accessible
                                try:
                                    name_param = elem.LookupParameter("Name")
                                    name = name_param.AsString() if name_param else "Not a Name"
                                except Exception:
                                    name = "Name Error"
                                    
                                if not name:  # Fallback if parameter is None or empty
                                    name = "Not a Name"

                            # Retrieve workset information
                            try:
                                workset_id = elem.WorksetId
                                workset = workset_table.GetWorkset(workset_id)
                                workset_name = workset.Name if workset else "No Workset"
                            except Exception:
                                workset_name = "Workset Error"

                            elements_detail.append("{}: <{}> {}: [{}]".format(workset_name, category, name, elem_id))

                    related_elements = '; \n '.join(elements_detail)
                    data.append({
                        'Document Name': doc.Title,
                        'Document Type': doc_type,
                        'Warning Descriptions': description,
                        'Related Elements': related_elements
                    })
            except Exception as e:
                logger.error("Error processing warnings in document {}: {}".format(doc.Title, str(e)))
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning("Encountered a null document; skipping.")

    # Write data to CSV
    if not data:
        logger.info("No warning data found in any document.")
        return "No warning data found in any document."
        
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        error_msg = "Error: You don't have permission to write to {}".format(output_path)
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = "Error: Failed to export CSV. {}".format(str(e))
        logger.error(error_msg)
        return error_msg

    table_html = generate_table_html(data, fieldnames)
    heading = "<h3>Top Warning Entries</h3>" if table_html else ""
    result_message = "CSV export successful. Exported {} warnings.\n".format(len(data)) + heading + table_html

    return result_message