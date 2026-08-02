# Controllers

This directory contains HTTP-facing controllers.

In our architecture, `api` modules define the FastAPI routes, request/response models (DTOs), and dependency injections. They then delegate the handling of the request to a corresponding function within a controller in this directory. The controller is responsible for orchestrating calls to one or more services to fulfill the request.

This separation keeps the API routing layer thin and focused solely on the HTTP interface contract.
