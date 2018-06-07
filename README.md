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
  * `0099-init.py`: initialize all the blocks of the pipeline.

The following files, enhance the behavior of previous blocks:

  * `0100-put.py`: 'put' function and CPU instruction.
  * `0105-compare.py`: Add `<`, `>`, `<=`, `>=`, `==`, `!=` to the language and
                    `JUMP <0`, `JUMP >0`... to the instruction set.
                    There are no CPU instruction for `<`, `>`.
  * `0110-while.py`: 'while(){}' statement and 'JUMP', 'JUMP IF ZERO' CPU
                   instructions.

The following files, enhance the user interface:

  * `1000-font-size.py`: change font size with `Ctrl +` and `Ctrl -`
  * `1010-open-close.py`: interactively open and close blocks.

The last one to be executed is the main program: `9999-main.py`

A good starting point is `0100-put.py`, it is heavily commented.


## Technical points

Beware: use only Python basic functionalities because it is
not really Python, but it is JavaScript wrote with the Python syntax.

Beware: all the files are concatenated.
So the global variables are common to all the files.


### The standard block

All the blocks use a list of `Item` named `items`
defined in `0005-framework.py`.
They are all displayed using the same method defined in `0015-SRC.py`



#### The `Item`

The most useful attributes of an `Item` are:

  * `x`, `y`: screen position in column and row.
  * `char`: user friendly string displayed on the screen.
  * `value`: the item value
  * `rule`: the meaning depends on the block
  * `children`: for trees. The leaves must also been defined in the list.
  * `previous_items`: the items in the previous blocks that triggered the
                      creation of this item.
  * `next_items`: the created items in the next block.
  * `color`: the CSS color of the item.
  * `error`: there is an error for this item: red background.

The most important method of item is `clone()`,
is is good starting point to create an item in the current
using an item from the last block.


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

Calling a hook and so all the functions added (in the order of addition):

```python
  XYZ.call('hook-name', data)
```

The hooks may be attached to `Blocks` or `Block`.

### Standard hooks

You can create or overload any hook you want.
There is the list of used hooks in the base system:

  * `init` is called by `0099-init.py`,
    so the blocks list of instances is fixed at this point.

  * `html_init` is called by `9999-main.py` to create the HTML elements.

  * `html_draw` is called when the element content must be updated.

  * `draw_cursor` is called to draw the blinking cursor.

  * `dump` is called to display the instance in an human readable form.

  * `set_time` is called to travel in the time
     (the data parameter must be an integer)
      * for `SRC` block it is used to implement undo/redo.
      * for `CPU` block it is used to see the CPU state at one point in time.
      * it will also allow in the future to see the different stages of YAC
        or OPT analysis.

  * `regtest` is called to run the regression tests.

  * `key` is called with the keyboard event as data.

  * `append` is called with the item added to the block.


The following hooks may have been defined as a simple method.
But in order to let any functionality to be added to the application
they are also defined as hooks:

  * `update_lex` is called to add a lexem to `LEX`
    the data parameter must be a list containing for example:
      * `100`: the priority of this lexem when parsing.
        0 is the higer priority.
      * `plus`: the name of the lexem, it will be used by YAC.
      * `[ \n\t]*[+][ \n\t]*`: the regular expression to match.
        the separator matching must be done at the LEX level.
      * `#808`: the color of the lexem.

  * `update_yac` is called to add a rule to `YAC`
    the data parameter must be a list containing for example:
     * `1000`: the rule priority.
     * `Binary`: the name of the rule, it will be the node name.
       the same name may be used more than once to make an `or`.
     * `['Expression', 'slash', 'Unary']` the list of lexem to match

  * `new_instruction` is called to add an instruction to the `CPU`
    the data parameter is the function emulating the instruction.
    The function may have attribute defined:
       * `fct.stox_code = 0xFF`: the instruction code.
       * `fct.stox_size = 2`: two bytes are needed after the instruction code.
       * `fct.stox_name = "foo"`: if it is not the function name

  * `update_asm` is called to add a rule to `ASM`
    the data parameter is the couple: name of the AST tree node
    and the function to call to generate the assembly and machine code
    for the node. For example `['While', asm_while]`

### The assembly langage

The function added with `update_asm` must generate the assembly language
and the machine code.

The function translating `*` `AST` node to assembly and code:

```python
def asm_multiply(block,   # The ASM block
             item     # An item from the AST block
            ):
    # Generate the code for the left operand
    asm_generate(block, item.children[0])

    # Generate the code for the right operand
    asm_generate(block, item.children[1])

    # The execution let the 2 values on the stack top
    # so now generate the multiply processor assembly line and CPU code.

    asm_Item(block,           # The ASM block
             item,            # The AST item (for cursor feedback)
             'MULTIPLY',      # The processor instructions
             '',              # No parameter
             [],              # Only one byte for the CPU code.
             # When executing multiply, display green
             # rectangles on the 2 bytes at the stack top.
             asm_feedback_binary
             )
```

There is the code of the instruction pushing the value of a variable on the stack.

```python
def asm_variable(block,  # The ASM block
             item,   # An item from the AST block
            ):
    variable_name = item.children[0].value
    if variable_name in block.variables:
            # Get the address of a yet defined variable
            addr = block.variables[variable_name]
            # The addr of the variable  must be highlighted
            #  if the cursor in SRC block is on the variable
            block.cpu.memory[addr].previous_items.append(item.children[0])
    else:
            # undefined variable used
            addr = 0xFFFF

    # Generate both the assembly line and machine code:

    asm_Item(block,             # The ASM block
             item.children[0],  # The AST item (for cursor feedback)
             'LOAD_AT_ADDRESS', # The processor instructions
             variable_name,     # instruction parameter
             asm_bytes(addr),   # A list of bytes to put after instruction code
             asm_feedback_variable # Draw the rectangle feedback on execution
             )
    block.items[-1].addr = addr # Needed by asm_feedback_variable
    if addr == 0xFFFF: # There is a problem
                block.items[-1].error = True
```


### The processor

It can be fully redefined, there is the description of
the current processor:
  * 8 bits data
  * 16 bits addresses.
  * Works on the heap.
  * Register: PC the Program Counter.
  * Register: SP the Stack Pointer.

All the data relatives to the processor and the memory and the instructions
are in stored in the `ASM` block.
It is done so because the `ASM` block generates in one stage the
assembly code and the machine code.
It is done so to avoid the creation of an assembly parser.

Useful methods of `ASM.cpu` to create new instructions are:
  * `set_PC(self, word)` change the PC register.
  * `get_data_word(self)` get the 16 bits value after the instruction code.
  * `get_data_byte(self)` get the 8 bits signed value after the instruction code.
  * `set_data_word(self, address, word)` set the 16 bits value at the indicated address.
  * `stack_push(self, value)` push the 8 bits signed value on the stack.
  * `stack_pop(self)` get the 8 bits signed value from the stack.
  * `store_at(self, address)` pop the stack top and put it at the indicated address.
  * `load_at(self, address)` push on the stack the 8 bits signed value
     stored at the indicated address.


## TODO list

The next things to enhance:

  * Allow options in the URL (source content, opened blocks...).
  * Add instructions `ROTATE(nr_items, shift)`, `JUMP FCT`, `RETURN`.
  * Add an integer to boolean function and use it for comparison operators.
  * Add optimization: `while(a>b)` become `while>(a,b)`.
  * Add documentation/parameters at the block bottom.
  * Add time travel to the syntactic analyzer: it is needed for debugging.
