# sqlalchemy-mutables

A minimal package for nested mutable datatypes in SQLAlchemy. Main feature is a JSON field that is RFC-7159 compliant.

Developed for SQLAlchemy `v1.3.24`. Your mileage may very with other versions.

## Installation
```
$ pip install sqlalchemy-mutables
```

## Usage

```
from sqlalchemy_mutables import NestedMutableListColumn

class MyTable(Base):
    mutable_list = Column(NestedMutableListColumn)
```

```
from sqlalchemy_mutables import NestedMutableDictColumn

class MyTable(Base):
    mutable_dict = Column(NestedMutableDictColumn)
```

### JSON
To be compliant with RFC-7159, 'primitives' need to be supported as top level 
values. These are values of type `str|int|float|bool` or `None`. Unfortunately, 
these types break SQLAlchemy `Mutable` functionality 
(specifically `bool` as this cannot be subclassed). To allow for these
while maintaining mutable functionality for `list` and `dict`, a wrapper class
has to be used via a `hybrid_property`.

```
from sqlalchemy_mutables import NestedMutableJSONColumn, NestedMutableJSONProperty

class MyTable(Base):
    _mutable_json = Column("mutable_json", NestedMutableJSONColumn)
    mutable_json = NestedMutableJSONProperty("_mutable_json")
```

It is possible to pass a custom functionality to the `getter` and/or `setter`:

```
def json_getter(value):
    if isinstance(value, (int, float)):
        value = value * 2
    return value

def json_setter(value):
    if isinstance(value, (int, float)):
        value = value / 2
    return value

class MyTable(Base):
    ...
    mutable_json = NestedMutableJSONProperty(
        "_mutable_json",
        fget=json_getter,
        fset=json_setter,
    )
```

Passed functions are executed in the existing `getter` and `setter` in the form of
`value = fc(value)`.
