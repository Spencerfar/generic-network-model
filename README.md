# Generic Network Model (GNM) of aging
The GNM model from https://journals.aps.org/pre/abstract/10.1103/PhysRevE.94.052409 and https://journals.aps.org/pre/abstract/10.1103/PhysRevE.98.032302. The model consists of a network of binary nodes that have value 0 (healthy) or 1 (damaged). Node stochastically damage with rates that depend on the state of neighbouring nodes, leading to propating damage throughout the network.

A python version of this model is located in gnm/ and a C++ version in gnm-cpp/. 


# Requirements
Python version of the model requires numpy. C++ version requires the boost graph library.

# Demo
example.py shows an example of using the python model. run.sh runs the C++ model.