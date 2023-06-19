
lolpop has a relatively flat conceptual model which contains three main resources to understand: 

- **Components**
- **Pipelines**
- **Runners** 

We'll dive into what each is and how they interact in this section.

We refer to the collective group of components, pipelines, and runners as "integrations". Integrations also contain a natural heiarchy: 

1. Runners can have children pipelines and components. 
2. Pipelines can have children components. 

lolpop's conceptual model has been designed with the following key principles in mind: 

- **Modularity**: Integrations should be designed so that they depend only on children.  
- **Abstraction**: Moving up in the heiarchy of integrations increases the abstraction. I.E. components should contain the most technical implementation details whereas pipelines and runners have less and increasily focus on workflow execution. 
- **Extensilbility**: Each integration can be easily extended and customized.  
- **Easy Testing**: As go modularity also goes ... testing. Having a modular system makes it easier to design and test integrations. 
## Components
*Components* are the core integration in lolpop and do most of the heavy lifting. These are the integrations that directly work with external libraries to introduce some functionality into your workflows, such as: training a model, transforming data, encoding features, versioning resources, etc. The methods of a component should provide a generic API into accomplishing the task specified. For example, we would example a model trainer to provide methods for `fit` and `predict`, among others. 

Components have an implicity `scope` associated with them. Components who are child to a runner are `global`, whereas component that are child to a pipeline are `local`. Global components are accessible to all child piplines and components of a runner. These are meant to be "essential" components that would not change throughout a workflow, such as a metadata tracker, metrics tracker, logger, etc. Local components are only accessible to other components that are children of the same pipeline. These are meant to be pipeline specific components thare could change from one pipeline to the next (if they are reused at all -- most local components probably will not be). 

lolpop contains many [built-in components](integrations.md), and users will likely wish to build some of their own as they get started with the system. 

## Pipelines
Many components are typically associated with a pipeline. *Pipelines* are able to perform actions across one or more components to accomplish parts of a workflow. The methods of a pipeline should provide a generic API into accomplishing small parts of the workflow. For example, a model training pipeline might have a method `train_model`. This method would know how to take incoming data, train a model or set of models, version those models, and return the winning model. This method would work across several components, such as a feature encoder, model trainer, hyperparameter tuner, metadata tracker, and resource version control. 

Pipelines are all independent from one another. They typically do not share any information between them. The only components that are shared between pipelines are global components. 

lolpop contains many [built-in pipelines](integrations.md), and users will likely wish to build some of their own as they get started with the system. 

## Runners 
One or more pipelines will be associated with a runner. *Runners* coordinate the actions in a pipeline and can also work across pipelines, when necessary. As pipelines are independent, the main way to coordinate between pipelines would be at the runner level of the heirarchy. Runners are expected to be use-case dependent. I.E. my training pipeline (and associated components) may be abstract enough to work across use cases, such as classification, regression, time-series forecasting, etc., but the runner between these use cases will likely be different as it will need to coordinate actions differently for each. Methods in runners typically execute an end-to-end workflow. 

Runners are also the expected integration level with external orchestrators. I.E. to scheduling your lolpop workflows via something like Airflow, it would be simple to import the runner you wish to use and provide the necessary configuration to run it. This can be accomplished in a few lines of code. It would also be reasonble to create orchestrator-specific runners in lolpop that would natively integrate with a standing orchestrator. 

lolpop contains many [built-in runners](integrations.md), and users will likely wish to build some of their own as they get started with the system. 

## Extensions
The hidden fourth integration is an extension. *Extensions* are simply components, pipelines, and runners that have been customized by a user. This can either be via extending an existing built-in integration and overwriting or adding functionality, or by creating entirely new components, pipelines, and runners. Both scnearios are easy for lolpop to accomodate. 

See the [extensions](extensions.md) section for more info on creating extensions. 

## ML Workflow Terminology 

In this documentation, and also the lolpop code base, you may find refence to various parts of the machine learning workflow. As these definitions can vary from one ML tool to another, we thought it would behoove all to lay down a quick glossary with respect to what they mean in lolpop. We've tried to take an approach that maps well to production workflows and work backwards from there (clarity in produciton is tantamount). Although external integrating libraries may refer to things differently, APIs, etc in built-in lolpop components try to adhere to the following (your own custom extensions may differ, and that's ok):

- Workflow: A *workflow* is the top-level concept in lolpop which we use when referring to something in lolpop being executed. Typically we would refer to a 'workflow' as being end-to-end (i.e. one or more runner methods), and a 'task' as being a smaller, perhaps atomic, piece of the workflow (i.e. a pipleine method). While workflow and tasks are conceptually not part of the lolpop heiarchy, we find it helpful when referring to parts of lolpop as things like 'pipeline' have a real conceptual meaning. 

- Resource: A *resource* is a generic term to correponds to one of many objects created by external libraries in the workflow. lolpop attempts to genericize the ml workflow in a few important ways to make it easier to design pipelines and runners across tools that might not necessarily share the same vocabulary.

In particular, the following resources are likely important aross many different use cases: 

- Run: This is meant to represent an instance of the workflow you are running. This ideally maps 1-1 with a `run` in the metadata tracker tool you use, but depending on your use case it could be more complicated and a single lolpop `run` could be several runs in the metadata tracker.  

- Dataset: A dataset should correspond to some data that you wish to identify. Datasets are typically versioned and tracked over time. For example, if my training dataset is a join between 4 different tables, I might wish to analyze, version, and track each table separate, was well as the joined table, and register them all as datasets. 

- Dataset Version: A dataset version should correspond to a single instance of a dataset. Data often changes over time, so dataset version are used to track data over time which can then be used for fun stuff like data drift analysis. 

- Model: A model should correspond to a *production* ML use case. I.E. you're building a churn model for your ecommerce business, your model might be called something like "ecommerce_churn". Over time I might use different algorithms to build models, but they would all be associated with the same model, "ecommerce_churn".

- Model Version:  A model version corresponds to a collection of experiments thare are run for a model at a specified time. Over time models need to be re-trained, each of these re-trainings would create a new model version. Conceptually, a model version should be able to be uniquely defined given a model and a run (i.e. model versions are contained within a single run), although a metadata tracker may actually provide a unique model version if if they share the lolpop conceptual model. 

- Experiment: An experiment is a single instance of fitting a specified algorithm to a given dataset. A model version typically contains many experiments, and some experiment will be identified as the best, or "winning" experiment. 



