
lolpop follows a simple [conceptual](concepts.md) model where workflows are constructed from three main parts: 

- **Components** are the most fundamental resource and usually interact directly with external libraries, such as using XGBoost to train a model.  

- **Pipelines** work with one or more *components* to accomplish small tasks. For example, a training *pipeline* would know how to train a model, which would involve working with a model trainer *component* to fit a model and a model repository *component* to store the model. 

- **Runners** work with one or more *pipelines* and *components* to execute end to end workflows. For example, a classification *runner* would know how to execute a full model training workflow which would include many pipeline tasks like generating the training data, fitting the model, versioning the model, analyzing the model, generating model metrics, etc. 

The relationship between components, pipelines, and runners is defined in [configuration](configuration.md) files which users can use to build runners and execute workflows. Users can use configuration files to change workflow behavior without writing any code, which should provide quick development iteration and also streamline production processes and inevitable debugging. All users need to do in order to begin [running workflows](running_workflows.md) is a runner and a configuration file. 

lolpop additionally provides a basic [testing framework](testing_workflows.md) which allows users to easily define and run tests on components, workflows, and runners. Proper testing is tantamount to every production process and lolpop to simplifies testing of complex workflows by making them modular, configurable, and 

lolpop also allows [extensibility](extensions.md) of the framework. Advanced users should be able to easily build components, pipelines, and runners that suit their use cases and package them up for reuse. 

Lastly, lolpop exposes many of its operational capabilities via a [command-line interface](cli.md). This is a natural place to start as you begin thinking about operationalizing your workflows. The CLI also exposes some nice development features, and is itself extensible as well. 

## In This Section 

- [Configuration](configuration.md): Learn how to build and work with configurations in lolpop.

- [Building Workflows](building_workflows.md): Learn how to build workflows in lolpop. 

- [Running Workflows](running_workflows.md): Learn how to run workflows built in lolpop. 

- [Testing Workflows](testing_workflows.md): Learn how to write tests and test workflows built in lolpop. 

- [lolpop Projects](lolpop_projects.md): Get started with lolpop projects. 