#!/usr/bin/env python3
"""
Test Script for Smart Emergency Response System Chatbot

Run this script to test the chatbot API without using the web interface.
Make sure the Flask server is running before executing this script.

Usage:
    python test_chatbot.py
"""

import requests
import json
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
BASE_URL = "http://localhost:5000"
CHAT_ENDPOINT = f"{BASE_URL}/chat"
HEALTH_CHECK_ENDPOINT = f"{BASE_URL}/health-check"

class ChatbotTester:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def check_server(self):
        """Check if Flask server is running"""
        try:
            response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=2)
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ Server is running on {BASE_URL}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}✗ Cannot connect to server at {BASE_URL}")
            print(f"  {Fore.YELLOW}Make sure Flask server is running: python app.py")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ Error checking server: {str(e)}")
            return False
    
    def test_query(self, query, expected_type="success"):
        """Test a single query"""
        try:
            print(f"\n{Fore.CYAN}Testing: {query}")
            
            response = requests.post(
                CHAT_ENDPOINT,
                json={"message": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if expected_type == "allowed" and "reply" in data:
                    print(f"{Fore.GREEN}✓ ALLOWED (Domain-specific response)")
                    print(f"  Response: {data['reply'][:100]}...")
                    self.passed += 1
                    self.test_results.append(("PASS", query))
                    
                elif expected_type == "rejected" and "reply" in data:
                    if "can only help with" in data["reply"].lower():
                        print(f"{Fore.YELLOW}⚠ REJECTED (Out of domain)")
                        print(f"  Response: {data['reply'][:100]}...")
                        self.passed += 1
                        self.test_results.append(("PASS", query))
                    else:
                        print(f"{Fore.RED}✗ FAILED (Expected rejection)")
                        self.failed += 1
                        self.test_results.append(("FAIL", query))
                        
                else:
                    print(f"{Fore.RED}✗ Unexpected response format: {data}")
                    self.failed += 1
                    self.test_results.append(("FAIL", query))
                    
            else:
                print(f"{Fore.RED}✗ Server returned status {response.status_code}")
                self.failed += 1
                self.test_results.append(("FAIL", query))
                
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}✗ Request timeout - API took too long")
            self.failed += 1
            self.test_results.append(("FAIL", query))
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {str(e)}")
            self.failed += 1
            self.test_results.append(("FAIL", query))
    
    def run_test_suite(self):
        """Run the complete test suite"""
        print(f"\n{Fore.BLUE}{'='*60}")
        print(f"{Fore.BLUE}Smart Emergency Response Chatbot - Test Suite")
        print(f"{Fore.BLUE}{'='*60}\n")
        
        # Check server first
        if not self.check_server():
            return
        
        # Test 1: In-domain queries (should be allowed)
        print(f"\n{Fore.MAGENTA}[TEST SUITE 1: In-Domain Queries]")
        print(f"{Fore.MAGENTA}These should receive helpful responses:")
        
        in_domain_queries = [
            "How do I perform CPR?",
            "How do I call an ambulance?",
            "What is first aid?",
            "What services does a hospital provide?",
            "How to treat a wound?",
        ]
        
        for query in in_domain_queries:
            self.test_query(query, "allowed")
        
        # Test 2: Out-of-domain queries (should be rejected)
        print(f"\n{Fore.MAGENTA}[TEST SUITE 2: Out-of-Domain Queries]")
        print(f"{Fore.MAGENTA}These should be rejected with a polite message:")
        
        out_domain_queries = [
            "What is the capital of France?",
            "How do I cook pizza?",
            "Tell me a joke",
            "What is Python programming?",
        ]
        
        for query in out_domain_queries:
            self.test_query(query, "rejected")
        
        # Test 3: Edge cases
        print(f"\n{Fore.MAGENTA}[TEST SUITE 3: Edge Cases]")
        print(f"{Fore.MAGENTA}Testing edge cases:")
        
        # Empty message
        print(f"\n{Fore.CYAN}Testing: Empty message")
        try:
            response = requests.post(
                CHAT_ENDPOINT,
                json={"message": ""},
                timeout=5
            )
            if response.status_code == 400:
                print(f"{Fore.GREEN}✓ Correctly rejected empty message")
                self.passed += 1
            else:
                print(f"{Fore.YELLOW}⚠ Unexpected response for empty message")
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {str(e)}")
            self.failed += 1
        
        # Long message
        print(f"\n{Fore.CYAN}Testing: Long message")
        long_msg = "I have a detailed health question. " * 20
        self.test_query(long_msg, "allowed")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{Fore.BLUE}{'='*60}")
        print(f"{Fore.BLUE}TEST SUMMARY")
        print(f"{Fore.BLUE}{'='*60}")
        print(f"{Fore.GREEN}Passed: {self.passed}")
        print(f"{Fore.RED}Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        
        if self.failed == 0:
            print(f"\n{Fore.GREEN}✓ All tests passed!")
        else:
            print(f"\n{Fore.YELLOW}⚠ Some tests failed. Check the output above.")
        
        print(f"\n{Fore.BLUE}{'='*60}\n")
    
    def interactive_mode(self):
        """Run interactive chat mode"""
        print(f"\n{Fore.BLUE}{'='*60}")
        print(f"{Fore.BLUE}Interactive Chat Mode")
        print(f"{Fore.BLUE}{'='*60}")
        print(f"{Fore.YELLOW}Type 'quit' to exit, 'help' for help\n")
        
        while True:
            try:
                user_input = input(f"{Fore.CYAN}You: ").strip()
                
                if user_input.lower() == 'quit':
                    print(f"{Fore.YELLOW}Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print(f"{Fore.YELLOW}Ask questions about:")
                    print(f"  - Health sector / hospitals")
                    print(f"  - Ambulance services")
                    print(f"  - First aid and CPR")
                    print(f"  - Emergency services")
                    continue
                
                if not user_input:
                    continue
                
                response = requests.post(
                    CHAT_ENDPOINT,
                    json={"message": user_input},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"{Fore.GREEN}Bot: {data.get('reply', 'No response')}\n")
                else:
                    print(f"{Fore.RED}Error: {response.status_code}\n")
                    
            except requests.exceptions.Timeout:
                print(f"{Fore.RED}Request timeout. Try again.\n")
            except requests.exceptions.ConnectionError:
                print(f"{Fore.RED}Cannot connect to server. Is Flask running?\n")
                break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Goodbye!")
                break


def main():
    """Main entry point"""
    import sys
    
    tester = ChatbotTester()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Interactive mode
        if tester.check_server():
            tester.interactive_mode()
    else:
        # Run test suite
        tester.run_test_suite()


if __name__ == "__main__":
    main()
