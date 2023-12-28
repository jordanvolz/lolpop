# Integration Frameworks

One of the key tenets of lolpop is that  workflows can be designed and built using integrations that slide into specific layers of abstraction. Users can collaborate and build workflows based on their knowledge of the system and expertise with different tools. I.E. low-level users might wish to build and implement integrations into model training frameworks, metadata trackers, prediction monitoring tools, etc., whereas higher level users might use those same integrations to develop higher level workflows that take various data sets and solve specific use cases. 

lolpop also believes strongly in the system being extensible -- meaning that users can build [extensions](extensions.md) to accomplish whatever it is that is needed and easily slot that into existing or new workloads. We believe everything should be extensible, from the [integrations](building_extensions.md) and [tests](testing_workflows.md) used, to the [CLI](extending_cli.md) experience itself. This also applies to the layers of abstraction within the workflow itself, which we call the `integration framework`. 

In this section we'll discuss lolpop's integration framework and illustrate how to customize this for users who wish to have additional flexibility on their workflows. 

!!! note 
    Using custom integration frameworks is considered experimental and should be done cautiously. [Let us know](contact.md) if you experiment with this and what your impressions are. 

## Default Integration Framework

lolpop leverages an existing integration framework that is particularly well suited for machine learning workflows. In particular, the layers of abstraction are: 

1. `Component`: Components are low-level building blocks that typically define integration with an external library, such as `sklearn`, `mlflow`, `evidentlyai`, etc. Components do most of the heavy lifting in understanding how to leverage these libraries to execute atomic functionality (i.e. training a model artifact, logging a metric, comparing the performance of two models, etc.). Components implement a common set of APIs according to their type. 

2. `Pipeline`: Pipelines use any number of components to execute a task that is more complex than any single component can handle. This might include training a model -- where features need to be created (via a feature transformer), a model artifact needs to be created (via a model trainer), the model needs to be versioned (via a metadata tracker). Pipelines execute work via component APIs such that components can be seamlessly swapped in and out of workflows without needed to rewrite code. 

3. `Runner`: Runners execute end-to-end workflows and are meant to match up to external orchestration tools. Runner typically work with one or more pipelines to execute work. This might include refreshing a model by grabbing the latest data, creating features, training a model, and comparing performance metrics to the currently deployed model to determine if a promotion is required. Runners typically leverage pipeline APIs so that workflows can be execute regardless of the pipelines used to execute them. 

lolpop's default integration framework also comes with a heirarchy, in which: 

1. Pipelines and Components are children of Runners. 

2. Components can additionally also be children of Pipelines. 

    This can be represented visually via: 

    ```yaml 
    runner: 
        component: 
        pipeline: 
            component: 
    ```

Users need not do anything in order to use this integration framework. It is the default behavior by lolpop and will be implemented in lieu of any other framework. 

## Defining Custom Integration Frameworks 

lolpop allows users to specify their own integration framework and will process it accordingly. In order to specify a custom integration framework, simply input `integration_framework:` in your workflow `yaml` file with the desired framework: 

```yaml 
integration_framework: 
    <insert framework here...>

<normal configuration...>
```

For example, the default integration framework would look like this: 

```yaml 
integration_framework: 
    runner: 
        component: 
        pipeline: 
            component: 
```

Let's imagine a world where our components are very complex. They are so complex that we need to abstract away functionality into "widgets". If we wished to build an integration framework that includes widgets, we would need to specify that in our integration_framework as follows: 

```yaml 
integration_framework: 
    runner: 
        component: 
            widget: 
        pipeline: 
            component:
                widget:  
```
Using custom integration frameworks you can make different types of workflow representations that should be able to satisfy requirements from many different types of ML (and even non-ML) workflows. 

## Behavior of the Integration Framework

lolpop's integration frameworks suppors any type of (yaml-compatible) name for your integration framework abstractions, but there are a few assumptions that lolpop makes that you should be aware of if you travel down this path. 

1. The framework must have a single root node. I.E. in our example, our root is `runner`. lolpop does not currently support having multiple nodes at the root [contact us](contact.md) if you have an example where multiple roots are needed. 

