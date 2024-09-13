Paradigm Shift
==============

With the update to version 1.0.0, ``optschedule`` has switched the
programming paradigm from object-oriented to procedural programming.
Before the update, the package would be used by first instantiating an
object of ``optschedule.Schedule`` class, then calling one of its
methods to create a schedule array:

.. code:: python

   import optschedule as sch

   # Creating a learning rate schedule
   schedule = sch.Schedule(n_steps = 1000) learning_rate =
   schedule.exponential_decay(initial_value=0.1, decay_rate=0.5)

   #... [insert schedule application]

With this update, schedule arrays can be created directly by calling one
of the `optschedule` functions and passing `n_steps` argument directly to the
function, without the need to instantiate `optschedule.Schedule` object:

.. code:: python

   import optschedule as sch

   # Creating learning rate schedule
   learning_rate = sch.exponential_decay(n_steps=1000, initial_value=0.1, decay_rate=0.5)

   #... [insert schedule application]

Note that function names, definitions and computations have remained the
same. For example, creating the exponential decay schedule works the
same as before, just instead of instantiating the object with
``n_steps`` argument, then calling ``exponential_decay()`` method, the
user can call ``exponential_decay()`` function directly from
``optschedule`` package and pass the ``n_steps`` argument (along with
others) to the function itself.

Reasons for the shift
---------------------

The primary reason for the shift is to remove the redundancy of
instantiating an object. This is considered unnecessary as it is
unlikely that the object will be used more than once. Another reason for
the shift is to make the package easier to use for non-developers
(scientists, academics, professionals), who might not have an intuitive
grasp of object-oriented paradigm.

Deprecation plan
----------------

While the default way of using ``optschedule`` now is the procedural
paradigm, ``optschedule.Schedule`` class is kept in the code base
(though sidelined) and there is no plan to remove it. This means users
will still be able to use their old code with ``optschedule.Schedule``
objects, with the only difference being deprecation warnings with every
use. It is strongly recommended, however, to adjust your codes to the
new paradigm.
