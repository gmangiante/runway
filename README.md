# runway: a data science platform

**EXECUTIVE SUMMARY**

**runway** is a proof-of-concept project to explore the
idea of a highly interactive, mobile-friendly, web-based platform for the construction and sharing of datasets and machine
learning models. Since it was originally created for the General Assembly Data Science Immersive program, I used it as an opportunity to synthesize all my learning from that program with pre-existing skills in full-stack web development. Although it is definitely still in
"pre-alpha" status, a number of interesting features have been at least partially realized in this incarnation of the project.

**FEATURE OVERVIEW**

- Provides both an unauthenticated "read-only" experience and an authenticated "power-user" experience
- Allows the creation of datasets comprising one or more data files via a simple form and file selection/drag-and-drop (NOTE: at this time, only CSV data is supported, with plans to expand format options in the future).
- For each data file, supports Exploratory Data Analysis using a variety of techniques and visualizations:
  - Data types overview
  - Null statistics per-column
  - Unique values per-column
  - Value distribution per-column
  - Correlation of numeric columns
  - More to come!
- For each data file, supports some basic transformation/cleaning techniques:
  - Dropping nulls in selected columns (by column or by row)
  - Imputing nulls in selected columns (zero, empty string, mean, mode, median)
  - One-hot encoding selected columns (including drop-first option)
- Allows creation of machine learning models based on these datasets using a simple form interface, including:
  - Model type selection (NOTE: currently only scikit-learn "fit/score/predict"-type models are supported, with plans to increase support for other models such as neural networks in the future)
  - Selecting either separate training and validation files or a single training-validation file (in which case the default train/test split is used for now)
  - Selecting target and feature columns from the list of numeric columns in the training and validation files
  - Choosing model parameters appropriate to the type of model
- At this time, the supported models are:
  - LinearRegression
  - LogisticRegression
- Allows asynchronous triggering of model fit process, with subsequent interactive notification when the fit process has completed
- Provides the primary training/validation scoring metric from sklearn, as well as additional scores and post-fit attributes as appropriate per model
- Facilitates tweaking models by creating new versions based on existing models
- Allows authenticated users to download Python pickle files of models for their own use

**ARCHITECTURE**
- Currently uses [PostgreSQL](https://www.postgresql.org/) as the back end for all storage, including data files and models. Could easily be adapted to other back end data stores.
- The middle/application tier (**runway-api**) is a [Flask](https://flask.palletsprojects.com/en/2.2.x/) API, served by [gunicorn](https://gunicorn.org/) to allow process spawning and server-side event publishing. This is a RESTful API that primarily consumes/produces JSON.
- The API uses [SQLAlchemy](https://www.sqlalchemy.org/) to communicate with the database, including the very handy ORM (object relational mapper).
- The front end application (**runway-app**) was built using the [Vue.js](https://vuejs.org/) JavaScript framework, enhanced via TypeScript.
- User management and authentication has been entirely outsourced to [auth0](https://auth0.com/) for both password-based and social login.

**FUTURE DIRECTIONS**
- Robustness - as a pre-alpha proof-of-concept project, there are plenty of edge cases and odd user behaviors yet to account for.
- Code cleanliness - since the development arc of this initial phase was only a couple of weeks, there are a number of hacky code practices that should be cleaned up prior to production release.
- Scalability - testing thus far has used only small datasets and relatively easy-to-train models; thorough load-testing should be conducted.
- User experience - the overall aesthetic is currently very minimal, and some paths are not as clear as they could be; additionally, error reporting (especially for modeling) is not handled well at this time.
- Expansion of input formats - as noted above, only CSV is currently supported for data ingestion.
- Expansion of data exploration/visualization beyond the basics noted here.
- Expansion of the number and type of machine learning models supported.
- Streaming data - at this time, only static datasets are supported; however, I would like to explore using streaming data services such as [ably](https://ably.com/) in the future for modeling.
- Predictions - at this point, only training and evaluation models is supported; an area to explore would be how to best facilitate both model owners and casual browsers using these models for actual predictions.

**CREDITS**

Please see code comments for specific citations of open-source articles and code snippets used in **runway**.


Please check out my portfolio at [https://portfolio.gabrielmangiante.me](https://portfolio.gabrielmangiante.me)!