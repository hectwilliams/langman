.. .. Langman documentation master file, created by
..    sphinx-quickstart on Mon Jan 29 21:37:14 2024.
..    You can adapt this file completely to your liking, but it should at least
..    contain the root `toctree` directive.

.. Welcome to Langman's documentation!
.. ===================================

..    :maxdepth: 2
..    :caption: Contents:

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

.. langman documentation master file, created by
   sphinx-quickstart on Tue Jan 23 09:43:48 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Langman documentation
===================================
.. .. toctree::
..    :maxdepth: 2
..    :caption: Contents:
..    :numbered:

Flask Server API
________________
.. automodule:: server.app
   :exclude-members: metadata, registry, methods
   :members:


Database ORM and Schema
_______________________
.. automodule:: server.langman_orm
   :exclude-members: metadata, registry, methods
   :members:

Client Stylesheet 
__________________

`Storybook Stylesheet <_static/storybook-static/index.html>`_ (``Requires Javascript``)

Client Application
__________________
The following describes the Javascript client.

.. js:module:: App 

.. js:class:: App 

   .. js:method:: constructor(props)
   
      The React lifecycle method to initialize the component. Sets the state `gameStatus` to 'logged out'. Also, bind methods.

      :param props object: The collection of properties for the object, which are typically set using JSX within a render method. 

   .. js:method:: startGame(nameValue, langValue)

      Contacts server to start a new game, then updates state accordingly.

      :param nameValue string: Name of player
      :param langValue string: Two-letter string indicating language choice 

      State is set for ``username``, ``language``, ``gameId``, ``badGuesses``, ``guessed``, ``playerId``, ``revealWord``


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

