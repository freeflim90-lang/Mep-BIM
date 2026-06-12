# -*- coding: utf-8 -*-

import clr
import csv
import os
from pyrevit import script, forms

from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System

from RevitServices.Persistence import DocumentManager

def collect_in_place_families(revit_doc):
    """
    Count the number of in-place families in a Revit document.

    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.

    Returns:
        int: The number of in-place families in the document.
    """
    try:
        collector = FilteredElementCollector(revit_doc).OfClass(FamilyInstance)
        model_in_place_elements = [elem for elem in collector if elem.Symbol.Family.IsInPlace]
        return len(model_in_place_elements)
    except Exception as e:
        logger.error("Error collecting in-place families for {}: {}".format(revit_doc.Title, str(e)))
        return 0

def get_non_builtin_categories_count(revit_doc):
    """
    Count the number of invalid built-in categories in the document using BuiltInCategory.INVALID.

    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.

    Returns:
        int: The number of invalid built-in categories.
    """
    try:
        all_categories = revit_doc.Settings.Categories
        non_builtin = []

        for category in all_categories:
            # Check if the category is not a built-in category
            if category.Id.IntegerValue < 0:  # Built-in categories have negative IDs
                continue
            non_builtin.append(category)

        count = len(non_builtin)
        return count
    except Exception as e:
        logger.error("Error counting invalid built-in categories in {}: {}".format(revit_doc.Title, str(e)))
        return 0

def collect_basic_data(docs, output_dir, file_name):
    """
    Collect basic audit data from a list of Revit documents and export to a CSV file.

    Args:
        docs (list): A list of Revit document objects.
        output_dir (str): The directory path where the CSV file will be saved.
        file_name (str): The name of the CSV file.

    Returns:
        str: A success message if the CSV export is successful, or an error message if an exception occurs.
    """
    output_path = os.path.join(output_dir, file_name)  # Ensure path is correct
    fieldnames = ['Document Name',
                  'Document Type',
                  'Purgeable Elements',
                  'Detail Groups',
                  'Detail Group Instances',
                  'In-Place Families',
                  'Non-Builtin Categories']
    data = []
    errors = []
    
    if not docs:
        errors.append("No documents provided for processing.")
        logger.error("No documents provided for processing.")
        return "No documents provided for processing."

    # Log how many documents we're processing
    logger.info("Processing {} documents for basic data collection".format(len(docs)))
    
    # Get the host document (first in the list)
    host_doc = docs[0] if docs else None
    
    for i, doc in enumerate(docs):
        if doc:  # Check if document is not null
            try:
                # Determine document type (host or linked)
                doc_type = "Host" if i == 0 else "Linked"
                
                # Log which document we're currently processing
                logger.info("Processing {}: {}".format(doc_type, doc.Title))
                
                unused_elements_count = sum(1 for elem in FilteredElementCollector(doc).OfClass(Family) 
                                           if not FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())
                
                detail_groups = len(set(g.Name for g in FilteredElementCollector(doc).OfClass(Group) 
                                       if g.GroupType and g.GroupType.FamilyName == "Detail Group"))
                
                detail_group_instances = len([g for g in FilteredElementCollector(doc).OfClass(Group) 
                                           if g.GroupType and g.GroupType.FamilyName == "Detail Group"])
                
                in_place_count = collect_in_place_families(doc)
                non_builtin_count = get_non_builtin_categories_count(doc)

                data.append({
                    'Document Name': doc.Title,
                    'Document Type': doc_type,
                    'Purgeable Elements': unused_elements_count,
                    'Detail Groups': detail_groups,
                    'Detail Group Instances': detail_group_instances,
                    'In-Place Families': in_place_count,
                    'Non-Builtin Categories': non_builtin_count
                    })
                
                logger.info("Successfully processed {}".format(doc.Title))
                
            except Exception as e:
                errors.append("Error processing document {}: {}".format(doc.Title, str(e)))
                logger.error("Error processing document {}: {}".format(doc.Title, str(e)))
        else:
            errors.append("Encountered a null document; skipping.")
            logger.warning("Encountered a null document; skipping.")

    # Write data to CSV if data was collected
    if data:
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            table_html = "<table>"
            table_html += "<tr>" + "".join("<th>{}</th>".format(field) for field in fieldnames[:5]) + "</tr>"
            for row in data[:10]:
                table_html += "<tr>" + "".join("<td>{}</td>".format(row[field]) for field in fieldnames[:5]) + "</tr>"
            table_html += "</table>"

            result_message = "CSV export successful. Exported data for {} documents.\n\n".format(len(data)) + table_html

        except Exception as e:
            result_message = "Failed to export CSV. Error: {}".format(str(e))
            logger.error("Failed to export CSV. Error: {}".format(str(e)))
    else:
        result_message = "No data to export."
        logger.warning("No data to export.")

    # Combine result message with any errors
    if errors:
        result_message += "\n" + "\n".join(errors)

    return result_message