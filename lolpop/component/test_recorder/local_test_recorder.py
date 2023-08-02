from lolpop.component.test_recorder.base_test_recorder import BaseTestRecorder
import itertools 

class LocalTestRecorder(BaseTestRecorder):
    __REQUIRED_CONF__ = {
        "config": []
    }

    test_results = []

    def record_test(self, obj, method, test, test_method, result, msg=None, *args, **kwargs):
        """Records the results of a test.

        Args:
            obj (object): the lolpop integration tested
            method (object): The method in the integration tested
            test (object): The test module used
            test_method (object): The method in the test module used 
            result (bool): The result of the test. True = passed. 
            msg (str, optional): Additiona information returned from the test. Defaults to None.
        """
        self.test_results.append(
            {"method" : "%s.%s" %(obj.name,method.__name__), 
             "test": "%s.%s" %(test, test_method.__name__), 
             "passed": result, "output": msg}
        )

    def print_report(self): 
        """Prints a testing repot. 
        """
        for key, group in itertools.groupby(self.test_results, key=lambda x: x['method']):
            print("Method: %s" %key)
            for g in group: 
                print("\t Test: %s" %g["test"])
                print("\t Passed: %s" %g["passed"])
                if g["output"] is not None: 
                    print("\t Output: %s" %g["output"] )
            


