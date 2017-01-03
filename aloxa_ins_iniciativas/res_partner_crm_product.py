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
#===============================================================================
# # REMOTE DEBUG
#import pydevd
# 
# # ...
# 
# # breakpoint
#pydevd.settrace("10.0.3.1")
#===============================================================================


from openerp.osv import fields, orm
from openerp import fields as fields_helper
from openerp import api

class res_partner_product_tags(orm.Model):
    #Las funciones deben de ser definidas antes de su uso    
    #Funcion que crea las Iniciativas
    def create_leads(self, cr, uid, ids, context):
        res = dict()            
        for i in ids:            
            sql_req= """
            SELECT DISTINCT rprpr.product_id
            FROM res_partner_res_partner_category_rel rprpr
            WHERE rprpr.category_id IN (
                        SELECT rprpr2.category_id AS category_id
                        FROM res_partner_res_partner_category_rel rprpr2              
                        WHERE          
                          rprpr2.partner_id = %d)
                  AND rprpr.product_id is NOT NULL            
            """ % (i,)
              
            cr.execute(sql_req)
            #dictfetchall devuelve algo del estilo [{'reg_no': 123},{'reg_no': 543},]
            sql_res = cr.dictfetchall()     
            #Obtenemos el modelo para Iniciativas
            crm_lead_obj = self.pool.get('crm.lead')
            #Iteramos en la lista de product_id devueltos por la query
            for r in sql_res:
                #Recuperamos el partner y product de la iteracion
                res_partner_obj = self.pool.get('res.partner')
                product_template_obj = self.pool.get('product.template')
                partner = res_partner_obj.browse(cr, uid, i, context)
                product = product_template_obj.browse(cr, uid, r['product_id'], context)
                if product:
                    #Comprobamos que si hay iniciativas para el res.partner y product_id 
                    sargs = ['&',('partner_id', '=', i),
                                 ('type', '=', 'lead'),
                                 ('product_id', '=', r['product_id'])]
                    crm_lead_id = crm_lead_obj.search(cr, uid, sargs, context=context)
                    #Creamos las iniciativas que no existan
                    if not crm_lead_id:
                        crm_lead_vals = {
                         'name':partner.name + '_' + product.name,
                         'partner_id':i,
                         'type':'lead',
                         'product_id':r['product_id'],
                         'phone':partner.phone if partner.phone else '',
                         'email_from':partner.email if partner.email else '',
                         'street':partner.street+'\n'+partner.city if partner.street and partner.city else ''
                         }
                        crm_lead_obj.create(cr, uid, crm_lead_vals, context=context)
        # Invocamos a la vista que muestra las Iniciativas
        return  {
            'type': 'ir.actions.act_window',
            'name': 'Leads',            
            'domain': ['|', ('type','=','lead'), ('type','=',False)],            
            'res_model': 'crm.lead',                               
            'view_type': 'form',
            'view_mode': 'tree,form',            
            'target': 'current',
            'nodestroy': True,
        }
    
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {                
                #===============================================================
                # 'al_product_ids': fields.function(get_product_ids,
                #                                   type='one2many',
                #                                   obj="product.template",
                #                                   method=True,
                #                                   string='Productos Asociados'),                               
                #===============================================================
                 
       }
    
res_partner_product_tags()

