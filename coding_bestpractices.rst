General hints
-------------

- Learn how to use wave assignment statements using ``p, q, r, s``

- Avoid GUI functions like ``ControlInfo`` in performance critical code
  as they are comparatively slow

- Use builtins instead of homebrown algorithms, operations like
  ``MatrixOP`` and ``Extract`` do their job fast and good

- Keep the number of memory allocations low, the most common operations
  to look out for are ``Make``, ``Redimension`` and ``Duplicate``

Anti Patterns
-------------

if and do/while instead of for loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   if(i > 0)
       do
           // do stuff
       while(i < count)
   endif

Good:

.. code-block:: igor

   for(i = 0; i < count; i += 1)
       // do stuff
   endfor

Reasons:

- Easier to understand
- Shorter
- Less indentation

Inconsistent WAVE/DFREF/NVAR/SVAR usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   WAVE/Z wv = mywave
   numRows = DimSize(wv, 0)

Good:

.. code-block:: igor

   // either if the wave always exists, don't add /Z
   WAVE wv = mywave
   numRows = DimSize(wv, 0)

   // or, if it might not exist, handle that case
   WAVE/Z wv = mywave

   if(!WaveExists(wv))
       Abort "Missing wave"
   endif

   numRows = DimSize(wv, 0)

Reasons:

- Unclear intent
- Possibly incorrect

Treating boolean variables as non-boolean
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   // code which shows that var can be either 1 or 0
   if(var == 1)
       // code
   elseif(var == 0)
       // code
   endif

Good:

.. code-block:: igor

   // In case var can be only 1 or 0, write it as
   if(var)
       // code
   else
       // code
   endif

   // Or handle the case where var != 1 and var != 0
   if(var == 1)
       // code
   elseif(var == 0)
       // code
   else
       // new code
   endif

Reasons:

- Unclear intent
- Possibly incorrect

Superfluous comparison for boolean values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   if(WaveExists(wv) == 1)
       // code
   endif

Good:

.. code-block:: igor

   if(WaveExists(wv))
       // code
   endif

Reasons:

- Less verbose code

Unnecessary variables
^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   variable var = GetVariable()
   SetVariable control value = _NUM:var
   // code which does not use var anymore

Good:

.. code-block:: igor

   SetVariable control value = _NUM:GetVariable()

Reasons:

- Shorter code
- Less variables

Wave/Datafolder creator functions don’t return the just created objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   Function CreateWave(varible param)

       Make myWave
   End

   Function someOtherFunction()

       WAVE/Z myWave

       if(!WaveExists(myWave))
           CreateWave(param)
       endif

       WAVE myWave
   End

Good:

.. code-block:: igor

   Function/Wave GetWave(variable param)

       // GetWaveFolder has the same logic as GetWave
       // Creates the datafolder if it does not exist
       // and returns a reference to it
       DFREF dfr = GetWaveFolder(param)

       WAVE/Z/SDFR=dfr data
       if(WaveExists(data))
           return data
       endif

       Make dfr:data/WAVE=data
       // fill wave with default content

       return data
   End

   Function someOtherFunction()
       WAVE wv = GetWave(param)

       // code
   End

Reasons:

- More reliable to use
- Less code at the call site
- Avoids code duplication at the call site
- Allows to handle changes to the wave structure in one place
  (centralized resource management)

Unnecessary use of StringMatch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   if(StringMatch(str, ""))
       // code
   endif

   if(StringMatch(str, "abcd"))
       // code
   endif

Good:

.. code-block:: igor

   // can be written with a helper function if(isEmpty(str))
   if(!cmpstr(str, ""))
       // ...
   endif

   // StringMatch is only required if you want to
   // use ! or * in the second parameter
   if(!cmpstr(str, "abcd"))
       // ...
   endif

Reasons:

- Faster
- Better readability

Unnecessary loops
^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   for(i = 10; i < 101; i += 1)
       mywave[i] = i^2
   endfor

Good:

.. code-block:: igor

   mywave[10, 100] = p^2

Reasons:

- Much faster (at least ten times)

See also ``DisplayHelpTopic "Waveform Arithmetic and Assignment"`` for
an in-depth introduction to the topic.

Unnecessary use of sprintf
^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   string str
   sprintf str, "%s", GetName()

Good:

.. code-block:: igor

   string str = GetName()

Reasons:

- Better readability
- Shorter
- Faster

Unnecessary use of Execute
^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   string cmd
   sprintf cmd, "wv = 1 + 2"
   Execute cmd

Good:

.. code-block:: igor

   wv = 1 + 2

Reasons:

- Better readability
- Shorter
- Faster

Avoid relying on the top window and prefer structure based GUI control procedures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   Function ButtonProc(string ctrlName) : ButtonControl

       GetWindow kwTopWin wtitle
       DoStuff(s_value)
   End

Good:

.. code-block:: igor

   // In case execution of this ButtonControl takes a long time
   // and you want to prevent another call while the first is still
   // progressing have a look at WMButtonAction::blockreentry
   Function ButtonProc(STRUCT WMButtonAction &ba) : ButtonControl

       switch(ba.eventCode)
           case 2:
               DoStuff(ba.win)
               break
       endswitch

       return 0
   End

Reasons:

- Less error prone (the top window could be different if ButtonProc is
  called programmatically)
- Easily expandable to other events
- Faster as only a reference to the structure must be passed to the
  function

Avoid magic numbers
^^^^^^^^^^^^^^^^^^^

Bad:

.. code:: igor

   settings[11][] = height

Good:

