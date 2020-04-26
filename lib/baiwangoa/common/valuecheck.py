#
# -*- coding:utf-8 -*-


class ValueCheck(object):

    @classmethod
    def none_check(cls, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                raise ValueError("{} is not None".format(k))
        else:
            return True

    @classmethod
    def value_fill(cls, d, def_dict):
        """
        :param d: user request value dice
        :param def_dict: default replace dict
        :return: Replaced  DictPack instance
        """
        if isinstance(d, dict):
            for k, v in def_dict.items():
                d.setdefault(k, v)
            return d
        else:
            raise ValueError('{} is not dict'.format(d))

    @classmethod
    def check_port(cls, por):
        try:
            port = int(por)
            if port > 65535 or port < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Bad port:{}".format(por))
