from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import admin 
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee


def check_admin():
	"""
	Prevent a non admin access
	"""
	if not current_user.is_admin:
		abort(403)

# Department views

@admin.route('/deparments', methods=['GET', 'POST'])
@login_required
def list_departments():
	"""
	List all departments
	"""
	check_admin()
	departments = Department.query.all()
	return render_template('admin/departments/departments.html',
							departments=departments, title = 'Departments')


@admin.route('/deparments/add', methods=['GET', 'POST'])
@login_required
def add_department():
	"""
	add deparment to the database
	"""
	check_admin()
	add_department = True
	form = DepartmentForm()
	if form.validate_on_submit():
		department = Department(name=form.name.data, description=form.description.data)
		try:
			#add department to the database
			db.session.add(department)
			db.session.commit()
			flash('You have successfully created a deparment')
		except:
			#in case department name already exists 
			flash('Error : Department name already exists')
		#redirect to departments page
		return redirect(url_for('admin.list_departments'))

	# load the department template
	return render_template('admin/departments/department.html', action ="Add", add_department=add_department, form=form, title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_admin()

	add_department = False
	department = Department.query.get_or_404(id)
	form = DepartmentForm(obj=department)
	if form.validate_on_submit():
		department.name = form.name.data
		department.description = form.description.data
		db.session.commit()
		flash('You have successfully edited the department')

		# return to the departments page
		return redirect(url_for('admin.list_departments'))

	form.description.data = department.description
	form.name.data = department.name 
	return render_template('admin/departments/department.html', action="Edit", add_department=add_department, form=form, department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
	"""
	Delete a department from the database
	"""
	check_admin()

	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash('You have successfully deleted the department.')

	# redirect to the departments page
	return redirect(url_for('admin.list_departments'))

	return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
	check_admin()
	"""
	List all roles
	"""
	roles = Role.query.all()
	return render_template('admin/roles/roles.html', roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
	"""
	Add a role to the database
	"""
	check_admin()
	add_role = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(name=form.name.data, description=form.description.data)
		try: 
			# add role to the database
			db.session.add(role)
			db.session.commit()
			flash('You have succesfully added one role.')
		except:
			# in case role name already exists
			flash('Error: Role already exists')

		#redirect to the list roles page
		return redirect(url_for('admin.list_roles'))

	# load the role template 
	return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	check_admin()

	add_role = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		db.session.add(role)
		db.session.commit()
		flash('You have successfully edited the role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	form.description.data = role.description
	form.name.data = role.name
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
	"""
	Delete a role from the database
	"""
	check_admin()

	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash('You have successfully deleted the role.')

	# redirect to the roles page
	return redirect(url_for('admin.list_roles'))

	return render_template(title="Delete Role")

@admin.route('/employees')
@login_required
def list_employees():
	"""
	List all employees
	"""
	check_admin()
	employees = Employee.query.all()
	return render_template('admin/employees/employees.html', employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET','POST'])
@login_required
def assign_employee(id):
	"""
	Assign employee to department
	"""
	check_admin()
	employee = Employee.query.get_or_404(id)
	#flash(employee)
	form = EmployeeAssignForm(obj=employee)
	#form = EmployeeAssignForm()
	if form.validate_on_submit():
		employee.department = form.department.data
		employee.role = form.role.data
		#db.session.add(employee)
		db.session.commit()
		flash('You have successfully assigned a department and role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html',
						   employee=employee, form=form,
						   title='Assign Employee')