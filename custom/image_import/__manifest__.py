# -*- coding: utf-8 -*-
{
    "name": "Import Product Image",

    "summary": """
        This module allows user to import product images""",

    "description": """
        This module allows user to import product images
            - Put all the images in folder 
            - Image name sholud be same as product name else the image will not be imported
            - Complete path must be specified in the image import wizard
    """,

    "author": "Billy Butcher",
    "website": "",
    "support": "billybutcher0004@gmail.com",
    "license": "OPL-1",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base","stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "wizard/views.xml",
    ],
    # "price":6.06,
    "currency":'USD',
    'images': [
        'static/description/image_import_description.png',
        'static/description/main_1.png', 
        'static/description/main_2.png',
    ],
}