#
# coding=utf-8


def filter_define(app):

    @app.template_filter('to_dict')
    def to_dict(immutabel_dict):
        """将 ImmutableMultiDict 转换为 Dict"""
        dct = {}
        for k, v in immutabel_dict.items():
            dct[k] = v
        return dct