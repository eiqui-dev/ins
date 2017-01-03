# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Solucións Aloxa S.L. <info@aloxa.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################


{
    "name": "Módulo de Gestión de Iniciativas para INS",
    "version": "0.1",
    "category": "",
    "icon": "/aloxa_ins_iniciativas/static/src/img/icon.png",
    "depends": [
                'base',
                'product',
                'crm',
                'sale_crm',
                ],
    "author": "Solucións Aloxa S.L.",
    "description": "Módulo de Gestión de Iniciativas para INS",
    "init_xml": [],
    "data": [             
             'res_partner_crm_product_view.xml',
             'security/ir.model.access.csv',
             ],
    "demo_xml": [],
    "installable": True,
    "active": False,
}