'''
Modelo para incorporar res.partner.category (etiquetas de cliente) al modelo
product.template
'''
class product_template_res_partner_category(orm.Model):
    #Funcion que crea las Iniciativas
    def create_leads(self, cr, uid, ids, context):
        res = dict()            
        for i in ids:            
            sql_req= """
            SELECT DISTINCT rprpr.partner_id
            FROM res_partner_res_partner_category_rel rprpr
            WHERE rprpr.category_id IN (
                        SELECT rprpr2.category_id AS category_id
                        FROM res_partner_res_partner_category_rel rprpr2              
                        WHERE          
                          rprpr2.product_id = %d)
                  AND rprpr.partner_id is NOT NULL            
            """ % (i,)
              
            cr.execute(sql_req)
            #dictfetchall devuelve algo del estilo [{'reg_no': 123},{'reg_no': 543},]
            sql_res = cr.dictfetchall()     
            #Obtenemos el modelo para Iniciativas
            crm_lead_obj = self.pool.get('crm.lead')
            #Iteramos en la lista de product_id devueltos por la query
            for r in sql_res:
                #Recuperamos el partner y product de la iteracion
                res_partner_obj = self.pool.get('res.partner')
                product_template_obj = self.pool.get('product.template')
                partner = res_partner_obj.browse(cr, uid, r['partner_id'], context)
                product = product_template_obj.browse(cr, uid, i, context)
                if product:
                    #Comprobamos que si hay iniciativas para el product.template y partner_id
                    sargs = ['&',('partner_id', '=', r['partner_id']),
                                 ('type', '=', 'lead'),
                                 ('product_id', '=', i)]
                    crm_lead_id = crm_lead_obj.search(cr, uid, sargs, context=context)
                    #Creamos las iniciativas que no existan
                    if not crm_lead_id:
                        crm_lead_vals = {
                         'name':partner.name + '_' + product.name,
                         'partner_id':r['partner_id'],
                         'type':'lead',
                         'product_id':i,
                         'phone':partner.phone if partner.phone else '',
                         'email_from':partner.email if partner.email else '',
                         'street':partner.street+'\n'+partner.city if partner.street and partner.city else ''
                         }
                        crm_lead_obj.create(cr, uid, crm_lead_vals, context=context)
        # Invocamos a la vista que muestra las Iniciativas
        return  {
            'type': 'ir.actions.act_window',
            'name': 'Leads',            
            'domain': ['|', ('type','=','lead'), ('type','=',False)],            
            'res_model': 'crm.lead',                               
            'view_type': 'form',
            'view_mode': 'tree,form',            
            'target': 'current',
            'nodestroy': True,
        }

    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {                
               'al_res_partner_category_ids' : fields.many2many('res.partner.category',
                                                       'res_partner_res_partner_category_rel',                                                     
                                                       'product_id',
                                                       'category_id',
                                                       'Etiquetas',)
                }
product_template_res_partner_category()

'''
Modelo que incorpora la relacion m2m a product.template desde res.partner.category
'''
class res_partner_category(orm.Model):
    _name = 'res.partner.category'
    _inherit = 'res.partner.category'
    _columns = {                
               'al_product_ids' : fields.many2many('product.template',
                                                   'res_partner_res_partner_category_rel',                                                     
                                                   'category_id',
                                                   'product_id',
                                                   'Productos',)
                }
res_partner_category()
    

'''
Modelo que extiende crm.lead (Iniciativas, Oportunidades) para incluir los productos
asociados a traves de las etiquetas de producto asociadas al res.partner
'''
class crm_lead_product(orm.Model):
    #Crea una llamada (crm.phonecall desde la Iniciativa)
    def create_phonecall(self, cr, uid, ids, context):
        for id in ids:
            crm_lead = self.browse(cr, uid, id, context=context)
            crm_phonecall_obj = self.pool.get('crm.phonecall')
            vals = {'name':'Llamada ' + crm_lead.partner_id.name + ' ' +
                           crm_lead.product_id.name if crm_lead.partner_id and crm_lead.product_id else False,
                    'opportunity_id' : id,
                    'partner_id' : crm_lead.partner_id.id if crm_lead.partner_id else False,
                    'state' : 'pending',
                    }
            crm_phonecall_id = crm_phonecall_obj.create(cr, uid, vals, context)
            return {
                'type': 'ir.actions.act_window',
                'name': 'Crear Llamada',
                'res_model': 'crm.phonecall',
                'res_id': crm_phonecall_id,
                'view_type': 'form',
                'view_mode': 'form,tree,calendar',            
                'target': 'current',
                'nodestroy': True,
            }
            
    #Crea una reunion (calendar.event desde la Iniciativa)
    def create_event(self, cr, uid, ids, context):
        for id in ids:
            crm_lead = self.browse(cr, uid, id, context=context)
            calendar_event_obj = self.pool.get('calendar.event')
            res_user_obj = self.pool.get('res.users')
            res_user = res_user_obj.browse(cr, uid, uid, context)
            vals = {'name':'Reunion ' + crm_lead.partner_id.name + ' ' +
                           crm_lead.product_id.name if crm_lead.partner_id and crm_lead.product_id else False,
                    'opportunity_id' : id,
                    'partner_ids' : [(6, 0, [crm_lead.partner_id.id if crm_lead.partner_id else False, res_user.partner_id.id])],
                    'state' : 'open',
                    'start':fields_helper.Datetime.now(),
                    'stop':fields_helper.Datetime.now(),
                    }
            calendar_event_id = calendar_event_obj.create(cr, uid, vals, context)
            return {
                'type': 'ir.actions.act_window',
                'name': 'Crear Reunion',
                'res_model': 'calendar.event',
                'res_id': calendar_event_id,
                'view_type': 'form',
                'view_mode': 'form,tree,calendar',            
                'target': 'current',
                'nodestroy': True,
            }

    _name = 'crm.lead'
    _inherit = 'crm.lead'        
    _columns = {                 
                'product_id' : fields.many2one('product.template', 'Producto'),
                }
     
                      
