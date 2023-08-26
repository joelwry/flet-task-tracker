---

# Task Tracker Application with Flet Framework

This is a simple task application built using the Flet framework in Python. It allows you to create, manage, and track tasks in a user-friendly interface.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Cloning the Repository](#cloning-the-repository)
  - [Installing Flet Framework](#installing-flet-framework)
- [Usage](#usage)

## Introduction

This todo application is built using the Flet framework, a Python library for creating interactive and responsive user interfaces. It provides features such as adding new tasks, marking tasks as completed, viewing task details, and more.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Cloning the Repository

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command to clone the repository:

   ```
   git clone https://github.com/joelwry/flet-task-tracker.git
   ```

### Installing Flet Framework

Before you can run the application, you need to install the Flet framework. Flet is a Python library that enables you to create interactive user interfaces. You can install it using pip:

```
pip install flet
```

## Usage

1. Navigate to the project directory:

   ```
   cd flet-task-tracker
   ```

2. Run the `main.py` script to start the application:

   ```
   flet flettask.py
   ```

3. The application will open by default default as a desktop application, allowing you to manage your tasks even down to filtering out expired task. It can also be opened as a web application by replacing the last line in the code with 

``` python
 ft.app(target=main, view=ft.AppView.WEB_BROWSER)

```


---
