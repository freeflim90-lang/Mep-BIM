# -*- coding: utf-8 -*-

import clr
import os
import csv
import codecs  # NEW: Import codecs for IronPython 2.7 compatibility
from lib.warning import collect_warning_data
from lib.basic import collect_basic_data
from lib.workset import collect_workset_data
from lib.view import collect_view_data
from lib.preview import show_audit_preview
from lib.ui import show_ui
from lib.discipline_mapper import show_discipline_mapper, DISCIPLINE_CODES  # NEW: Import discipline mapper
from pyrevit import script, forms

from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

doc = __revit__.ActiveUIDocument.Document

def validate_user_inputs(user_inputs):
    """Validate user inputs before processing."""
    if user_inputs is None:
        logger.warning("User cancelled the input.")
        return False, "User cancelled the input."

    # Check if output directory is specified
    if not user_inputs.get('output_dir'):
        logger.error("Error: Output directory is required.")
        return False, "Error: Output directory is required."
    
    # Check if at least one audit type is enabled
    if not any([user_inputs.get('enable_basic'), user_inputs.get('enable_workset'), user_inputs.get('enable_view')]):
        logger.error("Error: At least one audit type must be enabled.")
        return False, "Error: At least one audit type must be enabled."
    
    # Validate basic audit inputs
    if user_inputs.get('enable_basic'):
        if not all([user_inputs.get('warning_file_name'), user_inputs.get('audit_file_name')]):
            logger.error("Error: Warning and audit file names are required for basic audit.")
            return False, "Error: Warning and audit file names are required for basic audit."
    
    # Validate workset audit inputs
    if user_inputs.get('enable_workset'):
        if not all([user_inputs.get('workset_file_name'), user_inputs.get('view_keyword')]):
            logger.error("Error: Workset file name and view keyword are required for workset audit.")
            return False, "Error: Workset file name and view keyword are required for workset audit."
    
    # Validate view audit inputs
    if user_inputs.get('enable_view'):
        if not all([user_inputs.get('view_file_name'), user_inputs.get('view_patterns')]):
            logger.error("Error: View file name and patterns are required for view audit.")
            return False, "Error: View file name and patterns are required for view audit."
    
    return True, "Validation successful"

