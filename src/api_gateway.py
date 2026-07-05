import sqlite3
import time
import json
import requests
from functools import wraps

class CentralizedAPIGateway:
    """
    A centralized API Gateway with Circuit Breaker pattern implemented using SQLite
    for state management.
    """
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, db_path="circuit_breaker.db", failure_threshold=5, recovery_timeout=60):
        self.db_path = db_path
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the SQLite database for circuit breaker state."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS circuit_breaker (
                id INTEGER PRIMARY KEY,
                state TEXT NOT NULL,
                failure_count INTEGER NOT NULL,
                last_failure_time REAL
            )
        """)
        # Ensure there's always one row for the circuit breaker state
        cursor.execute("INSERT OR IGNORE INTO circuit_breaker (id, state, failure_count, last_failure_time) VALUES (1, ?, 0, 0.0)", (self.CLOSED,))
        conn.commit()
        conn.close()

    def _get_state(self):
        """Retrieves the current state of the circuit breaker from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT state, failure_count, last_failure_time FROM circuit_breaker WHERE id = 1")
        state, failure_count, last_failure_time = cursor.fetchone()
        conn.close()
        return state, failure_count, last_failure_time

    def _set_state(self, state, failure_count=None, last_failure_time=None):
        """Updates the state of the circuit breaker in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        update_query = "UPDATE circuit_breaker SET state = ?"
        params = [state]
        if failure_count is not None:
            update_query += ", failure_count = ?"
            params.append(failure_count)
        if last_failure_time is not None:
            update_query += ", last_failure_time = ?"
            params.append(last_failure_time)
        update_query += " WHERE id = 1"
        cursor.execute(update_query, params)
        conn.commit()
        conn.close()

    def _record_failure(self):
        """Records a failure and updates the failure count."""
        state, failure_count, _ = self._get_state()
        failure_count += 1
        last_failure_time = time.time()
        if failure_count >= self.failure_threshold and state == self.CLOSED:
            self._set_state(self.OPEN, failure_count, last_failure_time)
            print(f"Circuit tripped to OPEN state due to {failure_count} failures.")
        else:
            self._set_state(state, failure_count, last_failure_time)
            print(f"Recorded failure. Current failures: {failure_count}")

    def _record_success(self):
        """Records a success and resets the failure count if in HALF_OPEN state."""
        state, _, _ = self._get_state()
        if state == self.HALF_OPEN:
            self._set_state(self.CLOSED, failure_count=0, last_failure_time=0.0)
            print("Circuit restored to CLOSED state after success in HALF_OPEN.")
        elif state == self.CLOSED:
            self._set_state(self.CLOSED, failure_count=0, last_failure_time=0.0)
            print("Recorded success. Circuit remains CLOSED.")

    def circuit_breaker(self, service_name="default_service"):
        """
        Decorator for applying circuit breaker logic to a function.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                state, failure_count, last_failure_time = self._get_state()

                if state == self.OPEN:
                    if time.time() - last_failure_time > self.recovery_timeout:
                        self._set_state(self.HALF_OPEN)
                        print(f"Circuit moved to HALF_OPEN state for {service_name}.")
                    else:
                        print(f"Circuit is OPEN for {service_name}. Request blocked.")
                        raise CircuitBreakerOpenException(f"Circuit for {service_name} is OPEN.")
                
                if state == self.HALF_OPEN:
                    try:
                        print(f"Circuit is HALF_OPEN for {service_name}. Trying request...")
                        result = func(*args, **kwargs)
                        self._record_success()
                        return result
                    except (requests.exceptions.RequestException, json.JSONDecodeError, CircuitBreakerException) as e:
                        self._record_failure()
                        self._set_state(self.OPEN, failure_count=failure_count + 1, last_failure_time=time.time()) # Ensure state is OPEN after failure in HALF_OPEN
                        print(f"Request failed in HALF_OPEN for {service_name}. Circuit moved back to OPEN. Error: {e}")
                        raise CircuitBreakerOpenException(f"Circuit for {service_name} is OPEN after failure in HALF_OPEN.") from e

                if state == self.CLOSED:
                    try:
                        print(f"Circuit is CLOSED for {service_name}. Making request...")
                        result = func(*args, **kwargs)
                        self._record_success()
                        return result
                    except (requests.exceptions.RequestException, json.JSONDecodeError, CircuitBreakerException) as e:
                        self._record_failure()
                        print(f"Request failed in CLOSED for {service_name}. Error: {e}")
                        raise CircuitBreakerException(f"Service {service_name} failed.") from e
            return wrapper
        return decorator

class CircuitBreakerException(Exception):
    """Custom exception for circuit breaker related errors."""
    pass

class CircuitBreakerOpenException(CircuitBreakerException):
    """Custom exception when circuit breaker is open."""
    pass

