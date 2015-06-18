# from proteibb.util.property import Property
#
# class PlatformsProperty(Property):
#
#     def __init__(self):
#         Property.__init__(self, 'platforms', [])
#
#         def validate(val):
#             if not isinstance(val, list):
#                 return False
#             for p in val:
#                 if not isinstance(p, str) or not len(p):
#                     return False
#             return True
#         self._set_validator(validate)
