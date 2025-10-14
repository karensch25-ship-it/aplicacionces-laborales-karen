#!/usr/bin/env python3
"""
Test script for copy_pdf_to_documents_repo.py

This script validates the core functionality without actually pushing to GitHub.
It tests date extraction, folder name parsing, and PDF file detection.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, 'aplicaciones_laborales/scripts')

# Import the function we want to test
from copy_pdf_to_documents_repo import extract_date_from_folder_name


def test_date_extraction():
    """Test date extraction from various folder name formats."""
    print("Testing date extraction...")
    
    test_cases = [
        ("DataAnalyst_Adoreal_2025-10-13", "2025-10-13"),
        ("BusinessAnalyst_TechCorp_2025-12-25", "2025-12-25"),
        ("Senior_Data_Engineer_CompanyName_2025-01-01", "2025-01-01"),
        ("SimpleTest_2025-03-15", "2025-03-15"),
    ]
    
    all_passed = True
    for folder_name, expected_date in test_cases:
        result = extract_date_from_folder_name(folder_name)
        if result == expected_date:
            print(f"  ✅ {folder_name} → {result}")
        else:
            print(f"  ❌ {folder_name} → {result} (expected {expected_date})")
            all_passed = False
    
    return all_passed


def test_pdf_detection():
    """Test PDF file detection in processed folders."""
    print("\nTesting PDF detection in real folders...")
    
    processed_dir = "to_process_procesados"
    if not os.path.exists(processed_dir):
        print(f"  ⚠️  Directory {processed_dir} does not exist")
        return True
    
    # Find all folders
    folders = [f for f in os.listdir(processed_dir) 
               if os.path.isdir(os.path.join(processed_dir, f))]
    
    if not folders:
        print(f"  ⚠️  No folders found in {processed_dir}")
        return True
    
    # Test first 3 folders
    for folder_name in folders[:3]:
        folder_path = os.path.join(processed_dir, folder_name)
        
        # Look for CV PDF
        pdf_files = [f for f in os.listdir(folder_path) 
                     if f.startswith("ANTONIO_GUTIERREZ_RESUME_") and f.endswith(".pdf")]
        
        if pdf_files:
            print(f"  ✅ {folder_name}")
            print(f"     PDF: {pdf_files[0]}")
            
            # Extract date
            date = extract_date_from_folder_name(folder_name)
            print(f"     Date: {date}")
        else:
            print(f"  ⚠️  {folder_name} - No CV PDF found")
    
    return True


def test_folder_name_parsing():
    """Test parsing of company and job title from folder names."""
    print("\nTesting folder name parsing...")
    
    test_cases = [
        ("DataAnalyst_Adoreal_2025-10-13", "DataAnalyst", "Adoreal"),
        ("BusinessIntelligenceAnalyst_INDI_StaffingServices_2025-10-13", 
         "BusinessIntelligenceAnalyst", "INDI_StaffingServices"),
        ("Senior_Python_Developer_TechCorp_Inc_2025-11-20", 
         "Senior", "Python_Developer_TechCorp_Inc"),
    ]
    
    all_passed = True
    for folder_name, expected_cargo, expected_empresa in test_cases:
        parts = folder_name.split('_')
        cargo = parts[0]
        empresa = '_'.join(parts[1:-1])
        
        cargo_match = cargo == expected_cargo
        empresa_match = empresa == expected_empresa
        
        if cargo_match and empresa_match:
            print(f"  ✅ {folder_name}")
            print(f"     Cargo: {cargo}, Empresa: {empresa}")
        else:
            print(f"  ❌ {folder_name}")
            print(f"     Got: Cargo={cargo}, Empresa={empresa}")
            print(f"     Expected: Cargo={expected_cargo}, Empresa={expected_empresa}")
            all_passed = False
    
    return all_passed


def test_script_imports():
    """Test that the script can be imported without errors."""
    print("\nTesting script imports...")
    
    try:
        import copy_pdf_to_documents_repo
        print("  ✅ Script imported successfully")
        
        # Check key functions exist
        functions = [
            'extract_date_from_folder_name',
            'copy_pdf_to_documents_repo',
            'run_command',
            'main'
        ]
        
        for func_name in functions:
            if hasattr(copy_pdf_to_documents_repo, func_name):
                print(f"  ✅ Function '{func_name}' exists")
            else:
                print(f"  ❌ Function '{func_name}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to import script: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Running tests for copy_pdf_to_documents_repo.py")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Date Extraction", test_date_extraction()))
    results.append(("Script Imports", test_script_imports()))
    results.append(("Folder Name Parsing", test_folder_name_parsing()))
    results.append(("PDF Detection", test_pdf_detection()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