crm_lead_product()

#DEPRECATED=======================================
'''
Modelo para definir la entidad de la tabla de interseccion de
res.partner->res.partner.category (m2m)
product.template->res.partner.category (m2m)
'''
class res_partner_res_partner_category_rel(orm.Model):
    _name = 'res.partner.res.partner.category.rel'
    _table = 'res_partner_res_partner_category_rel'
    _log_access = "false"
    _columns = {
        'partner_id' : fields.integer('res_partner_id'),
        'product_id' : fields.integer('product_id'),
        'category_id' : fields.integer('product_id'),        
    }
      
res_partner_res_partner_category_rel()

'''
Modelo para sobreescribir el metodo que crear un Presupuesto a partir
de una Oportunidad
'''
class crm_make_sale_product_line(orm.Model):
    def makeOrder(self, cr, uid, ids, context=None):
        value = super(crm_make_sale_product_line, self).makeOrder(cr, uid, ids, context)
        #El campo res_id contiene el id del sale_order (Presupuesto)
        if value['res_id']:
            sale_order_id = value['res_id']
            sale_order_obj = self.pool.get('sale.order')            
            sale_order = sale_order_obj.browse(cr, uid, sale_order_id, context=context)
            #Obtenemos el id de Oportunidad
            opportunity_id = int(sale_order.origin.split(':')[1].strip())            
            #Localizamos la Oportunidad
            crm_lead_obj = self.pool.get('crm.lead')
            crm_lead = crm_lead_obj.browse(cr, uid, opportunity_id, context=context)
            #Obtencion del product_id asociado a la oportunidad
            '''
            El id que obtenemos de crm.lead (Oportunidad) es el del product.template
            Sin embargo para la sale_order_line necesitamos el id del product.product (Variante de Producto)
            '''
            product_template_id = crm_lead.product_id.id
            product_product_obj = self.pool.get('product.product')            
            sargs = [('product_tmpl_id', '=', product_template_id)]            
            product_ids = product_product_obj.search(cr, uid, sargs, context=context)
            for pro in product_ids:
                product_id = pro
                break                       
            #Agregamos una order_line para el product_id
            if 'product_id' in locals():
                sale_order_line_obj = self.pool.get('sale.order.line')
                solvals = {
                           'order_id' : sale_order_id,
                           'product_id' : product_id
                           }
                sale_order_line_id = sale_order_line_obj.create(cr, uid, solvals, context=context)
                #Agregamos la sale_order_line al sale_order
                sovals = {                       
                          'order_line' : [(6, 0, [sale_order_line_id])]
                          }
                sale_order_obj.write(cr, uid, sale_order_id, sovals, context=context)
        #Invocamos a la vista formulario de sale.order para ver el recien creado        
        return  {
            'type': 'ir.actions.act_window',
            'name': 'sale.order.form',
            'res_model': 'sale.order',
            'res_id': value['res_id'], #If you want to go on perticuler record then you can use res_id 
            'view_type': 'form',
            'view_mode': 'form',            
            'target': 'current',
            'nodestroy': True,
        }

    _name = 'crm.make.sale'
    _inherit = 'crm.make.sale'

crm_make_sale_product_line() 

