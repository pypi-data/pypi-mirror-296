.. include:: ../shared.rst

-------------
Fragmentation
-------------

|Fragment| is designed to handle arbetrary fragmentation problems, not just the many-body expansion. This is facilitated by a set-theoery based formalism where molecular systems defined as sets of nuclei. [gmbe]_


Math Details
============

Ineranlly systems and fragments are defined as sets of nuclei.

.. math:: 
    :name: eq:system

    F_A = \big\{A_1, A_2, \dots, A_n\big\} \;

In this formalism :math:`F_A` is a fragment consisting of multiple atoms :math:`A_n`. 

Once we have a system, we define how we want to partition atoms in the system into to form fragments. Atoms can belong to more than one fragment meaning they are free to overlap. These fragments constitute a fragmentation scheme which is a just a set of fragments (a set of sets)

.. math::
    :name: eq:scheme
    
    S_x = \big\{ F_A, F_B, F_C, \dots, F_N \big\} \;

In this formalism the subscript :math:`x` indicates this is a unique scheme. For a given supersystem there are many ways to partition the atoms so there are many different fragmentation schemes.

Then energy (or any property for that matter) can be calculated using the cardinalities derived from the `inclusion-exclusion <https://en.wikipedia.org/wiki/Inclusion–exclusion_principle>`_

.. math:: 
    :name: eq:energy

    E^{(x)} = \sum_{i \in S_x} C_{i,x} E_i

where :math:`C_{i,x}` is a weighting coefficient which prevents double counting. The simple way to calculate these coefficients is to start with a single fragment from out target scheme

.. math:: 
    :name: eq:target

    S_0 = \big\{F_A \big\}

and setting :math:`C_{A,0} = 1` and adding each fragment one-by-one by following two rules:

1. The fragmentation scheme is updated by adding then new fragment `and` the intersections between the new fragment and all fragments already in the scheme

.. math::
    :name: eq:s_update

    S_{x + 1} = S_x \cup \{ F_{\alpha} \} \cup \big\{ F_{\alpha} \cap F_{i}: F_{i} \in S_{x} \big\} \; .

2. The energy (and the weighting coefficients) are updated as

.. math:: 
    :name: eq:E_update

    E^{(x + 1)} = E^{(x)} + \Delta E^{(x + 1)}

where

.. math::
    :name: eq:E_delta

    \Delta E^{(x + 1)} = E_\alpha - \sum_{i \in S_x} C_{i,x} E_{i \cap \alpha} \;

which resolve the overlaps and double counting between fragments.
