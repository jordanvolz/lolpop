```
class RegressionRunner(ClassificationRunner):
    """
    A class for running regression models.

    Attributes:
    -----------
    problem_type : str
        Type of problem. Default value is `regression`.

    Methods:
    --------
    __init__(self, problem_type="regression", *args, **kwargs)
        Initializes an instance of RegressionRunner class.

    """

    def __init__(self, problem_type="regression", *args, **kwargs):
        """
        Initializes an instance of RegressionRunner class.

        Parameters:
        -----------
        problem_type : str, optional
            Type of problem. Default value is `regression`.
        args
            Additional arguments passed to parent class constructor.
        kwargs
            Additional keyword arguments passed to parent class constructor.
        """
        super().__init__(problem_type=problem_type, *args, **kwargs)

```
Note: As `RegressionRunner` class is inheriting from `ClassificationRunner`, it is expected that all the methods in `ClassificationRunner` class will follow similar documentation patterns as above (with proper description based on the method's functionality).