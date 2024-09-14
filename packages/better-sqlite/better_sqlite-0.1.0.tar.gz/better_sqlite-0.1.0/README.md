<p align="center">
  <img src="./assets/better_sqlite_logo.png" alt="Better SQLite Logo"/>
</p>
<hr>
<h4 align="center">✨ Simplify your SQLite experience without writing SQL</h4>

<p align="center">
  <a href="#🗒️ Overview">Overview</a> •
  <a href="#✨ Features">Features</a> •
  <a href="#🚀 Installation">Installation</a> •
  <a href="#📚 Usage">Usage</a> •
  <a href="#🧪 Testing">Testing</a> •
  <a href="#📝 License">License</a> •
  <a href="# 🤝 Contributing">Contributing</a>
</p>

## 🗒️ Overview

A simple and intuitive SQLite wrapper library for Python that provides an easy-to-use interface for interacting with SQLite Databases. This library allows you to perform basic CRUD ( Create, Read, Update, Delete) operations without having to write raw SQL queries.

## ✨ Features

- **Context Manager Support**: Automatically handles database connection and closing.
- **CRUD Operations**: Easy methods for creating tables, inserting, updating, retrieving, and deleting data.
- **No Raw SQL Required**: Simplified API for common database operations.

## 🚀 Installation

This library can be installed via pip( recommended ) or git by cloning the repository and installing it locally.

To install `Better SQLite` via git:

```bash
git clone https://github.com/ayrun3412/Better-SQlite.git
cd Better-SQLite
pip install .
```

Via pip:

```bash
# pip3 for MacOS & Linux
pip install better-sqlite
```

## 📚 Usage

### Creating a Table

```python
from better_sqlite import Database

with Database('example.db') as db:
    db.create_table("users", {"name": "TEXT", "age": "INTEGER"})
```

### Inserting Data

```python
with Database('example.db') as db:
    db.insert("users", {"name": "Alice", "age": 30})
```

### Retrieving Data

```python
with Database('example.db') as db:
    user = db.get("users", {"name": "Alice"})
    print(user)  # Output: {'name': 'Alice', 'age': 30}
```

### Updating Data

```python
with Database('example.db') as db:
    db.update("users", {"age": 31}, {"name": "Alice"})
```

### Deleting Data

```python
with Database('example.db') as db:
    db.delete("users", {"name": "Alice"})
```

## 🧪 Testing

 To ensure the functionality of the library, you can run the tests using `pytest`.

First, Install `pytest` if you haven't already:

```bash
pip install pytest
```

Then run, the tests:

```bash
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) for more details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.
