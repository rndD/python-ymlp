python-ymlp
===========

Python-ymlp is a [YMLP.COM](http://ymlp.com/) api wrapper for python, it's written in the way to copy original api strucure. For more information about YMLP api, visit [api page](http://www.ymlp.com/app/api.php).

Implemented methods:
1. Contacts 
    * Add
    * Delete
    * Unsubscribe
    * GetContact
2. Groups
    * GetList
3. Fields
    * GetList
    * GetID
4. Filters


Usage
---------
Example:

```python
from ymlp import YMLPManager
ymlp = YMLPManager(YMLP_USERNAME, YMLP_API_KEY) 
ymlp.Contacts.Add("st00nsa@gmail.com", 1) # add email in group with id 1

try:
    ymlp.Contacts.Add("st00nsa@gmail.com", 1)
except YMLPException as (code, info):
    if code == "3":                 #All error codes you can find in ymlp docs of Contancs.Add method
        print "contact already exist"

#format of returned data is exactly the same as described in the ymlp api docs
groups = ymlp.Groups.GetList()
fields_list = ymlp.Fields.GetList()
```