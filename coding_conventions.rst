Procedures
----------

- Always put code into external procedure files stored directly on
  disk

- Filenames are built from the characters ``[A-Za-z_-]`` and end with
  ``.ipf``

- For code used exclusively with Igor Pro 7 or higher use UTF-8 as text
  encoding and specify ``#pragma TextEncoding = "UTF-8"``. For lower versions
  the file encoding is OS-dependent, but the used charset should always be
  restricted to ASCII characters.

- The beginning of each procedure file has ``#pragma rtGlobals=3`` with
  optional comment

- For new code ``#pragma rtFunctionErrors=1`` is mandatory

- Always use UNIX (LF) end-of-line style

Whitespace and Comments
-----------------------

Comments
^^^^^^^^

- Use `doxygen <https://doxygen.nl>`__ for documenting files, functions, macros and
  constants. There is an `AWK script <https://github.com/byte-physics/doxygen-filter-ipf>`__
  available to use Igor Pro Files with Doxygen.

- Always add a space before a trailing comment as in

  .. code-block:: igor

     if(a < 0)
         b = 1
     else // positive numbers (including zero)
         b = 4711
     endif

- Prefer comments on separate lines instead of trailing comments

Doxygen
^^^^^^^

- Use ``///`` to start a doxygen comment and ``///<`` for documentation
  after the definition

- Align multiple ``@param`` arguments and document them in the same
  order as in the function signature:

  .. code-block:: igor

     /// @param pressure     Pressure of the cell
     /// @param temperature  Outdoor temperature
     /// @param length       Length of a soccer field
     Function PerformCalculation(variable pressure, variable temperature, variable length)

         // code
     End

- Use ``in/out`` specifiers for ``@param`` if the function uses
  call-by-value and call-by-reference parameters.

  .. code-block:: igor

     /// @param[in]  name    Name of the device
     /// @param[out] type    Device type
     /// @param[out] number  Device number
     Function ParseString(string name, variable &type, variable &number)

         // code
     End

- Optional parameters are documented as

  .. code-block:: igor

     /// @param verbose [optional, default = 0] Verbosely output
     ///                the steps of the performed calculations
     Function DoCalculation([variable verbose])

         // code
     End

- For documenting multiple return values use ``@retval`` as in

  .. code-block:: igor

     /// @param key     key to look for
     ///
     /// @retval result one on error, zero otherwise
     /// @retval unit   unit of the result [empty if not found]
     Function [variable result, string unit] GetProperty(string key)
         // code
     End

Whitespace
^^^^^^^^^^

- Every function should be separated by exactly one newline from other
  code

- Indentation is done with tabs, a tab consists of four spaces (in case
  you are coding not in Igor Pro).

- Comments on separate lines have the same indentation level as the
  surrounding code

- Separate function parameters from local variables and local variables
  from the rest of the function body by a newline

  .. code-block:: igor

     Function CalculatePressure(variable weight, variable size)

         variable i, numEntries

         // code
     End

- If you are targeting Igor Pro 7 or higher prefer inline parameter
  declarations as in

  .. code-block:: igor

     Function CalculatePressure(variable weight, variable size)

         variable i, numEntries

         // code
     End

  as that is easier to grasp for newcomers. And also works with
  multiple-return-value syntax.

- Add a space around mathematical/binary/comparison/logical operators and
  assignments, and add a space after a comma or semicolon

  .. code-block:: igor

     a = b + c * (d + 1) / 5

     if(a < b)
         c = a^2 + b^2
     end

     Make/O/N={1, 2} data

     for(i = 0; i < numWaves; i += 1)
         a = i^2
     endfor

     if(myStatus && myClock)
         e = f
     endif

     h = i | j

- Always avoid trailing whitespace, that is whitespace directly before the end-of-line character.
  Here ``␣`` denotes a space, and ``→`` a tab.

Good:

  .. code-block:: igor

     Function␣DoStuff()

     →print␣"Hi"

     →if(a␣<␣b)
     →→c␣=␣a^2␣+␣b^2
     →endif

     →Make/O/N={1,␣2}␣data
     End

Bad:

  .. code-block:: igor

     Function␣DoStuff()␣␣␣␣

     →print␣"Hi"␣␣

     →if(a␣<␣b)→
     →→c␣=␣a^2␣+␣b^2
     →endif→→␣

     →Make/O/N={1,␣2}␣data
     End

- Line continuation, available with Igor Pro 7 or higher, requires indentation
  with tabs as always, but alignment with spaces and a space in front of ``\\``.
  Multiple line continuation characters should be vertically aligned.
  ``␣`` denotes again a space, and ``→`` a tab.

  .. code-block:: igor

     Function␣DoStuff()

     →string␣str␣ =␣ "abcd"␣␣␣\
     →␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣+␣"efgh"␣\
     →␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣+␣"ijk"␣␣\

     →if(A && B \
     →␣␣␣&& C)
     →→// code
     End