.. code:: igor

   // either with file level constants
   static Constant HEIGHT_ROW = 11

   Function DoStuff()

       settings[HEIGHT_ROW][] = height
   End

   // or dimension labels, use SetDimLabel on the wave before
   settings[%height][] = height

   // or a set function (rarely an appropriate choice)
   Function SetHeight(WAVE settings, variable height)

       settings[11][] = height
   End

   SetHeight(settings, height)

Reasons:

- Better readability

- Less error prone

Unused parameters
^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   Function/S GetPath(string param)

       return "root:myFolder"
   End

Good:

.. code-block:: igor

   Function/S GetPath()
       return "root:myFolder"
   End

Reasons:

- Better readability
- Does not fake a dependency of the function upon the parameter

.. note::

   Unused function variables and file level constants should also be
   avoided. As there is currently no support from Igor Pro in doing that,
   visual inspection must be performed.

Avoid function calls in loop statements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bad:

.. code-block:: igor

   for(i = 0; i < ItemsInList(list); i += 1)
       // code
   endfor

Good:

.. code-block:: igor

   numItems = ItemsInList(list)
   for(i = 0; i < numItems ; i += 1)
       // code
   endfor

Reasons:

- Faster, the bad example calls ``ItemsInList`` every time the loop
  condition is executed

Performance tests
-----------------

Dimension labels versus numerical indizes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the following code

.. code:: igor

   #pragma rtGlobals=3
   #pragma igorVersion=6.3
   #include <FunctionProfiling>

   static Constant SIZE = 1e5

   Function Prepare()

       variable i

       Make/O/N=(SIZE) data = p^2

       for(i = 0; i < SIZE; i += 1)
           SetDimLabel 0, i, $num2str(i), data
       endfor
   End

   Function Dimlabel()

       string str
       variable i, acc
       Wave data

       for(i = 0; i < SIZE; i += 1)
           str = num2str(i)
           acc += data[%$str]
       endfor

       print/D acc
       print str
   End

   Function NumericalIndex()

       string str
       variable i, acc
       Wave data

       for(i = 0; i < SIZE; i += 1)
           // The num2str call is included here in order to minimize
           // the number of differences compared to Dimlabel()
           str = num2str(i)
           acc += data[i]
       endfor

       print/D acc
       print str
   End

   Function PerformTest()

       Prepare()
       print "Array indexing with dimlabels"
       print "Array indexing with dimlabels"
       RunFuncWithProfiling(Dimlabel)

       print "Array indexing with numerical indizes"
       RunFuncWithProfiling(NumericalIndex)
   End

we can compare the speed of dimension labels and numerical indizes.
This approach asssumes that the ``$`` operator can be ignored in terms
of execution speed.

Calling ``PerformTest()``

.. code:: text

     Array indexing with dimlabels
     333328333526912
     99999
     Total time=   21.39
     Array indexing with numerical indizes
     333328333526912
     99999
     Total time=   0.110777

clearly shows that numerical indizes are much faster than dimension
labels.

Therefore you should use numeric indizes in performance critical code
which usually is the case inside loops. In case you want to index a
fixed element in a loop by dimension labels call ``FindDimLabel``
before the loop and store the numerical index.

Versioned Waves
^^^^^^^^^^^^^^^

For waves that might change with further progression in a project it
makes sense to add a version to the wave, e.g. through its wave note.
This allows to upgrade old wave versions in case a customer loads an
old experiment and want to use it with a current program version.
A typical solution for such a getter function could look like this:

.. code-block:: igor

   Function/WAVE GetMyVersionedWave()

        string name = "myWave"
	variable versionOfNewWave = 4
	variable size = 9

	DFREF dfr = GetSourceDF()

	WAVE/Z/D/SDFR=dfr wv = $name

	if(ExistsWithCorrectLayoutVersion(wv, versionOfNewWave))
		return wv
	endif

	if(WaveExists(wv))

        // wave upgrade steps
		if(WaveVersionIsSmaller(wv, 2))
			Redimension/D/N=(7) wv
			wv[5, 7]     = NaN
		endif
		if(WaveVersionIsSmaller(wv, 3))
			Redimension/D/N=(10) wv
			wv[8,]     = NaN
		endif
		if(WaveVersionIsSmaller(wv, 4))
			DeletePoints/M=(ROWS) 4, 1, wv
		endif
	else
        // wave creation
		Make/D/N=(size) dfr:$name/WAVE=wv
		wv = NaN
	endif

	SetDimLabel ROWS, 0, firstRow, wv
	SetDimLabel ROWS, 1, secondRow, wv
	SetDimLabel ROWS, 2, thirdRow, wv
	SetDimLabel ROWS, 3, fourthRow, wv
	SetDimLabel ROWS, 4, fifthRow, wv
	SetDimLabel ROWS, 5, sixthRow, wv
	SetDimLabel ROWS, 6, seventhRow, wv
	SetDimLabel ROWS, 7, eighthRow, wv
	SetDimLabel ROWS, 8, ninthRow, wv

	SetWaveVersion(wv, versionOfNewWave)

	return wv
   End

The functions ``ExistsWithCorrectLayoutVersion``, ``WaveVersionIsSmaller`` and ``SetWaveVersion`` have to be implemented.

Notably the wave upgrade branch does each version upgrade sequentially.
These steps should contain clear code that allows to understand what was changed with each version upgrade.
Typically the change of the wave size (``Redimension``) and initial values setting must be part of each version upgrade.
In some cases it can be also useful to include the DimLabel changes in the upgrade steps.

It is not recommended to optimize changes over multiple versions in the upgrade steps.
e.g. in the upper example considering upgrade until version 3 one might think that the ``Redimension`` could be pulled
as ``Redimension/N=(size)`` before the upgrade steps because the wave size increases with each step up to version 3.
But such optimization is incompatible with the change introduced later with version 4, where a previous row gets deleted.

It is recommended to move complex upgrade changes into their own functions.
