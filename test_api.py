"""
Test script for the RAG DevKaluri API.

This script tests the API endpoints to ensure they're working correctly.
Run this after starting the API server to verify functionality.
"""

import requests
import json
import time
import sys

def test_api_endpoints():
    """Test all API endpoints."""
    base_url = "http://localhost:8000"
    
    print("=== RAG DevKaluri API Test Suite ===\n")
    
    # Test 1: Health Check
    print("1. Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        print("   Make sure the API server is running on http://localhost:8000")
        return False
    
    print()
    
    # Test 2: Root Endpoint
    print("2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            api_info = response.json()
            print(f"   API Version: {api_info.get('version', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
    
    print()
    
    # Test 3: Single Chat Query
    print("3. Testing Single Chat Query...")
    try:
        test_question = "Tell me about Dev"
        payload = {
            "question": test_question,
            "session_id": "test_session_1"
        }
        
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Single chat query passed")
            print(f"   Question: {result.get('question', 'N/A')}")
            print(f"   Answer: {result.get('answer', 'N/A')[:100]}...")
            print(f"   Status: {result.get('status', 'N/A')}")
        else:
            print(f"❌ Single chat query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Single chat query failed: {e}")
    
    print()
    
    # Test 4: Batch Chat Query
    print("4. Testing Batch Chat Query...")
    try:
        batch_questions = [
            {"question": "What are Dev's skills?", "session_id": "batch_test"},
            {"question": "What is Dev's background?", "session_id": "batch_test"}
        ]
        
        response = requests.post(
            f"{base_url}/chat/batch",
            json=batch_questions,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            results = response.json()
            print("✅ Batch chat query passed")
            print(f"   Processed {len(results)} questions")
            for i, result in enumerate(results):
                print(f"   Q{i+1}: {result.get('question', 'N/A')[:50]}...")
                print(f"   A{i+1}: {result.get('answer', 'N/A')[:80]}...")
        else:
            print(f"❌ Batch chat query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Batch chat query failed: {e}")
    
    print()
    
    # Test 5: Error Handling
    print("5. Testing Error Handling...")
    try:
        # Test with empty question
        payload = {"question": "", "session_id": "error_test"}
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Error handling passed (empty question rejected)")
        else:
            print(f"❌ Error handling failed - expected 400, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error handling test failed: {e}")
    
    print()
    print("=== Test Suite Complete ===")
    return True

def main():
    """Main test function."""
    print("Starting API tests...")
    print("Make sure the API server is running before running this test.")
    print("You can start it with: python -m uvicorn api_server:app --port 8000")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    success = test_api_endpoints()
    
    if success:
        print("\n🎉 All tests completed! Check individual test results above.")
    else:
        print("\n❌ Some tests failed. Please check the API server status.")
        sys.exit(1)

if __name__ == "__main__":
    main()
