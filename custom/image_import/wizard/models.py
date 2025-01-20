# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import os


class WizardImportImage(models.TransientModel):
    _name = 'wizard.import.image'
    _description = 'Wizard Import Image'
    
    folder_name = fields.Char('Folder Path', help="Enter Full Path To The Image Folder")

    def import_image(self):
        path = self.folder_name
        img_list = os.listdir(path)

        for each in img_list:
            product_name = os.path.splitext(each)[0]
            product_id = self.env["product.template"].search([("name","=",product_name)])
            if product_id:
                product_path = f"{path}/{each}"
                with open(product_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read())
                product_id.image_1920 = b64_string