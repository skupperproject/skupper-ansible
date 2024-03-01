# Linking sites

This example shows how to generate a token and link two sites.

The skupper_token and skupper_link roles rely on host variables.
When you invoke the `skupper_token` role for a given host, a skupper
token will be created and stored as a **host variable** named
**generated_token**.

In case you have a pre-generated token to use, you can add it as part
of the link definition and instead of setting the `host` in the link definition,
you must enter a `token` propery with the respective token in YAML.
Therefore, you won't need to call the `skupper_token` role.

Looking at the `inventory.yaml`, it defines 2 ansible nodes, each one
representing a skupper site.

The **_sample-a_** site defines a named token (**sample-a-token**), while
the other site **_sample-b_** defines a link to the **_sample-a_** site.

## Playbook

Along with the skupper_token and skupper_link roles, the playbook also 
performs some extra steps, so that the token creation and linking between
the two sites work.

Here are all the steps being performed:

* Create namespaces (sample-a and sample-b)
* Ensures skupper is initialized on both namespaces
* Deletes secret named **_sample-a-token_** from sample-a namespace
  (to prevent issues with the skupper token creation)
* Invoke skupper_token role (against sample-a)
* Invoke skupper_link role (against sample-b)