- Surround blocks like ``if/endif``, ``for/endfor, ``do/while``, ``switch/endswitch``,
  ``strswitch/endswitch`` with a newline if what they express is a logical group of its own

  .. code-block:: igor

     for(i = 0; i < numEntries; i += 1)
         // code
     endfor

     if(a > b)
         c = d
     elseif(a == b)
         c = e
     else
         c = 0
     endif

     switch(mode)
         case MODE1:
             a = "myString"
             break
         case MODE2:
             a = "someOtherString"
             break
         default:
             Abort "unknown mode"
     endswitch

  According to that reasoning the following snippet has no newline
  before ``for`` and ``if``

  .. code-block:: igor

     numEntries = ItemsInList(list)
     for(i = 0; i < numEntries; i += 1)
         // code
     endfor

     NVAR num = root:fancyNumber
     if(num < 5)
         // code
     endif

  When mutiple end statements match

  .. code-block:: igor

     for(i = 0; i < numEntries; i += 1)
         // code

         if(i < 5)
             // code
         endif
     endfor

  you should not add a trailing newline.

- There is no whitespace between different flags of an operation and no
  whitespace around ``=`` if used in a flag assignment.

  Good:

  .. code-block:: igor

     Wave/Z/T/SDFR=dfr wv = myWave

     Function/S DoStuff()
         // code
     End

  Bad:

  .. code-block:: igor

     Wave /Z /T /SDFR = dfr wv = myWave

- The ``&`` in a call-by-reference parameter is attached to the name

  Good:

  .. code-block:: igor

     Function DoStuff(variable &length, variable &height, variable &weight)

         // code
     End

  Bad:

  .. code-block:: igor

     Function DoStuff(variable& length, variable & height, variable  &  weight)

         // code
     End

Code
----

General
^^^^^^^

- Line length should not exceed 120 characters

- Use ``camelCase`` for variable/string/wave/dfref names and
  ``PascalCase`` for functions and structures

- Prefer structure-based GUI control procedures over old-style
  functions

- The variables ``i, j, k, l`` are reserved for loop counters, from
  outer to inner loops

- Use free waves for temporary waves as they are faster to work with

- Prefer generic builtin functions like ``IndexToScale``, ``DimSize`` over
  their 1D counterparts ``pnt2x``, ``numpnts``.

- Avoid generic functions like ``exists`` and prefer ``WaveExists``,
  ``NVAR_Exists``, ``SVAR_Exists``, etc.

- Write your code as much as possible without ``SetDataFolder``.
  Properly document if your function expects a certain folder to be the
  current data folder at the time of the function call. Always restore
  the previously active current data folder before returning from the
  function.

- Although Igor Pro code is case-insensitive use the offical
  upper/lower case as shown in the Igor Pro Help files for better
  readability

  .. code-block:: igor

     Make/N=(10) data
     AppendToGraph/W=$graph data
     WAVE/Z wv
     SVAR sv = abcd
     STRUCT Rectangular rect
     print ItemsInList(list)

  except for the following two cases:

  .. code-block:: igor

     variable storageCount
     string name

- Variable and function definitions and references to them must also
  never vary in case

- Don’t use variables for storing the result which is then returned

  Good:

  .. code-block:: igor

     if(someCondition)
         // code
         return 0
     else
         // code
         return 1
     endif
     // if it is important to know that the returned value
     // is a status, name the function something like GetStatusForFoo
     // and/or use the @return doxygen comment for explaining its meaning

  Bad:

  .. code-block:: igor

     variable status

     // code

     if(someCondition)
         // code
         status = 0
     else
         // code
         status = 1
     endif

     return status

- Avoid commented out code

- Don’t initialize variables and strings if not required and always
  initialize them on their own line.

  Good:

  .. code-block:: igor

     variable i = 1
     variable numEntries, maxLength
     string list

  Bad:

  .. code-block:: igor

     variable i = 0, numEntries = ItemsInList(list), maxLength
     string list = ""

- Don’t use the default value for an optional argument

  Good:

  .. code-block:: igor

     StringFromList(0, list)

  Bad:

  .. code-block:: igor

     StringFromList(0, list, ";")

- Use parentheses sparingly

  Good:

  .. code-block:: igor

     variable a = b * (1 + 2)

     if(a < b || a < c)
         // code
     endif

  Bad:

  .. code-block:: igor

     variable a = (b * (1 + 2))

     if((a < b) || (a < c))
         // code
     endif

