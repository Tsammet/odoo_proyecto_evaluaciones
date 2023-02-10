from odoo import models, fields, api
from odoo.exceptions import UserError

RISK = [
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
]

TERM_EMPLOYEE = [
    ('FIJO','FIJO'),
    ('INDEFINIDO','INDEFINIDO'),
    ('OBRA LABOR','OBRA LABOR')
]

class TsmEmployee(models.Model):
    _name = 'tsm.employee'
    _description = 'Empleados'
    _rec_name = 'full_name'

    full_name = fields.Char("Nombre Completo", compute = "nombre_completo")
    first_name = fields.Char('Nombres')
    last_name = fields.Char('Apellidos')
    birth_date = fields.Date('Fecha Nacimiento')
    email = fields.Char('Correo Electronico')
    cellphone = fields.Char('Telefono')
    salary = fields.Float('Salario')
    risk = fields.Selection(RISK, 'Riesgo')
    image = fields.Binary("Foto")
    code = fields.Char('Codigo de Empleado')
    start_date = fields.Date('Fecha inicio trabajo')
    department = fields.Many2one('tsm.department', 'Departamento de Trabajo')
    city = fields.Many2one('res.country.city', 'Ciudad')
    term = fields.Selection(TERM_EMPLOYEE, 'Termino Trabajador')
    position = fields.Many2one('tsm.position', 'Posición del Empleado')

    @api.one
    def nombre_completo(self):
        self.full_name = self.first_name + " " + self.last_name

    @api.constrains('code')
    def no_repeat(self):
        for i in self:
            if i.search([('code','=', i.code),('id','!=', i.id)]):
                raise UserError('Ya hay un empleado con este código')

class TsmDepartment(models.Model):
    _name = 'tsm.department'
    _description = 'Departamento de trabajo'

    name = fields.Char('Nombre del Departamento')
    head = fields.Many2one('tsm.employee', 'Jefe de Area')
    employee = fields.One2many('tsm.employee', 'department', 'Empleados')

class TsmEvaluation(models.Model):
    _name = 'tsm.evaluation'
    _description = 'Evaluación'

    employee = fields.Many2one('tsm.employee', 'Empleado')
    position = fields.Many2one('tsm.position', 'Posición')
    evaluation_line_ids = fields.One2many('tsm.evaluation.line','evaluation' ,'items')
    template_id = fields.Many2one('tsm.evaluate.template', 'Plantilla')

    # DE ESTA MANERA TRAIGO DATOS DE OTRA TABLA AUTOMATICAMENTE 
    @api.onchange('employee')
    def posicion(self):
        self.position = self.employee.position
    # DE ESTA MANERA TRAIGO DATOS DE OTRA TABLA AUTOMATICAMENTE 

    def button_load_template(self):

        data = self.template_id.evaluate_line

        evaluation_line_data = []

        for item in data:
            evaluation_line_data.append({
                'description': item.description,
                'ponderado': item.ponderacion
            })

        load_template = [(0,0,x) for x in evaluation_line_data ]
        self.evaluation_line_ids = load_template
        
        return

class TsmEvaluationLine(models.Model):
    _name = "tsm.evaluation.line"  
    _description = "Evaluación Linea"

    description = fields.Char('Descripción')
    ponderado = fields.Float('Ponderación')
    resultado = fields.Float('Resultado')
    evaluation = fields.Many2one('tsm.evaluation')
    
    
class TsmPosition(models.Model):
    _name = 'tsm.position'
    _description = 'Posición'

    name = fields.Char('Nombre del cargo')


class TsmEvaluateTemplate(models.Model):
    _name = 'tsm.evaluate.template'
    _description = 'Plantilla para evaluar'

    name = fields.Char('Nombre de la plantilla')
    evaluate_line = fields.One2many('tsm.evaluate.template.line', 'evaluate_template_id', 'Linea evaluación')



class TsmEvaluateTemplateLine(models.Model):
    _name = 'tsm.evaluate.template.line'
    _description = 'Linea evaluación'

    description = fields.Char('Descripción')
    ponderacion = fields.Float('Ponderación')
    evaluation_line_id = fields.Many2one('tsm.evaluation.line', 'Evaluación ID')
    evaluate_template_id = fields.Many2one('tsm.evaluate.template' , 'Plantilla evaluación')

    @api.constrains('ponderacion')
    def limite_ponderacion(self):
        for value in self:
            if value.ponderacion < 0 or value.ponderacion > 10:
                raise UserError("El valor debe estar entre 0  y 10")

    def button_create_evaluation_line(self):
        
        evaluate_line_data = {
            'description' : self.description,
            'ponderado' : self.ponderacion,
        }

        create_evaluate_line =  self.env['tsm.evaluation.line'].create(evaluate_line_data)
        self.evaluation_line_id = create_evaluate_line
        return

