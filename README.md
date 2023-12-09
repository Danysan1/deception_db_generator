# deception_db_generator
Deception Relational Database Generator for the final project Cybersecurity M @ Unibo

## Specification

> ### Project 2 - Deception component generator
> 
> Cybersecurity experts have recently proposed using defensive deception as a means to leverage the information asymmetry typically enjoyed by attackers as a tool for defenders. By creating fake services and components that appear as valuable targets to attackers, defenders can divert the attacker's attention and resources away from critical assets. Attackers might spend time and effort trying to compromise these fake elements, leaving less capacity to target actual valuable assets. The goal of this project is to create a fake resource generator for one specific type of resource.
>
> - The final output of the generator must be a OCI compatible image ready to be instantiated
> - The container image must include all the relevant "fake" data for its correct operation
> - The container must function out of the box, eventual configuration has to be provided during the generation to build the final working image
>
> You can choose one of the following resource types to implement
> 
> - Relational Database
>     - auto generate complex schema and data from scratch
>     - option to import an existing schema and generate data to populate it
>     - configurable settings for client connections (port, authentication, credentials)
> - ...
>
> ### References
>
> You can use LLM to generate the data, but it is better to use a local first model instead of relying on web api like chatGPT.
> 
> - https://python.langchain.com/docs/integrations/llms/llamacpp
> - https://medium.com/@karankakwani/build-and-run-llama2-llm-locally-a3b393c1570e


## Builder usage instructions

The builder creates an image based on PostgreSQL .
The base Postgres version can be chosen through the `POSTGRES_VERSION` argument (default: `11.2` , [alternatives here](https://hub.docker.com/_/postgres/)).
The name of the output image can be chosen through the `OUT_IMAGE_NAME` and `OUT_IMAGE_TAG` environment variables from `.env` (default: `registry.gitlab.com/dsantini/deception-db-generator:latest`).

## Image usage instructions

The port, username and password can be passed respectively through the options `POSTGRES_PORT`, `POSTGRES_USER` and `POSTGRES_PASSWORD` at the first startup.