def collect_audit_data(linked_docs, user_inputs, discipline_mapping=None):  # NEW: Added discipline_mapping parameter
    """Collect all audit data without exporting to files"""
    audit_results = {
        'warning_data': [],
        'basic_data': [],
        'workset_data': [],
        'view_data': []
    }
    
    try:
        # Collect basic audit data (warnings and model health)
        if user_inputs.get('enable_basic', False):
            logger.info("Collecting basic audit data...")
            
            # Collect warnings
            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        # NEW: Get discipline info for this document
                        doc_name = doc_obj.Title
                        discipline_code = discipline_mapping.get(doc_name, 'OTHER') if discipline_mapping else 'N/A'
                        discipline_full = DISCIPLINE_CODES.get(discipline_code, 'Unknown') if discipline_mapping else 'N/A'
                        
                        warnings = doc_obj.GetWarnings()
                        workset_table = doc_obj.GetWorksetTable() if doc_obj.IsWorkshared else None
                        
                        for warning in warnings:
                            description = warning.GetDescriptionText()
                            failing_elements = warning.GetFailingElements()
                            elements_detail = []
                            
                            for elem_id in failing_elements:
                                elem = doc_obj.GetElement(elem_id)
                                if elem:
                                    category = elem.Category.Name if elem.Category else "No Category"
                                    try:
                                        name = elem.Name
                                    except:
                                        name = elem.LookupParameter("Name").AsString() if elem.LookupParameter("Name") else "Not a Name"
                                        if not name:
                                            name = "Not a Name"
                                    
                                    workset_name = "No Workset"
                                    if workset_table:
                                        try:
                                            workset_id = elem.WorksetId
                                            workset = workset_table.GetWorkset(workset_id)
                                            workset_name = workset.Name if workset else "No Workset"
                                        except:
                                            pass
                                    
                                    elements_detail.append("{}: <{}> {}: [{}]".format(workset_name, category, name, elem_id))  # FIXED
                            
                            audit_results['warning_data'].append({
                                'Document Name': doc_name,
                                'Discipline': discipline_full,  # NEW
                                'Discipline Code': discipline_code,  # NEW
                                'Warning Descriptions': description,
                                'Related Elements': '; '.join(elements_detail)
                            })
                    except Exception as e:
                        logger.error("Error collecting warnings from {}: {}".format(doc_obj.Title, str(e)))  # FIXED
            
            # Collect basic model health data
            from lib.basic import collect_in_place_families, get_non_builtin_categories_count
            from lib.view import get_hidden_views_info

            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        # NEW: Get discipline info
                        doc_name = doc_obj.Title
                        discipline_code = discipline_mapping.get(doc_name, 'OTHER') if discipline_mapping else 'N/A'
                        discipline_full = DISCIPLINE_CODES.get(discipline_code, 'Unknown') if discipline_mapping else 'N/A'
                        
                        # Collect in-place families
                        in_place_count = collect_in_place_families(doc_obj)

                        # Collect other metrics
                        unused_elements_count = sum(
                            1 for elem in FilteredElementCollector(doc_obj).OfClass(Family)
                            if not FilteredElementCollector(doc_obj).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())

                        detail_groups = len(
                            set(g.Name for g in FilteredElementCollector(doc_obj).OfClass(Group)
                                if g.GroupType.FamilyName == "Detail Group"))

                        detail_group_instances = len(
                            [g for g in FilteredElementCollector(doc_obj).OfClass(Group)
                             if g.GroupType.FamilyName == "Detail Group"])

                        # Get non-builtin categories count
                        non_builtin_count = get_non_builtin_categories_count(doc_obj)

                        # Get hidden views info
                        hidden_views_count, hidden_views_info = get_hidden_views_info(doc_obj)

                        audit_results['basic_data'].append({
                            'Document Name': doc_name,
                            'Discipline': discipline_full,  # NEW
                            'Discipline Code': discipline_code,  # NEW
                            'Purgeable Elements': unused_elements_count,
                            'Detail Groups': detail_groups,
                            'Detail Group Instances': detail_group_instances,
                            'In-Place Families': in_place_count,
                            'Non-Builtin Categories': non_builtin_count,
                            'Hidden Views on Sheets': hidden_views_count,
                            'View Names & Sheet Names': hidden_views_info
                        })
                    except Exception as e:
                        logger.error("Error collecting basic data from {}: {}".format(doc_obj.Title, str(e)))  # FIXED
        
        # Collect workset data
        if user_inputs.get('enable_workset', False):
            logger.info("Collecting workset audit data...")
            from lib.workset import get_3d_views_with_keyword, get_worksets_by_visibility_in_view, get_all_worksets_simple
            
            for doc_obj in linked_docs:
                if doc_obj and doc_obj.IsWorkshared:
                    try:
                        doc_name = doc_obj.Title
                        
                        # NEW: Get discipline info
                        discipline_code = discipline_mapping.get(doc_name, 'OTHER') if discipline_mapping else 'N/A'
                        discipline_full = DISCIPLINE_CODES.get(discipline_code, 'Unknown') if discipline_mapping else 'N/A'
                        
                        # Get 3D views with keyword
                        matching_views = get_3d_views_with_keyword(
                            doc_obj, 
                            doc_name, 
                            user_inputs.get('view_keyword', 'Revizto')
                        )
                        
                        if matching_views:
                            for view_info in matching_views:
                                try:
                                    view = doc_obj.GetElement(ElementId(view_info['view_id']))
                                    if view:
                                        visible, hidden = get_worksets_by_visibility_in_view(doc_obj, view, doc_name)
                                        
                                        for workset in visible + hidden:
                                            audit_results['workset_data'].append({
                                                'Document Name': doc_name,
                                                'Discipline': discipline_full,  # NEW
                                                'Discipline Code': discipline_code,  # NEW
                                                'View Name': workset['view_name'],
                                                'View ID': workset['view_id'],
                                                'Workset Name': workset['workset_name'],
                                                'Workset ID': workset['workset_id'],
                                                'Visibility Setting': workset['visibility_setting'],
                                                'Actually Visible': workset['is_actually_visible'],
                                                'Is Open': workset['is_open'],
                                                'Owner': workset['owner']
                                            })
                                except Exception as e:
                                    logger.error("Error processing view {} in {}: {}".format(view_info['view_name'], doc_name, str(e)))
                        else:
                            # Fallback: get all worksets
                            all_worksets = get_all_worksets_simple(doc_obj, doc_name)
                            for workset in all_worksets:
                                audit_results['workset_data'].append({
                                    'Document Name': doc_name,
                                    'Discipline': discipline_full,  # NEW
                                    'Discipline Code': discipline_code,  # NEW
                                    'View Name': 'N/A',
                                    'View ID': 'N/A',
                                    'Workset Name': workset['workset_name'],
                                    'Workset ID': workset['workset_id'],
                                    'Visibility Setting': 'N/A',
                                    'Actually Visible': 'N/A',
                                    'Is Open': workset['is_open'],
                                    'Owner': workset['owner']
                                })
                    except Exception as e:
                        logger.error("Error processing document {}: {}".format(doc_obj.Title, str(e)))
        
        # Collect view data
        if user_inputs.get('enable_view', False):
            logger.info("Collecting view audit data...")
            from lib.view import get_all_views_by_type, check_view_name_compliance, get_view_details
            
            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        doc_name = doc_obj.Title
                        
                        # NEW: Get discipline info
                        discipline_code = discipline_mapping.get(doc_name, 'OTHER') if discipline_mapping else 'N/A'
                        discipline_full = DISCIPLINE_CODES.get(discipline_code, 'Unknown') if discipline_mapping else 'N/A'
                        
                        # Get all views
                        all_views = get_all_views_by_type(doc_obj, user_inputs.get('view_types'))
                        
                        for view in all_views:
                            try:
                                view_details = get_view_details(view, doc_obj)
                                compliance = check_view_name_compliance(view.Name, user_inputs.get('view_patterns', []))
                                
                                audit_results['view_data'].append({
                                    'Document Name': doc_name,
                                    'Discipline': discipline_full,  # NEW
                                    'Discipline Code': discipline_code,  # NEW
                                    'View Name': view_details['name'],
                                    'View ID': view_details['id'],
                                    'View Type': view_details['view_type'],
                                    'Scale': view_details['scale'],
                                    'Is Compliant': compliance['is_compliant'],
                                    'Matched Patterns': '; '.join(compliance['matched_patterns']),
                                    'Failed Patterns': '; '.join(compliance['failed_patterns']),
                                    'Exclusion Violations': '; '.join(compliance['exclusion_violations']),
                                    'Detail Level': view_details['detail_level'],
                                    'Phase': view_details['phase'],
                                    'Is On Sheet': view_details['is_on_sheet'],
                                    'Sheet Count': view_details['sheet_count']
                                })
                            except Exception as e:
                                logger.error("Error processing view {} in {}: {}".format(view.Name, doc_name, str(e)))
                    except Exception as e:
                        logger.error("Error processing document {}: {}".format(doc_obj.Title, str(e)))
        
    except Exception as e:
        logger.error("Error in data collection: {}".format(str(e)))
    
    return audit_results

