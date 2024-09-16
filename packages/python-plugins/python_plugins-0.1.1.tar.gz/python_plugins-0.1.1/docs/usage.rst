=====
Usage
=====

.. _installation:

Installation
==============

Install and update using pip:

.. code-block:: console

   (.venv) $ pip install -U python-plugins

email
======

.. code-block:: python
   
   # smtp's host
   host = "smtp.host"
   port = "465"
   # smtp's username and password
   user = "test@test.com"
   password = "your password"

   # receiver and subject and content
   to = "test2@test.com"
   data = {
      "to": to,
      "subject": "subject of msg",
      "content": "content of msg",
   }

   s = SmtpSSL(host, port, user, password)
   r = s.send_emsg(data)