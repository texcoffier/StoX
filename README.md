# StoX: From source to execution

This tool allow to edit a source code in a web page
and see all the stages from compilation to execution:

  * Source code edition
  * Lexical analysis
  * Syntactic analysis
  * Abstract Syntax Tree
  * Code optimization
  * Assembly generation
  * Machine code generation
  * Processor execution
  * Screen display

When moving the cursor in the source code,
the 8 next stages are updated to highlight
the consequences of the last instruction.

When the processor executes an instruction, previous
stages highlight execute/read/write/modify in
the previous stages.

Try it: [StoX.html](http://perso.univ-lyon1.fr/thierry.excoffier/PARSER/StoX.html)


## How to use

The tool is coded in Python and then translated into
JavaScript to be executed on the browser.

Type `make` to generate `xxx.js` and run regression tests
in Python and also with NodeJS.
The regression tests also run in the web browser when
loading the page `StoX.html`

## How to enhance

This project is based on functionality programming.
So to add a functionality, it is not necessary to modify files.
You only add your functionality in a new file.

The source filenames start by a number defining the order
of functionality addition.

  * `0000-js-compatibility.py`
  * `0002-utilities.py`
  * `0005-framework.py`: the 'Item', 'Block' and 'Blocks' classes.
  * `0010-blocks.py`:
  * `0015-SRC.py`: Source editor.
  * `0020-LEX.py`: Lexical analyzer.
  * `0025-YAC.py`: Syntactic analyze.
  * `0030-AST.py`: Abstract Syntax Tree generator.
  * `0035-OPT.py`: Code Optimizer.
  * `0040-ASM.py`: Assembly generation. Contains the instruction definitions.
  * `0045-OBJ.py`: The memory content (code, heap, stack).
  * `0050-CPU.py`: The CPU state.
  * `0055-TTY.py`: The screen.

The following files, enhance the behavior of previous blocks:

  * `0100-put.py`: 'put' function and CPU instruction.
  * `0105-compare.py`: Add `<`, `>`, `<=`, `>=`, `==`, `!=` to the language and
                    `JUMP <0`, `JUMP >0`... to the instruction set.
                    There are no CPU instruction for `<`, `>`.
  * `0110-while.py`: 'while(){}' statement and 'JUMP', 'JUMP IF ZERO' CPU
                   instructions.

The last one to be executed is the main program: '9999-main.py'

A good starting point is `0100-put.py`, it is heavily commented.


## Technical points

Beware: use only Python basic functionalities because it is
not really Python, but it is JavaScript wrote with the Python syntax.

Beware: all the file are concatenated.
So the global variables are common to all the files.

### Hooks

Defining the behavior:

```python
  def function_to_call(block_instance, data):
      pass
```

Adding a hook:

```python
  XYZ.add_filter('hook-name', function_to_call)
```

Calling a hook and so all the functions added:

```python
  XYZ.call('hook-name', data)
```

## TODO list

The next things to enhance:

  * Allow options in the URL (source content, opened blocks...).
  * Add instructions `ROTATE(nr_items, shift)`, `JUMP FCT`, `RETURN`.
  * Add an integer to boolean function and use it for comparison operators.
  * Add optimization: `while(a>b)` become `while>(a,b)`.
  * Add documentation/parameters at the block bottom.
  * Add time travel to the syntactic analyzer: it is needed for debugging.