- Use parentheses when combining operators with the same precedence

  Good:

  .. code-block:: igor

     if((A || B) && C)
         // code
     endif

     if(A == (B >= C))
         // code
     endif

  Bad:

  .. code-block:: igor

     if(A || B && C) // same as above as these are left to right
         // code
     endif

     if(A == B >= C) // same as above as these are right to left
         // code
     endif

  The reason is that remembering the exact associativity is too
  error-prone. See also ``DisplayHelpTopic "Operators"``.

- Always add a space after ``;`` when multiple statements are written
  in one line. But in general this should be avoided if possible.

- With try/catch always clear runtime errors twice

  .. code-block:: igor

     try
         err = GetRTError(1)
         WAVE wv = I_DONT_EXIST; AbortOnRTE
     catch
         err = GetRTError(1)
         // handle error
     endtry

  If you don’t clear it after ``try`` any still lingering runtime error
  will trigger an abort via ``AbortOnRTE`` and that results in
  difficult to diagnose bugs.

- Don’t mix ``$`` with other expressions as it makes the code too hard
  to read

  Bad:

  .. code-block:: igor

     WAVE/Z wv = root:$(str + "_suffix")

  Good:

  .. code-block:: igor

     string folder = str + "_suffix"
     WAVE/Z wv = root:$folder

  See ``DisplayHelpTopic "$ Precedence Issues In Commands"`` for the
  details how ``$`` works in complex expressions.

- Always add ``break`` statements in each branch of
  ``switch/strswitch`` statements. If you intentionally fallthrough
  mark that by an explicit comment. No break should be added after control flow
  statements like ``return``, ``continue``, ``Abort``, ``AbortOnValue``.

  .. code-block:: igor

     switch(state)
         case STATE_A:
             // do something
             break
         case STATE_B:
             // something else
             break
         case STATE_C: // fallthrough-by-design
         case STATE_D:
             // another thing
             break
         case STATE_E:
             return NaN
         default:
             // do nothing
             break
     endswitch

Waves
^^^^^

- In multidimensional wave assignments always specify the exact
  dimension for each value:

  .. code-block:: igor

     Make/N=(1,1,2) data = NaN
     data[0][0][] = 0

  In this example data will be set to ``0`` for both values. Each
  dimension is specified: p and q are fixed to ``0`` and both values in
  dimension r are set to ``0``.

  .. code-block:: igor

     Make/N=(1,1,2) data = NaN
     data[0][0] = 0

  In this example the output will be ``0`` and ``NaN`` when using Igor
  Pro 7 or higher. In Igor Pro 6 the assignement will result in ``0``
  for both values. The deprecated behaviour can be enabled in later versions by
  setting an Igor Option:

  .. code-block:: igor

     SetIgorOption FuncOptimize, WaveEqn = 1

  Therefore to avoid confusing code always specify what value should go in which
  dimension (row, column, layer, chunk).

Constants
^^^^^^^^^

- Use ``SNAKE_CASE`` for constants

- Static constants, which are required only in one file, should be
  defined at the top of the file

- Global constants are collated in a single file

- Explain magic numbers in a comment

  .. code-block:: igor

     static Constant DEFAULT_WAVE_SIZE = 128 // equals 2^8 which is
                                             // the width of the DAC signal

Macros
^^^^^^

- Use Macros only for window recreation macros

- Try to avoid changing window recreation macros by hand. Write instead
  a function to reset the panel to the default state and let Igor Pro
  rewrite the macro by ``DoWindow/R``.

- Don't mix machine generated code with developer maintained code. It is
  therefore advisable to put window recreation macros into separate procedure
  files.

Functions
^^^^^^^^^

- Try to keep their length below 50 lines (or half the screen height)

- Use ``PascalCase`` for function names (optionally prefixed by a
  ``SNAKE_CASE`` string ending in ``_`` denoting the filename)

- Make them ``static`` if they are only required inside the same
  procedure file

- Define all variables at the top of the function body as in

  .. code-block:: igor

     Function CalculatePressure(variable weight, variable size)

         variable i, numEntries

         // code
     End

  The reason for this rule is that there is no block-scope in Igor Pro,
  i. e.

  .. code-block:: igor

     if(someCondition)
         variable a = 4711
     endif

     print a

  is valid code. And that certainly will confuse people coming from
  C/C++.

  Please also note that in the example above a blank line separates
  the function declaration from general variable definitions.
  This will improve readability.

- Optional arguments should have defined default values:

  .. code-block:: igor

     Function DoCalculation(variable input, [variable verbose])

         if(ParamIsDefault(verbose))
             verbose = 0
         endif

         // code
     End

- Function Call with optional arguments:

  .. code-block:: igor

     DoCalculation(41, verbose = 1)

  When calling a function, each argument is separated by a comma
  followed by a whitespace. Optional arguments are set with surrounding
  white spaces before and after the equal sign.

