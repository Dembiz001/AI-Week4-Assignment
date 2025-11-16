"""
Automated testing for login page using Selenium with webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json


class LoginPageTester:
    """AI-enhanced login page tester with webdriver-manager"""
    
    def __init__(self, headless=True):
        self.driver = None
        self.results = []
        self.setup_driver(headless)
    
    def setup_driver(self, headless=True):
        """Setup Chrome driver using webdriver-manager"""
        try:
            # Setup Chrome options
            options = webdriver.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')  # Run in background
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Use webdriver-manager to automatically handle ChromeDriver
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.driver.implicitly_wait(10)
            print("✅ WebDriver setup successful with webdriver-manager")
            
        except Exception as e:
            print(f"❌ WebDriver setup failed: {e}")
            raise
    
    def test_login_scenario(self, username, password, expected_result, test_name):
        """Test a single login scenario"""
        try:
            # Navigate to test login page
            self.driver.get("https://the-internet.herokuapp.com/login")
            
            print(f"🧪 Running test: {test_name}")
            
            # Find elements using multiple selector strategies
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Clear and fill fields
            username_field.clear()
            password_field.clear()
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Click login
            login_button.click()
            
            # Wait for result
            time.sleep(2)
            
            # Determine test outcome
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # Check for success (redirect to secure area)
            if "secure" in current_url:
                actual_result = "success"
            # Check for failure (error message or same page)
            elif "login" in current_url or "error" in page_source or "invalid" in page_source:
                actual_result = "failure"
            else:
                actual_result = "unknown"
            
            # Verify test result
            test_passed = actual_result == expected_result
            
            result = {
                "test_name": test_name,
                "username": username,
                "password": "***" if password else "empty",
                "expected": expected_result,
                "actual": actual_result,
                "status": "PASS" if test_passed else "FAIL",
                "url": current_url
            }
            
            self.results.append(result)
            
            status_icon = "✅" if test_passed else "❌"
            print(f"   {status_icon} {test_name}: Expected {expected_result}, Got {actual_result}")
            
            return result
            
        except Exception as e:
            error_result = {
                "test_name": test_name,
                "status": "ERROR",
                "error": str(e)
            }
            self.results.append(error_result)
            print(f"   💥 ERROR in {test_name}: {e}")
            return error_result
    
    def run_comprehensive_tests(self):
        """Run a comprehensive suite of login tests"""
        test_cases = [
            # Valid credentials (using the-internet herokuapp test credentials)
            {"username": "tomsmith", "password": "SuperSecretPassword!", "expected": "success", "name": "Valid Credentials"},
            
            # Invalid credentials
            {"username": "wronguser", "password": "wrongpass", "expected": "failure", "name": "Invalid Username"},
            {"username": "tomsmith", "password": "wrongpass", "expected": "failure", "name": "Invalid Password"},
            
            # Edge cases
            {"username": "", "password": "somepassword", "expected": "failure", "name": "Empty Username"},
            {"username": "tomsmith", "password": "", "expected": "failure", "name": "Empty Password"},
            {"username": "", "password": "", "expected": "failure", "name": "Both Empty"},
            
            # Special characters
            {"username": "user@name", "password": "pass", "expected": "failure", "name": "Email as Username"},
            {"username": "user name", "password": "pass", "expected": "failure", "name": "Space in Username"},
        ]
        
        print("\n🚀 Starting comprehensive login tests...")
        for test_case in test_cases:
            self.test_login_scenario(
                test_case["username"],
                test_case["password"],
                test_case["expected"],
                test_case["name"]
            )
        
        return self.results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.get('status') == 'PASS'])
        failed_tests = len([r for r in self.results if r.get('status') == 'FAIL'])
        error_tests = len([r for r in self.results if r.get('status') == 'ERROR'])
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "success_rate": round(success_rate, 2)
            },
            "detailed_results": self.results,
            "test_environment": {
                "website": "https://the-internet.herokuapp.com/login",
                "driver": "Chrome with webdriver-manager"
            }
        }
        
        print(f"\n📊 === TEST REPORT ===")
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"💥 Errors: {error_tests}")
        print(f"🎯 Success Rate: {success_rate:.2f}%")
        
        # Print detailed results
        print(f"\n📝 Detailed Results:")
        for result in self.results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "💥"
            print(f"   {status_icon} {result['test_name']}: {result['status']}")
        
        return report
    
    def save_screenshot(self, filename="test_evidence.png"):
        """Save screenshot as evidence"""
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved as {filename}")
        except Exception as e:
            print(f"⚠️ Could not save screenshot: {e}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔚 WebDriver closed")


def check_prerequisites():
    """Check if all prerequisites are met"""
    try:
        import selenium
        import webdriver_manager
        print("✅ All prerequisites are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing prerequisite: {e}")
        print("💡 Run: pip install selenium webdriver-manager")
        return False


def main():
    """Main execution function"""
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    tester = LoginPageTester(headless=True)  # Set to False to see browser
    
    try:
        # Run tests
        print("🎬 Starting test execution...")
        results = tester.run_comprehensive_tests()
        
        # Generate report
        report = tester.generate_report()
        
        # Save results to file
        with open('test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save screenshot
        tester.save_screenshot("test_execution_evidence.png")
        
        print(f"\n💾 Results saved to 'test_results.json'")
        print(f"📸 Evidence saved to 'test_execution_evidence.png'")
        
        # Final status
        success_rate = report['summary']['success_rate']
        if success_rate >= 80:
            print("🎉 Excellent! Tests completed successfully!")
        elif success_rate >= 60:
            print("👍 Good! Most tests passed.")
        else:
            print("⚠️  Some tests failed. Review the results.")
        
    except Exception as e:
        print(f"💥 Critical error during test execution: {e}")
    
    finally:
        tester.close()


if __name__ == "__main__":
    main()