def export_audit_data(audit_results, user_inputs):
    """Export collected audit data to CSV files"""
    export_status = []
    
    try:
        output_dir = user_inputs['output_dir']
        
        # Export warnings
        if user_inputs.get('enable_basic') and audit_results['warning_data']:
            try:
                warning_path = os.path.join(output_dir, user_inputs['warning_file_name'])
                fieldnames = ['Document Name', 'Discipline', 'Discipline Code', 'Warning Descriptions', 'Related Elements']  # UPDATED
                
                # Use codecs.open for IronPython 2.7 compatibility
                with codecs.open(warning_path, 'w', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['warning_data'])
                
                export_status.append("[SUCCESS] Warning data exported: {}".format(warning_path))
            except Exception as e:
                export_status.append("[ERROR] Warning export failed: {}".format(str(e)))
        
        # Export basic audit
        if user_inputs.get('enable_basic') and audit_results['basic_data']:
            try:
                audit_path = os.path.join(output_dir, user_inputs['audit_file_name'])
                fieldnames = ['Document Name', 'Discipline', 'Discipline Code', 'Purgeable Elements', 'Detail Groups',   # UPDATED
                            'Detail Group Instances', 'In-Place Families', 'Non-Builtin Categories',
                            'Hidden Views on Sheets', 'View Names & Sheet Names']
                
                # Use codecs.open for IronPython 2.7 compatibility
                with codecs.open(audit_path, 'w', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['basic_data'])
                
                export_status.append("[SUCCESS] Basic audit data exported: {}".format(audit_path))
            except Exception as e:
                export_status.append("[ERROR] Basic audit export failed: {}".format(str(e)))
        
        # Export workset data
        if user_inputs.get('enable_workset') and audit_results['workset_data']:
            try:
                workset_path = os.path.join(output_dir, user_inputs['workset_file_name'])
                fieldnames = ['Document Name', 'Discipline', 'Discipline Code', 'View Name', 'View ID',   # UPDATED
                            'Workset Name', 'Workset ID', 'Visibility Setting', 'Actually Visible',
                            'Is Open', 'Owner']
                
                # Use codecs.open for IronPython 2.7 compatibility
                with codecs.open(workset_path, 'w', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['workset_data'])
                
                export_status.append("[SUCCESS] Workset data exported: {}".format(workset_path))
            except Exception as e:
                export_status.append("[ERROR] Workset export failed: {}".format(str(e)))
        
        # Export view data
        if user_inputs.get('enable_view') and audit_results['view_data']:
            try:
                view_path = os.path.join(output_dir, user_inputs['view_file_name'])
                fieldnames = ['Document Name', 'Discipline', 'Discipline Code', 'View Name', 'View ID',   # UPDATED
                            'View Type', 'Scale', 'Is Compliant', 'Matched Patterns', 'Failed Patterns',
                            'Exclusion Violations', 'Detail Level', 'Phase', 'Is On Sheet', 'Sheet Count']
                
                # Use codecs.open for IronPython 2.7 compatibility
                with codecs.open(view_path, 'w', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['view_data'])
                
                export_status.append("[SUCCESS] View data exported: {}".format(view_path))
            except Exception as e:
                export_status.append("[ERROR] View export failed: {}".format(str(e)))
                
    except Exception as e:
        export_status.append("[ERROR] Export error: {}".format(str(e)))
    
    return export_status