- Boolean optional arguments should be forced to (0,1)

  .. code-block:: igor

     Function DoCalculation([variable overwrite])

         overwrite = ParamIsDefault(overwrite) ? 0 : !!overwrite

         if(overwrite)
             // Some Code
         endif

         if(!overwrite)
             // Negation will work as expected
         endif
     End

  Without the double negation statement none of the above ``if``
  statements would get triggered if ``overwrite = NaN`` as both ``NaN`` and
  ``!NaN`` are false.

  This is also demonstrated in the following example

  .. code-block:: igor

     Function NaNisNotBool()
         if(NaN)
             print 0
         elseif(!NaN)
             print 1
         else
             print 2
         endif
     End

- If you don’t care about a function result, return ``NaN``/``""``/``$""``

  .. code-block:: igor

     Function Dostuff()

         if(!IsSomethingToDo())
             return NaN
         endif

         // code
     End

  The reason for this rule is that it makes the code easier to
  understand as these are the default return values (without
  multiple-return-value syntax) used by Igor Pro.

- Set pass-by-reference parameters to a save default value immediately
  at the beginning of the function and after the variable declarations

  .. code-block:: igor

     Function Dostuff(variable &param)

         string str

         param = NaN

         if(!isSomethingToDo())
             return NaN
         endif

         // code
     End

  The reason is that all function return paths should return
  well-defined values in the returned pass-by-reference parameters. If
  the passed parameter is a structure, write a structure initialization
  function to handle setting it to a safe default and call that.

- Be aware of the different initial values for return values when using
  multiple-return-value (MRS) syntax.

  .. code-block:: igor

     Function [variable var] New()
         // code
     End

     Function Old()
         // code
     End

  The function ``New()`` returns ``0.0`` whereas ``Old()`` returns
  ``NaN``.

Avoid Memory Leaks
^^^^^^^^^^^^^^^^^^

- When a functions that returns a free wave is called in an operation
  call or user-defined function call directly as parameter the free
  wave is not freed and thus causes a memory leak. To avoid these
  cases, free waves that are returned from functions must always
  be assigned to a wave reference variable.

  .. code-block:: igor

     Function/WAVE ReturnsFreeWave()

       Make/FREE wv

       return wv
     End

     Function LeakExample()
         Duplicate ReturnsFreeWave(), targetWave // Bad! Causes leak, DO NOT USE
         max = WaveMax(ReturnsFreeWave()) // Bad! Causes leak, DO NOT USE

         WAVE w = ReturnsFreeWave() // Good
         Duplicate w, targetWave

         WAVE w = ReturnsFreeWave() // Good
         max = WaveMax(w)
     End

Bitwise vs. logical operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Sometimes there are situations where the use of logical and bitwise
  operators gives technically the same result. However, if a function
  returns a true/false value, which in principal could be some abstract
  object then logical operators have to be used. This applies also for
  variables that use a value as flag to indicate a true/false state.
  This leaves bitwise operators for bit calculations that commonly
  include two or more bits.

  .. code-block:: igor

     Function IsFreeWave(WAVE wv)

         return WaveType(wv, 2) == 2
     End

     Function DoStuff()

         variable truthValue = 1
         variable bitValue = 0x10
         Make/FREE wv

         // use logical operation
         if(IsFreeWave(wv) && truthValue)
            // do something
         endif

         bitValue = bitValue << 2
         // Use bitwise operation
         print bitValue & 0x40

     End

Prefer named entities over unnamed ones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- For historircal reasons developers can use unnamed user data, background
  functions and window hooks. But as these are limited to one instance, it is
  always more appropriate, and future-proof, to use the named variants instead.

  Good:

  .. code-block:: igor

     SetWindow panel0 hook(cleanup)=DoPanelCleanup

     SetWindow panel0 userData(key)=abcd

     CtrlNamedBackground start, proc=DoStuffInBackground

  Bad:

  .. code-block:: igor

     SetWindow panel0 hook=DoPanelCleanup

     SetWindow panel0 userData=abcd

     SetBackground DoStuffInBackground()
     CtrlBackground start

No code outside the event switch in GUI control procedures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- GUI control procedures are called for all Igor Pro events. Some of these
  events, like the mouse-over event, can be fired very often. To keep the GUI
  responsive, it is therefore much more performant to avoid executing any code
  outside the switch statement.

  Good:

  .. code-block:: igor

     Function ButtonProcStart(STRUCT WMButtonAction &ba) : ButtonControl
       string method

       switch(ba.eventCode)
         case 2: // mouse up
           method = "fast"
           // ...
           break
       endswitch
     End

  Bad:

  .. code-block:: igor

     Function ButtonProcStart(STRUCT WMButtonAction &ba) : ButtonControl
       string method = "slow"

       switch(ba.eventCode)
         case 2: // mouse up
           // ...
           break
       endswitch
     End