2. The names used in your integration framework correspond to section names in your `yaml` definition. I.E. using the default framework, we might have a yaml file that looks like this: 

    ```yaml 
    pipeline: 
        process : MyProcessPipeline 
        train : MyTrainingPipeline
        predict : MyPredictionPipeline
    component: 
        metadata_tracker : MLFlowMetadataTracker
    config: 
        train_data: /path/to/train.csv
        eval_data: /path/to/test.csv
    ```

    If you include the default integration framework, you should notice that framework names match up exactly w/ the yaml section names: 

    ```yaml hl_lines="3 4 7 11"
    integration_framework: 
        runner: 
            component: 
            pipeline: 
                component: 

    pipeline: 
        process : MyProcessPipeline 
        train : MyTrainingPipeline
        predict : MyPredictionPipeline
    component: 
        metadata_tracker : MLFlowMetadataTracker
    config: 
        train_data: /path/to/train.csv
        eval_data: /path/to/test.csv
    ```
    Your custom integration framework works exactly the same. You can build an integration framework using abstraction layer `integration_type`, and then define that in the configuration by having a section for `integration_type` as well. 

3. Classes defined in your custom sections are found using standard lolpop search paths. As an example, assuming you have an integration layer `widget` with class `MyWidget`, i.e.: 

    ```yaml hl_lines="8-9"
    integration_framework: 
    runner: 
        widget:
        component: 
            widget: 
        ... 

    widget: 
        some_cool_widget: MyWidget

    ... 
    ```

    lolpo will search for `MyWidget` along the path `lolpop.widget` and `lolpop.extension.widget`. `MyWidget` would then be initialized and accessible under the `some_cool_widget` attribute of the parent (in this case, the `runner` object). For most use cases, we should expect users to create a custom extension for non-default abstraction layers in the integration framework. 

    In the future we may define custom search paths for each layer of the integration framework. ([contact us](contact.md) if this is something that interest you. (Technically, this is already possible, just not properly documented/tested at the moment))

4. The order of sibling nodes is important in the integration framework. The default behavior is as follows: 
    
    a. Siblings are processed in the order written. 

    b. After a node is processed, it is passed into sibling nodes. This means that it will be processed as a dependent integration and will be accessible to children of that node (via standard attribute assignment). For example, in the default setup, we have the following: 

    ```yaml title="Default Integration Framework"
    integration_framework: 
        runner: 
            component: 
            pipeline: 
                component: 
    ```

    In this scenario, runner components are processed first, and all runner components are passed into each pipeline. This effectively scopes the runner components are "global", as all pipelines can access them. Pipelines may additionally have pipeline specific components. By reversing the order, we create a different situation: 

    ```yaml title="A (likely) Bad Integration Framework"
    integration_framework: 
        runner: 
            pipeline: 
                component: 
            component: 
    ```

    This scenario would process `pipeline` before `component`. Pipelines would then be passed into each runner component. This might be desirable in some use cases, but it is not the intention behind the default integration framework.

    Note that you can prevent any layer of the integration framework from passing itself down to siblings via the configuration item `pass_integration_to_siblings`. This defaults to `True`, but can be turned off via setting it to `False` in the configuration for that layer. 

5. By default, all leaf integrations of the same type are aware of each other. For example, in our default framework, a `component` has access to all other components, but a `pipeline` does not know about other pipelines. This can be configured via the configuration value `update_peer_integrations`. The default value is to only enable this behavior for leaf nodes in your integration framework, but this can be overridden at each layer as needed. As an example, consider the following configuration: 

    ```yaml
    pipeline: 
        process : MyProcessPipeline 
        train : MyTrainingPipeline
        predict : MyPredictionPipeline
    component: 
        metadata_tracker : MLFlowMetadataTracker
        metrics_tracker : MLFlowMetricsTracker
    ```
    In the above, we've defined two global components and two pipelines. The components are leaf nodes in the default integration framework, meaning that they will, by default, be passed into each other. This means the following attributes will exist: `runner.metadata_tracker.metrics_tracker` and `runner.metrics_tracker.metadata_tracker`. However, as pipelines are not leaf nodes, pipelines will not, by default, know about each other. I.E., there is no `runner.process.train` attribute.

6. All layers of the integration framework support having a `config` section. This will be accessible to all integrations via the standard `_get_config` method. 

## Building Custom Integrations

To leverage customer integration frameworks, you'll likely need to build some custom integrations. This should be as simple as building some lolpop extensions that inherit the `BaseIntegration` class. Please see the section on [creating extensions](building_extensions.md) for more information. 




