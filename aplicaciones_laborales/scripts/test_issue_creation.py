#!/usr/bin/env python3
"""
Test script for create_issue_and_add_to_project.py
Tests the parsing logic and validation without making actual API calls.
"""

import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from create_issue_and_add_to_project import parse_folder_metadata

def test_folder_parsing():
    """Test various folder name formats."""
    test_cases = [
        {
            'input': 'DataAnalyst_CompanyX_2025-10-13',
            'expected': {
                'cargo': 'DataAnalyst',
                'empresa': 'CompanyX',
                'fecha': '2025-10-13',
                'folder_name': 'DataAnalyst_CompanyX_2025-10-13'
            }
        },
        {
            'input': 'Senior_Data_Engineer_TechCorp_2025-11-01',
            'expected': {
                'cargo': 'Senior_Data_Engineer',
                'empresa': 'TechCorp',
                'fecha': '2025-11-01',
                'folder_name': 'Senior_Data_Engineer_TechCorp_2025-11-01'
            }
        },
        {
            'input': 'ML_Engineer_TechCorp_2025-12-25',
            'expected': {
                'cargo': 'ML_Engineer',
                'empresa': 'TechCorp',
                'fecha': '2025-12-25',
                'folder_name': 'ML_Engineer_TechCorp_2025-12-25'
            }
        },
        {
            'input': 'DataAnalyst-ColombiaRemote_Konduit_2025-10-11',
            'expected': {
                'cargo': 'DataAnalyst-ColombiaRemote',
                'empresa': 'Konduit',
                'fecha': '2025-10-11',
                'folder_name': 'DataAnalyst-ColombiaRemote_Konduit_2025-10-11'
            }
        },
    ]
    
    print("=" * 60)
    print("Testing folder name parsing")
    print("=" * 60)
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        result = parse_folder_metadata(test_case['input'])
        expected = test_case['expected']
        
        if result == expected:
            print(f"✅ Test {i} PASSED: {test_case['input']}")
        else:
            print(f"❌ Test {i} FAILED: {test_case['input']}")
            print(f"   Expected: {expected}")
            print(f"   Got:      {result}")
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ All tests PASSED!")
        return 0
    else:
        print("❌ Some tests FAILED!")
        return 1

def test_edge_cases():
    """Test edge cases for folder parsing."""
    print("\n" + "=" * 60)
    print("Testing edge cases")
    print("=" * 60)
    
    edge_cases = [
        {
            'input': 'InvalidFormat',
            'should_fail': True,
            'description': 'Single word (no underscores)'
        },
        {
            'input': 'Cargo_Empresa',
            'should_fail': True,
            'description': 'Missing date'
        },
        {
            'input': '',
            'should_fail': True,
            'description': 'Empty string'
        }
    ]
    
    all_passed = True
    for i, test_case in enumerate(edge_cases, 1):
        result = parse_folder_metadata(test_case['input'])
        is_none = result is None
        
        if test_case['should_fail'] and is_none:
            print(f"✅ Edge case {i} PASSED: {test_case['description']}")
        elif not test_case['should_fail'] and not is_none:
            print(f"✅ Edge case {i} PASSED: {test_case['description']}")
        else:
            print(f"❌ Edge case {i} FAILED: {test_case['description']}")
            print(f"   Expected to fail: {test_case['should_fail']}")
            print(f"   Result was None: {is_none}")
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ All edge cases handled correctly!")
        return 0
    else:
        print("❌ Some edge cases failed!")
        return 1

if __name__ == '__main__':
    result1 = test_folder_parsing()
    result2 = test_edge_cases()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if result1 == 0 and result2 == 0:
        print("✅ ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED!")
        sys.exit(1)
