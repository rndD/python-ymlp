# -*- coding: utf-8 -*-
# ympl.py
# - User: rnd_d - st00nsa@gmail.com
# - Date: 8/22/12
# - Time: 6:16 PM
# - Description: API wrapper for http://www.ymlp.com/ | CC-BY-SA

import urllib
import logging
import inspect
import datetime

try:
    from django.utils import simplejson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

def whoami():
    """
    @return: Name of the function that calls this function
    @rtype: str
    """
    return inspect.stack()[1][3]

class YMLPException(Exception):
    pass

class YMLPSection(object):
    @classmethod
    def make_request(cls, command, args = None):
        """

        """
        return  cls.manager.make_request("%s.%s" % (cls.__name__, command ), args)


class YMLPManager(object):
    API_URL = "https://www.ymlp.com/api/"
    OUTPUT_FORMAT = "JSON"

    def __init__(self, username, key):
        self.key = key
        self.username = username

        self.Contacts.manager,\
        self.Groups.manager,\
        self.Fields.manager,\
        self.Filters.manager = self, self, self, self

    def make_request(self, command , args = None):
        if args is None:
            args = {}

        args["Key"] = self.key
        args["Username"] = self.username
        args["Output"] = self.OUTPUT_FORMAT
        f = urllib.urlopen("%s%s?%s" % (self.API_URL, command, urllib.urlencode(args)))
        result = json.loads(f.read())
        return result

    class Contacts(YMLPSection):

        @classmethod
        def Add(cls, email, group_id = None, overrule_unsubscribed_bounced = None, fields = None):
            """
            Contacts.Add() adds a new contact to one or more groups in your database.
            @param email:
            @param group_id: ID of the group or a comma-separated list of groups IDs; use Groups.GetList() to retrieve the ID for each group.
            @param overrule_unsubscribed_bounced: "0" or "1" (optional, default is "0"); if "1", the email address will be added even if this person previously unsubscribed or if the email address previously was removed by bounce back handling
            @param fields:data for any other field can be sent using the following syntax: FieldX=value (e.g.: Field2=John), where X is the ID of the field (use Fields.GetList() to retrieve the ID for each field)
            @type fields: dict
            """

            args = {
                "Email" : email
            }
            if not group_id is None:
                args["GroupId"] = group_id

            if not overrule_unsubscribed_bounced is None:
                args["OverruleUnsubscribedBounced"] = overrule_unsubscribed_bounced

            if fields:
                for field_id in fields:
                    args["Field%s" % field_id] = unicode(fields[field_id]).encode('utf-8')

            result = cls.make_request(whoami(), args)
            if result.get("Code") == "0":
                logging.info("%s : %s" % (datetime.datetime.now(), result.get("Output")))
                return True
            raise YMLPException(result.get("Code"), result.get("Output"))


        @classmethod
        def Delete(cls, email, group_id = None):
            """
            Contacts.Delete() removes a given email address from one or more groups.
            @param email:
            @param group_id:
            @rtype: bool
            """
            args = {"Email": email}
            if not group_id is None:
                args["GroupId"] = group_id
            result = cls.make_request(whoami(), args)
            if result.get("Code") == "0":
                logging.info("%s : %s" % (datetime.datetime.now(), result.get("Output")))
                return True
            raise YMLPException(result.get("Code"), result.get("Output"))

        @classmethod
        def Unsubscribe(cls, email):
            """
            Contacts.Unsubscribe() unsubscribes a given email address.
            @param email:
            @type email: str
            """
            args = {"Email": email}
            result = cls.make_request(whoami(), args)
            if type(result) is dict:
                if result.get("Code") == "0":
                    logging.info("%s : %s" % (datetime.datetime.now(), result.get("Output")))
                    return True
                else:
                    raise YMLPException(result.get("Code"), result.get("Output"))
            raise YMLPException(None, "")

        @classmethod
        def GetContact(cls, email):
            """
            Contacts.GetContact() retrieves all available information regarding a contact.
            @param email:
            """
            args = {"Email": email}
            result = cls.make_request(whoami(), args)
            if type(result) is dict and result.has_key("Code"):
                raise YMLPException(result["Code"], result.get("Output"))
            logging.info("%s : %s" % (datetime.datetime.now(), result.get("Output")))
            return result

        @classmethod
        def GetList(cls):
            pass
        @classmethod
        def GetUnsubscribed(cls):
            pass
        @classmethod
        def GetDeleted(cls):
            pass
        @classmethod
        def GetBounced(cls):
            pass


    class Groups(YMLPSection):

        @classmethod
        def GetList(cls):
            """
            Groups.GetList() lists the groups in your account, along with their group IDs and the number of contacts in each group.
            @return:
            """
            result = cls.make_request(whoami())
            if type(result) is dict and result.has_key("Code"):
                raise YMLPException(result["Code"], result.get("Output"))
            return result

        @classmethod
        def Add(cls):
            pass
        @classmethod
        def Delete(cls):
            pass
        @classmethod
        def Update(cls):
            pass
        @classmethod
            def Empty(cls):
            pass


    class Fields(YMLPSection):

        @classmethod
        def GetList(cls, overrule_deleted = None):
            """
            Filters.GetList() lists the filters in your account along with the filter ID, the filter name, the criterion description and the field-operand-value combination for each filter.
            @param overrule_deleted: whether or not to include deleted filters in the output (optional): 0 (default) or 1
            @type overrule_deleted: bool
            @return:
            """
            args = {}
            if not overrule_deleted is None:
                args["OverruleDeleted"] = overrule_deleted
            result = cls.make_request(whoami())
            if type(result) is dict and result.has_key("Code"):
                raise YMLPException(result["Code"], result.get("Output"))
            logging.info("%s : %s" % (datetime.datetime.now(), result))
            return result

        @classmethod
        def Add(cls):
            pass

        @classmethod
        def Delete(cls):
            pass

        @classmethod
        def Update(cls):
            pass

        @classmethod
        def GetID(cls, fields_list, field_alias = None, field_name = None):
            if field_alias:
                field = filter(lambda x: x["Alias"] == field_alias, fields_list)
            elif field_name:
                field = filter(lambda x: x["FieldName"] == field_name, fields_list)
            else:
                raise YMLPException("Alias or name of field is not set")

            if field:
                return field[0]["ID"]
            else:
                raise YMLPException("Field not found")

    class Filters(YMLPSection):

        @classmethod
        def GetList(cls):
            pass
        @classmethod
        def Add(cls):
            pass
        @classmethod
        def Delete(cls):
            pass
