import scrapy

from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class uvinumCSVItemExporter(CsvItemExporter):

    
    def __init__(self, *a, **kw):
            kw['delimiter'] = settings.get('CSV_DELIMITER', ';')
            super(uvinumCSVItemExporter, self).__init__(*a, **kw)
     
#     def __init__(self, *args, **kwargs):
#         delimiter = settings.get('CSV_DELIMITER', ';')
#         kwargs['delimiter'] = delimiter
# 
#         fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
#         if fields_to_export :
#             kwargs['fields_to_export'] = fields_to_export
# 
#         super(uvinumCSVItemExporter, self).__init__(*args, **kwargs)