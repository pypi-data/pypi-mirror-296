# tabpipe

tabpipe is a lightweight, multi-platform toolkit for tabular data processing.


## Things you can do with tabpipe

* Pipelining
  * Use built-in data transformations or create your own
  * Combine those transformations into a Pipeline
  * Train that pipeline on any dataframe (e.g. a Snowpark DataFrame)
  * Use the same pipeline to transform a different type of dataframe at predict time (e.g. a pandas DataFrame)

---
## TODO

### Essential

- Make expensive `fit` methods sample-based (especially those requiring complex parsing)
- Add missing tests (see TODOs in test files)
- Enforce case insensitiveness for feature names
- Improve documentation (when the API is more stable)
  - Improve docstrings
  - Layout (i.e. which modules to include; which info to show;...)
  - Add examples
- Add system for specifying parameters for Features
    - To be used downstream to change how the feature is processed
    - Support different value types, and well-defined sets of values
- Implement streaming pattern

### Nice to have

- Implement multi-threading for pandas transformations (could be useful to reduce latency in realtime inference)
- Port existing Transformation subclasses to PySpark (can be useful for handling user features)
---

## Future Improvements

1. **[High Priority]** Improve `DataFrame` abstraction and make it the de-facto enabler of multi-platform support.

    Right now, there are 2 separate mechanisms that make tabpipe multi-platform: one is the DataFrame abstraction, and the other is the implementation of several fit and transform methods in each data transformation (e.g.`_fit_pandas`, `_fit_snowpark`, `_transform_pandas`, `_transform_snowpark`). This is not ideal, as it makes the code harder to maintain. A better approach would be to have a single implementation for each method in any given transformation, and use the DataFrame abstraction to handle the differences between platforms. This would also make it easier to add support for new platforms in the future.
    - This hasn't been the case so far because that demands a lot of work to develop a solid abstraction layer.
    - If this project gets some traction, this will be one of the top priorities.
2. **[Unclear]** Refactoring `Pipeline` into a `Transformation` subclass.
    - Pros:
        - Conceptually, it makes sense, a pipeline *is* a transformation, and shares many of the same methods/attributes (fit, transform, output, etc).
        - This could eliminate duplicate logic and make the code easier to maintain.
        - Since `Pipeline` is a subclass of `Transformation`, it could be used as a transformation within another pipeline.
    - Cons:
        - This would require substantial refactoring in both `Pipeline` and `Transformation` classes.
---
## Credits

- Project structure created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
