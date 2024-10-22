> [!WARNING]
> 👨‍💻 WIP 👩‍💻

FTL python runtime vibes


# Summary
temporary throwaway repo to figure out how we want to tackle a python runtime for FTL. trying stuff in a separate repo to operate in yolo mode and make a mess. once we figure out what we want to do, we'll migrate it to the `ftl` repo.


# Goals
- [ ] emotionally come to terms with python
- [ ] figure out which package / project manager to use. currently [uv](https://docs.astral.sh/uv/)
- [ ] scaffold static analyzer for schema generation
- [ ] scaffold python runtime for FTL
- [ ] figure out build / publish pipeline
- [ ] migrate all of ^ to `ftl` repo

Concretely, we should have things in a place where we can read `modules/echo/echo.py`, parse it into an AST with type resolution, and scaffold out the pattern we'll use to traverse the AST and generate a schema.

Scaffold out enough of the runtime so that an annotated verb actually gets called.


# Running the jank

> [!TIP]
> use vscode. repo has been set up to have vscode prompt you to install recommended extensions. extension configuration will automatically work once they're installed. 
> 
> _after_ running `uv sync`, vscode _should_ automatically activate the virtual environment when you open the project. if it doesn't, open a python file in the repo and it should prompt you to activate the virtual environment. if that doesn't work, manually select the virtual environment by clicking on the python version in the bottom right corner of the vscode window. 

> [!NOTE]
> repo is using `hermit` to install `python3` and `uv`. [`uv`](https://docs.astral.sh/uv/) is the package manager and build tool. we'll use it to publish the ftl lib to pypi.


```bash
uv sync # Update the project's environment. Syncing ensures that all project dependencies are installed and up-to-date with the lockfile.

uv run modules/echo/echo.py # smoke test to make sure everything is setup correctly
```


# Current Setup
```
.
├── modules
│   └── echo
│       ├── README.md
│       ├── echo.py
│       └── pyproject.toml
├── packages
│   └── ftl
│       ├── README.md
│       ├── pyproject.toml
│       └── src
│           └── ftl
│               ├── __init__.py
│               ├── decorators
│               │   ├── __init__.py
│               │   └── verb.py
│               └── py.typed
├── pyproject.toml
└── uv.lock
```

## `modules`
contains `echo` module. identical to the `echo` module in the `ftl` repo.

## `packages`
contains `ftl` package. this is where the decorators (a.k.a annotations) and helper stuff will live

> [!NOTE]
> we can dump the static analyzer and runtime here for now too since we're just testing stuff out.