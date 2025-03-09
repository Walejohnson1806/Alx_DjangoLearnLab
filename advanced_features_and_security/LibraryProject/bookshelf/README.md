# Permissions and Groups Setup

## Overview

This document outlines the permissions and groups setup for the Django application.

## Custom Permissions

The following permissions have been added to the `Book` model:

- `can_view`: Allows viewing books.
- `can_create`: Allows creating new books.
- `can_edit`: Allows editing existing books.
- `can_delete`: Allows deleting books.

## Groups

The following groups have been created:

- **Editors**: Can create and edit books.
- **Viewers**: Can view books.
- **Admins**: Can view, create, edit, and delete books.

## Usage

Permissions are enforced in the views using the `@permission_required` decorator. Ensure users are assigned to the appropriate groups to access the desired functionalities.