from odoo import models, fields,api
from odoo.exceptions import ValidationError

#EstudiantesUV
class estudiantes(models.Model):
    _name = "estudiantes"
    _description = "almacena datos de los estudiantes de la universidad del valle"
 
    #Datos básicos
    nombre_completo = fields.Char("Nombre Completo",required = True)
    cedula = fields.Char("Cédula", required = True)
    codigo_id = fields.Char("ID Estudiante", required = True)
    estado = fields.Selection(selection=[("Activo", "Activo"),("Inactivo", "Inactivo")], string = "Estado", required = True, tracking = True)
    fecha_nacimiento = fields.Date("Fecha de nacimiento", required = True)
    est_facultad = fields.Many2one("facultades")

    def name_get(self): 
        result = []
        for rec in self:
            name = rec.nombre_completo
            result.append((rec.id, name))
        return result


#Facultades
class facultades(models.Model):
    _name = "facultades"
    _description = "almacena datos de los carreras de cada facultad de la universidad del valle"
 
    #Datos básicos
    facultad = fields.Char("Nombre de la facultad",required = True)
               
    def name_get(self): 
        result = []
        for rec in self:
            name = rec.facultad
            result.append((rec.id, name))
        return result 


#Docentes
class docentes(models.Model):
    _name = "docentes"
    _description = "almacena datos de los docentes de la universidad del valle"
 
    #Datos básicos
    nombre_completo = fields.Char("Nombre Completo",required = True)
    cedula = fields.Char("Cédula", required = True)
    codigo_id = fields.Char("ID Docente", required = True)
    estado = fields.Selection(selection=[("Activo", "Activo"),("Inactivo", "Inactivo")], string = "Estado", required = True, tracking = True)
    fecha_nacimiento = fields.Date("Fecha de nacimiento", required = True)
    doc_facultad = fields.Many2one("facultades")


    def name_get(self): 
        result = []
        for rec in self:
            name = rec.nombre_completo
            result.append((rec.id, name))
        return result
        
    

#Materias
class materias(models.Model):
    _name = "materias"
    _description = "almacena los datos de las materias  registradas en univalle"

    materia = fields.Char("Materia", required = True)
    diasemn = fields.Selection(selection=[("Lunes","Lunes"),
    ("Martes","Martes"),("Miércoles","Miércoles"),("Jueves","Jueves"),("Viernes","Viernes"),("Sábado","Sábado")],string = "Dia", required = True)
    horario = fields.Selection(selection=[("08:00 am - 10:00 am","08:00 am - 10:00 am"),
    ("10:00 am - 12:00 pm","10:00 am - 12:00 pm"),("14:00 pm - 16:00 pm","14:00 pm - 16:00 pm"),
    ("18:00 pm - 20:00 pm","18:00 pm - 20:00 pm"),("20:00 pm - 22:00 pm","20:00 pm - 22:00 pm")],   string = "Horario", required = True)
    docentes = fields.Many2one("docentes",required = True) 
    mat_facultad = fields.Many2one("facultades","Facultad") 
    
    nota1 = fields.Selection(selection=[("10", "10%"), ("20", "20%"), ("30", "30%"), ("40", "40%"), ("50", "50%")], string="P1")
    nota2 = fields.Selection(selection=[("10", "10%"), ("20", "20%"), ("30", "30%"), ("40", "40%"), ("50", "50%")], string="P2")
    nota3 = fields.Selection(selection=[("10", "10%"), ("20", "20%"), ("30", "30%"), ("40", "40%"), ("50", "50%")], string="P3")
    validador_peso_total = fields.Boolean("¿El peso es 100?", compute="_compute_validador_peso_total")

    def _pesoTotal(self):
        for rec in self:
            rec.not_total = int(rec.nota1) + int(rec.nota2) + int(rec.nota3)
    
    not_total = fields.Integer("Peso Total", compute = "_pesoTotal", default = 0)

    @api.depends('not_total')
    def _compute_validador_peso_total(self):
        for rec in self:
            validador_peso_total = False
            if rec.not_total:
                if rec.not_total == 100:
                    validador_peso_total = True
            rec.validador_peso_total = validador_peso_total


    def name_get(self): 
        result = []
        for rec in self:
            name = rec.materia
            result.append((rec.id, name))
        return result


#Matricula
class matricula(models.Model):
    _name = "matricula"
    _description = "almacena datos de las matriculas de estudiantes de la universidad del valle"
 
    #Datos básicos
    nom_matricula = fields.Selection(selection=[("I semestre 2022", "I semestre 2022"), ("II semestre 2022", "II semestre 2022")], string="Matrícula semestre")
    matricula_materia = fields.Many2many("materias",required = True)
    estudiantes = fields.Many2one ("res.users", "Estudiante")