# Singleton instance exported for other modules
gateway = CentralizedAPIGateway()

# --- Example Usage ---
if __name__ == "__main__":
    # Clean up previous db for fresh start
    import os
    if os.path.exists("circuit_breaker.db"):
        os.remove("circuit_breaker.db")

    gateway = CentralizedAPIGateway(failure_threshold=3, recovery_timeout=10)

    # A dummy API call function that sometimes fails
    def make_api_call(url, should_fail=False, json_error=False):
        print(f"Attempting to call {url}...")
        if should_fail:
            print("Simulating network error...")
            raise requests.exceptions.ConnectionError("Simulated connection error")
        if json_error:
            print("Simulating JSON decode error...")
            raise json.JSONDecodeError("Expecting value", "invalid json", 0)
        
        # Simulate a successful call
        print(f"Successfully called {url}")
        return {"status": "success", "data": "some data"}

    # Wrap the dummy API call with the circuit breaker
    @gateway.circuit_breaker(service_name="dummy_service")
    def protected_api_call(url, should_fail=False, json_error=False):
        return make_api_call(url, should_fail, json_error)

    print("\n--- Scenario 1: Multiple Failures (CLOSED -> OPEN) ---")
    for i in range(1, 6):
        try:
            print(f"\nAttempt {i}:")
            protected_api_call("http://example.com/api/data", should_fail=True)
        except CircuitBreakerException as e:
            print(f"Caught exception: {e}")
        except Exception as e:
            print(f"Caught unexpected exception: {e}")
        time.sleep(0.5) # Small delay

    print("\n--- Scenario 2: Circuit is OPEN, requests blocked ---")
    try:
        print("\nAttempt to call when OPEN:")
        protected_api_call("http://example.com/api/data")
    except CircuitBreakerOpenException as e:
        print(f"Caught expected exception: {e}")
    except Exception as e:
        print(f"Caught unexpected exception: {e}")

    print("\n--- Scenario 3: Wait for timeout, then HALF_OPEN ---")
    print(f"Waiting for {gateway.recovery_timeout} seconds...")
    time.sleep(gateway.recovery_timeout + 1) # Wait for recovery timeout

    try:
        print("\nAttempt to call when HALF_OPEN (should succeed):")
        protected_api_call("http://example.com/api/data")
    except CircuitBreakerException as e:
        print(f"Caught exception: {e}")
    except Exception as e:
        print(f"Caught unexpected exception: {e}")

    print("\n--- Scenario 4: HALF_OPEN fails, back to OPEN ---")
    # Force it back to HALF_OPEN for this test
    gateway._set_state(gateway.HALF_OPEN, failure_count=0, last_failure_time=time.time() - gateway.recovery_timeout - 1)
    try:
        print("\nAttempt to call when HALF_OPEN (should fail):")
        protected_api_call("http://example.com/api/data", should_fail=True)
    except CircuitBreakerOpenException as e:
        print(f"Caught expected exception: {e}")
    except Exception as e:
        print(f"Caught unexpected exception: {e}")

    print("\n--- Scenario 5: Test JSON decode error ---")
    # Reset circuit to CLOSED
    gateway._set_state(gateway.CLOSED, failure_count=0, last_failure_time=0.0)
    for i in range(1, 6):
        try:
            print(f"\nAttempt {i} with JSON error:")
            protected_api_call("http://example.com/api/data", json_error=True)
        except CircuitBreakerException as e:
            print(f"Caught exception: {e}")
        except Exception as e:
            print(f"Caught unexpected exception: {e}")
        time.sleep(0.5)

    print("\n--- Scenario 6: Test 405 (Method Not Allowed) - not directly handled by requests.exceptions.RequestException ---")
    # Reset circuit to CLOSED
    gateway._set_state(gateway.CLOSED, failure_count=0, last_failure_time=0.0)

    # A dummy API call function that simulates 405
    def make_api_call_405(url):
        print(f"Attempting to call {url} (simulating 405)...")
        # requests.exceptions.RequestException covers connection errors, timeouts, etc.
        # For HTTP status codes like 405, requests raises HTTPError if response.raise_for_status() is called.
        # We'll simulate this by raising a generic RequestException or a custom one.
        # For simplicity, let's just raise a generic RequestException for now.
        raise requests.exceptions.RequestException("Simulated 405: Method Not Allowed")

    @gateway.circuit_breaker(service_name="405_service")
    def protected_api_call_405(url):
        return make_api_call_405(url)

    for i in range(1, 6):
        try:
            print(f"\nAttempt {i} with 405 error:")
            protected_api_call_405("http://example.com/api/405")
        except CircuitBreakerException as e:
            print(f"Caught exception: {e}")
        except Exception as e:
            print(f"Caught unexpected exception: {e}")
        time.sleep(0.5)

    print("\n--- End of demonstration ---")
