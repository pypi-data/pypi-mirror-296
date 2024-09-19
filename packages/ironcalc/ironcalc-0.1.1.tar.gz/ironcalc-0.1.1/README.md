# IronCalc python bindings

To compile this and test it:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install maturin
$ maturin develop
$ cd examples
examples $ python example.py
```

From there if you use `python` you can `import ironcalc`. You can either create a new file, read it from a JSON string or import from Excel.


Hopefully the API is straightforward.