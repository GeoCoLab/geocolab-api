# !/usr/bin/env python
# encoding: utf-8

from .edi import EDIData, EDIExtraData


form_to_user_data = {
    'edi': EDIData,
    'edi_extra': EDIExtraData
}