def gather_documents():
    """Safely gather main document and linked documents."""
    linked_docs = []
    
    # Add main document if available
    if doc:
        linked_docs.append(doc)
        logger.info("Added main document: {}".format(doc.Title))
    else:
        logger.error("Error: No active document found.")
        return []

    # Gather linked documents
    try:
        link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
        linked_count = 0
        
        for link in link_instances:
            linked_doc = link.GetLinkDocument()
            if linked_doc:  # Check if the linked document is loaded
                linked_docs.append(linked_doc)
                linked_count += 1
                logger.info("Added linked document: {}".format(linked_doc.Title))
            else:
                logger.warning("Warning: Linked document could not be loaded: {}".format(link.Name))
        
        logger.info("Total documents gathered: {} (1 main + {} linked)".format(len(linked_docs), linked_count))  # FIXED
        
    except Exception as e:
        logger.error("Error gathering linked documents: {}".format(str(e)))
    
    return linked_docs

def main():
    """Main execution function with enhanced preview and export workflow."""
    output = script.get_output()
    
    # Show extended UI
    user_inputs = show_ui()
    
    # Validate inputs
    is_valid, validation_message = validate_user_inputs(user_inputs)
    if not is_valid:
        output.print_html("<p style='color: red;'>{}</p>".format(validation_message))
        return

    try:
        # Gather documents
        linked_docs = gather_documents()
        if not linked_docs:
            output.print_html("<p style='color: red;'>Error: No documents available for processing.</p>")
            return

        # NEW: Show discipline mapper
        output.print_html("<h2>AutoAudit Processing</h2>")
        output.print_html("<h3>Step 1: Assign Disciplines</h3>")
        output.print_html("<p>Opening discipline assignment window...</p>")
        
        discipline_mapping = show_discipline_mapper(linked_docs, project_doc=doc)  # Pass project doc for config
        
        if not discipline_mapping:
            output.print_html("<p style='color: red;'>Discipline assignment cancelled. Cannot proceed without discipline information.</p>")
            return
        
        # Display discipline assignments
        output.print_html("<h4>Discipline Assignments:</h4>")
        output.print_html("<ul>")
        for doc_name, discipline_code in discipline_mapping.items():
            discipline_full = DISCIPLINE_CODES.get(discipline_code, 'Unknown')
            output.print_html("<li><strong>{}</strong> → {} ({})</li>".format(doc_name, discipline_code, discipline_full))
        output.print_html("</ul>")

        # Display initial processing info
        output.print_html("<h3>Step 2: Collect Audit Data</h3>")
        output.print_html("<p><strong>Documents to process:</strong> {}</p>".format(len(linked_docs)))
        output.print_html("<p><strong>Output directory:</strong> {}</p>".format(user_inputs['output_dir']))
        
        enabled_audits = []
        if user_inputs.get('enable_basic'): enabled_audits.append("Basic Audit")
        if user_inputs.get('enable_workset'): enabled_audits.append("Workset Audit")
        if user_inputs.get('enable_view'): enabled_audits.append("View Audit")
        
        output.print_html("<p><strong>Enabled audits:</strong> {}</p>".format(', '.join(enabled_audits)))
        output.print_html("<p>Collecting audit data...</p>")

        # Collect all audit data (now with discipline mapping)
        audit_results = collect_audit_data(linked_docs, user_inputs, discipline_mapping)
        
        # Show data counts
        data_summary = []
        if audit_results['warning_data']: 
            data_summary.append("{} warnings".format(len(audit_results['warning_data'])))
        if audit_results['basic_data']: 
            data_summary.append("{} documents analyzed".format(len(audit_results['basic_data'])))
        if audit_results['workset_data']: 
            data_summary.append("{} workset entries".format(len(audit_results['workset_data'])))
        if audit_results['view_data']: 
            data_summary.append("{} views analyzed".format(len(audit_results['view_data'])))
        
        output.print_html("<p><strong>Data collected:</strong> {}</p>".format(', '.join(data_summary)))
        
        # NEW: Show discipline breakdown
        output.print_html("<h4>Data by Discipline:</h4>")
        discipline_counts = {}
        for data_type in ['warning_data', 'basic_data', 'workset_data', 'view_data']:
            for row in audit_results[data_type]:
                disc = row.get('Discipline Code', 'N/A')
                if disc not in discipline_counts:
                    discipline_counts[disc] = {'warnings': 0, 'basic': 0, 'worksets': 0, 'views': 0}
                
                if data_type == 'warning_data':
                    discipline_counts[disc]['warnings'] += 1
                elif data_type == 'basic_data':
                    discipline_counts[disc]['basic'] += 1
                elif data_type == 'workset_data':
                    discipline_counts[disc]['worksets'] += 1
                elif data_type == 'view_data':
                    discipline_counts[disc]['views'] += 1
        
        output.print_html("<ul>")
        for disc_code, counts in sorted(discipline_counts.items()):
            disc_name = DISCIPLINE_CODES.get(disc_code, 'Unknown')
            count_str = []
            if counts['warnings'] > 0: count_str.append("{} warnings".format(counts['warnings']))
            if counts['basic'] > 0: count_str.append("{} docs".format(counts['basic']))
            if counts['worksets'] > 0: count_str.append("{} worksets".format(counts['worksets']))
            if counts['views'] > 0: count_str.append("{} views".format(counts['views']))
            
            output.print_html("<li><strong>{} ({})</strong>: {}</li>".format(disc_code, disc_name, ', '.join(count_str)))
        output.print_html("</ul>")
        
        output.print_html("<h3>Step 3: Preview and Export</h3>")
        output.print_html("<p>Opening preview window...</p>")
        
        # Show preview and get user confirmation
        user_wants_export = show_audit_preview(
            warning_data=audit_results['warning_data'],
            basic_data=audit_results['basic_data'],
            workset_data=audit_results['workset_data'],
            view_data=audit_results['view_data']
        )
        
        if user_wants_export:
            output.print_html("<p>Exporting data to CSV files...</p>")
            
            # Export data to CSV files
            export_status = export_audit_data(audit_results, user_inputs)
            
            # Show export results
            output.print_html("<h3>Export Results:</h3>")
            for status in export_status:
                if status.startswith("[SUCCESS]"):
                    output.print_html("<p style='color: green;'>{}</p>".format(status))
                else:
                    output.print_html("<p style='color: red;'>{}</p>".format(status))
            
            output.print_html("<hr>")
            output.print_html("<h3>Processing Complete!</h3>")
            output.print_html("<p>Check the output directory: <strong>{}</strong></p>".format(user_inputs['output_dir']))
            output.print_html("<p><em>Note: All CSV files now include Discipline and Discipline Code columns.</em></p>")
            
        else:
            output.print_html("<p>Export cancelled by user.</p>")
            output.print_html("<p>Data was collected successfully but not exported to files.</p>")
        
        logger.info("AutoAudit processing completed")

    except Exception as e:
        error_msg = "Unexpected error during processing: {}".format(str(e))
        logger.error(error_msg)
        output.print_html("<p style='color: red;'>{}</p>".format(error_msg))
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()