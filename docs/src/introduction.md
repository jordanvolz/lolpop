Welcome to lolpop!

## What is lolpop? 

lolpop is a software engineering framework for machine learning workflows. 

Good system design should have: 
1. Standard set of logical components
2. Stable APIs for communication between components 
3. Canonical implementations of components and APIs 
4. Extensibility that allows people to implement their own versions.

So, what are the goals here? 
1. Endlessly extensible. I.E. you're a ds and you want to code. Let you code. 
2. Encourage modularity. Design a system where parts can easily be interchanged as needed. 
3. Easy to test/debug. Provide something that makes it easy to test and debug workflows
4. Provide a declarative experience. I.E., you can have people start executing workloads via configuration. (i.e. config + runner class → will be CLI eventually)
5. Logical implementation on CI/CD platform or delivery platform. easily "Environment aware" via 'profiles' my_workflow_dev.yaml, my_workflow_prod.yaml, etc. 
6. Lots of smart defaults/pre-built stuff to accelerate use case deployment. Be inclusive. Not trying to commercialize so anything you do or don't want to use is fine. 
7. Be unopinionated about other stuff that you are using. 
8.  Make switch fees minimal. Switch fees prevent teams from doing what is best for them and leadership often balks at them. We wanted to make it easy to switch to new tech, and also easy to bring existing workloads into Lolpop. Bringing in an existing workload should be a lightweight refactoring exercise, and let's be honest, you probably needed to refactor that code anyway. 
9. Open source. Forever and ever. Cuz you won't use it otherwise. 
10. Be a little opinionated about project structure?
In my experience, a lot of people want to be able to experiment easily with a lot of different stuff. ML changes quickly and making things modular and easily testible means that I can try a new model trainer or metadata tracker, etc on my existing workflow with minimal amount of effort. This makes it easy for me to decide if I want to implement some changes in my workflow downstream, etc. 
## How does it work?

Write your own components or use pre-built ones: 
```python
```

Design pipeline and runner workflows to use generic classes: 
```python
```

Configure runners to leverage specified components via configuration: 
```python
```

And, easily run your workflows operationally: 
```python
``` 

## Why lolpop? 

## What is lolpop *not*? 
1. It's not an orchestrator. In fact, you should probably use an orchestrator to run code you create with lolpop. We'll have some recommendations on how best to do that. 
2. We're not a pipelining tool. (but why not?)
3. We're not a metadata tracker, training platform, experiment tacker, etc. We think you should have and use those if you want to. Let lolpop work with those as needed. 
4 … 

## Next Steps

- Getting Started

- Integrations 

- Extensions 

- CLI 

- Examples 

- Resources 




